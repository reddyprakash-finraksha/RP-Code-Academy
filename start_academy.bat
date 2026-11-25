@echo off
cd /d "%~dp0ps_code_academy"
if not exist "%~dp0venv\Scripts\python.exe" (
  python -m venv "%~dp0venv"
  call "%~dp0venv\Scripts\activate"
  pip install --no-index --find-links "%~dp0wheels" -r requirements.txt
) else (
  call "%~dp0venv\Scripts\activate"
)
streamlit run app.py