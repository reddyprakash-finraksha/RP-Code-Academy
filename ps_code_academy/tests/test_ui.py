"""Headless UI smoke tests using Streamlit's AppTest."""
from pathlib import Path

from streamlit.testing.v1 import AppTest

from core import course, db, progress

APP = str(Path(__file__).resolve().parents[1] / "app.py")


def _app():
    at = AppTest.from_file(APP, default_timeout=60)
    return at.run()


def test_profile_creation_screen(data_dir):
    with db.session() as con:
        con.execute("DELETE FROM student")
    at = _app()
    assert not at.exception
    at.text_input[0].set_value("Asha")
    at.button[0].click().run()          # form values are only sent together with the submit click
    assert db.get_student()["name"] == "Asha"


def test_home_renders():
    at = _app()
    assert not at.exception
    assert any("Welcome back, Test Student" in m.value for m in at.markdown)


def test_each_page_renders_without_error():
    for page in ["lessons", "quizzes", "projects", "playground", "achievements", "my_progress", "teacher"]:
        at = AppTest.from_file(APP, default_timeout=60).run()
        at.switch_page(f"pages/{page}.py").run()
        assert not at.exception, (page, [e.value for e in at.exception])


def test_check_button_passes_and_records():
    at = AppTest.from_file(APP, default_timeout=60).run()
    at.switch_page("pages/lessons.py").run()
    at.text_area(key="code_m01-l1-e1").set_value('print("Hello, World!")').run()
    next(b for b in at.button if b.key == "chk_m01-l1-e1").click().run()
    assert not at.exception
    assert progress.get_item("m01-l1-e1")["completed"] == 1
    assert any("All 1 test" in s.value for s in at.success)


def test_teacher_requires_pin():
    at = AppTest.from_file(APP, default_timeout=60).run()
    at.switch_page("pages/teacher.py").run()
    assert any("choose a teacher PIN" in i.value for i in at.info)
    at.text_input[0].set_value("1234")
    at.text_input[1].set_value("1234")
    at.button[0].click().run()
    assert any(t.label == "Overview" for t in at.tabs)


def test_missing_profile_mid_session_does_not_crash_pages():
    """Regression: profile row disappears after app start -> no TypeError on any page."""
    at = AppTest.from_file(APP, default_timeout=60).run()
    with db.session() as con:
        con.execute("DELETE FROM student")
    for page in ["home", "teacher", "lessons", "my_progress"]:
        at.switch_page(f"pages/{page}.py").run()
        assert not at.exception, (page, [e.value for e in at.exception])


def test_require_student_gate_in_isolation():
    """The page-level guard shows the form and stops when there is no profile, and passes through when there is."""
    code = "import streamlit as st\nfrom components import ui\ns = ui.require_student()\nst.write('PAGE-RAN ' + s['name'])"
    with db.session() as con:
        con.execute("DELETE FROM student")
    at = AppTest.from_string(code, default_timeout=30).run()
    assert not at.exception and not any("PAGE-RAN" in m.value for m in at.markdown)
    assert any("set up your profile" in m.value for m in at.markdown)
    db.create_student("Asha")
    at = AppTest.from_string(code, default_timeout=30).run()
    assert any("PAGE-RAN Asha" in m.value for m in at.markdown)
