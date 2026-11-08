import tempfile
import unittest
from pathlib import Path

import apex_db
from server import athlete_post_login_mode


ROOT = Path(__file__).resolve().parents[1]


class AthletePostLoginModeTests(unittest.TestCase):
    def test_zero_modalities_requires_onboarding(self):
        self.assertEqual(athlete_post_login_mode([]), "onboarding")
        self.assertEqual(athlete_post_login_mode([{"status": "archived"}]), "onboarding")

    def test_one_modality_enters_directly(self):
        self.assertEqual(athlete_post_login_mode([{"status": "active"}]), "direct")
        self.assertEqual(
            athlete_post_login_mode([{"status": "paused"}, {"status": "archived"}]),
            "direct",
        )

    def test_two_or_more_modalities_require_selection(self):
        self.assertEqual(
            athlete_post_login_mode([{"status": "active"}, {"status": "paused"}]),
            "select_modality",
        )


class AthleteMultimodalityDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original_data_dir = apex_db.DATA_DIR
        cls.original_db_path = apex_db.DB_PATH
        cls.temp_dir = tempfile.TemporaryDirectory()
        apex_db.DATA_DIR = Path(cls.temp_dir.name)
        apex_db.DB_PATH = Path(cls.temp_dir.name) / "athlete-multimodality.sqlite3"
        apex_db.init_database()

    @classmethod
    def tearDownClass(cls):
        apex_db.DATA_DIR = cls.original_data_dir
        apex_db.DB_PATH = cls.original_db_path
        cls.temp_dir.cleanup()

    def test_seed_keeps_one_person_with_multiple_modalities(self):
        with apex_db.connection() as db:
            athlete = db.execute(
                "SELECT id FROM athletes WHERE document='52998224725'"
            ).fetchone()
            modalities = db.execute(
                "SELECT sport,is_primary,status,public_profile FROM athlete_modalities WHERE athlete_id=? ORDER BY id",
                (athlete["id"],),
            ).fetchall()
            accounts = db.execute(
                "SELECT COUNT(*) FROM athletes WHERE document='52998224725'"
            ).fetchone()[0]
        self.assertEqual(accounts, 1)
        self.assertEqual({row["sport"] for row in modalities}, {"Jiu-jítsu", "Judô", "Karatê"})
        self.assertEqual(sum(row["is_primary"] for row in modalities), 1)
        self.assertTrue(all(row["public_profile"] == 0 for row in modalities))

    def test_every_certificate_belongs_to_a_modality_of_the_same_athlete(self):
        with apex_db.connection() as db:
            mismatches = db.execute(
                """SELECT COUNT(*) FROM athlete_certificates ac
                   JOIN athlete_modalities am ON am.id=ac.modality_id
                   WHERE ac.athlete_id!=am.athlete_id"""
            ).fetchone()[0]
        self.assertEqual(mismatches, 0)

    def test_payment_seed_covers_competition_and_club_membership(self):
        with apex_db.connection() as db:
            rows = db.execute(
                """SELECT p.payment_type,p.status,p.amount_cents FROM athlete_payments p
                   JOIN athletes a ON a.id=p.athlete_id WHERE a.document='52998224725'"""
            ).fetchall()
        self.assertIn("competition_fee", {row["payment_type"] for row in rows})
        self.assertIn("club_membership", {row["payment_type"] for row in rows})
        self.assertTrue(all(row["amount_cents"] > 0 for row in rows))
        self.assertTrue({"paid", "pending"}.issubset({row["status"] for row in rows}))

    def test_live_championship_seed_has_published_categories_calls_and_bracket(self):
        with apex_db.connection() as db:
            categories = db.execute(
                "SELECT name,status,publication_status FROM competition_categories ORDER BY id"
            ).fetchall()
            rafael_bouts = db.execute(
                """SELECT b.bout_number,b.status,b.red_name,b.blue_name
                   FROM competition_bouts b
                   JOIN registrations r ON r.id=b.red_registration_id
                   JOIN athletes a ON a.id=r.athlete_id
                   WHERE a.document='52998224725'"""
            ).fetchall()
            notices = db.execute("SELECT priority,kind FROM competition_live_notices").fetchall()
            streams = db.execute(
                "SELECT arena_label,playback_type,playback_url,status,access_level FROM competition_streams ORDER BY id"
            ).fetchall()
            history = db.execute(
                "SELECT athlete_name,category_code,result_status,visibility FROM authorized_competition_history ORDER BY category_code"
            ).fetchall()
        self.assertGreaterEqual(len(categories), 3)
        self.assertTrue(all(row["publication_status"] == "published" for row in categories))
        self.assertEqual(rafael_bouts[0]["bout_number"], "128")
        self.assertEqual(rafael_bouts[0]["status"], "calling")
        self.assertIn("urgent", {row["priority"] for row in notices})
        self.assertEqual(len(streams), 3)
        self.assertTrue(all(row["playback_type"] == "hls" for row in streams))
        self.assertTrue(all(row["access_level"] == "authenticated" for row in streams))
        self.assertTrue(all(row["playback_url"] == "" for row in streams))
        self.assertEqual([row["category_code"] for row in history], ["1181", "1201"])
        self.assertTrue(all(row["athlete_name"] == "João Victor Mozer dos Santos" for row in history))
        self.assertTrue(all(row["result_status"] == "not_reported" for row in history))
        self.assertTrue(all(row["visibility"] == "authenticated" for row in history))


class AthleteMultimodalityContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / "apex-combate.html").read_text(encoding="utf-8")
        cls.server = (ROOT / "server.py").read_text(encoding="utf-8")
        cls.database = (ROOT / "apex_db.py").read_text(encoding="utf-8")

    def test_schema_separates_person_from_modalities_and_certificates(self):
        self.assertIn("CREATE TABLE IF NOT EXISTS athlete_modalities", self.database)
        self.assertIn("athlete_id INTEGER NOT NULL REFERENCES athletes(id) ON DELETE CASCADE", self.database)
        self.assertIn("training_center_name TEXT NOT NULL DEFAULT ''", self.database)
        self.assertIn("public_profile INTEGER NOT NULL DEFAULT 0", self.database)
        self.assertIn("public_profile = 0", self.server)
        self.assertNotIn('payload.get("publicProfile"', self.server)
        self.assertIn("CREATE TABLE IF NOT EXISTS athlete_certificates", self.database)
        self.assertIn("modality_id INTEGER NOT NULL REFERENCES athlete_modalities(id) ON DELETE CASCADE", self.database)
        self.assertIn("CREATE TABLE IF NOT EXISTS athlete_payments", self.database)
        self.assertIn("UNIQUE(athlete_id,payment_type,reference_key)", self.database)
        self.assertIn("CREATE TABLE IF NOT EXISTS competition_categories", self.database)
        self.assertIn("CREATE TABLE IF NOT EXISTS competition_bouts", self.database)
        self.assertIn("CREATE TABLE IF NOT EXISTS competition_live_notices", self.database)
        self.assertIn("CREATE TABLE IF NOT EXISTS competition_streams", self.database)
        self.assertIn("access_level TEXT NOT NULL DEFAULT 'authenticated'", self.database)
        self.assertIn("CREATE TABLE IF NOT EXISTS authorized_competition_history", self.database)
        self.assertIn("visibility TEXT NOT NULL DEFAULT 'authenticated'", self.database)
        self.assertNotIn("sport TEXT NOT NULL UNIQUE", self.database)

    def test_backend_exposes_authenticated_modality_and_certificate_operations(self):
        for route in (
            '"/api/athlete/modalities"',
            '"/api/athlete/certificates"',
            '"/api/athlete/guardian"',
            '"/api/athlete/payments/pay"',
            '"/api/athlete/dashboard"',
            '"/api/athlete/live"',
        ):
            self.assertIn(route, self.server)
        self.assertIn("def handle_upsert_athlete_modality", self.server)
        self.assertIn("def handle_upsert_athlete_certificate", self.server)
        self.assertIn("def handle_upsert_athlete_guardian", self.server)
        self.assertIn("def handle_pay_athlete_payment", self.server)
        self.assertIn("def handle_athlete_live", self.server)
        self.assertIn('"scope": "authenticated-athlete-read-only"', self.server)
        self.assertIn("WHERE id=? AND athlete_id=?", self.server)
        self.assertIn('query.get("modalityId"', self.server)

    def test_frontend_implements_zero_one_many_behavior(self):
        self.assertIn('id="athleteModalityGate"', self.html)
        self.assertIn('id="athleteFirstModalityButton"', self.html)
        self.assertIn('id="athleteModalitySwitchWrap"', self.html)
        self.assertIn("availableModalities.length === 1", self.html)
        self.assertIn("modalities.length > 1", self.html)
        self.assertIn("renderAthleteModalityGate([], true)", self.html)
        self.assertIn("switchWrap.hidden = available.length < 2", self.html)

    def test_profile_covers_personal_sports_documents_and_certificates(self):
        required_ids = (
            "athleteProfileRegistration",
            "athleteProfileBirthDate",
            "athleteProfileDocumentMasked",
            "athleteProfileEmailDisplay",
            "athleteProfilePhoneDisplay",
            "athleteModalityList",
            "athleteProfileInstructor",
            "athleteDocumentList",
            "athleteProfileCertificateList",
            "athleteJourneyTimeline",
            "athleteGuardianCard",
            "athleteGuardianAuthorization",
            "athletePaymentsSection",
            "athletePaymentRows",
            "athletePaymentForm",
            "athleteReceiptCode",
        )
        for element_id in required_ids:
            self.assertIn(f'id="{element_id}"', self.html)
            self.assertIn(f"'{element_id}'", self.html)

    def test_athlete_interface_contains_only_operationally_necessary_actions(self):
        athlete_pages = self.html.split("<!-- ÁREA COMPLETA DO ATLETA -->", 1)[1].split("<!-- DASHBOARD DO CLUBE", 1)[0]
        for future_action in (
            "Adicionar à carteira",
            "Baixar PDF",
            "Sincronizar calendário",
            "Exportar histórico",
            "Baixar comprovante",
            "Filtros avançados em preparação",
            "Desempenho na temporada",
            "athletePerformanceChart",
            "Perfil esportivo público",
            "athletePublicProfileSwitch",
            "athleteModalityPublic",
        ):
            self.assertNotIn(future_action, athlete_pages)
        self.assertIn('id="athleteCardValidity"', athlete_pages)
        self.assertIn('id="athleteCardValidationValidity"', athlete_pages)
        self.assertIn("const cardValidityIso", self.html)
        self.assertNotIn("Comunidade será liberada", self.html)
        self.assertNotIn("dashboardRoleSelect.addEventListener('change'", self.html)
        self.assertNotIn("athleteProfileCompleteness", self.html)
        self.assertNotIn('"profileComplete"', self.server)
        self.assertIn('id="dashboardRole" aria-label="Perfil do dashboard" disabled', self.html)
        for essential_page in ("page-home", "page-explore", "page-training", "page-journey", "page-profile"):
            self.assertIn(f'id="{essential_page}"', athlete_pages)

    def test_live_championship_center_covers_calls_categories_and_brackets(self):
        for element_id in (
            "athleteLiveCenter", "athleteLiveCompetition", "athleteLiveCategory", "athleteLiveQueue",
            "athleteBracket", "athleteLiveNotices", "athleteLiveBoutStatus", "athleteLiveArena",
            "athleteLiveBoutNumber", "athleteLiveCallTime", "athleteLiveBoutsBefore",
            "athleteLiveVideo", "athleteLiveStreams", "athleteLiveFilterPanel", "athleteLiveSearch",
            "athleteLiveSportFilter", "athleteLiveArenaFilter", "athleteLiveStatusFilter", "athleteLiveMineFilter",
        ):
            self.assertIn(f'id="{element_id}"', self.html)
        for contract in (
            "Chaves, categorias e chamadas",
            "Minha próxima luta",
            "Atualização automática a cada 30 segundos",
            "function renderAthleteLive(data)",
            "function loadAthleteLive",
            "startAthleteLivePolling()",
            "redIsMe",
            "blueIsMe",
            "Lutas ao vivo em vídeo",
            "Modo filtrar",
            "function selectAthleteLiveStream",
            "function applyAthleteLiveFilters",
            "controls playsinline preload=\"metadata\"",
        ):
            self.assertIn(contract, self.html)
        self.assertIn("WHERE r.athlete_id=? AND r.status!='cancelled'", self.server)
        self.assertIn("FROM competition_streams WHERE competition_id=? AND access_level='authenticated'", self.server)
        self.assertIn("def safe_stream_url", self.server)
        self.assertIn("APEX_STREAM_ORIGINS", self.server)
        self.assertIn("media-src 'self' blob:", self.server)
        self.assertIn("Campeonato não encontrado para este atleta", self.server)
        self.assertNotIn('elif path == "/api/athlete/live"', self.server)

    def test_authorized_owner_history_is_separate_from_authenticated_athlete_results(self):
        self.assertIn('id="authorizedHistorySection"', self.html)
        self.assertIn('id="authorizedCompetitionHistory"', self.html)
        self.assertIn("não altera o histórico do atleta autenticado", self.html)
        self.assertIn("data.authorizedCompetitionHistory", self.html)
        self.assertIn('"authorizedCompetitionHistory": [dict(row) for row in authorized_history]', self.server)
        self.assertIn("João Victor Mozer dos Santos", self.database)
        self.assertIn('"1181"', self.database)
        self.assertIn('"1201"', self.database)
        self.assertIn('"not_reported"', self.database)
        self.assertIn("sem colocação ou medalha presumida", self.html)

    def test_athlete_security_has_server_revocation_rate_limits_and_idle_timeout(self):
        for contract in (
            '"/api/logout"',
            "def revoke_token(payload: dict)",
            "token_is_revoked(payload)",
            'maximum=6, window=900',
            'self.send_header("Content-Security-Policy"',
            'self.send_header("Referrer-Policy", "no-referrer")',
        ):
            self.assertIn(contract, self.server)
        for contract in (
            "APEX_IDLE_TIMEOUT_MS = 20 * 60 * 1000",
            "revokeCurrentSessionTokens()",
            "Sessão inválida ou expirada; entre novamente",
        ):
            self.assertIn(contract, self.html)

    def test_payment_center_is_complete_and_does_not_collect_bank_secrets(self):
        for contract in (
            "Taxas de competição, mensalidades do clube e comprovantes",
            "A demonstração não realiza cobrança real",
            "Nenhuma cobrança real será realizada",
            "PIX",
            "Cartão pelo gateway",
            "Boleto",
        ):
            self.assertIn(contract, self.html)
        for forbidden in ("cardNumber", "cardCvv", "bankPassword", "Número do cartão", "CVV"):
            self.assertNotIn(forbidden, self.html)
        self.assertIn("payment[\"amount_cents\"]", self.server)
        self.assertIn("WHERE id=? AND athlete_id=?", self.server)
        self.assertIn("ATHLETE_PAYMENT_DEMO_CONFIRM", self.server)
        self.assertIn("UPDATE registrations SET payment_status='paid'", self.server)

    def test_certificates_are_linked_to_selected_modality(self):
        self.assertIn("modalityId: Number(document.getElementById('athleteCertificateModality').value)", self.html)
        self.assertIn("item[\"modality_id\"] == selected_modality[\"id\"]", self.server)
        self.assertNotIn('<option value="graduation_certificate">Certificado de graduação</option>', self.html)


if __name__ == "__main__":
    unittest.main()
