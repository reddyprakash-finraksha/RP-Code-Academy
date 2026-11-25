"""Generate course_data/ (JSON + Markdown) from tools/course_src.
Expected outputs are produced by running each reference solution in the real sandbox."""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

from core.sandbox import run_code  # noqa: E402
from course_src.mods_01_05 import MODULES_A  # noqa: E402
from course_src.mods_06_10 import MODULES_B  # noqa: E402
from course_src.mods_11_15 import MODULES_C  # noqa: E402
from course_src.projects import PROJECTS  # noqa: E402

OUT = ROOT / "course_data"


def tests_for(solution, inputs, label):
    tests = []
    for stdin in inputs:
        r = run_code(solution, stdin=stdin, timeout=10)
        if not r.ok:
            raise SystemExit(f"Reference solution failed for {label}:\n{r.stderr}{r.error}")
        tests.append({"input": stdin, "expected": r.stdout})
    return tests


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "modules").mkdir(parents=True)
    (OUT / "lessons").mkdir()
    ids = []
    for mi, m in enumerate(MODULES_A + MODULES_B + MODULES_C, start=1):
        mid = f"m{mi:02d}"
        ids.append(mid)
        mod = {"id": mid, "number": mi, "title": m["title"], "summary": m["summary"], "lessons": [], "quiz": m["quiz"]}
        for li, les in enumerate(m["lessons"], start=1):
            lid = f"{mid}-l{li}"
            (OUT / "lessons" / f"{lid}.md").write_text(les["markdown"], encoding="utf-8")
            exs = []
            for ei, e in enumerate(les["exercises"], start=1):
                eid = f"{lid}-e{ei}"
                exs.append({"id": eid, "title": e["title"], "prompt": e["prompt"], "starter": e["starter"],
                            "hints": e["hints"], "solution": e["solution"],
                            "tests": tests_for(e["solution"], e["tests"], eid)})
            mod["lessons"].append({"id": lid, "title": les["title"], "exercises": exs})
        (OUT / "modules" / f"{mid}.json").write_text(json.dumps(mod, indent=1, ensure_ascii=False), encoding="utf-8")
    projects = [dict(p, tests=tests_for(p["solution"], p["tests"], p["id"])) for p in PROJECTS]
    (OUT / "projects.json").write_text(json.dumps(projects, indent=1, ensure_ascii=False), encoding="utf-8")
    (OUT / "index.json").write_text(json.dumps({"version": "1.0.0", "modules": ids}, indent=1), encoding="utf-8")
    n_ex = sum(len(l["exercises"]) for m in MODULES_A + MODULES_B + MODULES_C for l in m["lessons"])
    print(f"Built {len(ids)} modules, {sum(len(m['lessons']) for m in MODULES_A+MODULES_B+MODULES_C)} lessons, "
          f"{n_ex} exercises, {len(projects)} projects")


if __name__ == "__main__":
    main()
