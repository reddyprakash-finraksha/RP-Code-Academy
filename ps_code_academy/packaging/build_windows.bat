@echo off
REM ============================================================
REM  RP Code Academy - reproducible Windows build (run on Windows 10/11)
REM  Needs: Python 3.12 (64-bit) on PATH, Inno Setup 6 (iscc.exe on PATH
REM  or in the default install folder).  Output: dist\RPCodeAcademy-Setup-1.0.0.exe
REM ============================================================
setlocal
cd /d "%~dp0\.."

echo [1/6] Creating virtual environment...
if exist .venv-build rmdir /s /q .venv-build
python -m venv .venv-build || goto :fail
call .venv-build\Scripts\activate.bat
python -m pip install --upgrade pip || goto :fail
pip install -r requirements-dev.txt || goto :fail

echo [2/6] Generating course content...
python tools\build_course.py || goto :fail

echo [3/6] Running automated tests...
python -m pytest -q tests || goto :fail

echo [4/6] Building application with PyInstaller...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
pyinstaller packaging\RPCodeAcademy.spec --noconfirm --clean || goto :fail

echo [5/6] Testing the packaged app (sandbox + server)...
python packaging\verify_build.py dist\RPCodeAcademy\RPCodeAcademy.exe || goto :fail

echo [6/6] Building installer with Inno Setup...
where iscc >nul 2>nul && (set "ISCC=iscc") || set "ISCC=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
"%ISCC%" packaging\installer.iss || goto :fail

echo.
echo SUCCESS: dist\RPCodeAcademy-Setup-1.0.0.exe
exit /b 0

:fail
echo.
echo BUILD FAILED. See the messages above.
exit /b 1
