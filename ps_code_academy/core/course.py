"""Loads course content (JSON + Markdown) from course_data/."""
from __future__ import annotations

import json
from functools import lru_cache

from . import config


def _read_json(rel: str):
    return json.loads((config.course_dir() / rel).read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def modules() -> list[dict]:
    """Full course tree: modules -> lessons -> exercises, plus quiz."""
    return [_read_json(f"modules/{m}.json") for m in _read_json("index.json")["modules"]]


@lru_cache(maxsize=1)
def projects() -> list[dict]:
    return _read_json("projects.json")


@lru_cache(maxsize=1)
def _index() -> dict:
    idx = {"module": {}, "lesson": {}, "exercise": {}, "project": {}}
    for m in modules():
        idx["module"][m["id"]] = m
        for les in m["lessons"]:
            les["module_id"] = m["id"]
            idx["lesson"][les["id"]] = les
            for ex in les["exercises"]:
                ex["lesson_id"], ex["module_id"] = les["id"], m["id"]
                idx["exercise"][ex["id"]] = ex
    for p in projects():
        idx["project"][p["id"]] = p
    return idx


def module(mid: str) -> dict:
    return _index()["module"][mid]


def lesson(lid: str) -> dict:
    return _index()["lesson"][lid]


def exercise(eid: str) -> dict:
    return _index()["exercise"][eid]


def project(pid: str) -> dict:
    return _index()["project"][pid]


def all_exercises() -> list[dict]:
    return list(_index()["exercise"].values())


def all_lessons() -> list[dict]:
    return list(_index()["lesson"].values())


def lesson_markdown(lid: str) -> str:
    return (config.course_dir() / "lessons" / f"{lid}.md").read_text(encoding="utf-8")


def counts() -> dict:
    return {"modules": len(modules()), "lessons": len(all_lessons()), "exercises": len(all_exercises()),
            "quiz_questions": sum(len(m["quiz"]) for m in modules()), "projects": len(projects())}
