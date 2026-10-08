import hashlib
import struct
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class WindowsInstallerContractTests(unittest.TestCase):
    def setUp(self):
        self.executable_path = ROOT / "releases/Instalar-Apex-Combate-Windows.exe"
        self.executable = self.executable_path.read_bytes()
        self.source = (ROOT / "windows-app/main.go").read_text(encoding="utf-8")

    def test_release_is_windows_x64_gui_executable(self):
        self.assertGreater(len(self.executable), 1_000_000)
        self.assertEqual(self.executable[:2], b"MZ")
        pe_offset = struct.unpack_from("<I", self.executable, 0x3C)[0]
        self.assertEqual(self.executable[pe_offset : pe_offset + 4], b"PE\0\0")
        machine = struct.unpack_from("<H", self.executable, pe_offset + 4)[0]
        self.assertEqual(machine, 0x8664)  # AMD64
        optional_header = pe_offset + 24
        magic = struct.unpack_from("<H", self.executable, optional_header)[0]
        self.assertEqual(magic, 0x20B)  # PE32+
        subsystem = struct.unpack_from("<H", self.executable, optional_header + 68)[0]
        self.assertEqual(subsystem, 2)  # Windows GUI
        resource_rva = struct.unpack_from("<I", self.executable, optional_header + 128)[0]
        self.assertNotEqual(resource_rva, 0)

    def test_release_checksum_matches(self):
        expected = (
            ROOT / "releases/Instalar-Apex-Combate-Windows.exe.sha256"
        ).read_text(encoding="utf-8").split()[0]
        actual = hashlib.sha256(self.executable).hexdigest()
        self.assertRegex(expected, r"^[0-9a-f]{64}$")
        self.assertEqual(actual, expected)

    def test_launcher_uses_edge_app_mode_without_opera(self):
        self.assertIn(
            "https://apex-combate-demo.onrender.com/apex-combate.html?v=44&source=windows",
            self.source,
        )
        self.assertIn('"--app="+appURL', self.source)
        self.assertIn('"Microsoft", "Edge", "Application", "msedge.exe"', self.source)
        self.assertIn('"Google", "Chrome", "Application", "chrome.exe"', self.source)
        self.assertNotIn("opera.exe", self.source.lower())

    def test_installer_creates_local_shortcuts_without_admin(self):
        self.assertIn('os.Getenv("LOCALAPPDATA")', self.source)
        self.assertIn("createShortcuts(installedExecutable, iconPath)", self.source)
        self.assertIn("Apex Combate.lnk", self.source)
        manifest = (ROOT / "windows-app/apex.manifest").read_text(encoding="utf-8")
        self.assertIn('requestedExecutionLevel level="asInvoker"', manifest)
        self.assertNotIn("requireAdministrator", manifest)

    def test_windows_download_page_and_server_contract(self):
        page = (ROOT / "instalar-apex-combate-windows.html").read_text(
            encoding="utf-8"
        )
        self.assertIn("releases/Instalar-Apex-Combate-Windows.exe", page)
        self.assertIn("não utiliza o Opera GX", page)
        server = (ROOT / "server.py").read_text(encoding="utf-8")
        self.assertIn("application/vnd.microsoft.portable-executable", server)
        self.assertIn('filename="Instalar-Apex-Combate-Windows.exe"', server)
        dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")
        self.assertIn("instalar-apex-combate-windows.html", dockerfile)
        self.assertIn("releases/Instalar-Apex-Combate-Windows.exe", dockerfile)


if __name__ == "__main__":
    unittest.main()
