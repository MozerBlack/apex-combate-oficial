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
        for decision in ("DEC-039", "DEC-040", "DEC-041", "DEC-042", "DEC-043", "DEC-044", "DEC-045", "DEC-046"):
            self.assertIn(decision, self.master)


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
        self.assertEqual(manifest["start_url"], "./apex-combate.html?v=43")
        self.assertIn("apex-combate.html?v=43", (ROOT / "index.html").read_text(encoding="utf-8"))
        sizes = {icon["sizes"] for icon in manifest["icons"]}
        self.assertTrue({"192x192", "512x512"}.issubset(sizes))

    def test_service_worker_is_registered(self):
        self.assertIn("serviceWorker.register('./apex-sw.js?v=43'", (ROOT / "apex-combate.html").read_text(encoding="utf-8"))
        self.assertIn("apex-combate-v43", (ROOT / "apex-sw.js").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
