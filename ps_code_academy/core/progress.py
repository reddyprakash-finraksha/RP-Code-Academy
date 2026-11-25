"""Progress tracking: attempts, hints, solutions, lessons, quizzes, projects."""
from __future__ import annotations

from datetime import date, datetime

from . import config, course, db

SENTINEL = object()


def _row(con, item_id):
    return con.execute("SELECT * FROM progress WHERE item_id = ?", (item_id,)).fetchone()


def get_item(item_id: str) -> dict:
    with db.session() as con:
        r = _row(con, item_id)
    return dict(r) if r else {"item_id": item_id, "completed": 0, "attempts": 0, "hints_used": 0,
                              "solution_viewed": 0, "first_passed_at": None, "last_code": None}


def save_code(item_id: str, code: str, kind: str = "exercise") -> None:
    with db.session() as con:
        con.execute("INSERT INTO progress(item_id, kind, last_code, updated_at) VALUES (?,?,?,?) "
                    "ON CONFLICT(item_id) DO UPDATE SET last_code=excluded.last_code, updated_at=excluded.updated_at",
                    (item_id, kind, code, db.now()))


def record_attempt(item_id: str, code: str, passed: bool, kind: str = "exercise") -> None:
    ts = db.now()
    with db.session() as con:
        con.execute("INSERT INTO submissions(item_id, passed, code, ts) VALUES (?,?,?,?)", (item_id, int(passed), code, ts))
        con.execute("INSERT OR IGNORE INTO progress(item_id, kind, updated_at) VALUES (?,?,?)", (item_id, kind, ts))
        con.execute("UPDATE progress SET attempts = attempts + 1, last_code = ?, updated_at = ?, "
                    "completed = CASE WHEN ? THEN 1 ELSE completed END, "
                    "first_passed_at = CASE WHEN ? AND first_passed_at IS NULL THEN ? ELSE first_passed_at END "
                    "WHERE item_id = ?", (code, ts, int(passed), int(passed), ts, item_id))


def failed_attempts(item_id: str) -> int:
    with db.session() as con:
        r = con.execute("SELECT COUNT(*) c FROM submissions WHERE item_id=? AND passed=0", (item_id,)).fetchone()
    return r["c"]


def use_hint(item_id: str, total: int, kind: str = "exercise") -> int:
    with db.session() as con:
        con.execute("INSERT OR IGNORE INTO progress(item_id, kind, updated_at) VALUES (?,?,?)", (item_id, kind, db.now()))
        con.execute("UPDATE progress SET hints_used = MIN(?, hints_used + 1) WHERE item_id = ?", (total, item_id))
        return _row(con, item_id)["hints_used"]


def view_solution(item_id: str, kind: str = "exercise") -> None:
    with db.session() as con:
        con.execute("INSERT OR IGNORE INTO progress(item_id, kind, updated_at) VALUES (?,?,?)", (item_id, kind, db.now()))
        con.execute("UPDATE progress SET solution_viewed = 1 WHERE item_id = ?", (item_id,))


def solution_unlocked(item_id: str, n_hints: int) -> bool:
    p = get_item(item_id)
    return bool(p["completed"] or p["solution_viewed"] or failed_attempts(item_id) >= config.SOLUTION_UNLOCK_ATTEMPTS
                or (n_hints and p["hints_used"] >= n_hints and p["attempts"] >= 1))


# ---- lessons / quizzes -----------------------------------------------------------
def set_lesson_complete(lesson_id: str, done: bool = True) -> None:
    with db.session() as con:
        if done:
            con.execute("INSERT OR IGNORE INTO lesson_progress(lesson_id, completed_at) VALUES (?,?)", (lesson_id, db.now()))
        else:
            con.execute("DELETE FROM lesson_progress WHERE lesson_id = ?", (lesson_id,))


def record_quiz(module_id: str, score: int, total: int) -> None:
    with db.session() as con:
        con.execute("INSERT INTO quiz_results(module_id, score, total, ts) VALUES (?,?,?,?)", (module_id, score, total, db.now()))


# ---- aggregate stats --------------------------------------------------------------
def _streak(days: set[date]) -> int:
    if not days:
        return 0
    cur = date.today() if date.today() in days else date.today().fromordinal(date.today().toordinal() - 1)
    n = 0
    while cur in days:
        n += 1
        cur = cur.fromordinal(cur.toordinal() - 1)
    return n


def stats() -> dict:
    with db.session() as con:
        prog = {r["item_id"]: dict(r) for r in con.execute("SELECT * FROM progress")}
        lessons_done = {r["lesson_id"] for r in con.execute("SELECT lesson_id FROM lesson_progress")}
        quizzes = [dict(r) for r in con.execute("SELECT * FROM quiz_results ORDER BY id")]
        sub_ts = [r["ts"] for r in con.execute("SELECT ts FROM submissions")]
    ex_ids = {e["id"] for e in course.all_exercises()}
    done_ex = {i for i, p in prog.items() if p["completed"] and i in ex_ids}
    done_pr = {i for i, p in prog.items() if p["completed"] and p["kind"] == "project"}
    best_quiz: dict[str, float] = {}
    for q in quizzes:
        best_quiz[q["module_id"]] = max(best_quiz.get(q["module_id"], 0), q["score"] / q["total"])
    per_module = {}
    for m in course.modules():
        ids = [e["id"] for les in m["lessons"] for e in les["exercises"]]
        d = sum(i in done_ex for i in ids)
        ls = sum(les["id"] in lessons_done for les in m["lessons"])
        qpass = best_quiz.get(m["id"], 0) >= config.PASS_MARK_QUIZ
        per_module[m["id"]] = {"exercises_done": d, "exercises_total": len(ids), "lessons_done": ls,
                               "lessons_total": len(m["lessons"]), "quiz_best": best_quiz.get(m["id"]),
                               "quiz_passed": qpass, "complete": d == len(ids) and qpass,
                               "percent": round(100 * d / len(ids)) if ids else 0}
    days = set()
    for ts in sub_ts:
        try:
            days.add(datetime.fromisoformat(ts).date())
        except ValueError:
            pass
    clean = sum(1 for i in done_ex if not prog[i]["hints_used"] and not prog[i]["solution_viewed"])
    total_ex = len(ex_ids)
    return {
        "prog": prog, "lessons_done": lessons_done, "quizzes": quizzes, "best_quiz": best_quiz,
        "exercises_done": len(done_ex), "exercises_total": total_ex,
        "projects_done": len(done_pr), "projects_total": len(course.projects()),
        "lessons_done_n": len(lessons_done), "lessons_total": len(course.all_lessons()),
        "quizzes_passed": sum(v >= config.PASS_MARK_QUIZ for v in best_quiz.values()),
        "modules_complete": sum(v["complete"] for v in per_module.values()),
        "per_module": per_module, "attempts": sum(p["attempts"] for p in prog.values()),
        "submissions": len(sub_ts), "streak": _streak(days), "active_days": len(days),
        "last_active": max(sub_ts) if sub_ts else None, "no_help_solves": clean,
        "perfect_quizzes": sum(1 for q in quizzes if q["score"] == q["total"]),
        "overall_percent": round(100 * len(done_ex) / total_ex) if total_ex else 0,
    }


def next_exercise() -> dict | None:
    done = {i for i, p in stats()["prog"].items() if p["completed"]}
    return next((e for e in course.all_exercises() if e["id"] not in done), None)


def reset_all() -> None:
    with db.session() as con:
        for t in ("progress", "submissions", "lesson_progress", "quiz_results", "achievements"):
            con.execute(f"DELETE FROM {t}")
