"""Child-process runner for student code.

Runs inside the isolated subprocess (never imported by the Streamlit app).
Uses only the standard library. Installs an audit hook that blocks networking,
process creation, native code loading, and file access outside the sandbox
folder, then executes the student's script.
"""
import builtins
import os
import sys
import traceback

BLOCKED_EVENTS = {
    "socket.connect", "socket.bind", "socket.sendto", "socket.getaddrinfo",
    "socket.gethostbyname", "subprocess.Popen", "os.system", "os.exec",
    "os.posix_spawn", "os.spawn", "os.fork", "os.forkpty", "os.startfile",
    "ctypes.dlopen", "ctypes.dlsym", "ctypes.call_function", "ctypes.cdata",
    "webbrowser.open", "pty.spawn", "winreg.OpenKey", "winreg.CreateKey",
    "os.kill", "os.killpg", "signal.pthread_kill",
}
BLOCKED_MODULES = {
    "socket", "_socket", "subprocess", "ctypes", "_ctypes", "multiprocessing",
    "winreg", "_winapi", "webbrowser", "pty", "ftplib", "smtplib", "telnetlib",
    "http.client", "urllib.request", "xmlrpc", "socketserver",
}
PATH_EVENTS = {
    "os.remove", "os.rename", "os.rmdir", "os.mkdir", "os.chmod", "os.chown",
    "os.symlink", "os.link", "os.truncate", "os.utime", "shutil.copyfile",
    "shutil.copytree", "shutil.move", "shutil.rmtree", "os.listdir",
    "os.scandir", "os.chdir", "os.walk", "glob.glob",
}
WRITE_FLAGS = os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC


def _evict_blocked_modules() -> None:
    """Frozen (PyInstaller) runtimes may have pre-loaded some of these; drop them so
    a student's `import` statement goes through the audited import path and is refused."""
    for name in list(sys.modules):
        if name in BLOCKED_MODULES or name.split(".")[0] in BLOCKED_MODULES:
            del sys.modules[name]


def _install_guards(sandbox: str) -> None:
    _evict_blocked_modules()
    real = os.path.realpath
    sandbox = real(sandbox)
    read_roots = {sandbox}
    for p in (sys.prefix, sys.base_prefix, sys.exec_prefix, getattr(sys, "_MEIPASS", None),
              os.path.dirname(os.__file__), os.path.dirname(sys.executable)):
        if p:
            read_roots.add(real(p))
    read_roots = tuple(read_roots)

    def inside(path, roots) -> bool:
        p = real(path)
        return any(p == r or p.startswith(r + os.sep) for r in roots)

    def to_path(x):
        if x is None or isinstance(x, int):
            return None
        try:
            return os.fsdecode(x)
        except Exception:
            return None

    def hook(event, args):
        if event == "open":
            p = to_path(args[0])
            if p is None:
                return
            flags = args[2] if len(args) > 2 and isinstance(args[2], int) else 0
            writing = bool(flags & WRITE_FLAGS)
            if p.startswith("<") or p in (os.devnull, "nul", "NUL"):
                return
            if not inside(p, (sandbox,) if writing else read_roots):
                raise PermissionError("RP Code Academy: your program may only use files in its own folder.")
        elif event in BLOCKED_EVENTS:
            raise PermissionError(f"RP Code Academy: '{event}' is not allowed in student programs.")
        elif event == "import":
            name = str(args[0])
            if name in BLOCKED_MODULES or name.split(".")[0] in BLOCKED_MODULES:
                raise ImportError(f"RP Code Academy: the module '{name}' is not allowed in this course.")
        elif event in PATH_EVENTS:
            for a in args[:2]:
                p = to_path(a)
                if p is not None and not inside(p, read_roots if event in ("os.listdir", "os.scandir", "os.walk", "glob.glob") else (sandbox,)):
                    raise PermissionError("RP Code Academy: your program may only use files in its own folder.")

    sys.addaudithook(hook)


def main(argv) -> int:
    script, sandbox = argv[1], argv[2]
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    try:
        sys.stdin.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    os.chdir(sandbox)
    with open(script, "r", encoding="utf-8") as fh:
        source = fh.read()
    _install_guards(sandbox)
    sys.argv = ["main.py"]
    sys.setrecursionlimit(1000)
    try:
        code = compile(source, "main.py", "exec")
    except SyntaxError as exc:
        traceback.print_exception(type(exc), exc, None, file=sys.stderr)
        return 1
    g = {"__name__": "__main__", "__file__": "main.py", "__builtins__": builtins}
    try:
        exec(code, g)
    except SystemExit as exc:
        return exc.code if isinstance(exc.code, int) else 0
    except BaseException as exc:  # noqa: BLE001
        frames = [f for f in traceback.extract_tb(exc.__traceback__) if f.filename == "main.py"]
        sys.stderr.write("Traceback (most recent call last):\n")
        sys.stderr.write("".join(traceback.StackSummary.from_list(frames).format()))
        sys.stderr.write("".join(traceback.format_exception_only(type(exc), exc)))
        return 1
    finally:
        try:
            sys.stdout.flush()
        except Exception:
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
