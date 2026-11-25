import pandas as pd
import streamlit as st

from components import ui
from core import config, course, progress

ui.hero("My Progress", "See how far you have come.")
s = progress.stats()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Modules complete", f"{s['modules_complete']} / {len(course.modules())}")
c2.metric("Quizzes passed", f"{s['quizzes_passed']} / {len(course.modules())}")
c3.metric("Total attempts", s["attempts"])
c4.metric("Days practised", s["active_days"])
st.progress(s["overall_percent"] / 100, text=f"Exercises: {s['exercises_done']} / {s['exercises_total']}")

rows = []
for m in course.modules():
    pm = s["per_module"][m["id"]]
    q = pm["quiz_best"]
    rows.append({"Module": f"{m['number']}. {m['title']}", "Lessons": f"{pm['lessons_done']}/{pm['lessons_total']}",
                 "Exercises": f"{pm['exercises_done']}/{pm['exercises_total']}", "Progress %": pm["percent"],
                 "Best quiz": "-" if q is None else f"{round(q * 100)}%", "Done": "✅" if pm["complete"] else ""})
st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch",
             column_config={"Progress %": st.column_config.ProgressColumn("Progress %", min_value=0, max_value=100, format="%d%%")})
