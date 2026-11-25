"""Central configuration and path resolution for RP Code Academy."""
from __future__ import annotations

import os
import sys
from pathlib import Path

APP_NAME = "RP Code Academy"
APP_ID = "RPCodeAcademy"
VERSION = "1.0.0"

# Student code limits
RUN_TIMEOUT_SEC = 5.0
MAX_OUTPUT_BYTES = 20_000
MAX_CODE_CHARS = 20_000
MEMORY_LIMIT_MB = 256
PASS_MARK_QUIZ = 0.7
SOLUTION_UNLOCK_ATTEMPTS = 3
BACKUP_KEEP = 20
AUTO_BACKUP_HOURS = 24
SERVER_PORT = 8765


def is_frozen() -> bool:
    return bool(getattr(sys, "frozen", False))


def base_dir() -> Path:
    """Folder holding app.py, course_data, assets (works frozen or not)."""
    if is_frozen():
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
    return Path(__file__).resolve().parents[1]


def data_dir() -> Path:
    """Per-Windows-account writable data folder. Override with PSCA_DATA_DIR."""
    env = os.environ.get("PSCA_DATA_DIR")
    if env:
        p = Path(env)
    elif os.name == "nt":
        p = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local")) / APP_ID
    else:
        p = Path.home() / ".rpcodeacademy"
    p.mkdir(parents=True, exist_ok=True)
    return p


def db_path() -> Path:
    return data_dir() / "psca.db"


def subdir(name: str) -> Path:
    p = data_dir() / name
    p.mkdir(parents=True, exist_ok=True)
    return p


def course_dir() -> Path:
    return base_dir() / "course_data"


def assets_dir() -> Path:
    return base_dir() / "assets"
