#!/usr/bin/env python3
"""Static project checks used locally and by GitHub Actions."""

from __future__ import annotations

import json
import py_compile
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DOCUMENTATION_FILES = (
    "README.md",
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

REQUIRED_FILES = (
    "apex-combate.html",
    "index.html",
    "server.py",
    "apex_db.py",
    "manifest.webmanifest",
    "apex-sw.js",
    "README.md",
    ".gitignore",
    "Dockerfile",
    "android-apk/README.md",
    "android-apk/build-apk.sh",
    "android-apk/src/main/AndroidManifest.xml",
    "android-apk/src/main/java/br/com/apexcombate/app/MainActivity.java",
    "android-apk/src/main/res/drawable/apex_icon.png",
    "releases/Apex-Combate-Demo-v44.apk",
    "releases/Apex-Combate-Demo-v44.apk.sha256",
    "releases/QR-Instalar-Apex-Combate-v44.png",
    "releases/README.md",
    "instalar-apex-combate.html",
    *(f"docs/{name}" for name in DOCUMENTATION_FILES),
)


def fail(message: str) -> None:
    print(f"ERRO: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_required_files() -> None:
    missing = [name for name in REQUIRED_FILES if not (ROOT / name).is_file()]
    if missing:
        fail("arquivos obrigatórios ausentes: " + ", ".join(missing))
    legacy_root_docs = ("README-APEX-COMBATE.md", *DOCUMENTATION_FILES[1:])
    misplaced = [name for name in legacy_root_docs if (ROOT / name).exists()]
    if misplaced:
        fail("documentação complementar deve permanecer em docs/: " + ", ".join(misplaced))


def check_python() -> None:
    for name in ("server.py", "apex_db.py", "scripts/smoke_test.py", "scripts/v38_flow_test.py"):
        py_compile.compile(str(ROOT / name), doraise=True)


def check_html_contract() -> None:
    html = (ROOT / "apex-combate.html").read_text(encoding="utf-8")
    choices = re.findall(r'data-role-choice="([^"]+)"', html)
    if choices != ["athlete", "academy", "federation"]:
        fail(f"perfis públicos inesperados: {choices}")
    required = ("ATLETA", "CLUBE", "FEDERAÇÃO", "🥋", "Plataforma Universal de Artes Marciais", "welcomeScreen", "enter-apex-login", "manifest.webmanifest", "apex-sw.js?v=44")
    for value in required:
        if value not in html:
            fail(f"contrato HTML ausente: {value}")
    if html.index('id="welcomeScreen"') > html.index('id="authScreen"'):
        fail("a apresentação pública deve preceder o login")
    login_header = re.search(
        r'<header class="auth-header auth-header--language-only"[^>]*>(.*?)</header>',
        html,
        re.DOTALL,
    )
    if not login_header:
        fail("cabeçalho discreto do tradutor ausente no login")
    header = login_header.group(1)
    if 'id="authLanguage"' not in header or 'id="authLanguageCode"' not in header:
        fail("tradutor ausente no cabeçalho do login")
    for removed in ('class="auth-brand', 'class="auth-nav"', 'id="authTopLogin"'):
        if removed in header:
            fail(f"controle superior obsoleto no login: {removed}")

    if html.count('id="appReturnHome"') != 1:
        fail("o shell autenticado deve conter exatamente um controle Voltar ao início")
    shell_start = html.index('<div class="app-shell">')
    topbar_start = html.index('<header class="topbar">', shell_start)
    topbar_end = html.index('</header>', topbar_start)
    topbar = html[topbar_start:topbar_end]
    for contract in ('id="appReturnHome"', 'class="return-home-btn"', 'type="button"', 'data-logout', 'aria-labelledby="appReturnHomeLabel"', 'aria-label="Voltar ao início e encerrar sessão"', 'id="appReturnHomeLabel"', '>Voltar ao início</span>'):
        if contract not in topbar:
            fail(f"controle autenticado de retorno incompleto: {contract}")
    logout_handler = html[html.index("document.querySelectorAll('[data-logout]')"):][:2600]
    for contract in ("activeSessionToken = '';", "activeAdminToken = '';", "sessionStorage.removeItem('apex-session')", "sessionStorage.removeItem('apex-admin-jwt')", "sessionStorage.removeItem('apex-profile')", "localStorage.removeItem('apex-technician-operations-v38')", "showWelcomeScreen();"):
        if contract not in logout_handler:
            fail(f"encerramento seguro da sessão incompleto: {contract}")

    css = html.split("<style>", 1)[1].split("</style>", 1)[0]
    for token in ("--font-micro: clamp(", "--font-caption: clamp(", "--font-small: clamp(", "--font-label: clamp(", "--font-body: clamp(", "--font-body-lg: clamp("):
        if token not in css:
            fail(f"escala tipográfica fluida ausente: {token}")
    if len(re.findall(r"font-size\s*:\s*var\(--font-", css)) < 400:
        fail("escala tipográfica v43 não foi aplicada de forma abrangente")
    if re.search(r"font-size\s*:\s*[6-9]px\b", css):
        fail("a interface ainda contém texto funcional crítico entre 6 e 9 px")
    if not re.search(r"input,\s*select,\s*textarea\s*\{\s*font-size:\s*16px\s*!important;", css):
        fail("controles de formulário móveis não possuem mínimo de 16 px")
    for contract in (".return-home-btn { height: 39px;", ".return-home-btn { width: 39px; padding: 0; }", ".return-home-btn { min-width: 44px; }", ".location-pill, .return-home-btn, .circle-btn { height: 48px; }"):
        if contract not in css:
            fail(f"responsividade do retorno autenticado ausente: {contract}")


def check_manifest() -> None:
    manifest = json.loads((ROOT / "manifest.webmanifest").read_text(encoding="utf-8"))
    if manifest.get("name") != "Apex Combate":
        fail("nome inválido no manifesto")
    if manifest.get("display") != "standalone" or manifest.get("orientation") != "any":
        fail("configuração PWA incompleta")
    if manifest.get("start_url") != "./apex-combate.html?v=44":
        fail("URL inicial do manifesto não corresponde à v44")
    index = (ROOT / "index.html").read_text(encoding="utf-8")
    if "apex-combate.html?v=44" not in index:
        fail("entrada principal não aponta para a v44")
    for icon in manifest.get("icons", []):
        icon_path = ROOT / icon.get("src", "")
        if not icon_path.is_file():
            fail(f"ícone PWA ausente: {icon_path.relative_to(ROOT)}")


def check_android_apk() -> None:
    namespace = "{http://schemas.android.com/apk/res/android}"
    manifest_path = ROOT / "android-apk/src/main/AndroidManifest.xml"
    manifest = ET.parse(manifest_path).getroot()
    if manifest.get("package") != "br.com.apexcombate.app":
        fail("identificador Android inválido")
    if manifest.get(namespace + "versionCode") != "44" or manifest.get(namespace + "versionName") != "44.0-demo":
        fail("versão do APK demonstrativo inválida")
    application = manifest.find("application")
    if application is None or application.get(namespace + "usesCleartextTraffic") != "false":
        fail("o APK Android deve bloquear tráfego sem criptografia")
    source = (ROOT / "android-apk/src/main/java/br/com/apexcombate/app/MainActivity.java").read_text(encoding="utf-8")
    for required in ("https://apex-combate-demo.onrender.com", "MIXED_CONTENT_NEVER_ALLOW", "setSafeBrowsingEnabled(true)", "setWebContentsDebuggingEnabled(false)"):
        if required not in source:
            fail(f"contrato Android ausente: {required}")
    if "http://" in source or "onReceivedSslError" in source:
        fail("o invólucro Android contém comportamento de rede inseguro")
    installer = (ROOT / "instalar-apex-combate.html").read_text(encoding="utf-8")
    for required in ("releases/Apex-Combate-Demo-v44.apk", "releases/QR-Instalar-Apex-Combate-v44.png", "Android 6.0+", "Abrir a versão web/PWA"):
        if required not in installer:
            fail(f"página de instalação Android incompleta: {required}")
    dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")
    for required in ("instalar-apex-combate.html", "releases/Apex-Combate-Demo-v44.apk", "releases/QR-Instalar-Apex-Combate-v44.png"):
        if required not in dockerfile:
            fail(f"artefato Android ausente da imagem Docker: {required}")


def check_master_document() -> None:
    master = (ROOT / "docs/documentacao-mestre-apex-combate.md").read_text(encoding="utf-8")
    if master.count("## Parte ") != 10:
        fail("o documento mestre deve manter exatamente 10 partes")
    for term in ("Apex Combate", "Apex’s Forge", "Apex Central", "Plataforma Universal de Artes Marciais", "DEC-041", "DEC-042", "DEC-043", "DEC-044", "DEC-045", "DEC-046", "DEC-047", "DEC-048"):
        if term not in master:
            fail(f"documento mestre sem termo obrigatório: {term}")


def check_readme_links() -> None:
    for readme_path in (ROOT / "README.md", ROOT / "docs/README.md"):
        content = readme_path.read_text(encoding="utf-8")
        links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", content)
        for link in links:
            if link.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = link.split("#", 1)[0]
            if target and not (readme_path.parent / target).exists():
                fail(f"link local quebrado em {readme_path.relative_to(ROOT)}: {link}")


def main() -> None:
    check_required_files()
    check_python()
    check_html_contract()
    check_manifest()
    check_android_apk()
    check_master_document()
    check_readme_links()
    print("Apex Combate: verificações estáticas concluídas com sucesso.")


if __name__ == "__main__":
    main()
