"""Automatic test-case checking for exercises and projects."""
from __future__ import annotations

from dataclasses import dataclass, field

from . import sandbox


def normalize(text: str) -> str:
    lines = [ln.rstrip() for ln in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


@dataclass
class TestOutcome:
    index: int
    passed: bool
    stdin: str
    expected: str
    actual: str
    error: str = ""
    timed_out: bool = False


@dataclass
class CheckResult:
    passed: bool
    outcomes: list[TestOutcome] = field(default_factory=list)

    @property
    def passed_count(self) -> int:
        return sum(o.passed for o in self.outcomes)

    @property
    def first_failure(self) -> TestOutcome | None:
        return next((o for o in self.outcomes if not o.passed), None)


def check(item: dict, code: str, runner=sandbox.run_code) -> CheckResult:
    outcomes: list[TestOutcome] = []
    for i, t in enumerate(item["tests"], start=1):
        r = runner(code, stdin=t["input"])
        actual = normalize(r.stdout)
        expected = normalize(t["expected"])
        ok = r.ok and actual == expected
        outcomes.append(TestOutcome(i, ok, t["input"], expected, actual,
                                    error=(r.error or r.stderr).strip(), timed_out=r.timed_out))
    return CheckResult(all(o.passed for o in outcomes) and bool(outcomes), outcomes)
