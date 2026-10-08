import hashlib
import unittest
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ANDROID = "http://schemas.android.com/apk/res/android"


def attr(name):
    return f"{{{ANDROID}}}{name}"


class AndroidApkContractTests(unittest.TestCase):
    def setUp(self):
        self.manifest_path = ROOT / "android-apk/src/main/AndroidManifest.xml"
        self.java_path = ROOT / "android-apk/src/main/java/br/com/apexcombate/app/MainActivity.java"
        self.build_script_path = ROOT / "android-apk/build-apk.sh"
        self.release_path = ROOT / "releases/Apex-Combate-Demo-v44.apk"
        self.root = ET.parse(self.manifest_path).getroot()
        self.application = self.root.find("application")

    def test_manifest_identity_sdk_and_permissions(self):
        self.assertEqual(self.root.attrib["package"], "br.com.apexcombate.app")
        self.assertEqual(self.root.attrib[attr("versionCode")], "44")
        self.assertEqual(self.root.attrib[attr("versionName")], "44.0-demo")
        uses_sdk = self.root.find("uses-sdk")
        self.assertEqual(uses_sdk.attrib[attr("minSdkVersion")], "23")
        self.assertEqual(uses_sdk.attrib[attr("targetSdkVersion")], "33")
        permissions = {
            item.attrib[attr("name")] for item in self.root.findall("uses-permission")
        }
        self.assertEqual(
            permissions,
            {"android.permission.INTERNET", "android.permission.ACCESS_NETWORK_STATE"},
        )

    def test_manifest_security_and_launcher(self):
        self.assertEqual(self.application.attrib[attr("usesCleartextTraffic")], "false")
        self.assertEqual(self.application.attrib[attr("allowBackup")], "false")
        self.assertEqual(self.application.attrib[attr("debuggable")], "false")
        self.assertEqual(self.application.attrib[attr("label")], "Apex Combate")
        activity = self.application.find("activity")
        self.assertEqual(activity.attrib[attr("name")], ".MainActivity")
        self.assertEqual(activity.attrib[attr("exported")], "true")
        actions = {
            node.attrib[attr("name")] for node in activity.findall("intent-filter/action")
        }
        categories = {
            node.attrib[attr("name")]
            for node in activity.findall("intent-filter/category")
        }
        self.assertIn("android.intent.action.MAIN", actions)
        self.assertIn("android.intent.category.LAUNCHER", categories)

    def test_native_shell_contract(self):
        source = self.java_path.read_text(encoding="utf-8")
        self.assertIn("package br.com.apexcombate.app;", source)
        self.assertIn(
            'https://apex-combate-demo.onrender.com/apex-combate.html?v=44&source=apk',
            source,
        )
        self.assertNotIn("http://", source)
        self.assertIn("setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW)", source)
        self.assertIn("setWebContentsDebuggingEnabled(false)", source)
        self.assertIn("setSafeBrowsingEnabled(true)", source)
        self.assertNotIn("onReceivedSslError", source)
        self.assertIn("onShowFileChooser", source)
        self.assertIn("webView.canGoBack()", source)

    def test_launcher_icon_matches_official_artwork(self):
        official = (ROOT / "icons/apex-512.png").read_bytes()
        launcher = (
            ROOT / "android-apk/src/main/res/drawable/apex_icon.png"
        ).read_bytes()
        self.assertEqual(hashlib.sha256(launcher).digest(), hashlib.sha256(official).digest())

    def test_distribution_page_and_qr_are_published(self):
        installer = (ROOT / "instalar-apex-combate.html").read_text(encoding="utf-8")
        self.assertIn("releases/Apex-Combate-Demo-v44.apk", installer)
        self.assertIn("releases/QR-Instalar-Apex-Combate-v44.png", installer)
        self.assertIn("Abrir a versão web/PWA", installer)
        qr = (ROOT / "releases/QR-Instalar-Apex-Combate-v44.png").read_bytes()
        self.assertTrue(qr.startswith(b"\x89PNG\r\n\x1a\n"))
        dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")
        self.assertIn("instalar-apex-combate.html", dockerfile)
        self.assertIn("releases/Apex-Combate-Demo-v44.apk", dockerfile)
        self.assertIn("releases/QR-Instalar-Apex-Combate-v44.png", dockerfile)

    def test_reproducible_build_script_has_required_stages(self):
        script = self.build_script_path.read_text(encoding="utf-8")
        for command in ("aapt2", "javac", "d8", "zipalign", "apksigner"):
            self.assertIn(command, script)
        self.assertIn("openssl pkcs8", script)
        self.assertIn("Apex-Combate-Demo-v44.apk", script)
        self.assertIn("sha256sum", script)

    def test_committed_release_integrity(self):
        expected = (ROOT / "releases/Apex-Combate-Demo-v44.apk.sha256").read_text(
            encoding="utf-8"
        ).split()[0]
        actual = hashlib.sha256(self.release_path.read_bytes()).hexdigest()
        self.assertRegex(expected, r"^[0-9a-f]{64}$")
        self.assertEqual(actual, expected)
        with zipfile.ZipFile(self.release_path) as apk:
            names = set(apk.namelist())
        self.assertIn("AndroidManifest.xml", names)
        self.assertIn("classes.dex", names)
        self.assertIn("res/drawable/apex_icon.png", names)
        self.assertTrue(any(name.startswith("META-INF/") and name.endswith(".RSA") for name in names))


if __name__ == "__main__":
    unittest.main()
