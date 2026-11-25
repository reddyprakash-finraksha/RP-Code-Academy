"""SQLite storage. One database file per computer / Windows account."""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

from . import config

SCHEMA_VERSION = 1

SCHEMA = """
CREATE TABLE IF NOT EXISTS student(
    id INTEGER PRIMARY KEY CHECK (id = 1),
    name TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS progress(
    item_id TEXT PRIMARY KEY,
    kind TEXT NOT NULL DEFAULT 'exercise',
    completed INTEGER NOT NULL DEFAULT 0,
    attempts INTEGER NOT NULL DEFAULT 0,
    hints_used INTEGER NOT NULL DEFAULT 0,
    solution_viewed INTEGER NOT NULL DEFAULT 0,
    first_passed_at TEXT,
    last_code TEXT,
    updated_at TEXT
);
CREATE TABLE IF NOT EXISTS submissions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id TEXT NOT NULL,
    passed INTEGER NOT NULL,
    code TEXT,
    ts TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS lesson_progress(
    lesson_id TEXT PRIMARY KEY,
    completed_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS quiz_results(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_id TEXT NOT NULL,
    score INTEGER NOT NULL,
    total INTEGER NOT NULL,
    ts TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS achievements(
    key TEXT PRIMARY KEY,
    unlocked_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS settings(
    key TEXT PRIMARY KEY,
    value TEXT
);
CREATE INDEX IF NOT EXISTS idx_sub_item ON submissions(item_id);
"""

TABLES = ("student", "progress", "submissions", "lesson_progress", "quiz_results", "achievements", "settings")


def now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def connect(path: Path | str | None = None) -> sqlite3.Connection:
    con = sqlite3.connect(str(path or config.db_path()), timeout=10)
    con.row_factory = sqlite3.Row
    return con


@contextmanager
def session(path: Path | str | None = None):
    con = connect(path)
    try:
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()


def init_db(path: Path | str | None = None) -> None:
    with session(path) as con:
        con.executescript(SCHEMA)
        con.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")


def get_student():
    with session() as con:
        return con.execute("SELECT * FROM student WHERE id = 1").fetchone()


def create_student(name: str) -> None:
    name = " ".join(name.split())[:60]
    if not name:
        raise ValueError("Name cannot be empty.")
    with session() as con:
        con.execute(
            "INSERT OR REPLACE INTO student(id, name, created_at) "
            "VALUES (1, ?, COALESCE((SELECT created_at FROM student WHERE id=1), ?))",
            (name, now()),
        )


def get_setting(key: str, default: str | None = None) -> str | None:
    with session() as con:
        row = con.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
    return row["value"] if row else default


def set_setting(key: str, value: str) -> None:
    with session() as con:
        con.execute("INSERT OR REPLACE INTO settings(key, value) VALUES (?, ?)", (key, value))
