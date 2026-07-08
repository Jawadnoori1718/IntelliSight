"""Persistent memory — every event and rule fire logged to a local SQLite DB.

The database lives in the app's data directory and survives restarts. Old rows
are pruned on startup so it can't grow forever.
"""

import sqlite3
import time
from pathlib import Path

from PySide6.QtCore import QStandardPaths

RETENTION_DAYS = 30


def _default_db_path() -> Path:
    base = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
    folder = Path(base) if base else (Path.home() / ".bigbrother")
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "timeline.db"


class Timeline:
    def __init__(self, path=None):
        db_path = str(path) if path else str(_default_db_path())
        self._conn = sqlite3.connect(db_path)
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ts REAL NOT NULL,
                kind TEXT NOT NULL,
                label TEXT NOT NULL,
                category TEXT,
                snapshot TEXT
            )
            """
        )
        self._conn.commit()
        self._prune()

    def add(self, kind, label, category=None, snapshot=None) -> None:
        self._conn.execute(
            "INSERT INTO events (ts, kind, label, category, snapshot) VALUES (?, ?, ?, ?, ?)",
            (time.time(), kind, label, category, snapshot),
        )
        self._conn.commit()

    def query(self, search="", limit=500) -> list:
        sql = "SELECT ts, kind, label, category, snapshot FROM events"
        params = []
        if search.strip():
            sql += " WHERE label LIKE ?"
            params.append(f"%{search.strip()}%")
        sql += " ORDER BY ts DESC LIMIT ?"
        params.append(limit)
        rows = self._conn.execute(sql, params).fetchall()
        return [
            {"ts": r[0], "kind": r[1], "label": r[2], "category": r[3], "snapshot": r[4]}
            for r in rows
        ]

    def count(self) -> int:
        return self._conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]

    def clear(self) -> None:
        self._conn.execute("DELETE FROM events")
        self._conn.commit()

    def close(self) -> None:
        try:
            self._conn.close()
        except Exception:
            pass

    def _prune(self) -> None:
        cutoff = time.time() - RETENTION_DAYS * 86400
        self._conn.execute("DELETE FROM events WHERE ts < ?", (cutoff,))
        self._conn.commit()
