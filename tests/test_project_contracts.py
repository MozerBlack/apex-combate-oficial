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
        cls.master = (ROOT / "documentacao-mestre-apex-combate.md").read_text(encoding="utf-8")

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

    def test_logout_returns_to_welcome_screen(self):
        logout_handler = self.html[self.html.index("document.querySelectorAll('[data-logout]')"):]
        self.assertIn("showWelcomeScreen();", logout_handler[:2200])

    def test_club_login_contract_is_preserved(self):
        self.assertIn("perfil: 'clube'", self.html)
        self.assertIn("payload.get(\"perfil\")", self.server)

    def test_athlete_country_field_remains_absent(self):
        self.assertNotIn('id="athleteCountry"', self.html)
        self.assertNotIn('name="country"', self.html)

    def test_owner_central_is_disabled(self):
        self.assertIn("APEX_CENTRAL_ENABLED = False", self.server)

    def test_document_master_has_all_parts_and_current_decisions(self):
        self.assertEqual(self.master.count("## Parte "), 10)
        for decision in ("DEC-039", "DEC-040", "DEC-041", "DEC-042", "DEC-043", "DEC-044", "DEC-045"):
            self.assertIn(decision, self.master)


class PwaContractTests(unittest.TestCase):
    def test_manifest_is_valid_and_installable(self):
        manifest = json.loads((ROOT / "manifest.webmanifest").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "Apex Combate")
        self.assertEqual(manifest["display"], "standalone")
        self.assertEqual(manifest["orientation"], "any")
        sizes = {icon["sizes"] for icon in manifest["icons"]}
        self.assertTrue({"192x192", "512x512"}.issubset(sizes))

    def test_service_worker_is_registered(self):
        self.assertIn("serviceWorker.register('./apex-sw.js?v=42'", (ROOT / "apex-combate.html").read_text(encoding="utf-8"))
        self.assertIn("apex-combate-v42", (ROOT / "apex-sw.js").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
