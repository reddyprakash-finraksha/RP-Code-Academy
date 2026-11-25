import streamlit as st

from components import ui
from core import achievements, course, db, progress

s = ui.require_student()
st_ = progress.stats()
ui.hero(f"Welcome back, {s['name']}! 🐍", "Learn Python step by step. Everything works offline.")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Exercises passed", f"{st_['exercises_done']} / {st_['exercises_total']}")
c2.metric("Lessons done", f"{st_['lessons_done_n']} / {st_['lessons_total']}")
c3.metric("Projects", f"{st_['projects_done']} / {st_['projects_total']}")
c4.metric("Day streak", st_["streak"])
st.progress(st_["overall_percent"] / 100, text=f"Course progress: {st_['overall_percent']}%")

nxt = progress.next_exercise()
st.subheader("Continue learning")
if nxt:
    les = course.lesson(nxt["lesson_id"])
    mod = course.module(nxt["module_id"])
    st.write(f"Next up: **{mod['title']} → {les['title']}** → *{nxt['title']}*")
    if st.button("Continue ▶", type="primary"):
        st.session_state["jump"] = (mod["id"], les["id"])
        st.switch_page("pages/lessons.py")
else:
    st.success("You finished every exercise. Amazing work! Try the projects and quizzes you missed.")

st.subheader("Recent achievements")
have = achievements.unlocked()
recent = [a for a in achievements.ACHIEVEMENTS if a[0] in have][-4:]
if recent:
    cols = st.columns(len(recent))
    for col, a in zip(cols, recent):
        with col:
            ui.card(a[1], a[2], a[3])
else:
    st.caption("Pass your first exercise to earn your first badge.")
