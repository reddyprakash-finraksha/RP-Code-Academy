import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


@pytest.fixture(autouse=True)
def data_dir(tmp_path, monkeypatch):
    monkeypatch.setenv("PSCA_DATA_DIR", str(tmp_path / "data"))
    from core import db
    db.init_db()
    db.create_student("Test Student")
    return tmp_path / "data"
