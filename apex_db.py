#!/usr/bin/env python3
"""Persistent data layer for Apex Combate's local development server.

Uses only Python's standard library so the preview can run without external
services. The schema is deliberately portable to PostgreSQL for production.
"""

from __future__ import annotations

from contextlib import contextmanager
from datetime import date, datetime, timezone
from pathlib import Path
import base64
import hashlib
import hmac
import os
import re
import secrets
import sqlite3

ROOT = Path(__file__).resolve().parent
DATA_DIR = Path(os.environ.get("APEX_DATA_DIR", str(ROOT / "data"))).expanduser().resolve()
DB_PATH = Path(os.environ.get("APEX_DB_PATH", str(DATA_DIR / "apex-combate.sqlite3"))).expanduser().resolve()
SECRET_PATH = Path(os.environ.get("APEX_JWT_SECRET_FILE", str(DATA_DIR / ".jwt-secret"))).expanduser().resolve()
PBKDF2_ITERATIONS = 260_000


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def normalize_document(value: str) -> str:
    return "".join(character for character in str(value).upper() if character.isalnum())


def normalize_birth_date(value: str) -> str | None:
    clean = str(value).strip()
    for pattern in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d"):
        try:
            parsed = datetime.strptime(clean, pattern).date()
            if date(1900, 1, 1) <= parsed <= date.today():
                return parsed.isoformat()
        except ValueError:
            pass
    digits = re.sub(r"\D", "", clean)
    if len(digits) == 8:
        candidates = [digits[:4] + "-" + digits[4:6] + "-" + digits[6:]] if digits[:4].isdigit() and int(digits[:4]) >= 1900 else []
        candidates.append(digits[4:] + "-" + digits[2:4] + "-" + digits[:2])
        for candidate in candidates:
            try:
                parsed = date.fromisoformat(candidate)
                if date(1900, 1, 1) <= parsed <= date.today():
                    return parsed.isoformat()
            except ValueError:
                pass
    return None


def hash_password(password: str, *, salt: bytes | None = None) -> str:
    salt = salt or secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${base64.urlsafe_b64encode(salt).decode()}${base64.urlsafe_b64encode(digest).decode()}"


def verify_password(password: str, encoded: str) -> bool:
    try:
        algorithm, iterations, salt_text, digest_text = encoded.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        salt = base64.urlsafe_b64decode(salt_text.encode())
        expected = base64.urlsafe_b64decode(digest_text.encode())
        actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, int(iterations))
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def get_jwt_secret() -> bytes:
    configured_secret = os.environ.get("APEX_JWT_SECRET", "").encode("utf-8")
    if configured_secret:
        if len(configured_secret) < 32:
            raise RuntimeError("APEX_JWT_SECRET must contain at least 32 characters")
        return configured_secret
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SECRET_PATH.parent.mkdir(parents=True, exist_ok=True)
    if SECRET_PATH.exists():
        secret = SECRET_PATH.read_bytes()
        if len(secret) >= 32:
            return secret
    secret = secrets.token_bytes(48)
    SECRET_PATH.write_bytes(secret)
    try:
        os.chmod(SECRET_PATH, 0o600)
    except OSError:
        pass
    return secret


@contextmanager
def connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(DB_PATH, timeout=10)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    try:
        yield db
        db.commit()
    finally:
        db.close()


def row_to_dict(row: sqlite3.Row | None) -> dict | None:
    return dict(row) if row is not None else None


