from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path


class StateStore:
    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        with self.connect() as db:
            db.execute(
                """CREATE TABLE IF NOT EXISTS messages (
                    message_key TEXT PRIMARY KEY,
                    mailbox TEXT NOT NULL,
                    uidvalidity TEXT NOT NULL,
                    uid TEXT NOT NULL,
                    status TEXT NOT NULL,
                    evidence_path TEXT,
                    lease_until TEXT,
                    created_at TEXT NOT NULL,
                    completed_at TEXT
                )"""
            )
            db.execute(
                """CREATE TABLE IF NOT EXISTS incidents (
                    fingerprint TEXT PRIMARY KEY,
                    status TEXT NOT NULL,
                    occurrence_count INTEGER NOT NULL DEFAULT 1,
                    evidence_path TEXT NOT NULL,
                    analysis_path TEXT,
                    report_path TEXT,
                    action TEXT,
                    confidence REAL,
                    lease_until TEXT,
                    first_seen TEXT NOT NULL,
                    last_seen TEXT NOT NULL,
                    last_analyzed TEXT,
                    approved_at TEXT,
                    ignored_at TEXT,
                    last_error TEXT
                )"""
            )
            db.execute(
                """CREATE TABLE IF NOT EXISTS mailbox_cursors (
                    mailbox TEXT PRIMARY KEY,
                    uidvalidity TEXT NOT NULL,
                    last_uid TEXT NOT NULL,
                    last_message_time TEXT NOT NULL,
                    initialized_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )"""
            )

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path, timeout=5)
        db.execute("PRAGMA busy_timeout=5000")
        try:
            yield db
            db.commit()
        finally:
            db.close()

    def claim(self, key: str, mailbox: str, uidvalidity: str, uid: str, evidence_path: str, lease_minutes: int) -> bool:
        now = datetime.now(timezone.utc)
        lease = now + timedelta(minutes=lease_minutes)
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT status, lease_until FROM messages WHERE message_key = ?", (key,)).fetchone()
            if row and (row[0] == "completed" or (row[1] and datetime.fromisoformat(row[1]) > now)):
                return False
            db.execute(
                """INSERT INTO messages(message_key, mailbox, uidvalidity, uid, status, evidence_path, lease_until, created_at)
                   VALUES(?, ?, ?, ?, 'claimed', ?, ?, ?)
                   ON CONFLICT(message_key) DO UPDATE SET status='claimed', evidence_path=excluded.evidence_path,
                     lease_until=excluded.lease_until""",
                (key, mailbox, uidvalidity, uid, evidence_path, lease.isoformat(), now.isoformat()),
            )
        return True

    def complete(self, key: str) -> bool:
        with self.connect() as db:
            cursor = db.execute(
                "UPDATE messages SET status='completed', completed_at=?, lease_until=NULL WHERE message_key=?",
                (datetime.now(timezone.utc).isoformat(), key),
            )
            return cursor.rowcount == 1

    def release(self, key: str) -> None:
        with self.connect() as db:
            db.execute(
                "UPDATE messages SET status='retry', lease_until=NULL WHERE message_key=? AND status!='completed'",
                (key,),
            )

    def get_mailbox_cursor(self, mailbox: str) -> dict | None:
        with self.connect() as db:
            row = db.execute(
                """SELECT uidvalidity, last_uid, last_message_time, initialized_at, updated_at
                   FROM mailbox_cursors WHERE mailbox=?""",
                (mailbox,),
            ).fetchone()
        if not row:
            return None
        return {
            "uidvalidity": row[0],
            "last_uid": row[1],
            "last_message_time": row[2],
            "initialized_at": row[3],
            "updated_at": row[4],
        }

    def reset_mailbox_cursor(
        self, mailbox: str, uidvalidity: str, last_uid: str, last_message_time: str
    ) -> None:
        now = datetime.now(timezone.utc).isoformat()
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            db.execute(
                "UPDATE messages SET status='superseded', lease_until=NULL WHERE mailbox=? AND status!='completed'",
                (mailbox,),
            )
            db.execute(
                """INSERT INTO mailbox_cursors(
                       mailbox, uidvalidity, last_uid, last_message_time, initialized_at, updated_at
                   ) VALUES(?, ?, ?, ?, ?, ?)
                   ON CONFLICT(mailbox) DO UPDATE SET uidvalidity=excluded.uidvalidity,
                      last_uid=excluded.last_uid, last_message_time=excluded.last_message_time,
                      initialized_at=excluded.initialized_at, updated_at=excluded.updated_at""",
                (mailbox, uidvalidity, last_uid, last_message_time, now, now),
            )

    def advance_mailbox_cursor(
        self, mailbox: str, uidvalidity: str, uid: str, message_time: str
    ) -> None:
        now = datetime.now(timezone.utc).isoformat()
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                "SELECT uidvalidity, last_uid FROM mailbox_cursors WHERE mailbox=?",
                (mailbox,),
            ).fetchone()
            if row and row[0] == uidvalidity and int(uid) > int(row[1]):
                db.execute(
                    """UPDATE mailbox_cursors SET last_uid=?, last_message_time=?, updated_at=?
                       WHERE mailbox=? AND uidvalidity=?""",
                    (uid, message_time, now, mailbox, uidvalidity),
                )

    def claim_retry(self, mailbox: str, initialized_at: str, lease_minutes: int, limit: int) -> list[dict]:
        now = datetime.now(timezone.utc)
        lease = now + timedelta(minutes=lease_minutes)
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            rows = db.execute(
                """SELECT message_key, evidence_path FROM messages
                   WHERE mailbox=? AND created_at>=? AND evidence_path IS NOT NULL
                     AND (status='retry' OR (status='claimed' AND lease_until<?))
                   ORDER BY created_at LIMIT ?""",
                (mailbox, initialized_at, now.isoformat(), limit),
            ).fetchall()
            for key, _path in rows:
                db.execute(
                    "UPDATE messages SET status='claimed', lease_until=? WHERE message_key=?",
                    (lease.isoformat(), key),
                )
        return [{"message_key": row[0], "evidence_path": row[1]} for row in rows]

    def claim_incident(
        self,
        fingerprint: str,
        evidence_path: str,
        cooldown_hours: int,
        lease_minutes: int,
    ) -> bool:
        now = datetime.now(timezone.utc)
        lease = now + timedelta(minutes=lease_minutes)
        cooldown_start = now - timedelta(hours=cooldown_hours)
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute(
                "SELECT status, lease_until, last_analyzed, occurrence_count FROM incidents WHERE fingerprint=?",
                (fingerprint,),
            ).fetchone()
            if row:
                db.execute(
                    "UPDATE incidents SET occurrence_count=?, last_seen=?, evidence_path=? WHERE fingerprint=?",
                    (row[3] + 1, now.isoformat(), evidence_path, fingerprint),
                )
                active_lease = row[1] and datetime.fromisoformat(row[1]) > now
                within_cooldown = row[2] and datetime.fromisoformat(row[2]) > cooldown_start
                if active_lease or within_cooldown:
                    return False
                db.execute(
                    """UPDATE incidents SET status='analyzing', lease_until=?, last_error=NULL
                       WHERE fingerprint=?""",
                    (lease.isoformat(), fingerprint),
                )
                return True
            db.execute(
                """INSERT INTO incidents(
                       fingerprint, status, evidence_path, lease_until, first_seen, last_seen
                   ) VALUES(?, 'analyzing', ?, ?, ?, ?)""",
                (fingerprint, evidence_path, lease.isoformat(), now.isoformat(), now.isoformat()),
            )
            return True

    def record_analysis(
        self,
        fingerprint: str,
        analysis_path: str,
        report_path: str,
        action: str,
        confidence: float,
    ) -> None:
        now = datetime.now(timezone.utc).isoformat()
        with self.connect() as db:
            db.execute(
                """UPDATE incidents SET status='analyzed', analysis_path=?, report_path=?, action=?,
                   confidence=?, lease_until=NULL, last_analyzed=? WHERE fingerprint=?""",
                (analysis_path, report_path, action, confidence, now, fingerprint),
            )

    def fail_incident(self, fingerprint: str, error: str) -> None:
        with self.connect() as db:
            db.execute(
                "UPDATE incidents SET status='failed', lease_until=NULL, last_error=? WHERE fingerprint=?",
                (error[:2000], fingerprint),
            )

    def approve_incident(self, fingerprint: str) -> None:
        with self.connect() as db:
            db.execute(
                "UPDATE incidents SET status='approved', approved_at=? WHERE fingerprint=?",
                (datetime.now(timezone.utc).isoformat(), fingerprint),
            )

    def ignore_incident(self, fingerprint: str) -> None:
        with self.connect() as db:
            db.execute(
                "UPDATE incidents SET status='ignored', ignored_at=? WHERE fingerprint=?",
                (datetime.now(timezone.utc).isoformat(), fingerprint),
            )

    def get_incident(self, fingerprint: str) -> dict | None:
        with self.connect() as db:
            row = db.execute(
                """SELECT status, analysis_path, report_path, action, confidence
                   FROM incidents WHERE fingerprint=?""",
                (fingerprint,),
            ).fetchone()
        if not row:
            return None
        return {
            "status": row[0],
            "analysis_path": row[1],
            "report_path": row[2],
            "action": row[3],
            "confidence": row[4],
        }
