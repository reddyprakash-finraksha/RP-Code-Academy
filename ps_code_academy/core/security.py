"""Teacher PIN (PBKDF2). A classroom speed-bump, not strong security."""
from __future__ import annotations

import hashlib
import hmac
import os

from . import db

ITER = 200_000


def pin_is_set() -> bool:
    return db.get_setting("teacher_pin_hash") is not None


def _hash(pin: str, salt: bytes) -> str:
    return hashlib.pbkdf2_hmac("sha256", pin.encode(), salt, ITER).hex()


def set_pin(pin: str) -> None:
    pin = pin.strip()
    if len(pin) < 4:
        raise ValueError("PIN must be at least 4 characters.")
    salt = os.urandom(16)
    db.set_setting("teacher_pin_salt", salt.hex())
    db.set_setting("teacher_pin_hash", _hash(pin, salt))


def verify_pin(pin: str) -> bool:
    h, s = db.get_setting("teacher_pin_hash"), db.get_setting("teacher_pin_salt")
    if not h or not s:
        return False
    return hmac.compare_digest(h, _hash(pin.strip(), bytes.fromhex(s)))


def clear_pin() -> None:
    with db.session() as con:
        con.execute("DELETE FROM settings WHERE key IN ('teacher_pin_hash','teacher_pin_salt')")
