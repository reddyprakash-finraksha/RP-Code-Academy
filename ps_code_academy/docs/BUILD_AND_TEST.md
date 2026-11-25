# Build, Test, Release

## Prerequisites (Windows 10/11 x64)
Python 3.12 (64-bit, on PATH) and Inno Setup 6.

## One command
```
packaging\build_windows.bat
```
It: creates a clean venv, installs pinned dependencies, regenerates course data, **runs the tests**, builds with PyInstaller (one-folder), **verifies the packaged app** (frozen sandbox + server health), then builds `dist\RPCodeAcademy-Setup-1.0.0.exe`. It stops at the first failure.

## Without a Windows PC
Push the repository to GitHub and run the **Build Windows installer** workflow (`.github/workflows/build-windows.yml`, Actions tab > Run workflow). Download the installer from the run's artifacts.

## Developer commands
```
pip install -r requirements-dev.txt
python tools/build_course.py          # regenerate course_data/
python -m pytest -q tests             # 33 tests
streamlit run app.py                  # run from source
python packaging/verify_build.py dist/RPCodeAcademy/RPCodeAcademy.exe
```

## Test coverage
- Sandbox: output, stdin, errors, timeout, output cap, network/process/file blocks, cleanup, env stripping, memory bomb, size limit
- Course integrity: 15/45/150/5 counts, unique ids, every reference solution passes its tests, starters do not pass, wrong answers are reported
- Services: attempts, hints, solution unlock, stats, achievements, backup/restore/prune, CSV reports, PIN, validation
- UI (Streamlit AppTest): profile setup, every page renders, Check button records progress, teacher PIN flow

## Manual Windows acceptance checklist
1. Install on a clean Windows 10 and 11 VM with networking disabled; shortcut launches the app.
2. Create profile, pass an exercise, close and relaunch: progress persists.
3. Run `while True: pass` - stops after 5 s; Task Manager shows no leftover python/RPCodeAcademy child.
4. Run `import socket`, `open("C:/Windows/win.ini")`, `import os; os.system("calc")` - all refused.
5. Teacher: set PIN, export CSVs, backup, restore.
6. Uninstall: app removed, `%LOCALAPPDATA%\RPCodeAcademy` kept.
