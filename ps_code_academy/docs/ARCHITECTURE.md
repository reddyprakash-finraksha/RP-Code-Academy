# Architecture

```
launcher.py            PyInstaller entry. Starts Streamlit on 127.0.0.1:8765, opens the browser.
                       `--sandbox-run` = child mode that executes student code (same exe, so no external Python needed).
app.py                 Streamlit shell: profile gate, auto-backup, navigation, error boundary.
pages/                 home, lessons, quizzes, projects, playground, achievements, my_progress, teacher
components/            ui.py (CSS/cards), exercise.py (editor + run/check/hint/solution panel)
core/                  config, db (SQLite schema), course (loader), sandbox + runner, checker, progress,
                       achievements, backup, reports, security (PIN), logging_setup
course_data/           index.json, modules/mNN.json (lessons, exercises, quiz), lessons/*.md, projects.json
tools/                 course_src/ (authoring DSL) + build_course.py (generates course_data/)
packaging/             RPCodeAcademy.spec, installer.iss, build_windows.bat, verify_build.py
tests/                 pytest suite (sandbox, course integrity, services, headless UI)
```

## Course content pipeline
Authors write lessons/exercises in `tools/course_src`. Tests list only **stdin**; `build_course.py` runs each reference solution inside the real sandbox to record the expected stdout, so tests can never disagree with the solution. Re-run it after editing: `python tools/build_course.py`.

## Sandbox (core/sandbox.py + core/runner.py)
| Control | Mechanism |
|---|---|
| Isolation | New subprocess, private temp working dir (always deleted), env stripped to a few safe variables |
| Time | Wall-clock timeout, process tree killed (`taskkill /T` on Windows, `killpg` on POSIX) |
| Output | Reader threads cap stdout/stderr (20 KB) and kill the process on overflow |
| Memory | Windows Job Object `ProcessMemoryLimit`; POSIX `RLIMIT_AS` |
| Processes | Job Object `ActiveProcessLimit=1`, `KILL_ON_JOB_CLOSE`, UI restrictions; audit hook blocks spawn/exec/fork |
| Network / native code | Audit hook blocks socket events and imports of socket, subprocess, ctypes, multiprocessing, winreg, http.client, urllib.request, ... |
| Files | Audit hook: writes only inside the sandbox dir; reads only sandbox + Python/bundle install dirs |
| Frozen app | `RPCodeAcademy.exe --sandbox-run` re-uses the bundled interpreter; blocked modules pre-loaded by the bundle are evicted before the hook is installed |

**Limits:** audit hooks are a strong guard-rail for a classroom of beginners, not a hardened sandbox against a determined attacker (no Windows AppContainer / low-integrity token). Reference solutions are stored in plain JSON on disk. Windows-specific Job Object code is exercised only on Windows.

## Data model (SQLite)
`student` (single row), `progress` (per exercise/project), `submissions` (every check), `lesson_progress`, `quiz_results`, `achievements`, `settings` (PIN hash, last backup). Schema version in `PRAGMA user_version`.
