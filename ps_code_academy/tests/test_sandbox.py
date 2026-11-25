import os
import time

from core import config, sandbox


def test_basic_output_and_stdin():
    r = sandbox.run_code('print("hi")\nprint(input().upper())', stdin="abc\n")
    assert r.ok and r.stdout == "hi\nABC\n"


def test_runtime_error_is_friendly():
    r = sandbox.run_code("def f():\n    return 1/0\nf()")
    assert not r.ok and "ZeroDivisionError" in r.stderr and "runner.py" not in r.stderr


def test_syntax_error():
    r = sandbox.run_code("print('x'")
    assert not r.ok and "SyntaxError" in r.stderr


def test_timeout_kills_infinite_loop():
    t = time.time()
    r = sandbox.run_code("while True:\n    pass", timeout=1)
    assert r.timed_out and not r.ok and time.time() - t < 6


def test_output_limit():
    r = sandbox.run_code('while True:\n    print("x" * 1000)', timeout=5, max_output=5000)
    assert r.output_truncated and len(r.stdout) <= 5000


def test_blocks_network_and_subprocess():
    assert "not allowed" in sandbox.run_code("import socket").stderr
    assert "not allowed" in sandbox.run_code("import subprocess").stderr
    assert "not allowed" in sandbox.run_code("import os\nos.system('echo hi')").stderr


def test_blocks_files_outside_sandbox(tmp_path):
    secret = tmp_path / "secret.txt"
    secret.write_text("top secret")
    r = sandbox.run_code(f"print(open({str(secret)!r}).read())")
    assert "top secret" not in r.stdout and "PermissionError" in r.stderr
    r = sandbox.run_code(f"open({str(tmp_path / 'new.txt')!r}, 'w').write('x')")
    assert "PermissionError" in r.stderr and not (tmp_path / "new.txt").exists()


def test_can_use_own_folder_and_cleans_up():
    import tempfile, glob
    before = set(glob.glob(os.path.join(tempfile.gettempdir(), "psca_run_*")))
    r = sandbox.run_code('open("a.txt","w").write("z")\nprint(open("a.txt").read())')
    after = set(glob.glob(os.path.join(tempfile.gettempdir(), "psca_run_*")))
    assert r.stdout == "z\n" and after == before


def test_code_size_limit():
    r = sandbox.run_code("x=1\n" * config.MAX_CODE_CHARS)
    assert r.error and not r.ok


def test_environment_is_stripped(monkeypatch):
    monkeypatch.setenv("SECRET_TOKEN", "abc123")
    r = sandbox.run_code('import os\nprint(os.environ.get("SECRET_TOKEN"))')
    assert r.stdout.strip() == "None"


def test_memory_bomb_is_contained():
    r = sandbox.run_code("x = bytearray(2 * 1024 ** 3)\nprint(len(x))", timeout=5)
    assert not r.ok
