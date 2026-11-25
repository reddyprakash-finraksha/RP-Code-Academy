"""Database backups and restore using SQLite's online backup API."""
from __future__ import annotations

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

from . import config, db


def backup_dir() -> Path:
    return config.subdir("backups")


def create_backup(label: str = "manual") -> Path:
    dest = backup_dir() / f"psca_{label}_{datetime.now():%Y%m%d_%H%M%S}.db"
    src, dst = db.connect(), sqlite3.connect(str(dest))
    try:
        src.backup(dst)
    finally:
        dst.close()
        src.close()
    db.set_setting("last_backup", db.now())
    _prune()
    return dest


def list_backups() -> list[Path]:
    return sorted(backup_dir().glob("psca_*.db"), reverse=True)


def _prune() -> None:
    for old in list_backups()[config.BACKUP_KEEP:]:
        try:
            old.unlink()
        except OSError:
            pass


def auto_backup_if_due() -> Path | None:
    last = db.get_setting("last_backup")
    if last:
        try:
            if datetime.now() - datetime.fromisoformat(last) < timedelta(hours=config.AUTO_BACKUP_HOURS):
                return None
        except ValueError:
            pass
    return create_backup("auto")


def validate_backup(path: Path) -> bool:
    try:
        con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
        try:
            names = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            ok = con.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
        finally:
            con.close()
        return ok and set(db.TABLES) <= names
    except sqlite3.Error:
        return False


def restore_backup(path: Path) -> None:
    path = Path(path)
    if not validate_backup(path):
        raise ValueError("This file is not a valid RP Code Academy backup.")
    create_backup("pre-restore")
    src, dst = sqlite3.connect(str(path)), db.connect()
    try:
        src.backup(dst)
    finally:
        src.close()
        dst.close()
