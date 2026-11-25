"""RP Code Academy - Streamlit entry point."""
import streamlit as st

from components import ui
from core import backup, config, db, logging_setup, progress

st.set_page_config(page_title=config.APP_NAME, page_icon="🐍", layout="wide")
log = logging_setup.setup()
db.init_db()

if "booted" not in st.session_state:
    st.session_state["booted"] = True
    try:
        backup.auto_backup_if_due()
    except Exception:  # noqa: BLE001  (a failed backup must never block learning)
        log.exception("auto backup failed")

ui.inject_css()
student = db.get_student()

if student is None:
    ui.hero(f"Welcome to {config.APP_NAME}", "Let's set up your profile. This stays on this computer.")
    with st.form("profile"):
        name = st.text_input("What is your name?", max_chars=60)
        if st.form_submit_button("Start learning", type="primary"):
            try:
                db.create_student(name)
                st.rerun()
            except ValueError as e:
                st.error(str(e))
    st.stop()

pages = [
    st.Page("pages/home.py", title="Home", icon="🏠", default=True),
    st.Page("pages/lessons.py", title="Lessons", icon="📘"),
    st.Page("pages/quizzes.py", title="Quizzes", icon="📝"),
    st.Page("pages/projects.py", title="Projects", icon="🛠️"),
    st.Page("pages/playground.py", title="Playground", icon="🧪"),
    st.Page("pages/achievements.py", title="Achievements", icon="🏅"),
    st.Page("pages/my_progress.py", title="My Progress", icon="📊"),
    st.Page("pages/teacher.py", title="Teacher", icon="🎓"),
]
nav = st.navigation(pages)
with st.sidebar:
    st.markdown(f"### 🐍 {config.APP_NAME}")
    st.write(f"**{student['name']}**")
    pct = progress.stats()["overall_percent"]
    st.progress(pct / 100, text=f"{pct}% complete")
    st.caption(f"v{config.VERSION} · works offline")
try:
    nav.run()
except Exception as exc:  # noqa: BLE001
    log.exception("page crashed")
    st.error(f"Oops, something went wrong ({type(exc).__name__}). Your progress is saved. Try another page or reload.")
