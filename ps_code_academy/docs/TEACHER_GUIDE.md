# RP Code Academy - Teacher Guide

## Installation (Windows 10/11, 64-bit)
1. Run `RPCodeAcademy-Setup-1.0.0.exe` as administrator on each classroom computer. No internet required.
2. A desktop shortcut and Start-menu entries are created.
3. Silent install for imaging: `RPCodeAcademy-Setup-1.0.0.exe /VERYSILENT /SUPPRESSMSGBOXES /NORESTART`.

## Where data lives
`%LOCALAPPDATA%\RPCodeAcademy` (one folder per **Windows user account**):
`psca.db` (progress), `backups\`, `reports\`, `logs\`.
**One profile per computer account.** If several students share a computer, give each their own Windows account, or reset progress between students (Teacher > Settings). To share one profile across all accounts on a PC, set the machine-wide environment variable `PSCA_DATA_DIR` (for example `C:\ProgramData\RPCodeAcademy`) and grant users write access.
Uninstalling keeps student data. Delete the folder above to remove it.

## Teacher dashboard
Open **Teacher** in the sidebar. The first visit asks you to choose a PIN (4+ characters).
- **Overview**: totals, streak, last activity, and exercises with 3+ failed attempts ("needs attention").
- **Modules / Exercises**: per-module and per-exercise status, attempts, hints, solution views.
- **Reports (CSV)**: exercises, modules and quizzes; open in Excel. Copies can also be saved to `reports\`.
- **Backups**: automatic daily backup (latest 20 kept), manual backup, restore from list or uploaded file. A safety backup is made before every restore.
- **Settings**: rename student, change PIN, reset all progress (type RESET).

The dashboard shows only the profile on **this** computer. To collect results from many PCs, export CSVs from each (or copy `psca.db` backups) and combine them.

### Forgot the PIN?
On the computer, run `"C:\Program Files\RPCodeAcademy\RPCodeAcademy.exe" --reset-teacher-pin`. The PIN is a classroom speed-bump, not strong security: anyone with local access could do this.

## Course map
15 modules x 3 lessons = 45 lessons; 150 auto-checked exercises; 15 quizzes (4 questions each); 5 projects.
1 Getting Started - 2 Variables & Types - 3 Numbers & Math - 4 Strings - 5 Input & Output - 6 Conditionals - 7 Loops - 8 Lists - 9 Tuples & Sets - 10 Dictionaries - 11 Functions - 12 Standard Library - 13 File Handling - 14 Error Handling - 15 OOP.
Projects: Number Guessing Game, Grade Book, To-Do List Manager, Text Analyzer, Bank Account.
A module counts as **complete** when all its exercises pass and its quiz is passed (70%).

## Safety of student code
Student programs run in a separate process with a 5 s time limit, 20 KB output cap, 256 MB memory limit, a private temp folder (deleted afterwards), a stripped environment, and blocks on network access, launching programs, native code, and files outside their folder.

## Troubleshooting
- Browser did not open: go to `http://localhost:8765`.
- "Port in use": another copy is running; the shortcut simply opens it.
- Windows Firewall prompt: the app listens on `127.0.0.1` only; choose Cancel/Block, it still works.
- Logs: `%LOCALAPPDATA%\RPCodeAcademy\logs\psca.log`.
