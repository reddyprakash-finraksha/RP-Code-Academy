# RP Code Academy v1.0

Offline-first Python learning platform for Windows classrooms. Streamlit + SQLite + JSON/Markdown content, packaged with PyInstaller and Inno Setup.

- 15 modules, 45 lessons, 150 auto-checked exercises with hints and solutions, 15 quizzes, 5 projects
- Safe code execution (subprocess, timeout, output cap, memory limit, file/network blocks)
- Achievements, progress tracking, teacher dashboard (PIN), backups, CSV reports
- Works fully offline after installation

Docs: `docs/STUDENT_GUIDE.md`, `docs/TEACHER_GUIDE.md`, `docs/ARCHITECTURE.md`, `docs/BUILD_AND_TEST.md`

Quick start from source: `pip install -r requirements-dev.txt && python tools/build_course.py && streamlit run app.py`
Build the installer: `packaging\build_windows.bat` (Windows) or the GitHub Actions workflow.
