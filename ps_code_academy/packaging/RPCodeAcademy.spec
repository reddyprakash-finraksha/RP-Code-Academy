# -*- mode: python ; coding: utf-8 -*-
# Build:  pyinstaller packaging/RPCodeAcademy.spec --noconfirm
# One-folder build (NOT one-file): one process per run, faster start, and the
# sandbox Job Object (ActiveProcessLimit=1) works without a bootloader parent.
from pathlib import Path
from PyInstaller.utils.hooks import collect_all, copy_metadata

ROOT = Path(SPECPATH).parent

datas, binaries, hiddenimports = [], [], []
for pkg in ("streamlit", "altair", "pydeck"):
    d, b, h = collect_all(pkg)
    datas += d; binaries += b; hiddenimports += h
for dist in ("streamlit", "pandas", "numpy", "pyarrow", "altair", "pydeck", "tornado", "click", "packaging"):
    try:
        datas += copy_metadata(dist)
    except Exception:
        pass

# App source + content (Streamlit executes page scripts from disk, so they ship as data files)
for folder in ("pages", "components", "core", "course_data", "assets", ".streamlit"):
    datas.append((str(ROOT / folder), folder))
datas.append((str(ROOT / "app.py"), "."))

# Standard-library modules student programs may import (PyInstaller cannot see these)
hiddenimports += [
    "math", "random", "statistics", "datetime", "collections", "itertools", "functools", "string", "json",
    "csv", "re", "time", "os", "sys", "io", "textwrap", "decimal", "fractions", "operator", "heapq", "bisect",
    "copy", "enum", "dataclasses", "typing", "abc", "pathlib", "calendar", "numbers", "array", "pprint",
    "traceback", "contextlib", "glob", "shutil", "tempfile", "uuid", "hashlib", "base64", "zlib", "secrets",
    "unicodedata", "struct", "queue", "types", "warnings", "weakref", "keyword",
    "core.runner", "core.sandbox", "core.checker", "core.course", "core.progress", "core.achievements",
    "core.backup", "core.reports", "core.security", "core.db", "core.config", "core.logging_setup",
    "components.ui", "components.exercise",
]

a = Analysis(
    [str(ROOT / "launcher.py")],
    pathex=[str(ROOT)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    excludes=["tkinter", "matplotlib", "scipy", "IPython", "notebook", "pytest"],
    noarchive=False,
)
pyz = PYZ(a.pure)
icon = ROOT / "packaging" / "icon.ico"
exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name="RPCodeAcademy", console=False,
          icon=str(icon) if icon.exists() else None, upx=False)
coll = COLLECT(exe, a.binaries, a.datas, strip=False, upx=False, name="RPCodeAcademy")
