#!/usr/bin/env python3
"""End-to-end smoke test for a running Apex Combate server."""

from __future__ import annotations

import json
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE_URL = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8080").rstrip("/")


def request(path: str, *, payload: dict | None = None, token: str | None = None) -> tuple[int, bytes, str]:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    headers = {"Accept": "application/json"}
    if payload is not None:
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = Request(BASE_URL + path, data=data, headers=headers, method="POST" if payload is not None else "GET")
    try:
        with urlopen(req, timeout=8) as response:
            return response.status, response.read(), response.headers.get_content_type()
    except HTTPError as error:
        return error.code, error.read(), error.headers.get_content_type()


def wait_for_health() -> dict:
    last_error: Exception | None = None
    for _ in range(40):
        try:
            status, body, _ = request("/api/health")
            if status == 200:
                return json.loads(body)
        except (URLError, TimeoutError, json.JSONDecodeError) as error:
            last_error = error
        time.sleep(0.25)
    raise RuntimeError(f"servidor não ficou pronto: {last_error}")


def main() -> None:
    health = wait_for_health()
    assert health["ok"] is True
    assert health["database"] == "ready"

    status, app, content_type = request("/apex-combate.html?v=40")
    assert status == 200 and b"Apex Combate" in app and content_type == "text/html"

    status, body, _ = request("/api/login/atleta", payload={"documento": "529.982.247-25", "nascimento": "10/05/1998"})
    assert status == 200, body.decode("utf-8", errors="replace")
    login = json.loads(body)
    assert login["ok"] is True and login["perfil"] == "atleta"

    status, body, _ = request("/api/athlete/dashboard", token=login["token"])
    assert status == 200, body.decode("utf-8", errors="replace")
    dashboard = json.loads(body)
    assert dashboard["ok"] is True
    assert dashboard["documents"], "documentos do atleta ausentes"
    assert dashboard["classes"], "turmas do atleta ausentes"
    assert "readiness" in dashboard

    status, body, _ = request("/api/login", payload={"usuario": "RYUZOKAN", "senha": "2026", "perfil": "clube"})
    assert status == 200, body.decode("utf-8", errors="replace")
    club_login = json.loads(body)
    assert club_login["ok"] is True and club_login["role"] == "CLUB_ADMIN"

    status, body, _ = request("/api/club/dashboard", token=club_login["token"])
    assert status == 200, body.decode("utf-8", errors="replace")
    club_dashboard = json.loads(body)
    assert club_dashboard["students"], "alunos do clube ausentes"
    assert club_dashboard["classes"], "turmas do clube ausentes"
    assert club_dashboard["delegations"], "delegação do clube ausente"

    for protected_path in ("/data/.jwt-secret", "/server.py", "/.env", "/documentacao-mestre-apex-combate.md"):
        status, _, _ = request(protected_path)
        assert status == 404, f"arquivo sensível exposto: {protected_path} ({status})"

    print("Apex Combate: smoke test concluído com sucesso.")


if __name__ == "__main__":
    main()