def init_database() -> None:
    with connection() as db:
        db.executescript(
            """
            PRAGMA journal_mode = WAL;
            CREATE TABLE IF NOT EXISTS federations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                code TEXT NOT NULL UNIQUE,
                country TEXT NOT NULL DEFAULT 'BR',
                state TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'active',
                plan_name TEXT NOT NULL DEFAULT 'Enterprise',
                contact TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS clubs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                federation_id INTEGER REFERENCES federations(id),
                name TEXT NOT NULL,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                city TEXT NOT NULL,
                state TEXT NOT NULL DEFAULT 'PR',
                status TEXT NOT NULL DEFAULT 'regular',
                registration_code TEXT NOT NULL UNIQUE,
                active_students INTEGER NOT NULL DEFAULT 0,
                monthly_revenue_cents INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS athletes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                club_id INTEGER REFERENCES clubs(id),
                full_name TEXT NOT NULL,
                document TEXT NOT NULL UNIQUE,
                birth_date TEXT NOT NULL,
                registration_code TEXT NOT NULL UNIQUE,
                sport TEXT NOT NULL,
                rank_name TEXT NOT NULL DEFAULT '',
                plan_name TEXT NOT NULL DEFAULT '',
                contact TEXT NOT NULL DEFAULT '',
                email TEXT NOT NULL DEFAULT '',
                phone TEXT NOT NULL DEFAULT '',
                weight_kg REAL,
                current_category TEXT NOT NULL DEFAULT '',
                emergency_name TEXT NOT NULL DEFAULT '',
                emergency_phone TEXT NOT NULL DEFAULT '',
                profile_updated_at TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'active',
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS athlete_documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                athlete_id INTEGER NOT NULL REFERENCES athletes(id) ON DELETE CASCADE,
                document_type TEXT NOT NULL,
                file_name TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'pending',
                issued_at TEXT NOT NULL DEFAULT '',
                expires_at TEXT NOT NULL DEFAULT '',
                reviewed_by TEXT NOT NULL DEFAULT '',
                notes TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                UNIQUE(athlete_id, document_type)
            );
            CREATE TABLE IF NOT EXISTS athlete_guardians (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                athlete_id INTEGER NOT NULL REFERENCES athletes(id) ON DELETE CASCADE,
                full_name TEXT NOT NULL,
                relationship TEXT NOT NULL,
                document TEXT NOT NULL DEFAULT '',
                phone TEXT NOT NULL,
                email TEXT NOT NULL DEFAULT '',
                authorized_competitions INTEGER NOT NULL DEFAULT 0,
                emergency_contact INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL,
                UNIQUE(athlete_id, document)
            );
            CREATE TABLE IF NOT EXISTS technicians (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                club_id INTEGER NOT NULL REFERENCES clubs(id),
                full_name TEXT NOT NULL,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                document TEXT NOT NULL UNIQUE,
                registration_code TEXT NOT NULL UNIQUE,
                specialties TEXT NOT NULL DEFAULT '',
                contact TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'active',
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS federation_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                federation_id INTEGER REFERENCES federations(id),
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                permission TEXT NOT NULL,
                scope TEXT NOT NULL DEFAULT 'federation',
                destination TEXT NOT NULL,
                active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS competitions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                federation_id INTEGER REFERENCES federations(id),
                name TEXT NOT NULL UNIQUE,
                slug TEXT NOT NULL UNIQUE,
                sport TEXT NOT NULL,
                city TEXT NOT NULL,
                state TEXT NOT NULL,
                venue TEXT NOT NULL,
                event_date TEXT NOT NULL,
                registration_deadline TEXT NOT NULL,
                fee_cents INTEGER NOT NULL DEFAULT 0,
                level TEXT NOT NULL DEFAULT 'Estadual',
                status TEXT NOT NULL DEFAULT 'open',
                organizer TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS competition_staff (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                competition_id INTEGER NOT NULL REFERENCES competitions(id),
                technician_id INTEGER NOT NULL REFERENCES technicians(id),
                function_name TEXT NOT NULL DEFAULT 'Técnico',
                status TEXT NOT NULL DEFAULT 'confirmed',
                accreditation_code TEXT NOT NULL UNIQUE,
                created_at TEXT NOT NULL,
                UNIQUE(competition_id, technician_id)
            );
            CREATE TABLE IF NOT EXISTS club_classes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                club_id INTEGER NOT NULL REFERENCES clubs(id) ON DELETE CASCADE,
                technician_id INTEGER REFERENCES technicians(id),
                name TEXT NOT NULL,
                sport TEXT NOT NULL,
                level_name TEXT NOT NULL DEFAULT 'Todos os níveis',
                weekday INTEGER NOT NULL,
                start_time TEXT NOT NULL,
                duration_minutes INTEGER NOT NULL DEFAULT 60,
                capacity INTEGER NOT NULL DEFAULT 20,
                location TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'active',
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS class_enrollments (
                class_id INTEGER NOT NULL REFERENCES club_classes(id) ON DELETE CASCADE,
                athlete_id INTEGER NOT NULL REFERENCES athletes(id) ON DELETE CASCADE,
                status TEXT NOT NULL DEFAULT 'active',
                joined_at TEXT NOT NULL,
                PRIMARY KEY(class_id, athlete_id)
            );
            CREATE TABLE IF NOT EXISTS attendance_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_id INTEGER NOT NULL REFERENCES club_classes(id) ON DELETE CASCADE,
                athlete_id INTEGER NOT NULL REFERENCES athletes(id) ON DELETE CASCADE,
                checked_in_at TEXT NOT NULL,
                source TEXT NOT NULL DEFAULT 'club',
                recorded_by TEXT NOT NULL DEFAULT '',
                UNIQUE(class_id, athlete_id, checked_in_at)
            );
            CREATE TABLE IF NOT EXISTS delegations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                club_id INTEGER NOT NULL REFERENCES clubs(id) ON DELETE CASCADE,
                competition_id INTEGER NOT NULL REFERENCES competitions(id) ON DELETE CASCADE,
                name TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'draft',
                deadline TEXT NOT NULL DEFAULT '',
                notes TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL,
                UNIQUE(club_id, competition_id)
            );
            CREATE TABLE IF NOT EXISTS delegation_members (
                delegation_id INTEGER NOT NULL REFERENCES delegations(id) ON DELETE CASCADE,
                athlete_id INTEGER NOT NULL REFERENCES athletes(id) ON DELETE CASCADE,
                registration_id INTEGER REFERENCES registrations(id),
                approval_status TEXT NOT NULL DEFAULT 'pending',
                documents_status TEXT NOT NULL DEFAULT 'pending',
                category_status TEXT NOT NULL DEFAULT 'pending',
                payment_status TEXT NOT NULL DEFAULT 'pending',
                added_at TEXT NOT NULL,
                PRIMARY KEY(delegation_id, athlete_id)
            );
            CREATE TABLE IF NOT EXISTS registrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                competition_id INTEGER NOT NULL REFERENCES competitions(id),
                athlete_id INTEGER NOT NULL REFERENCES athletes(id),
                technician_id INTEGER REFERENCES technicians(id),
                category TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                payment_status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL,
                UNIQUE(competition_id, athlete_id)
            );
            CREATE TABLE IF NOT EXISTS competition_operations (
                registration_id INTEGER PRIMARY KEY REFERENCES registrations(id) ON DELETE CASCADE,
                stage TEXT NOT NULL DEFAULT 'confirmed',
                call_time TEXT NOT NULL DEFAULT '',
                arena_label TEXT NOT NULL DEFAULT '',
                bout_number TEXT NOT NULL DEFAULT '',
                bouts_before INTEGER NOT NULL DEFAULT 0,
                warmup_minutes INTEGER NOT NULL DEFAULT 20,
                weigh_in_status TEXT NOT NULL DEFAULT 'pending',
                equipment_status TEXT NOT NULL DEFAULT 'pending',
                strategy_notes TEXT NOT NULL DEFAULT '',
                result TEXT NOT NULL DEFAULT '',
                result_note TEXT NOT NULL DEFAULT '',
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS technician_checklists (
                registration_id INTEGER NOT NULL REFERENCES registrations(id) ON DELETE CASCADE,
                item_key TEXT NOT NULL,
                label TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0,
                updated_at TEXT NOT NULL,
                PRIMARY KEY(registration_id,item_key)
            );
            CREATE TABLE IF NOT EXISTS technician_notices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                competition_id INTEGER NOT NULL REFERENCES competitions(id),
                technician_id INTEGER NOT NULL REFERENCES technicians(id),
                registration_id INTEGER REFERENCES registrations(id),
                kind TEXT NOT NULL DEFAULT 'info',
                priority TEXT NOT NULL DEFAULT 'normal',
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                source TEXT NOT NULL DEFAULT 'Organização',
                read_at TEXT,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS technician_incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                registration_id INTEGER NOT NULL REFERENCES registrations(id),
                technician_id INTEGER NOT NULL REFERENCES technicians(id),
                incident_type TEXT NOT NULL,
                details TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'reported',
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS technician_support_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                competition_id INTEGER NOT NULL REFERENCES competitions(id),
                technician_id INTEGER NOT NULL REFERENCES technicians(id),
                request_type TEXT NOT NULL,
                message TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'open',
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS homologations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                federation_id INTEGER REFERENCES federations(id),
                protocol TEXT NOT NULL UNIQUE,
                event_name TEXT NOT NULL,
                organizer TEXT NOT NULL,
                sport TEXT NOT NULL,
                event_date TEXT NOT NULL,
                level TEXT NOT NULL,
                venue TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'under_review',
                created_by TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                actor TEXT NOT NULL,
                profile TEXT NOT NULL,
                action TEXT NOT NULL,
                entity_type TEXT NOT NULL,
                entity_id TEXT NOT NULL,
                metadata TEXT NOT NULL DEFAULT '{}',
                ip_address TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_athletes_club ON athletes(club_id);
            CREATE INDEX IF NOT EXISTS idx_athlete_documents ON athlete_documents(athlete_id,status);
            CREATE INDEX IF NOT EXISTS idx_guardians_athlete ON athlete_guardians(athlete_id);
            CREATE INDEX IF NOT EXISTS idx_technicians_club ON technicians(club_id);
            CREATE INDEX IF NOT EXISTS idx_classes_club ON club_classes(club_id,weekday,start_time);
            CREATE INDEX IF NOT EXISTS idx_attendance_athlete ON attendance_records(athlete_id,checked_in_at DESC);
            CREATE INDEX IF NOT EXISTS idx_delegations_club ON delegations(club_id,competition_id);
            CREATE INDEX IF NOT EXISTS idx_staff_competition ON competition_staff(competition_id);
            CREATE INDEX IF NOT EXISTS idx_operations_stage ON competition_operations(stage);
            CREATE INDEX IF NOT EXISTS idx_notices_technician ON technician_notices(technician_id,created_at DESC);
            CREATE INDEX IF NOT EXISTS idx_incidents_technician ON technician_incidents(technician_id,created_at DESC);
            CREATE INDEX IF NOT EXISTS idx_support_technician ON technician_support_requests(technician_id,created_at DESC);
            CREATE INDEX IF NOT EXISTS idx_competitions_date ON competitions(event_date);
            CREATE INDEX IF NOT EXISTS idx_audit_created ON audit_log(created_at DESC);
            """
        )
        migrate_schema(db)
        seed_database(db)


