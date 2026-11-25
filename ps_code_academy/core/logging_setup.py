"""Rotating file logging so teachers can diagnose problems offline."""
from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler

from . import config

_done = False


def setup() -> logging.Logger:
    global _done
    log = logging.getLogger("psca")
    if _done:
        return log
    log.setLevel(logging.INFO)
    try:
        h = RotatingFileHandler(config.subdir("logs") / "psca.log", maxBytes=500_000, backupCount=3, encoding="utf-8")
        h.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
        log.addHandler(h)
    except OSError:
        log.addHandler(logging.NullHandler())
    _done = True
    return log
