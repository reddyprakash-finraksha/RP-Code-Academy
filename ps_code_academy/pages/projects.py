import streamlit as st

from components import exercise, ui
from core import course, progress

ui.hero("Practical Projects", "Five mini-projects that combine what you learned.")
stt = progress.stats()
projs = course.projects()
pid = st.radio("Project", [p["id"] for p in projs], horizontal=True,
               format_func=lambda i: f"{'✅ ' if stt['prog'].get(i, {}).get('completed') else ''}{course.project(i)['title']}")
p = course.project(pid)
reqs = "\n".join(f"- {r}" for r in p["requirements"])
item = dict(p, prompt=f"### {p['title']}\n{p['brief']}\n\n**Requirements**\n{reqs}")
exercise.render(item, kind="project")