def ensure_column(db: sqlite3.Connection, table: str, column: str, definition: str) -> None:
    columns = {row[1] for row in db.execute(f"PRAGMA table_info({table})").fetchall()}
    if column not in columns:
        db.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")


def migrate_schema(db: sqlite3.Connection) -> None:
    """Small in-place migrations for persisted development databases."""
    ensure_column(db, "federations", "contact", "TEXT NOT NULL DEFAULT ''")
    ensure_column(db, "clubs", "federation_id", "INTEGER")
    ensure_column(db, "federation_users", "federation_id", "INTEGER")
    ensure_column(db, "federation_users", "scope", "TEXT NOT NULL DEFAULT 'federation'")
    ensure_column(db, "competitions", "federation_id", "INTEGER")
    ensure_column(db, "registrations", "technician_id", "INTEGER")
    ensure_column(db, "athletes", "email", "TEXT NOT NULL DEFAULT ''")
    ensure_column(db, "athletes", "phone", "TEXT NOT NULL DEFAULT ''")
    ensure_column(db, "athletes", "weight_kg", "REAL")
    ensure_column(db, "athletes", "current_category", "TEXT NOT NULL DEFAULT ''")
    ensure_column(db, "athletes", "emergency_name", "TEXT NOT NULL DEFAULT ''")
    ensure_column(db, "athletes", "emergency_phone", "TEXT NOT NULL DEFAULT ''")
    ensure_column(db, "athletes", "profile_updated_at", "TEXT NOT NULL DEFAULT ''")
    ensure_column(db, "homologations", "federation_id", "INTEGER")
    db.execute("CREATE INDEX IF NOT EXISTS idx_clubs_federation ON clubs(federation_id)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_competitions_federation ON competitions(federation_id)")


