"""Post-build verification of the PyInstaller output (works on Windows and Linux).
Usage: python packaging/verify_build.py <path-to-RPCodeAcademy[.exe]>"""
import os
import subprocess
import sys
import tempfile
import time
import urllib.request

exe = os.path.abspath(sys.argv[1])
env = dict(os.environ, PSCA_DATA_DIR=tempfile.mkdtemp(prefix="psca_verify_"))
failures = []


def sandbox(code, stdin=""):
    d = tempfile.mkdtemp()
    script = os.path.join(d, "main.py")
    with open(script, "w") as fh:
        fh.write(code)
    return subprocess.run([exe, "--sandbox-run", script, d], input=stdin, capture_output=True, text=True,
                          timeout=60, cwd=d, env=env)


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else f"  -> {detail}"))
    if not ok:
        failures.append(name)


r = sandbox('import math, random, statistics, datetime, json, csv, collections\nprint(math.sqrt(16), input())', "hi\n")
check("frozen sandbox runs code + stdlib imports", r.stdout.strip() == "4.0 hi", r.stderr)
r = sandbox("import socket")
check("frozen sandbox blocks socket", "not allowed" in r.stderr, r.stderr)
r = sandbox("print(open('/etc/hosts').read())" if os.name != "nt" else "print(open(r'C:\\Windows\\win.ini').read())")
check("frozen sandbox blocks outside files", "PermissionError" in r.stderr, r.stderr)

proc = subprocess.Popen([exe], env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    ok = False
    for _ in range(60):
        time.sleep(1)
        try:
            ok = urllib.request.urlopen("http://localhost:8765/_stcore/health", timeout=2).read() == b"ok"
            if ok:
                break
        except Exception:
            pass
    check("packaged server answers /_stcore/health", ok)
finally:
    proc.terminate()
    try:
        proc.wait(10)
    except Exception:
        proc.kill()
sys.exit(1 if failures else 0)
