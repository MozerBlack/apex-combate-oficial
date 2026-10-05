#!/usr/bin/env python3
"""Integration test for Apex Combate v38 athlete and club flows."""

from __future__ import annotations

import json
import sys
from urllib.error import HTTPError
from urllib.request import Request, urlopen

BASE_URL = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8080").rstrip("/")


def request(path: str, payload: dict | None = None, token: str = "") -> tuple[int, dict]:
    headers = {"Accept": "application/json"}
    data = None
    method = "GET"
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
        method = "POST"
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = Request(BASE_URL + path, data=data, headers=headers, method=method)
    try:
        with urlopen(req, timeout=10) as response:
            return response.status, json.loads(response.read())
    except HTTPError as error:
        return error.code, json.loads(error.read() or b"{}")


def main() -> None:
    status, athlete_login = request("/api/login/atleta", {"documento": "52998224725", "nascimento": "1998-05-10"})
    assert status == 200 and athlete_login["ok"]
    athlete_token = athlete_login["token"]

    status, profile = request("/api/athlete/profile", {
        "email": "rafael@example.com", "phone": "+55 41 99999-4821", "weight": "80,1",
        "category": "Adulto • Médio • Até 82,3 kg", "emergencyName": "Ana Martins",
        "emergencyPhone": "+55 41 98888-4821",
    }, athlete_token)
    assert status == 200 and profile["profile"]["weight_kg"] == 80.1

    status, document = request("/api/athlete/documents", {
        "type": "graduation_certificate", "fileName": "graduacao-rafael.pdf",
        "issuedAt": "2026-03-18", "expiresAt": "2028-03-18",
    }, athlete_token)
    assert status == 201 and document["document"]["status"] == "pending"

    status, club_login = request("/api/login", {"usuario": "RYUZOKAN", "senha": "2026", "perfil": "clube"})
    assert status == 200 and club_login["role"] == "CLUB_ADMIN"
    club_token = club_login["token"]

    status, club_dashboard = request("/api/club/dashboard", token=club_token)
    assert status == 200 and club_dashboard["students"] and club_dashboard["classes"]
    athlete_id = next(item["id"] for item in club_dashboard["students"] if item["registration_code"] == "AC-2026-001842")
    technician_id = club_dashboard["assignments"][0]["technician_id"]
    competition_id = club_dashboard["delegations"][0]["competition_id"]

    status, new_class = request("/api/club/classes", {
        "name": "Treino técnico v38", "sport": "Jiu-jítsu", "level": "Competidores",
        "technicianId": technician_id, "weekday": 2, "startTime": "18:00",
        "duration": 75, "capacity": 18, "location": "Tatame de testes",
    }, club_token)
    assert status == 201 and new_class["class"]["status"] == "active"

    status, attendance = request("/api/club/attendance", {
        "classId": new_class["class"]["id"], "athleteId": athlete_id,
    }, club_token)
    assert status == 201 and attendance["attendance"]["athlete"] == "Rafael Martins"

    status, delegation = request("/api/club/delegations/members", {
        "competitionId": competition_id, "athleteId": athlete_id,
        "approvalStatus": "approved", "documentsStatus": "verified",
        "categoryStatus": "confirmed", "paymentStatus": "paid",
    }, club_token)
    assert status == 200 and delegation["approval_status"] == "approved"

    status, updated_dashboard = request("/api/club/dashboard", token=club_token)
    assert status == 200
    assert any(item["name"] == "Treino técnico v38" for item in updated_dashboard["classes"])
    assert updated_dashboard["metrics"]["attendanceToday"] >= 1

    status, technician_login = request("/api/login", {"usuario": "TECNICO.MARCELO", "senha": "TECNICO2026", "perfil": "clube"})
    assert status == 200 and technician_login["role"] == "CLUB_TECHNICIAN"
    status, denied = request("/api/club/classes", {
        "name": "Turma indevida", "sport": "Jiu-jítsu", "level": "Todos", "weekday": 1,
        "startTime": "08:00", "duration": 60, "capacity": 10, "location": "Tatame",
    }, technician_login["token"])
    assert status == 403 and denied["ok"] is False

    print("Apex Combate v38: fluxo integrado de atleta e clube aprovado.")


if __name__ == "__main__":
    main()
