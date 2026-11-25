import streamlit as st

from components import ui
from core import achievements, config, course, progress

ui.hero("Module Quizzes", f"Pass mark: {int(config.PASS_MARK_QUIZ * 100)}%. You can retake any quiz.")
stt = progress.stats()
mods = course.modules()
mid = st.selectbox("Choose a quiz", [m["id"] for m in mods],
                   format_func=lambda i: f"{course.module(i)['number']}. {course.module(i)['title']}"
                   + (f"  (best {round(stt['best_quiz'][i] * 100)}%)" if i in stt["best_quiz"] else ""))
mod = course.module(mid)

with st.form(f"quiz_{mid}"):
    answers = []
    for i, q in enumerate(mod["quiz"], start=1):
        answers.append(st.radio(f"{i}. {q['question']}", range(len(q["options"])), index=None,
                                format_func=lambda k, q=q: q["options"][k], key=f"q_{mid}_{i}"))
    submitted = st.form_submit_button("Submit answers", type="primary")

if submitted:
    if any(a is None for a in answers):
        st.warning("Please answer every question first.")
    else:
        score = sum(a == q["answer"] for a, q in zip(answers, mod["quiz"]))
        total = len(mod["quiz"])
        progress.record_quiz(mid, score, total)
        (st.success if score / total >= config.PASS_MARK_QUIZ else st.warning)(
            f"You scored {score} / {total}" + (" - passed! 🎉" if score / total >= config.PASS_MARK_QUIZ else " - try again after reviewing the lessons."))
        for i, (a, q) in enumerate(zip(answers, mod["quiz"]), start=1):
            ok = a == q["answer"]
            st.markdown(f"{'✅' if ok else '❌'} **Q{i}.** Correct answer: *{q['options'][q['answer']]}*. {q['explanation']}")
        for a in achievements.evaluate():
            st.toast(f"{a[1]} Achievement unlocked: {a[2]}!", icon="🏅")
