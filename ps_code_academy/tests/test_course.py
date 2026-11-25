from concurrent.futures import ThreadPoolExecutor

from core import checker, course


def test_required_counts():
    c = course.counts()
    assert (c["modules"], c["lessons"], c["exercises"], c["projects"]) == (15, 45, 150, 5)
    assert c["quiz_questions"] >= 15 * 4


def test_structure_and_ids_unique():
    ids = [e["id"] for e in course.all_exercises()]
    assert len(ids) == len(set(ids)) == 150
    for m in course.modules():
        assert len(m["lessons"]) == 3 and len(m["quiz"]) >= 4
        for q in m["quiz"]:
            assert 0 <= q["answer"] < len(q["options"])
        for les in m["lessons"]:
            assert course.lesson_markdown(les["id"]).startswith("#")
    for e in course.all_exercises():
        assert e["prompt"] and e["solution"] and e["hints"] and e["tests"], e["id"]


def test_every_reference_solution_passes_its_tests():
    items = course.all_exercises() + course.projects()
    with ThreadPoolExecutor(8) as pool:
        results = list(pool.map(lambda it: (it["id"], checker.check(it, it["solution"])), items))
    failed = [i for i, r in results if not r.passed]
    assert not failed, failed


def test_starter_code_does_not_already_pass():
    # a few trivial starters (bug-fix tasks) may be allowed; the rest must require work
    items = [e for e in course.all_exercises() if e["id"] != "m01-l2-e1"] + course.projects()
    with ThreadPoolExecutor(8) as pool:
        results = list(pool.map(lambda it: (it["id"], checker.check(it, it["starter"]).passed), items))
    assert not [i for i, ok in results if ok]


def test_wrong_answer_is_reported():
    ex = course.exercise("m03-l1-e1")
    res = checker.check(ex, "print(1)")
    assert not res.passed and res.first_failure.actual == "1" and res.first_failure.expected == "96"
