import streamlit as st

from components import exercise, ui
from core import course, progress

ui.hero("Lessons & Exercises", "Read a lesson, then practise with auto-checked exercises.")
stt = progress.stats()
mods = course.modules()

if "jump" in st.session_state:
    mid, lid = st.session_state.pop("jump")
    st.session_state["sel_module"], st.session_state["sel_lesson"] = mid, lid

mid = st.selectbox("Module", [m["id"] for m in mods], key="sel_module",
                   format_func=lambda i: f"{'✅' if stt['per_module'][i]['complete'] else '📘'} "
                                         f"{course.module(i)['number']}. {course.module(i)['title']} "
                                         f"({stt['per_module'][i]['percent']}%)")
mod = course.module(mid)
lesson_ids = [l["id"] for l in mod["lessons"]]
if st.session_state.get("sel_lesson") not in lesson_ids:
    st.session_state["sel_lesson"] = lesson_ids[0]
lid = st.radio("Lesson", lesson_ids, key="sel_lesson", horizontal=True,
               format_func=lambda i: f"{'✅ ' if i in stt['lessons_done'] else ''}{course.lesson(i)['title']}")
les = course.lesson(lid)

st.caption(mod["summary"])
st.markdown(course.lesson_markdown(lid))
done = lid in stt["lessons_done"]
if st.button("Mark lesson as not done" if done else "✔ Mark lesson as done", key=f"ld_{lid}"):
    progress.set_lesson_complete(lid, not done)
    st.rerun()

st.divider()
st.subheader(f"Exercises ({len(les['exercises'])})")
first_open = True
for n, ex in enumerate(les["exercises"], start=1):
    p = stt["prog"].get(ex["id"], {})
    mark = "✅" if p.get("completed") else ("🟡" if p.get("attempts") else "⬜")
    with st.expander(f"{mark} Exercise {n}: {ex['title']}", expanded=(not p.get("completed") and first_open)):
        exercise.render(ex)
    if not p.get("completed"):
        first_open = False
