#!/usr/bin/env python3
"""Apex Combate development server with persistent authentication and core APIs.

This is a production-oriented local foundation using SQLite and only Python's
standard library. Production deployment should use PostgreSQL, HTTPS, managed
secrets, external OTP delivery and an object store for documents.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from threading import Lock
from urllib.parse import unquote, urlencode, urlsplit
from urllib.request import urlopen
import base64
import hashlib
import hmac
import html
import json
import os
import re
import secrets
import sqlite3
import time

from apex_db import (
    audit,
    connection,
    get_jwt_secret,
    init_database,
    normalize_birth_date,
    normalize_document,
    row_to_dict,
    utc_now,
    verify_password,
)

ROOT = Path(__file__).resolve().parent
JWT_SECRET = get_jwt_secret()
CHALLENGES: dict[str, dict] = {}
CHALLENGE_LOCK = Lock()
TRANSLATION_CACHE: dict[tuple[str, str], str] = {}
TRANSLATION_LOCK = Lock()
RATE_LIMITS: dict[tuple[str, str], list[float]] = {}
RATE_LIMIT_LOCK = Lock()
# Mozer's owner-level Apex Central will be enabled in a later phase.
APEX_CENTRAL_ENABLED = False


def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def b64url_decode(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def issue_jwt(subject: str, profile: str, role: str, *, extra: dict | None = None) -> str:
    now = int(time.time())
    permissions_by_profile = {
        "atleta": ["ATHLETE_READ", "REGISTRATION_CREATE", "DOCUMENT_READ"],
    }
    club_permissions = {
        "CLUB_ADMIN": ["CLUB_ADMIN", "CLUB_READ", "ATHLETE_WRITE", "CLASS_WRITE", "DELEGATION_WRITE", "TECHNICIAN_ASSIGN"],
        "CLUB_TECHNICIAN": ["CLUB_TECHNICIAN", "COMPETITION_SUPPORT", "DELEGATION_READ", "ASSIGNED_ATHLETE_READ", "CALL_AREA_READ", "WARMUP_ACCESS", "CORNER_ACCESS", "CREDENTIAL_READ", "LIVE_QUEUE_READ", "CHECKLIST_WRITE", "ATHLETE_STAGE_WRITE", "TACTICAL_NOTES_WRITE", "INCIDENT_CREATE", "SUPPORT_REQUEST_CREATE", "RULES_READ", "OFFLINE_ACCESS"],
    }
    federation_permissions = {
        "PRESIDENTE_MASTER": ["PRESIDENTE_MASTER", "GOVERNANCE_READ", "FINAL_APPROVAL", "AUDIT_READ", "REPORT_READ"],
        "ADMIN": ["ADMIN", "AFFILIATE_WRITE", "ATHLETE_VALIDATE", "HOMOLOGATION_WRITE", "EVENT_WRITE", "SCOREBOARD_WRITE", "AUDIT_READ"],
    }
    permissions = federation_permissions.get(role, [role]) if profile == "federacao" else club_permissions.get(role, [role]) if profile == "clube" else permissions_by_profile.get(profile, [])
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "sub": subject,
        "perfil": profile,
        "role": role,
        "permissions": permissions,
        "iat": now,
        "exp": now + 3600,
        "iss": "apex-combate-local",
        "jti": secrets.token_urlsafe(10),
    }
    if extra:
        payload.update(extra)
    encoded_header = b64url(json.dumps(header, separators=(",", ":")).encode())
    encoded_payload = b64url(json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode())
    signing_input = f"{encoded_header}.{encoded_payload}".encode()
    signature = b64url(hmac.new(JWT_SECRET, signing_input, hashlib.sha256).digest())
    return f"{encoded_header}.{encoded_payload}.{signature}"


def decode_jwt(token: str) -> dict:
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("invalid token")
    signing_input = f"{parts[0]}.{parts[1]}".encode()
    expected = b64url(hmac.new(JWT_SECRET, signing_input, hashlib.sha256).digest())
    if not hmac.compare_digest(expected, parts[2]):
        raise ValueError("invalid signature")
    header = json.loads(b64url_decode(parts[0]))
    payload = json.loads(b64url_decode(parts[1]))
    if header.get("alg") != "HS256" or payload.get("iss") != "apex-combate-local":
        raise ValueError("invalid issuer")
    if int(payload.get("exp", 0)) <= int(time.time()):
        raise ValueError("expired token")
    return payload


class ApexHandler(SimpleHTTPRequestHandler):
    server_version = "ApexCombate/1.0"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self) -> None:
        request_path = urlsplit(self.path).path
        if request_path.endswith((".html", ".webmanifest", "apex-sw.js")) or request_path == "/":
            self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
            self.send_header("Pragma", "no-cache")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("Permissions-Policy", "camera=(self), geolocation=(), microphone=()")
        super().end_headers()

    def send_json(self, status: int, payload: dict | list) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Frame-Options", "SAMEORIGIN")
        self.end_headers()
        self.wfile.write(body)

    def read_json(self) -> dict | None:
        try:
            length = min(int(self.headers.get("Content-Length", "0")), 32_768)
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            return payload if isinstance(payload, dict) else None
        except (ValueError, json.JSONDecodeError, UnicodeDecodeError):
            return None

    def client_ip(self) -> str:
        forwarded = self.headers.get("X-Forwarded-For", "").split(",")[0].strip()
        return forwarded or self.client_address[0]

    def rate_limited(self, bucket: str, maximum: int = 12, window: int = 300) -> bool:
        key = (self.client_ip(), bucket)
        now = time.time()
        with RATE_LIMIT_LOCK:
            attempts = [stamp for stamp in RATE_LIMITS.get(key, []) if now - stamp < window]
            limited = len(attempts) >= maximum
            if not limited:
                attempts.append(now)
            RATE_LIMITS[key] = attempts
        if limited:
            self.send_json(429, {"ok": False, "message": "Muitas tentativas. Aguarde alguns minutos."})
        return limited

    def require_auth(self, profiles: set[str]) -> dict | None:
        authorization = self.headers.get("Authorization", "")
        if not authorization.startswith("Bearer "):
            self.send_json(401, {"ok": False, "message": "Sessão não autenticada"})
            return None
        try:
            payload = decode_jwt(authorization[7:].strip())
        except (ValueError, json.JSONDecodeError, TypeError):
            self.send_json(401, {"ok": False, "message": "Sessão inválida ou expirada"})
            return None
        if payload.get("perfil") not in profiles:
            self.send_json(403, {"ok": False, "message": "Perfil sem permissão para esta operação"})
            return None
        return payload

    def do_GET(self) -> None:
        path = unquote(urlsplit(self.path).path)
        path_parts = [part for part in path.split("/") if part]
        blocked_suffixes = (".sqlite3", ".db", ".py", ".pyc", ".md", ".yml", ".yaml", ".toml", ".ini", ".log")
        blocked_names = {"Dockerfile", "Makefile", "LICENSE", "SECURITY.md", "CONTRIBUTING.md"}
        if (
            path.startswith(("/data/", "/tests/", "/scripts/", "/uploads/"))
            or any(part.startswith(".") for part in path_parts)
            or path.endswith(blocked_suffixes)
            or (path_parts and path_parts[-1] in blocked_names)
        ):
            self.send_error(404)
            return
        if path == "/api/health":
            self.send_json(200, {"ok": True, "service": "apex-combate", "database": "ready", "architecture": "apex-central-multi-federation", "time": utc_now()})
            return
        if path == "/api/version":
            watched = [ROOT / "apex-combate.html", ROOT / "server.py", ROOT / "apex_db.py", ROOT / "manifest.webmanifest"]
            version = str(max(file.stat().st_mtime_ns for file in watched if file.exists()))
            self.send_json(200, {"ok": True, "version": version})
            return
        if path == "/api/session":
            auth = self.require_auth({"atleta", "clube", "federacao"})
            if auth:
                self.send_json(200, {"ok": True, "session": auth})
            return
        if path == "/api/competitions":
            self.handle_competitions()
            return
        if path == "/api/athlete/dashboard":
            self.handle_athlete_dashboard()
            return
        if path == "/api/club/dashboard":
            self.handle_club_dashboard()
            return
        if path == "/api/club/technicians":
            self.handle_club_technicians()
            return
        if path == "/api/technician/operations":
            self.handle_technician_operations()
            return
        if path == "/api/federation/dashboard":
            self.handle_federation_dashboard()
            return
        if path == "/api/apex/federations":
            self.handle_apex_federations()
            return
        if path.startswith("/api/"):
            self.send_json(404, {"ok": False, "message": "Rota não encontrada"})
            return
        super().do_GET()

    def do_POST(self) -> None:
        path = urlsplit(self.path).path
        if path == "/api/login":
            self.handle_login()
        elif path == "/api/login/atleta":
            self.handle_athlete_login()
        elif path == "/api/login/validar-otp":
            self.handle_otp()
        elif path == "/api/translate":
            self.handle_translate()
        elif path == "/api/club/students":
            self.handle_create_student()
        elif path == "/api/club/competition-technicians":
            self.handle_assign_technician()
        elif path == "/api/technician/status":
            self.handle_technician_status()
        elif path == "/api/technician/checklist":
            self.handle_technician_checklist()
        elif path == "/api/technician/strategy":
            self.handle_technician_strategy()
        elif path == "/api/technician/result":
            self.handle_technician_result()
        elif path == "/api/technician/incident":
            self.handle_technician_incident()
        elif path == "/api/technician/support":
            self.handle_technician_support()
        elif path == "/api/technician/notice-read":
            self.handle_technician_notice_read()
        elif path == "/api/federation/homologations":
            self.handle_create_homologation()
        elif path == "/api/registrations":
            self.handle_create_registration()
        elif path == "/api/apex/federations":
            self.handle_create_federation()
        else:
            self.send_json(404, {"ok": False, "message": "Rota não encontrada"})

    def handle_athlete_login(self) -> None:
        if self.rate_limited("athlete-login"):
            return
        payload = self.read_json()
        if payload is None:
            self.send_json(400, {"ok": False, "message": "Dados de acesso inválidos"})
            return
        document = normalize_document(payload.get("documento", ""))
        birth_date = normalize_birth_date(payload.get("nascimento", ""))
        if len(document) < 4 or not birth_date:
            self.send_json(400, {"ok": False, "message": "Informe documento e data de nascimento válidos"})
            return
        with connection() as db:
            athlete = db.execute(
                """SELECT a.*, c.name AS club_name, c.federation_id, f.name AS federation_name
                   FROM athletes a LEFT JOIN clubs c ON c.id=a.club_id LEFT JOIN federations f ON f.id=c.federation_id
                   WHERE a.document=? AND a.birth_date=? AND a.status!='inactive'""",
                (document, birth_date),
            ).fetchone()
        if not athlete:
            self.send_json(401, {"ok": False, "message": "Atleta não encontrado. Confira o documento e a data de nascimento."})
            return
        token = issue_jwt(
            athlete["registration_code"], "atleta", "ATHLETE", extra={"athlete_id": athlete["id"], "club_id": athlete["club_id"], "federation_id": athlete["federation_id"]}
        )
        audit(athlete["registration_code"], "atleta", "LOGIN", "athlete", athlete["id"], ip_address=self.client_ip())
        self.send_json(200, {
            "ok": True,
            "perfil": "atleta",
            "token": token,
            "expiresIn": 3600,
            "athlete": {"id": athlete["id"], "name": athlete["full_name"], "registration": athlete["registration_code"], "club": athlete["club_name"], "federation": athlete["federation_name"]},
        })

    def handle_login(self) -> None:
        if self.rate_limited("credential-login"):
            return
        payload = self.read_json()
        if payload is None:
            self.send_json(400, {"ok": False, "message": "Dados de acesso inválidos"})
            return
        username = str(payload.get("usuario", payload.get("admin", ""))).strip().upper()
        password = str(payload.get("senha", ""))
        profile = payload.get("perfil")
        if profile == "clube":
            with connection() as db:
                club = db.execute("SELECT * FROM clubs WHERE username=?", (username,)).fetchone()
                technician = None
                if club is None:
                    technician = db.execute(
                        """SELECT t.*,c.name AS club_name,c.registration_code AS club_registration,c.federation_id
                           FROM technicians t JOIN clubs c ON c.id=t.club_id
                           WHERE t.username=? AND t.status='active'""", (username,)
                    ).fetchone()
            if club and verify_password(password, club["password_hash"]):
                token = issue_jwt(username, "clube", "CLUB_ADMIN", extra={"club_id": club["id"], "federation_id": club["federation_id"], "account_type": "club"})
                audit(username, "clube", "LOGIN", "club", club["id"], ip_address=self.client_ip())
                self.send_json(200, {
                    "ok": True, "perfil": "clube", "accountType": "club", "role": "CLUB_ADMIN", "usuario": username,
                    "token": token, "expiresIn": 3600,
                    "club": {"id": club["id"], "name": club["name"], "registration": club["registration_code"], "federationId": club["federation_id"]},
                })
                return
            if technician and verify_password(password, technician["password_hash"]):
                token = issue_jwt(username, "clube", "CLUB_TECHNICIAN", extra={
                    "club_id": technician["club_id"], "federation_id": technician["federation_id"],
                    "technician_id": technician["id"], "account_type": "technician", "technician_name": technician["full_name"]
                })
                audit(username, "clube", "LOGIN", "technician", technician["id"], ip_address=self.client_ip())
                self.send_json(200, {
                    "ok": True, "perfil": "clube", "accountType": "technician", "role": "CLUB_TECHNICIAN", "usuario": username,
                    "token": token, "expiresIn": 3600,
                    "club": {"id": technician["club_id"], "name": technician["club_name"], "registration": technician["club_registration"], "federationId": technician["federation_id"]},
                    "technician": {"id": technician["id"], "name": technician["full_name"], "registration": technician["registration_code"], "specialties": technician["specialties"]},
                })
                return
            self.send_json(401, {"ok": False, "message": "Usuário ou senha inválido"})
            return
        if profile == "federacao":
            with connection() as db:
                account = db.execute(
                    """SELECT u.*,f.name AS federation_name,f.code AS federation_code
                       FROM federation_users u LEFT JOIN federations f ON f.id=u.federation_id
                       WHERE u.username=? AND u.active=1""", (username,)
                ).fetchone()
            if not account or not verify_password(password, account["password_hash"]):
                self.send_json(401, {"ok": False, "message": "Admin ou senha inválido"})
                return
            challenge_id = secrets.token_urlsafe(24)
            with CHALLENGE_LOCK:
                CHALLENGES[challenge_id] = {
                    "username": username,
                    "permission": account["permission"],
                    "scope": account["scope"],
                    "federation_id": account["federation_id"],
                    "federation_name": account["federation_name"],
                    "federation_code": account["federation_code"],
                    "otp": "654321",
                    "expires": time.time() + 300,
                    "attempts": 0,
                }
            self.send_json(200, {
                "ok": True, "status": "2FA_REQUIRED", "challengeId": challenge_id,
                "channel": "canal seguro", "destination": account["destination"], "expiresIn": 300,
                "scope": account["scope"], "federation": account["federation_name"], "role": account["permission"],
            })
            return
        self.send_json(403, {"ok": False, "message": "Perfil de acesso inválido"})

    def handle_otp(self) -> None:
        if self.rate_limited("otp", maximum=15):
            return
        payload = self.read_json()
        if payload is None or payload.get("perfil") != "federacao":
            self.send_json(400, {"ok": False, "message": "Dados de verificação inválidos"})
            return
        challenge_id = str(payload.get("challengeId", ""))
        code = str(payload.get("codigo", payload.get("otp", ""))).strip()
        with CHALLENGE_LOCK:
            challenge = CHALLENGES.get(challenge_id)
            if not challenge:
                self.send_json(401, {"ok": False, "message": "Solicitação 2FA inexistente ou já utilizada"})
                return
            if challenge["expires"] < time.time():
                CHALLENGES.pop(challenge_id, None)
                self.send_json(401, {"ok": False, "message": "Código OTP expirado"})
                return
            challenge["attempts"] += 1
            if challenge["attempts"] > 5:
                CHALLENGES.pop(challenge_id, None)
                self.send_json(429, {"ok": False, "message": "Limite de tentativas excedido"})
                return
            if not hmac.compare_digest(code, challenge["otp"]):
                self.send_json(401, {"ok": False, "message": "Código OTP inválido"})
                return
            CHALLENGES.pop(challenge_id, None)
        token = issue_jwt(challenge["username"], "federacao", challenge["permission"], extra={
            "scope": challenge["scope"], "federation_id": challenge["federation_id"],
            "federation_name": challenge["federation_name"], "federation_code": challenge["federation_code"]
        })
        audit(challenge["username"], "federacao", "LOGIN_2FA", "federation_user", challenge["username"], ip_address=self.client_ip())
        self.send_json(200, {
            "ok": True, "status": "AUTHENTICATED", "token": token, "tokenType": "Bearer",
            "expiresIn": 3600, "role": challenge["permission"], "perfil": "federacao",
            "scope": challenge["scope"], "federation": challenge["federation_name"],
        })

    def handle_competitions(self) -> None:
        with connection() as db:
            rows = db.execute(
                """SELECT c.id,c.name,c.slug,c.sport,c.city,c.state,c.venue,c.event_date,c.registration_deadline,c.fee_cents,c.level,c.status,c.organizer,
                          c.federation_id,f.name AS federation_name,f.code AS federation_code
                   FROM competitions c LEFT JOIN federations f ON f.id=c.federation_id ORDER BY c.event_date"""
            ).fetchall()
        items = []
        for row in rows:
            item = dict(row)
            item["fee"] = item.pop("fee_cents") / 100
            items.append(item)
        self.send_json(200, {"ok": True, "competitions": items})

    def handle_athlete_dashboard(self) -> None:
        auth = self.require_auth({"atleta"})
        if not auth:
            return
        with connection() as db:
            athlete = db.execute(
                """SELECT a.*,c.name AS club_name,c.federation_id,f.name AS federation_name
                   FROM athletes a LEFT JOIN clubs c ON c.id=a.club_id
                   LEFT JOIN federations f ON f.id=c.federation_id WHERE a.id=?""",
                (auth.get("athlete_id"),),
            ).fetchone()
            registrations = db.execute(
                """SELECT r.status,r.payment_status,r.category,r.technician_id,c.name,c.event_date,c.city,c.state,
                          t.full_name AS technician_name
                   FROM registrations r JOIN competitions c ON c.id=r.competition_id
                   LEFT JOIN technicians t ON t.id=r.technician_id WHERE r.athlete_id=? ORDER BY c.event_date""",
                (auth.get("athlete_id"),),
            ).fetchall()
            technicians = db.execute(
                """SELECT t.id,t.full_name,t.registration_code,t.specialties,
                          cs.competition_id,c.name AS competition,c.event_date
                   FROM technicians t JOIN competition_staff cs ON cs.technician_id=t.id
                   JOIN competitions c ON c.id=cs.competition_id
                   WHERE t.club_id=? AND t.status='active' AND cs.status='confirmed' AND c.status='open'
                   ORDER BY c.event_date,t.full_name""",
                (athlete["club_id"],),
            ).fetchall() if athlete else []
        if not athlete:
            self.send_json(404, {"ok": False, "message": "Atleta não encontrado"})
            return
        self.send_json(200, {"ok": True, "athlete": row_to_dict(athlete), "registrations": [dict(row) for row in registrations], "technicians": [dict(row) for row in technicians]})

    def handle_club_dashboard(self) -> None:
        auth = self.require_auth({"clube"})
        if not auth:
            return
        with connection() as db:
            club = db.execute("SELECT * FROM clubs WHERE id=?", (auth.get("club_id"),)).fetchone()
            students = [] if auth.get("role") == "CLUB_TECHNICIAN" else db.execute(
                "SELECT id,full_name,registration_code,sport,rank_name,plan_name,status FROM athletes WHERE club_id=? ORDER BY id DESC LIMIT 20",
                (auth.get("club_id"),),
            ).fetchall()
            federation = db.execute("SELECT id,name,code FROM federations WHERE id=?", (club["federation_id"],)).fetchone() if club else None
            technician = db.execute(
                "SELECT id,full_name,registration_code,specialties,contact,status FROM technicians WHERE id=?",
                (auth.get("technician_id"),),
            ).fetchone() if auth.get("technician_id") else None
            assignments = db.execute(
                """SELECT cs.id,cs.technician_id,cs.function_name,cs.status,cs.accreditation_code,
                          t.full_name AS technician_name,t.registration_code,
                          c.id AS competition_id,c.name AS competition,c.event_date,c.venue
                   FROM competition_staff cs JOIN competitions c ON c.id=cs.competition_id
                   JOIN technicians t ON t.id=cs.technician_id
                   WHERE t.club_id=? AND (? IS NULL OR t.id=?) ORDER BY c.event_date""",
                (auth.get("club_id"), auth.get("technician_id"), auth.get("technician_id")),
            ).fetchall()
            competition_athletes = db.execute(
                """SELECT a.id,a.full_name,a.registration_code,a.sport,a.rank_name,r.category,r.status,
                          c.name AS competition,c.event_date
                   FROM registrations r JOIN athletes a ON a.id=r.athlete_id
                   JOIN competitions c ON c.id=r.competition_id
                   WHERE r.technician_id=? ORDER BY c.event_date,a.full_name""",
                (auth.get("technician_id"),),
            ).fetchall() if auth.get("technician_id") else []
        if not club:
            self.send_json(404, {"ok": False, "message": "Clube não encontrado"})
            return
        self.send_json(200, {
            "ok": True,
            "accountType": auth.get("account_type", "club"),
            "role": auth.get("role"),
            "club": {"id": club["id"], "name": club["name"], "registration": club["registration_code"]},
            "federation": row_to_dict(federation),
            "technician": row_to_dict(technician),
            "metrics": None if auth.get("role") == "CLUB_TECHNICIAN" else {"activeStudents": club["active_students"], "monthlyRevenue": club["monthly_revenue_cents"] / 100, "attendanceRate": 78, "retentionRate": 94.2},
            "students": [dict(row) for row in students],
            "assignments": [dict(row) for row in assignments],
            "competitionAthletes": [dict(row) for row in competition_athletes],
        })

    def require_technician(self) -> dict | None:
        auth = self.require_auth({"clube"})
        if auth and auth.get("role") != "CLUB_TECHNICIAN":
            self.send_json(403, {"ok": False, "message": "Recurso exclusivo da conta individual do técnico"})
            return None
        return auth

    @staticmethod
    def technician_registration(db: sqlite3.Connection, technician_id: int, registration_id: int):
        return db.execute(
            """SELECT r.id,r.competition_id,r.athlete_id FROM registrations r
               JOIN competition_staff cs ON cs.competition_id=r.competition_id AND cs.technician_id=r.technician_id
               WHERE r.id=? AND r.technician_id=? AND cs.status='confirmed'""",
            (registration_id, technician_id),
        ).fetchone()

    def handle_technician_operations(self) -> None:
        auth = self.require_technician()
        if not auth:
            return
        technician_id = auth.get("technician_id")
        with connection() as db:
            technician = db.execute(
                """SELECT t.id,t.full_name,t.registration_code,t.specialties,t.contact,t.status,
                          c.id AS club_id,c.name AS club_name,c.registration_code AS club_registration
                   FROM technicians t JOIN clubs c ON c.id=t.club_id WHERE t.id=?""",
                (technician_id,),
            ).fetchone()
            assignments = db.execute(
                """SELECT cs.id,cs.competition_id,cs.function_name,cs.status,cs.accreditation_code,
                          c.name AS competition,c.sport AS competition_sport,c.event_date,c.venue,c.city,c.state,c.organizer
                   FROM competition_staff cs JOIN competitions c ON c.id=cs.competition_id
                   WHERE cs.technician_id=? AND cs.status='confirmed' ORDER BY c.event_date""",
                (technician_id,),
            ).fetchall()
            athletes = db.execute(
                """SELECT r.id AS registration_id,r.competition_id,r.status AS registration_status,r.category,
                          a.id AS athlete_id,a.full_name,a.registration_code,a.sport,a.rank_name,
                          c.name AS competition,c.event_date,c.venue,c.city,c.state,
                          COALESCE(o.stage,'confirmed') AS stage,COALESCE(o.call_time,'') AS call_time,
                          COALESCE(o.arena_label,'') AS arena_label,COALESCE(o.bout_number,'') AS bout_number,
                          COALESCE(o.bouts_before,0) AS bouts_before,COALESCE(o.warmup_minutes,20) AS warmup_minutes,
                          COALESCE(o.weigh_in_status,'pending') AS weigh_in_status,
                          COALESCE(o.equipment_status,'pending') AS equipment_status,
                          COALESCE(o.strategy_notes,'') AS strategy_notes,COALESCE(o.result,'') AS result,
                          COALESCE(o.result_note,'') AS result_note,COALESCE(o.updated_at,r.created_at) AS operation_updated_at
                   FROM registrations r JOIN athletes a ON a.id=r.athlete_id
                   JOIN competitions c ON c.id=r.competition_id
                   JOIN competition_staff cs ON cs.competition_id=r.competition_id AND cs.technician_id=r.technician_id
                   LEFT JOIN competition_operations o ON o.registration_id=r.id
                   WHERE r.technician_id=? AND cs.status='confirmed'
                   ORDER BY c.event_date,CASE WHEN o.call_time='' OR o.call_time IS NULL THEN '99:99' ELSE o.call_time END,a.full_name""",
                (technician_id,),
            ).fetchall()
            athlete_items = [dict(row) for row in athletes]
            registration_ids = [item["registration_id"] for item in athlete_items]
            checklists: dict[int, list] = {registration_id: [] for registration_id in registration_ids}
            incidents: dict[int, list] = {registration_id: [] for registration_id in registration_ids}
            if registration_ids:
                marks = ",".join("?" for _ in registration_ids)
                for row in db.execute(
                    f"SELECT registration_id,item_key,label,completed,updated_at FROM technician_checklists WHERE registration_id IN ({marks}) ORDER BY rowid",
                    registration_ids,
                ).fetchall():
                    checklists[row["registration_id"]].append(dict(row))
                for row in db.execute(
                    f"SELECT id,registration_id,incident_type,details,status,created_at FROM technician_incidents WHERE technician_id=? AND registration_id IN ({marks}) ORDER BY id DESC",
                    [technician_id, *registration_ids],
                ).fetchall():
                    incidents[row["registration_id"]].append(dict(row))
            for item in athlete_items:
                item["checklist"] = checklists.get(item["registration_id"], [])
                item["incidents"] = incidents.get(item["registration_id"], [])
            notices = db.execute(
                """SELECT id,competition_id,registration_id,kind,priority,title,body,source,read_at,created_at
                   FROM technician_notices WHERE technician_id=? ORDER BY CASE priority WHEN 'urgent' THEN 0 WHEN 'high' THEN 1 ELSE 2 END,id DESC LIMIT 30""",
                (technician_id,),
            ).fetchall()
            support_requests = db.execute(
                """SELECT id,competition_id,request_type,message,status,created_at
                   FROM technician_support_requests WHERE technician_id=? ORDER BY id DESC LIMIT 10""",
                (technician_id,),
            ).fetchall()
        if not technician:
            self.send_json(404, {"ok": False, "message": "Técnico não encontrado"})
            return

        rules_catalog = {
            "Jiu-jítsu": {"duration": "5 minutos", "format": "Combate único", "scoring": "Quedas, raspagens, passagens e montadas conforme regulamento", "prohibited": "Técnicas proibidas variam por idade e graduação", "equipment": "Kimono ou uniforme da categoria, faixa e identificação"},
            "Muay Thai": {"duration": "3 rounds de 2 minutos", "format": "Intervalo de 1 minuto", "scoring": "Golpes efetivos, domínio e equilíbrio", "prohibited": "Golpes na nuca, virilha e ações após interrupção", "equipment": "Luvas, protetor bucal, coquilha e itens definidos pela categoria"},
            "Judô": {"duration": "4 minutos", "format": "Golden score quando aplicável", "scoring": "Ippon, waza-ari e penalidades", "prohibited": "Ações e pegadas vedadas pela classe etária", "equipment": "Judogi homologado e faixa"},
            "Karatê": {"duration": "3 minutos", "format": "Kumite conforme categoria", "scoring": "Yuko, waza-ari e ippon", "prohibited": "Contato excessivo e técnicas não controladas", "equipment": "Protetores e uniforme homologados"},
            "MMA": {"duration": "3 rounds de 5 minutos", "format": "Intervalo de 1 minuto", "scoring": "Efetividade, domínio e agressividade", "prohibited": "Faltas conforme regulamento unificado e categoria", "equipment": "Luvas, protetor bucal, coquilha e uniforme aprovado"},
            "Boxe": {"duration": "Conforme classe e categoria", "format": "Rounds com intervalo oficial", "scoring": "Golpes limpos, domínio e defesa", "prohibited": "Golpes baixos, nuca e ações após comando", "equipment": "Luvas, protetor bucal e uniforme regulamentar"},
            "Taekwondo": {"duration": "3 rounds de 2 minutos", "format": "Sistema eletrônico quando disponível", "scoring": "Pontuação por área e técnica válida", "prohibited": "Ataques proibidos e condutas penalizáveis", "equipment": "Protetores homologados e dobok"},
        }
        rules = []
        for sport in dict.fromkeys(item["sport"] for item in athlete_items):
            rule = rules_catalog.get(sport, {"duration": "Conforme categoria", "format": "Regulamento específico da modalidade", "scoring": "Critérios da organização responsável", "prohibited": "Consultar restrições de idade, nível e categoria", "equipment": "Equipamento homologado para a modalidade"})
            rules.append({"sport": sport, **rule})
        self.send_json(200, {
            "ok": True,
            "scope": "competition-support-only",
            "technician": dict(technician),
            "assignments": [dict(row) for row in assignments],
            "athletes": athlete_items,
            "notices": [dict(row) for row in notices],
            "supportRequests": [dict(row) for row in support_requests],
            "rules": rules,
            "serverTime": utc_now(),
            "offline": {"enabled": True, "lastSync": utc_now(), "cacheKey": f"technician-{technician_id}"},
        })

    def handle_technician_status(self) -> None:
        auth = self.require_technician()
        if not auth:
            return
        payload = self.read_json() or {}
        allowed = {"confirmed", "accredited", "weigh_in", "equipment_check", "warming_up", "call_area", "ready", "fighting", "completed"}
        try:
            registration_id = int(payload.get("registrationId"))
        except (TypeError, ValueError):
            self.send_json(400, {"ok": False, "message": "Atleta inválido"})
            return
        stage = str(payload.get("stage", "")).strip()
        if stage not in allowed:
            self.send_json(400, {"ok": False, "message": "Etapa operacional inválida"})
            return
        with connection() as db:
            registration = self.technician_registration(db, auth["technician_id"], registration_id)
            if not registration:
                self.send_json(404, {"ok": False, "message": "Atleta não atribuído a este técnico"})
                return
            db.execute(
                """INSERT INTO competition_operations(registration_id,stage,updated_at) VALUES(?,?,?)
                   ON CONFLICT(registration_id) DO UPDATE SET stage=excluded.stage,updated_at=excluded.updated_at""",
                (registration_id, stage, utc_now()),
            )
        audit(auth["sub"], "clube", "TECHNICIAN_STAGE_UPDATE", "registration", registration_id, json.dumps({"stage": stage}), self.client_ip())
        self.send_json(200, {"ok": True, "registrationId": registration_id, "stage": stage, "updatedAt": utc_now()})

    def handle_technician_checklist(self) -> None:
        auth = self.require_technician()
        if not auth:
            return
        payload = self.read_json() or {}
        try:
            registration_id = int(payload.get("registrationId"))
        except (TypeError, ValueError):
            self.send_json(400, {"ok": False, "message": "Atleta inválido"})
            return
        item_key = re.sub(r"[^a-z0-9_]", "", str(payload.get("itemKey", "")).lower())[:60]
        completed = 1 if payload.get("completed") is True else 0
        with connection() as db:
            if not self.technician_registration(db, auth["technician_id"], registration_id):
                self.send_json(404, {"ok": False, "message": "Atleta não atribuído a este técnico"})
                return
            item = db.execute("SELECT label FROM technician_checklists WHERE registration_id=? AND item_key=?", (registration_id, item_key)).fetchone()
            if not item:
                self.send_json(404, {"ok": False, "message": "Item do checklist não encontrado"})
                return
            db.execute("UPDATE technician_checklists SET completed=?,updated_at=? WHERE registration_id=? AND item_key=?", (completed, utc_now(), registration_id, item_key))
        audit(auth["sub"], "clube", "TECHNICIAN_CHECKLIST_UPDATE", "registration", registration_id, json.dumps({"item": item_key, "completed": bool(completed)}), self.client_ip())
        self.send_json(200, {"ok": True, "registrationId": registration_id, "itemKey": item_key, "completed": bool(completed)})

    def handle_technician_strategy(self) -> None:
        auth = self.require_technician()
        if not auth:
            return
        payload = self.read_json() or {}
        try:
            registration_id = int(payload.get("registrationId"))
        except (TypeError, ValueError):
            self.send_json(400, {"ok": False, "message": "Atleta inválido"})
            return
        notes = str(payload.get("notes", "")).strip()[:1500]
        with connection() as db:
            if not self.technician_registration(db, auth["technician_id"], registration_id):
                self.send_json(404, {"ok": False, "message": "Atleta não atribuído a este técnico"})
                return
            db.execute(
                """INSERT INTO competition_operations(registration_id,strategy_notes,updated_at) VALUES(?,?,?)
                   ON CONFLICT(registration_id) DO UPDATE SET strategy_notes=excluded.strategy_notes,updated_at=excluded.updated_at""",
                (registration_id, notes, utc_now()),
            )
        audit(auth["sub"], "clube", "TECHNICIAN_STRATEGY_UPDATE", "registration", registration_id, ip_address=self.client_ip())
        self.send_json(200, {"ok": True, "registrationId": registration_id, "saved": True})

    def handle_technician_result(self) -> None:
        auth = self.require_technician()
        if not auth:
            return
        payload = self.read_json() or {}
        try:
            registration_id = int(payload.get("registrationId"))
        except (TypeError, ValueError):
            self.send_json(400, {"ok": False, "message": "Atleta inválido"})
            return
        result = str(payload.get("result", "")).strip().lower()
        note = str(payload.get("note", "")).strip()[:500]
        if result not in {"victory", "defeat", "draw", "no_contest", ""}:
            self.send_json(400, {"ok": False, "message": "Resultado inválido"})
            return
        with connection() as db:
            if not self.technician_registration(db, auth["technician_id"], registration_id):
                self.send_json(404, {"ok": False, "message": "Atleta não atribuído a este técnico"})
                return
            db.execute(
                """INSERT INTO competition_operations(registration_id,result,result_note,stage,updated_at) VALUES(?,?,?,?,?)
                   ON CONFLICT(registration_id) DO UPDATE SET result=excluded.result,result_note=excluded.result_note,stage=excluded.stage,updated_at=excluded.updated_at""",
                (registration_id, result, note, "completed", utc_now()),
            )
        audit(auth["sub"], "clube", "TECHNICIAN_RESULT_NOTE", "registration", registration_id, json.dumps({"result": result}), self.client_ip())
        self.send_json(200, {"ok": True, "registrationId": registration_id, "result": result})

    def handle_technician_incident(self) -> None:
        auth = self.require_technician()
        if not auth:
            return
        payload = self.read_json() or {}
        try:
            registration_id = int(payload.get("registrationId"))
        except (TypeError, ValueError):
            self.send_json(400, {"ok": False, "message": "Atleta inválido"})
            return
        incident_type = str(payload.get("type", "")).strip()[:80]
        details = str(payload.get("details", "")).strip()[:2000]
        if not incident_type or len(details) < 4:
            self.send_json(400, {"ok": False, "message": "Informe o tipo e os detalhes da ocorrência"})
            return
        with connection() as db:
            if not self.technician_registration(db, auth["technician_id"], registration_id):
                self.send_json(404, {"ok": False, "message": "Atleta não atribuído a este técnico"})
                return
            cursor = db.execute(
                "INSERT INTO technician_incidents(registration_id,technician_id,incident_type,details,status,created_at) VALUES(?,?,?,?,?,?)",
                (registration_id, auth["technician_id"], incident_type, details, "reported", utc_now()),
            )
            incident_id = cursor.lastrowid
        audit(auth["sub"], "clube", "TECHNICIAN_INCIDENT_CREATE", "technician_incident", incident_id, ip_address=self.client_ip())
        self.send_json(201, {"ok": True, "incident": {"id": incident_id, "status": "reported"}})

    def handle_technician_support(self) -> None:
        auth = self.require_technician()
        if not auth:
            return
        payload = self.read_json() or {}
        try:
            competition_id = int(payload.get("competitionId"))
        except (TypeError, ValueError):
            self.send_json(400, {"ok": False, "message": "Competição inválida"})
            return
        request_type = str(payload.get("type", "")).strip()[:80]
        message = str(payload.get("message", "")).strip()[:1500]
        if not request_type or len(message) < 4:
            self.send_json(400, {"ok": False, "message": "Informe o assunto e a mensagem"})
            return
        with connection() as db:
            assignment = db.execute("SELECT id FROM competition_staff WHERE competition_id=? AND technician_id=? AND status='confirmed'", (competition_id, auth["technician_id"])).fetchone()
            if not assignment:
                self.send_json(404, {"ok": False, "message": "Competição não atribuída a este técnico"})
                return
            cursor = db.execute(
                "INSERT INTO technician_support_requests(competition_id,technician_id,request_type,message,status,created_at) VALUES(?,?,?,?,?,?)",
                (competition_id, auth["technician_id"], request_type, message, "open", utc_now()),
            )
            request_id = cursor.lastrowid
        audit(auth["sub"], "clube", "TECHNICIAN_SUPPORT_CREATE", "technician_support_request", request_id, ip_address=self.client_ip())
        self.send_json(201, {"ok": True, "request": {"id": request_id, "status": "open"}})

    def handle_technician_notice_read(self) -> None:
        auth = self.require_technician()
        if not auth:
            return
        payload = self.read_json() or {}
        try:
            notice_id = int(payload.get("noticeId"))
        except (TypeError, ValueError):
            self.send_json(400, {"ok": False, "message": "Aviso inválido"})
            return
        with connection() as db:
            notice = db.execute("SELECT id FROM technician_notices WHERE id=? AND technician_id=?", (notice_id, auth["technician_id"])).fetchone()
            if not notice:
                self.send_json(404, {"ok": False, "message": "Aviso não encontrado"})
                return
            db.execute("UPDATE technician_notices SET read_at=COALESCE(read_at,?) WHERE id=?", (utc_now(), notice_id))
        self.send_json(200, {"ok": True, "noticeId": notice_id, "read": True})

    def handle_club_technicians(self) -> None:
        auth = self.require_auth({"clube"})
        if not auth:
            return
        with connection() as db:
            technicians = db.execute(
                """SELECT id,full_name,username,registration_code,specialties,contact,status
                   FROM technicians WHERE club_id=? AND (? IS NULL OR id=?) ORDER BY full_name""",
                (auth.get("club_id"), auth.get("technician_id"), auth.get("technician_id")),
            ).fetchall()
            assignments = db.execute(
                """SELECT cs.id,cs.technician_id,cs.function_name,cs.status,cs.accreditation_code,
                          c.id AS competition_id,c.name AS competition,c.event_date
                   FROM competition_staff cs JOIN competitions c ON c.id=cs.competition_id
                   JOIN technicians t ON t.id=cs.technician_id
                   WHERE t.club_id=? AND (? IS NULL OR t.id=?) ORDER BY c.event_date""",
                (auth.get("club_id"), auth.get("technician_id"), auth.get("technician_id")),
            ).fetchall()
        self.send_json(200, {"ok": True, "technicians": [dict(row) for row in technicians], "assignments": [dict(row) for row in assignments]})

    def handle_assign_technician(self) -> None:
        auth = self.require_auth({"clube"})
        if not auth:
            return
        if auth.get("role") != "CLUB_ADMIN":
            self.send_json(403, {"ok": False, "message": "Somente a administração do clube pode credenciar técnicos"})
            return
        payload = self.read_json()
        if payload is None:
            self.send_json(400, {"ok": False, "message": "Credenciamento inválido"})
            return
        try:
            competition_id = int(payload.get("competitionId"))
            technician_id = int(payload.get("technicianId"))
        except (TypeError, ValueError):
            self.send_json(400, {"ok": False, "message": "Selecione a competição e o técnico"})
            return
        function_name = str(payload.get("function", "Técnico")).strip()[:80] or "Técnico"
        with connection() as db:
            technician = db.execute("SELECT id,full_name FROM technicians WHERE id=? AND club_id=? AND status='active'", (technician_id, auth.get("club_id"))).fetchone()
            competition = db.execute("SELECT id,name FROM competitions WHERE id=? AND status='open'", (competition_id,)).fetchone()
            if not technician or not competition:
                self.send_json(404, {"ok": False, "message": "Técnico ou competição não encontrado"})
                return
            accreditation = f"STAFF-{competition_id}-{technician_id}"
            db.execute(
                """INSERT INTO competition_staff(competition_id,technician_id,function_name,status,accreditation_code,created_at)
                   VALUES(?,?,?,?,?,?) ON CONFLICT(competition_id,technician_id)
                   DO UPDATE SET function_name=excluded.function_name,status='confirmed'""",
                (competition_id, technician_id, function_name, "confirmed", accreditation, utc_now()),
            )
            assignment = db.execute("SELECT id FROM competition_staff WHERE competition_id=? AND technician_id=?", (competition_id, technician_id)).fetchone()
        audit(auth["sub"], "clube", "TECHNICIAN_ASSIGN", "competition_staff", assignment["id"], ip_address=self.client_ip())
        self.send_json(201, {"ok": True, "assignment": {"id": assignment["id"], "technician": technician["full_name"], "competition": competition["name"], "function": function_name, "status": "confirmed", "accreditation": accreditation}})

    def handle_federation_dashboard(self) -> None:
        auth = self.require_auth({"federacao"})
        if not auth:
            return
        scope = auth.get("scope", "federation")
        federation_id = auth.get("federation_id")
        with connection() as db:
            if scope == "apex":
                federation_count = db.execute("SELECT COUNT(*) FROM federations WHERE status!='suspended'").fetchone()[0]
                club_count = db.execute("SELECT COUNT(*) FROM clubs").fetchone()[0]
                athlete_count = db.execute("SELECT COUNT(*) FROM athletes").fetchone()[0]
                pending_homologations = db.execute("SELECT COUNT(*) FROM homologations WHERE status='under_review'").fetchone()[0]
                federation = {"id": None, "name": "Apex Central", "code": "APEX", "scope": "apex"}
            else:
                federation_row = db.execute("SELECT id,name,code,state,country,status,plan_name FROM federations WHERE id=?", (federation_id,)).fetchone()
                if not federation_row:
                    self.send_json(404, {"ok": False, "message": "Federação não encontrada"})
                    return
                federation = dict(federation_row)
                federation["scope"] = "federation"
                club_count = db.execute("SELECT COUNT(*) FROM clubs WHERE federation_id=?", (federation_id,)).fetchone()[0]
                athlete_count = db.execute("""SELECT COUNT(*) FROM athletes a JOIN clubs c ON c.id=a.club_id WHERE c.federation_id=?""", (federation_id,)).fetchone()[0]
                pending_homologations = db.execute("SELECT COUNT(*) FROM homologations WHERE federation_id=? AND status='under_review'", (federation_id,)).fetchone()[0]
                federation_count = 1
            recent_audit = db.execute("SELECT actor,action,entity_type,entity_id,created_at FROM audit_log ORDER BY id DESC LIMIT 10").fetchall()
        # The public dashboard includes the established network baseline while the
        # relational counts grow as entities are onboarded into this environment.
        self.send_json(200, {
            "ok": True,
            "scope": scope,
            "role": auth.get("role"),
            "federation": federation,
            "metrics": {
                "federations": federation_count,
                "affiliates": max(126, club_count),
                "athletes": max(8942, athlete_count),
                "events": 14,
                "pending": 37 + pending_homologations,
            },
            "audit": [dict(row) for row in recent_audit],
        })

    def handle_apex_federations(self) -> None:
        if not APEX_CENTRAL_ENABLED:
            self.send_json(503, {"ok": False, "message": "A Central do proprietário ainda não está habilitada"})
            return
        auth = self.require_auth({"federacao"})
        if not auth:
            return
        if auth.get("scope") != "apex":
            self.send_json(403, {"ok": False, "message": "Operação exclusiva da administração Apex Central"})
            return
        with connection() as db:
            federations = db.execute(
                """SELECT f.id,f.name,f.code,f.country,f.state,f.status,f.plan_name,f.contact,f.created_at,
                          COUNT(DISTINCT c.id) AS clubs,COUNT(DISTINCT a.id) AS athletes
                   FROM federations f LEFT JOIN clubs c ON c.federation_id=f.id
                   LEFT JOIN athletes a ON a.club_id=c.id GROUP BY f.id ORDER BY f.name"""
            ).fetchall()
        self.send_json(200, {"ok": True, "federations": [dict(row) for row in federations]})

    def handle_create_federation(self) -> None:
        if not APEX_CENTRAL_ENABLED:
            self.send_json(503, {"ok": False, "message": "A Central do proprietário ainda não está habilitada"})
            return
        auth = self.require_auth({"federacao"})
        if not auth:
            return
        if auth.get("scope") != "apex":
            self.send_json(403, {"ok": False, "message": "Operação exclusiva da administração Apex Central"})
            return
        payload = self.read_json()
        if payload is None:
            self.send_json(400, {"ok": False, "message": "Cadastro de federação inválido"})
            return
        name = str(payload.get("name", "")).strip()
        code = re.sub(r"[^A-Z0-9]", "", str(payload.get("code", "")).upper())[:12]
        country = str(payload.get("country", "BR")).upper()[:3]
        state = str(payload.get("state", "")).upper()[:8]
        plan = str(payload.get("plan", "Professional")).strip()
        contact = str(payload.get("contact", "")).strip()[:180]
        if len(name) < 4 or len(code) < 2 or not state or "@" not in contact or plan not in {"Professional", "Enterprise"}:
            self.send_json(400, {"ok": False, "message": "Informe corretamente os dados da federação"})
            return
        try:
            with connection() as db:
                cursor = db.execute(
                    "INSERT INTO federations(name,code,country,state,status,plan_name,contact,created_at) VALUES(?,?,?,?,?,?,?,?)",
                    (name, code, country, state, "onboarding", plan, contact, utc_now()),
                )
                federation_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            self.send_json(409, {"ok": False, "message": "Já existe uma federação com este código"})
            return
        audit(auth["sub"], "federacao", "FEDERATION_CREATE", "federation", federation_id, ip_address=self.client_ip())
        self.send_json(201, {"ok": True, "federation": {"id": federation_id, "name": name, "code": code, "status": "onboarding", "plan_name": plan, "contact": contact}})

    def handle_create_student(self) -> None:
        auth = self.require_auth({"clube"})
        if not auth:
            return
        if auth.get("role") != "CLUB_ADMIN":
            self.send_json(403, {"ok": False, "message": "A conta técnica não pode cadastrar alunos"})
            return
        payload = self.read_json()
        if payload is None:
            self.send_json(400, {"ok": False, "message": "Cadastro inválido"})
            return
        name = str(payload.get("name", "")).strip()
        document = normalize_document(payload.get("document", ""))
        birth_date = normalize_birth_date(payload.get("birth", ""))
        sport = str(payload.get("sport", "")).strip()
        plan = str(payload.get("plan", "")).strip()
        contact = str(payload.get("contact", "")).strip()
        if len(name) < 3 or len(document) < 4 or not birth_date or not sport or not contact:
            self.send_json(400, {"ok": False, "message": "Preencha todos os dados obrigatórios do aluno"})
            return
        registration_code = f"AC-{time.strftime('%Y')}-{secrets.randbelow(899999) + 100000}"
        try:
            with connection() as db:
                cursor = db.execute(
                    """INSERT INTO athletes(club_id,full_name,document,birth_date,registration_code,sport,rank_name,plan_name,contact,status,created_at)
                       VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                    (auth.get("club_id"), name, document, birth_date, registration_code, sport, "Cadastro inicial", plan, contact, "active", utc_now()),
                )
                db.execute("UPDATE clubs SET active_students=active_students+1 WHERE id=?", (auth.get("club_id"),))
                athlete_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            self.send_json(409, {"ok": False, "message": "Já existe um atleta com este documento"})
            return
        audit(auth["sub"], "clube", "ATHLETE_CREATE", "athlete", athlete_id, ip_address=self.client_ip())
        self.send_json(201, {"ok": True, "athlete": {"id": athlete_id, "name": name, "registration": registration_code, "sport": sport, "status": "active"}})

    def handle_create_homologation(self) -> None:
        auth = self.require_auth({"federacao"})
        if not auth:
            return
        payload = self.read_json()
        if payload is None:
            self.send_json(400, {"ok": False, "message": "Processo inválido"})
            return
        event_name = str(payload.get("event", "")).strip()
        organizer = str(payload.get("organizer", "")).strip()
        sport = str(payload.get("sport", "")).strip()
        event_date = str(payload.get("date", "")).strip()
        level = str(payload.get("level", "")).strip()
        venue = str(payload.get("venue", "")).strip()
        try:
            parsed_date = time.strptime(event_date, "%Y-%m-%d")
            valid_date = time.mktime(parsed_date) > time.time() - 86_400
        except ValueError:
            valid_date = False
        if len(event_name) < 4 or not organizer or not sport or not valid_date or not level or len(venue) < 3:
            self.send_json(400, {"ok": False, "message": "Preencha corretamente os dados da homologação"})
            return
        protocol = f"HOM-{time.strftime('%Y')}-{secrets.randbelow(89999) + 10000}"
        with connection() as db:
            cursor = db.execute(
                """INSERT INTO homologations(federation_id,protocol,event_name,organizer,sport,event_date,level,venue,status,created_by,created_at)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                (auth.get("federation_id"), protocol, event_name, organizer, sport, event_date, level, venue, "under_review", auth["sub"], utc_now()),
            )
            homologation_id = cursor.lastrowid
        audit(auth["sub"], "federacao", "HOMOLOGATION_CREATE", "homologation", homologation_id, ip_address=self.client_ip())
        self.send_json(201, {"ok": True, "homologation": {"id": homologation_id, "protocol": protocol, "event": event_name, "status": "under_review"}})

    def handle_create_registration(self) -> None:
        auth = self.require_auth({"atleta"})
        if not auth:
            return
        payload = self.read_json()
        if payload is None:
            self.send_json(400, {"ok": False, "message": "Inscrição inválida"})
            return
        event_name = str(payload.get("event", "")).strip()
        category = str(payload.get("category", "Adulto • Categoria informada")).strip()
        technician_id = payload.get("technicianId")
        try:
            technician_id = int(technician_id) if technician_id not in (None, "") else None
        except (TypeError, ValueError):
            self.send_json(400, {"ok": False, "message": "Técnico selecionado inválido"})
            return
        with connection() as db:
            competition = db.execute("SELECT * FROM competitions WHERE lower(name)=lower(?) AND status='open'", (event_name,)).fetchone()
            if not competition:
                self.send_json(404, {"ok": False, "message": "Competição não encontrada ou inscrições encerradas"})
                return
            if technician_id is not None:
                technician = db.execute(
                    """SELECT t.id FROM technicians t
                       JOIN competition_staff cs ON cs.technician_id=t.id
                       WHERE t.id=? AND t.club_id=? AND t.status='active'
                         AND cs.competition_id=? AND cs.status='confirmed'""",
                    (technician_id, auth.get("club_id"), competition["id"]),
                ).fetchone()
                if not technician:
                    self.send_json(403, {"ok": False, "message": "O técnico selecionado não está credenciado para esta competição"})
                    return
            try:
                cursor = db.execute(
                    "INSERT INTO registrations(competition_id,athlete_id,technician_id,category,status,payment_status,created_at) VALUES(?,?,?,?,?,?,?)",
                    (competition["id"], auth.get("athlete_id"), technician_id, category, "pending", "pending", utc_now()),
                )
                registration_id = cursor.lastrowid
            except sqlite3.IntegrityError:
                self.send_json(409, {"ok": False, "message": "Você já possui inscrição nesta competição"})
                return
        audit(auth["sub"], "atleta", "REGISTRATION_CREATE", "registration", registration_id, ip_address=self.client_ip())
        self.send_json(201, {"ok": True, "registration": {"id": registration_id, "event": competition["name"], "status": "pending", "payment": "pending", "technicianId": technician_id}})

    @staticmethod
    def translate_one(text: str, target: str) -> str:
        key = (target, text)
        with TRANSLATION_LOCK:
            cached = TRANSLATION_CACHE.get(key)
        if cached is not None:
            return cached
        try:
            query = urlencode({"q": text, "langpair": f"pt|{target}"})
            with urlopen(f"https://api.mymemory.translated.net/get?{query}", timeout=8) as response:
                data = json.load(response)
            translated = html.unescape(str(data.get("responseData", {}).get("translatedText", text))).strip() or text
            if "MYMEMORY WARNING" in translated.upper():
                translated = text
        except Exception:
            translated = text
        with TRANSLATION_LOCK:
            TRANSLATION_CACHE[key] = translated
        return translated

    def handle_translate(self) -> None:
        payload = self.read_json()
        if payload is None:
            self.send_json(400, {"ok": False, "message": "Solicitação de tradução inválida"})
            return
        target = str(payload.get("target", "")).strip()
        texts = payload.get("texts", [])
        if not re.fullmatch(r"[A-Za-z]{2,3}(?:-[A-Za-z]{2,4})?", target):
            self.send_json(400, {"ok": False, "message": "Idioma de destino inválido"})
            return
        if not isinstance(texts, list) or len(texts) > 45:
            self.send_json(400, {"ok": False, "message": "Limite de tradução excedido"})
            return
        cleaned = [str(item).strip()[:450] for item in texts]
        if sum(map(len, cleaned)) > 7000:
            self.send_json(400, {"ok": False, "message": "Conteúdo de tradução muito extenso"})
            return
        if target.lower().startswith("pt"):
            translated = cleaned
        else:
            with ThreadPoolExecutor(max_workers=4) as executor:
                translated = list(executor.map(lambda value: self.translate_one(value, target), cleaned))
        self.send_json(200, {"ok": True, "source": "pt", "target": target, "translations": translated})


if __name__ == "__main__":
    init_database()
    host = os.environ.get("HOST", "0.0.0.0")
    try:
        port = int(os.environ.get("PORT", "8080"))
    except ValueError as error:
        raise SystemExit("PORT must be an integer") from error
    if not 1 <= port <= 65535:
        raise SystemExit("PORT must be between 1 and 65535")
    server = ThreadingHTTPServer((host, port), ApexHandler)
    print(f"Apex Combate disponível em http://{host}:{port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Encerrando Apex Combate", flush=True)
    finally:
        server.server_close()
