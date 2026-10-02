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
                status TEXT NOT NULL DEFAULT 'active',
                created_at TEXT NOT NULL
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
            CREATE INDEX IF NOT EXISTS idx_technicians_club ON technicians(club_id);
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
