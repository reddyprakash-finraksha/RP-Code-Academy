import tempfile
from pathlib import Path

import pandas as pd
import streamlit as st

from components import ui
from core import backup, config, course, db, progress, reports, security

ui.hero("Teacher Dashboard", "Progress for the student profile on THIS computer only.")

# ---- PIN gate ------------------------------------------------------------------
if not security.pin_is_set():
    st.info("First time here: choose a teacher PIN (at least 4 characters). Students should not know it.")
    with st.form("setpin"):
        p1 = st.text_input("New PIN", type="password")
        p2 = st.text_input("Repeat PIN", type="password")
        if st.form_submit_button("Save PIN", type="primary"):
            if p1 != p2:
                st.error("The PINs do not match.")
            else:
                try:
                    security.set_pin(p1)
                    st.session_state["teacher_ok"] = True
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))
    st.stop()

if not st.session_state.get("teacher_ok"):
    with st.form("login"):
        pin = st.text_input("Teacher PIN", type="password")
        if st.form_submit_button("Unlock", type="primary"):
            if security.verify_pin(pin):
                st.session_state["teacher_ok"] = True
                st.rerun()
            else:
                st.error("Wrong PIN.")
    st.stop()

if st.button("🔒 Lock dashboard"):
    st.session_state["teacher_ok"] = False
    st.rerun()

s = progress.stats()
stu = ui.require_student()
tab_over, tab_mod, tab_ex, tab_rep, tab_bak, tab_set = st.tabs(
    ["Overview", "Modules", "Exercises", "Reports (CSV)", "Backups", "Settings"])

with tab_over:
    st.subheader(stu["name"])
    c = st.columns(4)
    c[0].metric("Overall", f"{s['overall_percent']}%")
    c[1].metric("Exercises", f"{s['exercises_done']}/{s['exercises_total']}")
    c[2].metric("Lessons", f"{s['lessons_done_n']}/{s['lessons_total']}")
    c[3].metric("Projects", f"{s['projects_done']}/{s['projects_total']}")
    c = st.columns(4)
    c[0].metric("Quizzes passed", f"{s['quizzes_passed']}/{len(course.modules())}")
    c[1].metric("Attempts", s["attempts"])
    c[2].metric("Streak (days)", s["streak"])
    c[3].metric("Last active", (s["last_active"] or "never").replace("T", " "))
    st.markdown("**Needs attention** (many attempts, not yet passed)")
    stuck = [(i, p) for i, p in s["prog"].items() if p["attempts"] >= 3 and not p["completed"]]
    if stuck:
        rows = []
        for i, p in sorted(stuck, key=lambda x: -x[1]["attempts"]):
            title = course.exercise(i)["title"] if i in {e["id"] for e in course.all_exercises()} else course.project(i)["title"]
            rows.append({"ID": i, "Title": title, "Attempts": p["attempts"], "Hints": p["hints_used"]})
        st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
    else:
        st.success("Nothing stuck right now.")
    viewed = sum(1 for p in s["prog"].values() if p["solution_viewed"])
    st.caption(f"Solutions viewed: {viewed} | Exercises passed without any help: {s['no_help_solves']}")

with tab_mod:
    rows = []
    for m in course.modules():
        pm = s["per_module"][m["id"]]
        q = pm["quiz_best"]
        rows.append({"Module": f"{m['number']}. {m['title']}", "Lessons": f"{pm['lessons_done']}/{pm['lessons_total']}",
                     "Exercises": f"{pm['exercises_done']}/{pm['exercises_total']}", "Progress %": pm["percent"],
                     "Best quiz": "-" if q is None else f"{round(q * 100)}%", "Complete": "Yes" if pm["complete"] else "No"})
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch",
                 column_config={"Progress %": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%d%%")})

with tab_ex:
    mid = st.selectbox("Module", [m["id"] for m in course.modules()],
                       format_func=lambda i: f"{course.module(i)['number']}. {course.module(i)['title']}", key="t_mod")
    rows = []
    for les in course.module(mid)["lessons"]:
        for e in les["exercises"]:
            p = s["prog"].get(e["id"], {})
            rows.append({"Lesson": les["title"], "Exercise": e["title"],
                         "Status": "Completed" if p.get("completed") else ("Attempted" if p.get("attempts") else "Not started"),
                         "Attempts": p.get("attempts", 0), "Hints": p.get("hints_used", 0),
                         "Solution viewed": "Yes" if p.get("solution_viewed") else "", "Passed on": p.get("first_passed_at") or ""})
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")

with tab_rep:
    st.write("CSV files open directly in Excel.")
    c = st.columns(3)
    c[0].download_button("⬇ Exercises CSV", reports.exercise_report(), "psca_exercises.csv", "text/csv", width="stretch")
    c[1].download_button("⬇ Modules CSV", reports.module_report(), "psca_modules.csv", "text/csv", width="stretch")
    c[2].download_button("⬇ Quizzes CSV", reports.quiz_report(), "psca_quizzes.csv", "text/csv", width="stretch")
    if st.button("Also save copies to the reports folder"):
        paths = reports.save_all()
        st.success(f"Saved {len(paths)} files to: {paths[0].parent}")

with tab_bak:
    st.write(f"Backups are made automatically once a day and kept in `{backup.backup_dir()}` (latest {config.BACKUP_KEEP}).")
    if st.button("Create backup now", type="primary"):
        st.success(f"Backup created: {backup.create_backup('manual').name}")
    files = backup.list_backups()
    if files:
        pick = st.selectbox("Restore from", files, format_func=lambda p: p.name)
        if st.checkbox("I understand this replaces current progress (a safety backup is made first)"):
            if st.button("Restore selected backup"):
                try:
                    backup.restore_backup(pick)
                    st.success("Restored. Reload the page to see the restored data.")
                except ValueError as e:
                    st.error(str(e))
    up = st.file_uploader("...or restore from a backup file (.db)", type=["db"])
    if up is not None and st.button("Restore uploaded file"):
        tmp = Path(tempfile.mkstemp(suffix=".db")[1])
        tmp.write_bytes(up.getvalue())
        try:
            backup.restore_backup(tmp)
            st.success("Restored from uploaded file.")
        except ValueError as e:
            st.error(str(e))
        finally:
            tmp.unlink(missing_ok=True)

with tab_set:
    st.markdown("**Rename student**")
    with st.form("rename"):
        name = st.text_input("Name", value=stu["name"])
        if st.form_submit_button("Save name"):
            try:
                db.create_student(name)
                st.success("Saved.")
            except ValueError as e:
                st.error(str(e))
    st.markdown("**Change PIN**")
    with st.form("chpin"):
        n1 = st.text_input("New PIN", type="password")
        if st.form_submit_button("Change PIN"):
            try:
                security.set_pin(n1)
                st.success("PIN changed.")
            except ValueError as e:
                st.error(str(e))
    st.markdown("**Reset all progress** (for a new student on this computer)")
    confirm = st.text_input("Type RESET to confirm")
    if st.button("Reset progress", disabled=confirm != "RESET"):
        backup.create_backup("pre-reset")
        progress.reset_all()
        st.session_state.clear()
        st.success("Progress cleared (a backup was saved first). Reload the page.")
    st.caption(f"Data folder: {config.data_dir()}  |  Version {config.VERSION}")
