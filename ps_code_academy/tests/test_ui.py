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
