#!/usr/bin/env python3
"""Static project checks used locally and by GitHub Actions."""

from __future__ import annotations

import json
import py_compile
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = (
    "apex-combate.html",
    "index.html",
    "server.py",
    "apex_db.py",
    "manifest.webmanifest",
    "apex-sw.js",
    "documentacao-mestre-apex-combate.md",
    "registro-de-decisoes-apex-combate.md",
    "README.md",
    ".gitignore",
    "Dockerfile",
)


def fail(message: str) -> None:
    print(f"ERRO: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_required_files() -> None:
    missing = [name for name in REQUIRED_FILES if not (ROOT / name).is_file()]
    if missing:
        fail("arquivos obrigatórios ausentes: " + ", ".join(missing))


def check_python() -> None:
    for name in ("server.py", "apex_db.py", "scripts/smoke_test.py"):
        py_compile.compile(str(ROOT / name), doraise=True)


def check_html_contract() -> None:
    html = (ROOT / "apex-combate.html").read_text(encoding="utf-8")
    choices = re.findall(r'data-role-choice="([^"]+)"', html)
    if choices != ["athlete", "academy", "federation"]:
        fail(f"perfis públicos inesperados: {choices}")
    required = ("ATLETA", "CLUBE", "FEDERAÇÃO", "manifest.webmanifest", "apex-sw.js?v=37")
    for value in required:
        if value not in html:
            fail(f"contrato HTML ausente: {value}")


def check_manifest() -> None:
    manifest = json.loads((ROOT / "manifest.webmanifest").read_text(encoding="utf-8"))
    if manifest.get("name") != "Apex Combate":
        fail("nome inválido no manifesto")
    if manifest.get("display") != "standalone" or manifest.get("orientation") != "any":
        fail("configuração PWA incompleta")
    for icon in manifest.get("icons", []):
        icon_path = ROOT / icon.get("src", "")
        if not icon_path.is_file():
            fail(f"ícone PWA ausente: {icon_path.relative_to(ROOT)}")


def check_master_document() -> None:
    master = (ROOT / "documentacao-mestre-apex-combate.md").read_text(encoding="utf-8")
    if master.count("## Parte ") != 10:
        fail("o documento mestre deve manter exatamente 10 partes")
    for term in ("Apex Combate", "Apex’s Forge", "Apex Central", "DEC-037"):
        if term not in master:
            fail(f"documento mestre sem termo obrigatório: {term}")


def check_readme_links() -> None:
    content = (ROOT / "README.md").read_text(encoding="utf-8")
    links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", content)
    for link in links:
        if link.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = link.split("#", 1)[0]
        if target and not (ROOT / target).exists():
            fail(f"link local quebrado no README: {link}")


def main() -> None:
    check_required_files()
    check_python()
    check_html_contract()
    check_manifest()
    check_master_document()
    check_readme_links()
    print("Apex Combate: verificações estáticas concluídas com sucesso.")


if __name__ == "__main__":
    main()
