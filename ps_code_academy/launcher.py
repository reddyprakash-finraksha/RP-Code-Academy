"""Windows entry point (PyInstaller).

* `RPCodeAcademy.exe`                    -> starts the local server and opens the browser
* `RPCodeAcademy.exe --sandbox-run ...`  -> internal: runs student code (see core/runner.py)
* `RPCodeAcademy.exe --reset-teacher-pin`-> clears the teacher PIN (needs local access)
"""
import os
import sys

if len(sys.argv) > 1 and sys.argv[1] == "--sandbox-run":
    from core import runner
    sys.exit(runner.main(sys.argv[1:]))

import socket
import threading
import time
import webbrowser
from pathlib import Path


def _base() -> Path:
    return Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))


def _port_free(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) != 0


def main() -> int:
    base = _base()
    sys.path.insert(0, str(base))
    os.chdir(base)
    from core import config, db, logging_setup, security

    log = logging_setup.setup()
    db.init_db()
    if "--reset-teacher-pin" in sys.argv:
        security.clear_pin()
        print("Teacher PIN cleared. You will be asked to choose a new one.")
        return 0

    port = config.SERVER_PORT
    url = f"http://localhost:{port}"
    if not _port_free(port):                       # already running: just open it
        webbrowser.open(url)
        return 0

    threading.Thread(target=lambda: (time.sleep(2.5), webbrowser.open(url)), daemon=True).start()
    os.environ.update({"STREAMLIT_SERVER_HEADLESS": "true", "STREAMLIT_BROWSER_GATHER_USAGE_STATS": "false",
                       "STREAMLIT_GLOBAL_DEVELOPMENT_MODE": "false", "STREAMLIT_SERVER_FILE_WATCHER_TYPE": "none",
                       "STREAMLIT_SERVER_ADDRESS": "127.0.0.1"})
    log.info("Starting RP Code Academy %s on %s", config.VERSION, url)
    from streamlit.web import cli as stcli
    sys.argv = ["streamlit", "run", str(base / "app.py"), f"--server.port={port}", "--global.developmentMode=false"]
    return stcli.main()


if __name__ == "__main__":
    sys.exit(main() or 0)
