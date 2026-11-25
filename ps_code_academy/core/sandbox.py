"""Run student code in an isolated subprocess.

Protections: temp working folder (always removed), wall-clock timeout, output
cap, stripped environment, audit-hook guards (see runner.py), Windows Job Object
(memory limit, single process, kill-on-close, no UI access), POSIX rlimits.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from dataclasses import dataclass
from pathlib import Path

from . import config

IS_WIN = os.name == "nt"


@dataclass
class RunResult:
    stdout: str = ""
    stderr: str = ""
    returncode: int = 0
    timed_out: bool = False
    output_truncated: bool = False
    duration: float = 0.0
    error: str = ""          # sandbox-level problem (not the student's error)

    @property
    def ok(self) -> bool:
        return self.returncode == 0 and not self.timed_out and not self.output_truncated and not self.error


# ---- Windows job object ------------------------------------------------------
def _make_job(memory_mb: int):
    """Create a Job Object limiting memory/processes. Returns handle or None."""
    if not IS_WIN:
        return None
    try:
        import ctypes
        from ctypes import wintypes

        k32 = ctypes.WinDLL("kernel32", use_last_error=True)

        class IO_COUNTERS(ctypes.Structure):
            _fields_ = [(n, ctypes.c_ulonglong) for n in (
                "ReadOperationCount", "WriteOperationCount", "OtherOperationCount",
                "ReadTransferCount", "WriteTransferCount", "OtherTransferCount")]

        class BASIC(ctypes.Structure):
            _fields_ = [("PerProcessUserTimeLimit", ctypes.c_longlong), ("PerJobUserTimeLimit", ctypes.c_longlong),
                        ("LimitFlags", wintypes.DWORD), ("MinimumWorkingSetSize", ctypes.c_size_t),
                        ("MaximumWorkingSetSize", ctypes.c_size_t), ("ActiveProcessLimit", wintypes.DWORD),
                        ("Affinity", ctypes.c_size_t), ("PriorityClass", wintypes.DWORD),
                        ("SchedulingClass", wintypes.DWORD)]

        class EXTENDED(ctypes.Structure):
            _fields_ = [("BasicLimitInformation", BASIC), ("IoInfo", IO_COUNTERS),
                        ("ProcessMemoryLimit", ctypes.c_size_t), ("JobMemoryLimit", ctypes.c_size_t),
                        ("PeakProcessMemoryUsed", ctypes.c_size_t), ("PeakJobMemoryUsed", ctypes.c_size_t)]

        class UI(ctypes.Structure):
            _fields_ = [("UIRestrictionsClass", wintypes.DWORD)]

        k32.CreateJobObjectW.restype = wintypes.HANDLE
        job = k32.CreateJobObjectW(None, None)
        if not job:
            return None
        info = EXTENDED()
        # ACTIVE_PROCESS(0x8) | PROCESS_MEMORY(0x100) | KILL_ON_JOB_CLOSE(0x2000) | DIE_ON_UNHANDLED_EXCEPTION(0x400)
        info.BasicLimitInformation.LimitFlags = 0x8 | 0x100 | 0x2000 | 0x400
        info.BasicLimitInformation.ActiveProcessLimit = 1
        info.ProcessMemoryLimit = memory_mb * 1024 * 1024
        k32.SetInformationJobObject(job, 9, ctypes.byref(info), ctypes.sizeof(info))   # ExtendedLimitInformation
        ui = UI()
        # DESKTOP|DISPLAYSETTINGS|EXITWINDOWS|GLOBALATOMS|HANDLES|READCLIPBOARD|SYSTEMPARAMETERS|WRITECLIPBOARD
        ui.UIRestrictionsClass = 0xFF
        k32.SetInformationJobObject(job, 4, ctypes.byref(ui), ctypes.sizeof(ui))        # BasicUIRestrictions
        return (k32, job)
    except Exception:
        return None


def _assign_job(job, proc) -> None:
    if not job:
        return
    try:
        k32, handle = job
        k32.AssignProcessToJobObject(handle, int(proc._handle))  # type: ignore[attr-defined]
    except Exception:
        pass


def _close_job(job) -> None:
    if job:
        try:
            job[0].CloseHandle(job[1])
        except Exception:
            pass


def _posix_limits(timeout: float, memory_mb: int):
    def apply():
        import resource
        os.setsid()
        mem = memory_mb * 1024 * 1024
        for res, val in ((resource.RLIMIT_AS, mem), (resource.RLIMIT_CPU, int(timeout) + 2),
                         (resource.RLIMIT_FSIZE, 2 * 1024 * 1024), (resource.RLIMIT_CORE, 0)):
            try:
                resource.setrlimit(res, (val, val))
            except (ValueError, OSError):
                pass
    return apply


def _runner_cmd(script: str, sandbox: str) -> list[str]:
    if config.is_frozen():
        return [sys.executable, "--sandbox-run", script, sandbox]
    return [sys.executable, "-I", str(Path(__file__).with_name("runner.py")), script, sandbox]


def _kill(proc: subprocess.Popen) -> None:
    try:
        if IS_WIN:
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], capture_output=True,
                           creationflags=0x08000000, timeout=5)
        else:
            import signal
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
    except Exception:
        pass
    try:
        proc.kill()
    except Exception:
        pass


def run_code(code: str, stdin: str = "", timeout: float | None = None,
             max_output: int | None = None, memory_mb: int | None = None) -> RunResult:
    timeout = timeout or config.RUN_TIMEOUT_SEC
    max_output = max_output or config.MAX_OUTPUT_BYTES
    memory_mb = memory_mb or config.MEMORY_LIMIT_MB
    if len(code) > config.MAX_CODE_CHARS:
        return RunResult(returncode=1, error=f"Program is too long (limit {config.MAX_CODE_CHARS} characters).")

    sandbox = tempfile.mkdtemp(prefix="psca_run_")
    result = RunResult()
    proc = None
    job = None
    start = time.monotonic()
    try:
        script = os.path.join(sandbox, "main.py")
        with open(script, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(code)

        env = {"PYTHONIOENCODING": "utf-8", "PYTHONHASHSEED": "0", "PYTHONDONTWRITEBYTECODE": "1",
               "PYTHONUTF8": "1", "TEMP": sandbox, "TMP": sandbox, "TMPDIR": sandbox}
        if IS_WIN:
            for k in ("SystemRoot", "SYSTEMROOT", "windir"):
                if k in os.environ:
                    env[k] = os.environ[k]
        kwargs: dict = {}
        if IS_WIN:
            kwargs["creationflags"] = 0x08000000 | 0x00000200   # NO_WINDOW | NEW_PROCESS_GROUP
            job = _make_job(memory_mb)
        else:
            kwargs["preexec_fn"] = _posix_limits(timeout, memory_mb)

        proc = subprocess.Popen(_runner_cmd(script, sandbox), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, cwd=sandbox, env=env, **kwargs)
        _assign_job(job, proc)

        chunks: dict[str, bytearray] = {"out": bytearray(), "err": bytearray()}
        state = {"truncated": False}

        def pump(pipe, key):
            try:
                while True:
                    data = pipe.read1(4096) if hasattr(pipe, "read1") else pipe.read(4096)
                    if not data:
                        break
                    room = max_output - len(chunks[key])
                    if room <= 0 or len(data) > room:
                        chunks[key].extend(data[:max(room, 0)])
                        state["truncated"] = True
                        _kill(proc)
                        break
                    chunks[key].extend(data)
            except (OSError, ValueError):
                pass

        def feed():
            try:
                proc.stdin.write(stdin.encode("utf-8"))
                proc.stdin.close()
            except (OSError, ValueError):
                pass

        threads = [threading.Thread(target=pump, args=(proc.stdout, "out"), daemon=True),
                   threading.Thread(target=pump, args=(proc.stderr, "err"), daemon=True),
                   threading.Thread(target=feed, daemon=True)]
        for t in threads:
            t.start()
        try:
            proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            result.timed_out = True
            _kill(proc)
            proc.wait()
        for t in threads:
            t.join(timeout=2)
        result.returncode = proc.returncode if proc.returncode is not None else 1
        result.output_truncated = state["truncated"]
        result.stdout = chunks["out"].decode("utf-8", errors="replace")
        result.stderr = chunks["err"].decode("utf-8", errors="replace")
        if result.timed_out:
            result.stderr += f"\nStopped: your program ran for more than {timeout:g} seconds (maybe an endless loop?)."
        if result.output_truncated:
            result.stderr += "\nStopped: your program printed too much output."
    except Exception as exc:  # noqa: BLE001
        result.error = f"Could not run your program: {exc}"
        result.returncode = 1
    finally:
        if proc is not None and proc.poll() is None:
            _kill(proc)
        for s in (getattr(proc, "stdin", None), getattr(proc, "stdout", None), getattr(proc, "stderr", None)):
            try:
                if s:
                    s.close()
            except Exception:
                pass
        _close_job(job)
        shutil.rmtree(sandbox, ignore_errors=True)
        result.duration = time.monotonic() - start
    return result
