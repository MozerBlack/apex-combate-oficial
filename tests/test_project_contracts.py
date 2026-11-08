import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ProductContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / "apex-combate.html").read_text(encoding="utf-8")
        cls.server = (ROOT / "server.py").read_text(encoding="utf-8")
        cls.master = (ROOT / "docs/documentacao-mestre-apex-combate.md").read_text(encoding="utf-8")

    def test_exactly_three_public_profile_choices(self):
        choices = re.findall(r'data-role-choice="([^"]+)"', self.html)
        self.assertEqual(choices, ["athlete", "academy", "federation"])

    def test_public_labels_are_official(self):
        for label in ("ATLETA", "CLUBE", "FEDERAÇÃO"):
            self.assertIn(f">{label}</strong>", self.html)

    def test_welcome_screen_precedes_login_and_requires_explicit_action(self):
        self.assertIn('<body class="prelogin-active auth-active">', self.html)
        self.assertLess(self.html.index('id="welcomeScreen"'), self.html.index('id="authScreen"'))
        self.assertNotIn('class="welcome-header"', self.html)
        self.assertNotIn('id="welcomeLanguage"', self.html)
        self.assertIn('class="welcome-primary enter-apex-login"', self.html)
        self.assertIn('class="welcome-title-emoji"', self.html)
        self.assertIn("Plataforma Universal de Artes Marciais", self.html)
        self.assertIn("addEventListener('click', showLoginScreen)", self.html)
        self.assertNotRegex(self.html, r"setTimeout\s*\(\s*showLoginScreen")

    def test_login_header_keeps_only_the_translator(self):
        match = re.search(
            r'<header class="auth-header auth-header--language-only"[^>]*>(.*?)</header>',
            self.html,
            re.DOTALL,
        )
        self.assertIsNotNone(match)
        header = match.group(1)
        self.assertIn('id="authLanguage"', header)
        self.assertIn('id="authLanguageCode"', header)
        for removed in (
            'class="auth-brand',
            'class="auth-nav"',
            'id="navModalities"',
            'id="navAcademies"',
            'id="navCompetitions"',
            'id="navAbout"',
            'id="authTopLogin"',
        ):
            self.assertNotIn(removed, header)
        self.assertIn("border: 0", self.html)
        self.assertIn("background: transparent", self.html)

    def test_authenticated_shell_has_one_secure_return_control(self):
        self.assertEqual(self.html.count('id="appReturnHome"'), 1)
        shell_start = self.html.index('<div class="app-shell">')
        topbar_start = self.html.index('<header class="topbar">', shell_start)
        topbar_end = self.html.index('</header>', topbar_start)
        topbar = self.html[topbar_start:topbar_end]
        self.assertIn('id="appReturnHome"', topbar)
        self.assertIn('class="return-home-btn"', topbar)
        self.assertIn('type="button"', topbar)
        self.assertIn('data-logout', topbar)
        self.assertIn('aria-labelledby="appReturnHomeLabel"', topbar)
        self.assertIn('aria-label="Voltar ao início e encerrar sessão"', topbar)
        self.assertIn('<span id="appReturnHomeLabel" class="return-home-label">Voltar ao início</span>', topbar)
        self.assertIn('.return-home-btn { width: 39px; padding: 0; }', self.html)
        self.assertIn('.return-home-btn { min-width: 44px; }', self.html)

    def test_logout_returns_to_welcome_screen_clears_and_revokes_session(self):
        start = self.html.index("const APEX_IDLE_TIMEOUT_MS")
        end = self.html.index("const roleDefaultPage", start)
        secure_handler = self.html[start:end]
        for contract in (
            "fetch('/api/logout'",
            "keepalive: true",
            "activeSessionToken = '';",
            "activeAdminToken = '';",
            "sessionStorage.removeItem('apex-session')",
            "sessionStorage.removeItem('apex-admin-jwt')",
            "sessionStorage.removeItem('apex-profile')",
            "sessionStorage.removeItem('apex-federation-scope')",
            "sessionStorage.removeItem('apex-club-account-type')",
            "localStorage.removeItem('apex-technician-operations-v38')",
            "showWelcomeScreen();",
            "APEX_IDLE_TIMEOUT_MS = 20 * 60 * 1000",
        ):
            self.assertIn(contract, secure_handler)

    def test_club_login_contract_is_preserved(self):
        self.assertIn("perfil: 'clube'", self.html)
        self.assertIn("payload.get(\"perfil\")", self.server)

    def test_athlete_country_field_remains_absent(self):
        self.assertNotIn('id="athleteCountry"', self.html)
        self.assertNotIn('name="country"', self.html)

    def test_athlete_authenticated_identity_drives_all_personal_surfaces(self):
        required_ids = (
            "sidebarProfileName", "athleteHomeGreeting", "athleteCardName",
            "athleteProfileName", "athleteRailName", "competitionAthleteIdentity",
            "athleteRegistrationRows", "athleteRecentActivity", "athleteRailNotices",
        )
        for element_id in required_ids:
            self.assertIn(f'id="{element_id}"', self.html)
            self.assertIn(f"'{element_id}'", self.html)
        self.assertIn("function renderAthleteCompleteDashboard(data)", self.html)
        self.assertIn("athlete.registration_code", self.html)
        self.assertIn("athlete.club_city", self.html)
        self.assertIn("data.readiness?.documentsVerified", self.html)
        self.assertIn("c.city AS club_city", self.server)
        self.assertIn("r.created_at,c.id AS competition_id", self.server)
        athlete_pages = self.html.split('id="page-home"', 1)[1].split('id="page-academy"', 1)[0]
        athlete_rail = self.html.split('<aside class="right-rail">', 1)[1].split('</aside>', 1)[0]
        for fixed_identity in ("Rafael Martins", "AC-2026-001842"):
            self.assertNotIn(fixed_identity, athlete_pages)
            self.assertNotIn(fixed_identity, athlete_rail)

    def test_athlete_competitions_and_results_do_not_impersonate_another_athlete(self):
        self.assertIn("function renderAthleteCompetitions(competitions = [])", self.html)
        self.assertIn("await fetch('/api/competitions')", self.html)
        self.assertIn("Resultados oficiais ainda não integrados.", self.html)
        journey = self.html.split('id="page-journey"', 1)[1].split('id="page-profile"', 1)[0]
        for fabricated_value in ("Paraná Regional", "Copa Curitiba", "Open Sul", ">#18<", ">420<"):
            self.assertNotIn(fabricated_value, journey)

    def test_owner_central_is_disabled(self):
        self.assertIn("APEX_CENTRAL_ENABLED = False", self.server)

    def test_complementary_documentation_is_grouped_under_docs(self):
        documentation = (
            "admin-apex-central.md",
            "apexs-forge.md",
            "backend-apex-combate.md",
            "compatibilidade-apex-combate.md",
            "documentacao-mestre-apex-combate.md",
            "identidade-visual-apex-combate.md",
            "perfis-e-permissoes-apex-combate.md",
            "plano-produto-apex-combate.md",
            "registro-de-decisoes-apex-combate.md",
            "sistema-login-apex-combate.md",
        )
        self.assertTrue((ROOT / "docs/README.md").is_file())
        self.assertFalse((ROOT / "README-APEX-COMBATE.md").exists())
        for name in documentation:
            self.assertTrue((ROOT / "docs" / name).is_file(), name)
            self.assertFalse((ROOT / name).exists(), name)
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("[Índice documental](docs/README.md)", readme)

    def test_document_master_has_all_parts_and_current_decisions(self):
        self.assertEqual(self.master.count("## Parte "), 10)
        for decision in ("DEC-039", "DEC-040", "DEC-041", "DEC-042", "DEC-043", "DEC-044", "DEC-045", "DEC-046", "DEC-047", "DEC-048", "DEC-049", "DEC-050", "DEC-051", "DEC-052", "DEC-053", "DEC-054", "DEC-055", "DEC-056", "DEC-057", "DEC-058", "DEC-059", "DEC-060", "DEC-061"):
            self.assertIn(decision, self.master)
        self.assertIn("revisão completa do ATLETA", self.master)


class TypographyContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / "apex-combate.html").read_text(encoding="utf-8")
        cls.css = cls.html.split("<style>", 1)[1].split("</style>", 1)[0]

    def test_fluid_semantic_scale_is_declared(self):
        expected_tokens = (
            "--font-micro: clamp(",
            "--font-caption: clamp(",
            "--font-small: clamp(",
            "--font-label: clamp(",
            "--font-body: clamp(",
            "--font-body-lg: clamp(",
        )
        for token in expected_tokens:
            self.assertIn(token, self.css)
        self.assertIn("@supports (font-size: clamp(", self.css)
        fixed_fallbacks = (
            "--font-micro: 10px;",
            "--font-caption: 11px;",
            "--font-small: 12px;",
            "--font-label: 13px;",
            "--font-body: 14px;",
            "--font-body-lg: 15px;",
        )
        for fallback in fixed_fallbacks:
            self.assertIn(fallback, self.css)
        self.assertGreaterEqual(self.css.count("font-size: var(--font-"), 400)

    def test_critically_small_functional_fonts_are_eliminated(self):
        self.assertNotRegex(self.css, r"font-size\s*:\s*[6-9]px\b")

    def test_mobile_form_controls_prevent_ios_automatic_zoom(self):
        self.assertRegex(
            self.css,
            r"(?s)@media\s*\(max-width:\s*820px\).*?input,\s*select,\s*textarea\s*\{\s*font-size:\s*16px\s*!important;",
        )


class PwaContractTests(unittest.TestCase):
    def test_manifest_is_valid_and_installable(self):
        manifest = json.loads((ROOT / "manifest.webmanifest").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "Apex Combate")
        self.assertEqual(manifest["display"], "standalone")
        self.assertEqual(manifest["orientation"], "any")
        self.assertEqual(manifest["start_url"], "./apex-combate.html?v=44")
        self.assertIn("apex-combate.html?v=44", (ROOT / "index.html").read_text(encoding="utf-8"))
        sizes = {icon["sizes"] for icon in manifest["icons"]}
        self.assertTrue({"192x192", "512x512"}.issubset(sizes))

    def test_service_worker_is_registered(self):
        self.assertIn("serviceWorker.register('./apex-sw.js?v=44'", (ROOT / "apex-combate.html").read_text(encoding="utf-8"))
        self.assertIn("apex-combate-v44", (ROOT / "apex-sw.js").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
