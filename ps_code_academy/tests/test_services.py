import sqlite3

import pytest

from core import achievements, backup, config, course, db, progress, reports, security


def test_attempt_flow_and_unlock():
    iid = "m01-l1-e1"
    for _ in range(config.SOLUTION_UNLOCK_ATTEMPTS):
        assert not progress.solution_unlocked(iid, 2)
        progress.record_attempt(iid, "x", False)
    assert progress.solution_unlocked(iid, 2)
    progress.record_attempt(iid, "ok", True)
    p = progress.get_item(iid)
    assert p["completed"] == 1 and p["attempts"] == 4 and p["first_passed_at"]
    progress.record_attempt(iid, "again", False)
    assert progress.get_item(iid)["completed"] == 1      # never un-completes


def test_hints_capped():
    for _ in range(5):
        n = progress.use_hint("m01-l1-e1", 2)
    assert n == 2


def test_stats_and_modules():
    ids = [e["id"] for les in course.module("m01")["lessons"] for e in les["exercises"]]
    for i in ids:
        progress.record_attempt(i, "c", True)
    progress.record_quiz("m01", 4, 4)
    st = progress.stats()
    assert st["exercises_done"] == 10 and st["per_module"]["m01"]["complete"] and st["modules_complete"] == 1
    assert st["perfect_quizzes"] == 1 and st["no_help_solves"] == 10 and st["streak"] == 1


def test_achievements_unlock_once():
    assert achievements.evaluate() == []
    progress.record_attempt("m01-l1-e1", "c", True)
    new = [a[0] for a in achievements.evaluate()]
    assert "first_run" in new and achievements.evaluate() == []


def test_lessons_and_reset():
    progress.set_lesson_complete("m01-l1")
    assert "m01-l1" in progress.stats()["lessons_done"]
    progress.record_attempt("m01-l1-e1", "c", True)
    progress.reset_all()
    assert progress.stats()["exercises_done"] == 0 and not progress.stats()["lessons_done"]


def test_backup_restore_roundtrip():
    progress.record_attempt("m01-l1-e1", "c", True)
    path = backup.create_backup("manual")
    assert backup.validate_backup(path)
    progress.reset_all()
    assert progress.stats()["exercises_done"] == 0
    backup.restore_backup(path)
    assert progress.stats()["exercises_done"] == 1
    assert any("pre-restore" in p.name for p in backup.list_backups())


def test_restore_rejects_garbage(tmp_path):
    bad = tmp_path / "bad.db"
    bad.write_bytes(b"not a database")
    with pytest.raises(ValueError):
        backup.restore_backup(bad)
    other = tmp_path / "other.db"
    sqlite3.connect(other).execute("CREATE TABLE x(a)").connection.close()
    with pytest.raises(ValueError):
        backup.restore_backup(other)


def test_backup_prune(monkeypatch):
    monkeypatch.setattr(config, "BACKUP_KEEP", 3)
    import time
    for _ in range(5):
        backup.create_backup("manual")
        time.sleep(1.05)
    assert len(backup.list_backups()) == 3


def test_auto_backup_only_when_due():
    assert backup.auto_backup_if_due() is not None
    assert backup.auto_backup_if_due() is None


def test_reports_csv():
    progress.record_attempt("m01-l1-e1", "c", True)
    data = reports.exercise_report().decode("utf-8-sig").splitlines()
    assert len(data) == 151 and "Completed" in data[1] and "Test Student" in data[1]
    assert len(reports.module_report().decode("utf-8-sig").splitlines()) == 16
    assert len(reports.save_all()) == 3


def test_teacher_pin():
    assert not security.pin_is_set()
    with pytest.raises(ValueError):
        security.set_pin("12")
    security.set_pin("s3cret")
    assert security.verify_pin("s3cret") and not security.verify_pin("nope")
    security.clear_pin()
    assert not security.pin_is_set()


def test_student_name_validation():
    with pytest.raises(ValueError):
        db.create_student("   ")
    db.create_student("  Asha   Rao ")
    assert db.get_student()["name"] == "Asha Rao"
