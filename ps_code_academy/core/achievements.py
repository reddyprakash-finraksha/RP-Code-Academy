"""Achievements, evaluated from progress statistics."""
from __future__ import annotations

from . import db, progress

# key, icon, title, description, predicate(stats)
ACHIEVEMENTS = [
    ("first_run", "🚀", "Liftoff", "Pass your first exercise", lambda s: s["exercises_done"] >= 1),
    ("ten", "🔟", "Warming Up", "Pass 10 exercises", lambda s: s["exercises_done"] >= 10),
    ("fifty", "🌟", "Half Century", "Pass 50 exercises", lambda s: s["exercises_done"] >= 50),
    ("hundred", "💯", "Centurion", "Pass 100 exercises", lambda s: s["exercises_done"] >= 100),
    ("all_ex", "🏆", "Exercise Master", "Pass all 150 exercises", lambda s: s["exercises_done"] >= s["exercises_total"]),
    ("lesson5", "📖", "Bookworm", "Complete 5 lessons", lambda s: s["lessons_done_n"] >= 5),
    ("all_lessons", "🎓", "Scholar", "Complete all 45 lessons", lambda s: s["lessons_done_n"] >= s["lessons_total"]),
    ("quiz_pass", "📝", "Quiz Taker", "Pass a module quiz", lambda s: s["quizzes_passed"] >= 1),
    ("quiz_perfect", "🎯", "Perfect Score", "Get 100% on a quiz", lambda s: s["perfect_quizzes"] >= 1),
    ("module1", "🧩", "Module Complete", "Finish a module (all exercises + quiz)", lambda s: s["modules_complete"] >= 1),
    ("module5", "🧱", "Building Blocks", "Finish 5 modules", lambda s: s["modules_complete"] >= 5),
    ("all_modules", "👑", "Python Graduate", "Finish all 15 modules", lambda s: s["modules_complete"] >= 15),
    ("project1", "🛠️", "Maker", "Complete a practical project", lambda s: s["projects_done"] >= 1),
    ("all_projects", "🏗️", "Builder", "Complete all 5 projects", lambda s: s["projects_done"] >= s["projects_total"]),
    ("no_help", "🧠", "Self-Reliant", "Pass 10 exercises with no hints or solutions", lambda s: s["no_help_solves"] >= 10),
    ("streak3", "🔥", "On Fire", "Practise 3 days in a row", lambda s: s["streak"] >= 3),
    ("persistent", "💪", "Never Give Up", "Make 100 attempts", lambda s: s["attempts"] >= 100),
]


def unlocked() -> dict[str, str]:
    with db.session() as con:
        return {r["key"]: r["unlocked_at"] for r in con.execute("SELECT * FROM achievements")}


def evaluate() -> list[tuple]:
    """Unlock any newly earned achievements; return the new ones."""
    s = progress.stats()
    have = unlocked()
    new = []
    with db.session() as con:
        for a in ACHIEVEMENTS:
            if a[0] not in have and a[4](s):
                con.execute("INSERT OR IGNORE INTO achievements(key, unlocked_at) VALUES (?,?)", (a[0], db.now()))
                new.append(a)
    return new
