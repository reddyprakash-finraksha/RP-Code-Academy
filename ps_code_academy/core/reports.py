"""CSV reports (UTF-8 with BOM so Excel opens them correctly)."""
from __future__ import annotations

import csv
import io
from datetime import datetime
from pathlib import Path

from . import config, course, db, progress


def _csv(header: list[str], rows: list[list]) -> bytes:
    buf = io.StringIO(newline="")
    w = csv.writer(buf)
    w.writerow(header)
    w.writerows(rows)
    return ("\ufeff" + buf.getvalue()).encode("utf-8")


def _student() -> str:
    s = db.get_student()
    return s["name"] if s else ""


def exercise_report() -> bytes:
    st, name = progress.stats(), _student()
    rows = []
    for m in course.modules():
        for les in m["lessons"]:
            for e in les["exercises"]:
                p = st["prog"].get(e["id"], {})
                rows.append([name, m["title"], les["title"], e["id"], e["title"],
                             "Completed" if p.get("completed") else ("Attempted" if p.get("attempts") else "Not started"),
                             p.get("attempts", 0), p.get("hints_used", 0), "Yes" if p.get("solution_viewed") else "No",
                             p.get("first_passed_at") or ""])
    return _csv(["Student", "Module", "Lesson", "Exercise ID", "Exercise", "Status", "Attempts",
                 "Hints used", "Solution viewed", "First passed"], rows)


def module_report() -> bytes:
    st, name = progress.stats(), _student()
    rows = []
    for m in course.modules():
        pm = st["per_module"][m["id"]]
        q = pm["quiz_best"]
        rows.append([name, m["id"], m["title"], f'{pm["lessons_done"]}/{pm["lessons_total"]}',
                     f'{pm["exercises_done"]}/{pm["exercises_total"]}', f'{pm["percent"]}%',
                     "" if q is None else f"{round(q * 100)}%", "Yes" if pm["complete"] else "No"])
    return _csv(["Student", "Module ID", "Module", "Lessons", "Exercises", "Exercise %", "Best quiz", "Complete"], rows)


def quiz_report() -> bytes:
    name = _student()
    with db.session() as con:
        rows = [[name, r["module_id"], r["score"], r["total"], f'{round(100 * r["score"] / r["total"])}%', r["ts"]]
                for r in con.execute("SELECT * FROM quiz_results ORDER BY id")]
    return _csv(["Student", "Module ID", "Score", "Out of", "Percent", "Taken at"], rows)


def save_all() -> list[Path]:
    out = config.subdir("reports")
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    paths = []
    for label, fn in (("exercises", exercise_report), ("modules", module_report), ("quizzes", quiz_report)):
        p = out / f"psca_{label}_{stamp}.csv"
        p.write_bytes(fn())
        paths.append(p)
    return paths