def seed_database(db: sqlite3.Connection) -> None:
    now = utc_now()
    federation_seeds = [
        ("Federação Paranaense de Artes Marciais", "FPAM", "BR", "PR", "active", "Enterprise", now),
        ("Federação Catarinense de Artes Marciais", "FECAM-SC", "BR", "SC", "active", "Professional", now),
        ("Federação Gaúcha de Esportes de Combate", "FGERGS", "BR", "RS", "active", "Enterprise", now),
        ("Federação de Artes Marciais de São Paulo", "FEMASP", "BR", "SP", "onboarding", "Professional", now),
        ("Federação de Esportes de Combate do Rio de Janeiro", "FECRJ", "BR", "RJ", "active", "Professional", now),
    ]
    db.executemany(
        """INSERT OR IGNORE INTO federations(name,code,country,state,status,plan_name,created_at)
           VALUES(?,?,?,?,?,?,?)""",
        federation_seeds,
    )
    federation_id = db.execute("SELECT id FROM federations WHERE code='FPAM'").fetchone()[0]
    if db.execute("SELECT COUNT(*) FROM clubs").fetchone()[0] == 0:
        db.execute(
            """INSERT INTO clubs(federation_id,name,username,password_hash,city,state,registration_code,active_students,monthly_revenue_cents,created_at)
               VALUES(?,?,?,?,?,?,?,?,?,?)""",
            (federation_id, "Dojo Norte", "RYUZOKAN", hash_password("2026"), "Curitiba", "PR", "FIL-PR-00126", 184, 2_486_000, now),
        )
    db.execute("UPDATE clubs SET federation_id=? WHERE federation_id IS NULL", (federation_id,))
    club_id = db.execute("SELECT id FROM clubs WHERE username='RYUZOKAN'").fetchone()[0]
    if db.execute("SELECT COUNT(*) FROM athletes").fetchone()[0] == 0:
        athletes = [
            (club_id, "Rafael Martins", "52998224725", "1998-05-10", "AC-2026-001842", "Jiu-jítsu", "Faixa azul • 3º grau", "Competidor", "rafael@example.com", "active", now),
            (club_id, "Beatriz Nunes", "PASSBR2026103", "1997-08-22", "AC-2026-002103", "Muay Thai", "Intermediário", "Ilimitado", "beatriz@example.com", "active", now),
            (club_id, "Enzo Costa", "REG002811", "2014-03-16", "AC-2026-002811", "Judô", "Faixa amarela", "Infantil", "responsavel@example.com", "pending", now),
        ]
        db.executemany(
            """INSERT INTO athletes(club_id,full_name,document,birth_date,registration_code,sport,rank_name,plan_name,contact,status,created_at)
               VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
            athletes,
        )
    db.execute(
        """UPDATE athletes SET email='rafael@example.com',phone='+55 41 99999-4821',weight_kg=79.8,
           current_category='Adulto • Médio • Até 82,3 kg',emergency_name='Ana Martins',
           emergency_phone='+55 41 98888-4821',profile_updated_at=? WHERE document='52998224725'""", (now,)
    )
    db.execute(
        """UPDATE athletes SET email='beatriz@example.com',phone='+55 41 99911-3022',weight_kg=58.6,
           current_category='Adulto • Até 60 kg • Intermediário',emergency_name='Paulo Nunes',
           emergency_phone='+55 41 98777-3022',profile_updated_at=? WHERE document='PASSBR2026103'""", (now,)
    )
    db.execute(
        """UPDATE athletes SET email='responsavel@example.com',phone='+55 41 99821-1100',weight_kg=44.2,
           current_category='Infantil • Até 46 kg',emergency_name='Carla Costa',
           emergency_phone='+55 41 99821-1100',profile_updated_at=? WHERE document='REG002811'""", (now,)
    )
    athlete_profiles = db.execute("SELECT id,document FROM athletes WHERE club_id=?", (club_id,)).fetchall()
    athlete_by_document = {row["document"]: row["id"] for row in athlete_profiles}
    document_seeds = [
        ("52998224725", "identity", "identidade-rafael.pdf", "verified", "2026-01-12", "2032-01-12", "Federação Paranaense", "Documento validado"),
        ("52998224725", "medical_certificate", "atestado-rafael.pdf", "verified", "2026-03-15", "2027-03-15", "Dojo Norte", "Apto para competição"),
        ("52998224725", "responsibility_term", "termo-2026.pdf", "verified", "2026-01-05", "2026-12-31", "Dojo Norte", "Temporada 2026"),
        ("PASSBR2026103", "identity", "passaporte-beatriz.pdf", "verified", "2026-02-10", "2030-02-10", "Federação Paranaense", "Documento validado"),
        ("PASSBR2026103", "medical_certificate", "atestado-beatriz.pdf", "verified", "2026-04-18", "2027-04-18", "Dojo Norte", "Apta para competição"),
        ("REG002811", "identity", "identidade-enzo.pdf", "pending", "2026-08-01", "2031-08-01", "", "Aguardando validação"),
        ("REG002811", "guardian_authorization", "autorizacao-enzo.pdf", "pending", "2026-09-20", "2026-12-31", "", "Assinatura pendente"),
    ]
    for athlete_document, document_type, file_name, status, issued_at, expires_at, reviewed_by, notes in document_seeds:
        athlete_id = athlete_by_document.get(athlete_document)
        if athlete_id:
            db.execute(
                """INSERT OR IGNORE INTO athlete_documents
                   (athlete_id,document_type,file_name,status,issued_at,expires_at,reviewed_by,notes,created_at,updated_at)
                   VALUES(?,?,?,?,?,?,?,?,?,?)""",
                (athlete_id, document_type, file_name, status, issued_at, expires_at, reviewed_by, notes, now, now),
            )
    enzo_id = athlete_by_document.get("REG002811")
    if enzo_id:
        db.execute(
            """INSERT OR IGNORE INTO athlete_guardians
               (athlete_id,full_name,relationship,document,phone,email,authorized_competitions,emergency_contact,created_at)
               VALUES(?,?,?,?,?,?,?,?,?)""",
            (enzo_id, "Carla Costa", "Mãe", "RESP110022", "+55 41 99821-1100", "responsavel@example.com", 1, 1, now),
        )
    technician_seeds = [
        (club_id, "Marcelo Mendes", "TECNICO.MARCELO", "TECNICO2026", "TEC998100", "TEC-PR-00421", "Jiu-jítsu • Competição", "marcelo@dojonorte.apex"),
        (club_id, "Camila Souza", "TECNICA.CAMILA", "TECNICO2026", "TEC998101", "TEC-PR-00438", "Muay Thai • Corner", "camila@dojonorte.apex"),
        (club_id, "Renata Oliveira", "TECNICA.RENATA", "TECNICO2026", "TEC998102", "TEC-PR-00452", "Judô • Infantil", "renata@dojonorte.apex"),
    ]
    for technician_club_id, full_name, username, password, document, registration_code, specialties, contact in technician_seeds:
        if db.execute("SELECT 1 FROM technicians WHERE username=?", (username,)).fetchone() is None:
            db.execute(
                """INSERT INTO technicians(club_id,full_name,username,password_hash,document,registration_code,specialties,contact,status,created_at)
                   VALUES(?,?,?,?,?,?,?,?,?,?)""",
                (technician_club_id, full_name, username, hash_password(password), document, registration_code, specialties, contact, "active", now),
            )

    if db.execute("SELECT COUNT(*) FROM club_classes WHERE club_id=?", (club_id,)).fetchone()[0] == 0:
        class_seeds = [
            ("Jiu-jítsu • Iniciantes", "Jiu-jítsu", "Iniciante", 1, "07:00", 75, 24, "Tatame 1", "TECNICO.MARCELO"),
            ("Judô • Infantil", "Judô", "Infantil", 3, "09:30", 60, 18, "Tatame 2", "TECNICA.RENATA"),
            ("Muay Thai • Fundamentos", "Muay Thai", "Fundamentos", 5, "11:00", 75, 28, "Sala 2", "TECNICA.CAMILA"),
            ("Equipe de competição", "Multimodalidades", "Competidores", 5, "20:00", 90, 24, "Tatame 1", "TECNICO.MARCELO"),
        ]
        for name, sport, level_name, weekday, start_time, duration, capacity, location, technician_username in class_seeds:
            technician_id = db.execute("SELECT id FROM technicians WHERE username=?", (technician_username,)).fetchone()[0]
            db.execute(
                """INSERT INTO club_classes(club_id,technician_id,name,sport,level_name,weekday,start_time,duration_minutes,capacity,location,status,created_at)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
                (club_id, technician_id, name, sport, level_name, weekday, start_time, duration, capacity, location, "active", now),
            )
    classes = db.execute("SELECT id,name,start_time FROM club_classes WHERE club_id=? ORDER BY id", (club_id,)).fetchall()
    rafael_id = athlete_by_document.get("52998224725")
    beatriz_id = athlete_by_document.get("PASSBR2026103")
    enzo_id = athlete_by_document.get("REG002811")
    enrollment_map = {
        "Jiu-jítsu • Iniciantes": [rafael_id],
        "Judô • Infantil": [enzo_id],
        "Muay Thai • Fundamentos": [beatriz_id],
        "Equipe de competição": [rafael_id, beatriz_id],
    }
    for club_class in classes:
        for athlete_id in enrollment_map.get(club_class["name"], []):
            if athlete_id:
                db.execute(
                    "INSERT OR IGNORE INTO class_enrollments(class_id,athlete_id,status,joined_at) VALUES(?,?,?,?)",
                    (club_class["id"], athlete_id, "active", now),
                )
    attendance_day = date.today().isoformat()
    for club_class in classes:
        for athlete_id in enrollment_map.get(club_class["name"], [])[:1]:
            if athlete_id:
                db.execute(
                    "INSERT OR IGNORE INTO attendance_records(class_id,athlete_id,checked_in_at,source,recorded_by) VALUES(?,?,?,?,?)",
                    (club_class["id"], athlete_id, f"{attendance_day}T{club_class['start_time']}:00+00:00", "seed", "SYSTEM"),
                )

    federation_accounts = [
        (federation_id, "ADMIN", "MASTER2026", "ADMIN", "federation", "SMS final 4821"),
        (federation_id, "PRESIDENTE", "MASTER2026", "PRESIDENTE_MASTER", "federation", "e-mail p***@federacao.org"),
    ]
    for account_federation_id, username, password, permission, scope, destination in federation_accounts:
        if db.execute("SELECT 1 FROM federation_users WHERE username=?", (username,)).fetchone() is None:
            db.execute(
                """INSERT INTO federation_users(federation_id,username,password_hash,permission,scope,destination,active,created_at)
                   VALUES(?,?,?,?,?,?,?,?)""",
                (account_federation_id, username, hash_password(password), permission, scope, destination, 1, now),
            )
    db.execute("UPDATE federation_users SET federation_id=?,scope='federation' WHERE username IN ('ADMIN','PRESIDENTE')", (federation_id,))
    if db.execute("SELECT COUNT(*) FROM competitions").fetchone()[0] == 0:
        competitions = [
            (federation_id, "Curitiba Open de Artes Marciais", "curitiba-open-2026", "Jiu-jítsu", "Curitiba", "PR", "Ginásio Tarumã", "2026-10-18", "2026-10-05", 12000, "Estadual", "open", "Federação Paranaense", now),
            (federation_id, "Copa Sul de Jiu-jítsu", "copa-sul-jiu-jitsu-2026", "Jiu-jítsu", "Florianópolis", "SC", "Arena Sul", "2026-11-09", "2026-10-28", 11000, "Interestadual", "open", "Liga Sul", now),
            (federation_id, "Festival Paranaense de Judô", "festival-paranaense-judo-2026", "Judô", "Londrina", "PR", "Ginásio Moringão", "2026-11-23", "2026-11-10", 9000, "Estadual", "open", "Federação Paranaense", now),
            (federation_id, "Brazil Karate Challenge", "brazil-karate-challenge-2026", "Karatê", "São Paulo", "SP", "Ibirapuera", "2026-12-07", "2026-11-25", 14000, "Nacional", "open", "Confederação Nacional", now),
            (federation_id, "Muay Thai Grand Prix Sul", "muay-thai-grand-prix-sul-2026", "Muay Thai", "Porto Alegre", "RS", "Ginásio Tesourinha", "2026-12-14", "2026-12-02", 13000, "Interestadual", "open", "Liga Sul", now),
        ]
        db.executemany(
            """INSERT INTO competitions(federation_id,name,slug,sport,city,state,venue,event_date,registration_deadline,fee_cents,level,status,organizer,created_at)
               VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            competitions,
        )
    db.execute("UPDATE competitions SET federation_id=? WHERE federation_id IS NULL", (federation_id,))
    db.execute("UPDATE homologations SET federation_id=? WHERE federation_id IS NULL", (federation_id,))
    curitiba = db.execute("SELECT id FROM competitions WHERE slug='curitiba-open-2026'").fetchone()
    if curitiba:
        for username, function_name in [("TECNICO.MARCELO", "Técnico principal"), ("TECNICA.CAMILA", "Corner")]:
            technician = db.execute("SELECT id FROM technicians WHERE username=?", (username,)).fetchone()
            if technician and db.execute("SELECT 1 FROM competition_staff WHERE competition_id=? AND technician_id=?", (curitiba[0], technician[0])).fetchone() is None:
                db.execute(
                    "INSERT INTO competition_staff(competition_id,technician_id,function_name,status,accreditation_code,created_at) VALUES(?,?,?,?,?,?)",
                    (curitiba[0], technician[0], function_name, "confirmed", f"STAFF-{curitiba[0]}-{technician[0]}", now),
                )

    athlete = db.execute("SELECT id FROM athletes WHERE document='52998224725'").fetchone()
    competition = db.execute("SELECT id FROM competitions WHERE slug='curitiba-open-2026'").fetchone()
    if athlete and competition and db.execute("SELECT COUNT(*) FROM registrations").fetchone()[0] == 0:
        db.execute(
            "INSERT INTO registrations(competition_id,athlete_id,category,status,payment_status,created_at) VALUES(?,?,?,?,?,?)",
            (competition[0], athlete[0], "Adulto • Médio • Faixa azul", "confirmed", "paid", now),
        )
    marcelo = db.execute("SELECT id FROM technicians WHERE username='TECNICO.MARCELO'").fetchone()
    if athlete and competition and marcelo:
        db.execute(
            "UPDATE registrations SET technician_id=? WHERE competition_id=? AND athlete_id=? AND technician_id IS NULL",
            (marcelo[0], competition[0], athlete[0]),
        )

    # Operação demonstrativa completa da área privada do técnico.
    beatriz = db.execute("SELECT id FROM athletes WHERE document='PASSBR2026103'").fetchone()
    if beatriz and competition and marcelo:
        db.execute(
            """INSERT OR IGNORE INTO registrations(competition_id,athlete_id,technician_id,category,status,payment_status,created_at)
               VALUES(?,?,?,?,?,?,?)""",
            (competition[0], beatriz[0], marcelo[0], "Adulto • Até 60 kg • Intermediário", "confirmed", "paid", now),
        )
        db.execute(
            "UPDATE registrations SET technician_id=? WHERE competition_id=? AND athlete_id=?",
            (marcelo[0], competition[0], beatriz[0]),
        )

    if competition:
        db.execute(
            """INSERT OR IGNORE INTO delegations(club_id,competition_id,name,status,deadline,notes,created_at)
               VALUES(?,?,?,?,?,?,?)""",
            (club_id, competition[0], "Delegação Dojo Norte • Curitiba Open", "review", "2026-10-05", "Delegação oficial do clube", now),
        )
        delegation = db.execute("SELECT id FROM delegations WHERE club_id=? AND competition_id=?", (club_id, competition[0])).fetchone()
        if delegation:
            for document, approval_status, documents_status, category_status, payment_status in [
                ("52998224725", "approved", "verified", "confirmed", "paid"),
                ("PASSBR2026103", "approved", "verified", "confirmed", "paid"),
                ("REG002811", "pending", "pending", "pending", "pending"),
            ]:
                athlete_id = athlete_by_document.get(document)
                if not athlete_id:
                    continue
                registration = db.execute("SELECT id FROM registrations WHERE competition_id=? AND athlete_id=?", (competition[0], athlete_id)).fetchone()
                db.execute(
                    """INSERT OR IGNORE INTO delegation_members
                       (delegation_id,athlete_id,registration_id,approval_status,documents_status,category_status,payment_status,added_at)
                       VALUES(?,?,?,?,?,?,?,?)""",
                    (delegation["id"], athlete_id, registration["id"] if registration else None, approval_status, documents_status, category_status, payment_status, now),
                )

    operation_seeds = [
        ("52998224725", "ready", "10:40", "Tatame 3", "128", 3, 20, "approved", "approved", "Controlar a distância, buscar pegada dominante e manter ritmo no primeiro minuto."),
        ("PASSBR2026103", "weigh_in", "11:20", "Ringue 1", "146", 8, 25, "pending", "pending", "Pressão com segurança, atenção aos chutes baixos e saída lateral após combinação."),
    ]
    checklist_labels = [
        ("document", "Documento do atleta"), ("credential", "Credencial da competição"),
        ("category", "Categoria e chave"), ("weigh_in", "Pesagem oficial"),
        ("uniform", "Uniforme regulamentar"), ("protective_equipment", "Equipamentos obrigatórios"),
        ("hydration", "Hidratação"), ("warmup", "Aquecimento concluído"),
        ("call_area", "Entrada na área de chamada"), ("corner_ready", "Corner preparado"),
    ]
    for document, stage, call_time, arena, bout, bouts_before, warmup, weigh_status, equipment_status, strategy in operation_seeds:
        registration = db.execute(
            """SELECT r.id FROM registrations r JOIN athletes a ON a.id=r.athlete_id
               WHERE a.document=? AND r.competition_id=? AND r.technician_id=?""",
            (document, competition[0] if competition else 0, marcelo[0] if marcelo else 0),
        ).fetchone()
        if not registration:
            continue
        db.execute(
            """INSERT OR IGNORE INTO competition_operations
               (registration_id,stage,call_time,arena_label,bout_number,bouts_before,warmup_minutes,weigh_in_status,equipment_status,strategy_notes,updated_at)
               VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
            (registration[0], stage, call_time, arena, bout, bouts_before, warmup, weigh_status, equipment_status, strategy, now),
        )
        for index, (item_key, label) in enumerate(checklist_labels):
            completed = 1 if (document == "52998224725" and index < 6) or (document == "PASSBR2026103" and index < 3) else 0
            db.execute(
                "INSERT OR IGNORE INTO technician_checklists(registration_id,item_key,label,completed,updated_at) VALUES(?,?,?,?,?)",
                (registration[0], item_key, label, completed, now),
            )

    if competition and marcelo and db.execute("SELECT COUNT(*) FROM technician_notices WHERE technician_id=?", (marcelo[0],)).fetchone()[0] == 0:
        rafael_registration = db.execute(
            """SELECT r.id FROM registrations r JOIN athletes a ON a.id=r.athlete_id
               WHERE r.competition_id=? AND r.technician_id=? AND a.document='52998224725'""",
            (competition[0], marcelo[0]),
        ).fetchone()
        notice_seeds = [
            (competition[0], marcelo[0], rafael_registration[0] if rafael_registration else None, "call", "urgent", "Chamada programada", "Rafael Martins deve se apresentar no Tatame 3 antes da luta 128.", "Área de chamada", now),
            (competition[0], marcelo[0], None, "weigh_in", "high", "Pesagem disponível", "A pesagem da categoria de Beatriz Nunes estará disponível no setor B.", "Pesagem oficial", now),
            (competition[0], marcelo[0], None, "meeting", "normal", "Reunião técnica", "Reunião técnica confirmada para 09:45, sala 2.", "Organização do evento", now),
        ]
        db.executemany(
            """INSERT INTO technician_notices(competition_id,technician_id,registration_id,kind,priority,title,body,source,created_at)
               VALUES(?,?,?,?,?,?,?,?,?)""",
            notice_seeds,
        )


def audit(actor: str, profile: str, action: str, entity_type: str, entity_id: str, metadata: str = "{}", ip_address: str = "") -> None:
    with connection() as db:
        db.execute(
            "INSERT INTO audit_log(actor,profile,action,entity_type,entity_id,metadata,ip_address,created_at) VALUES(?,?,?,?,?,?,?,?)",
            (actor, profile, action, entity_type, str(entity_id), metadata, ip_address, utc_now()),
        )
