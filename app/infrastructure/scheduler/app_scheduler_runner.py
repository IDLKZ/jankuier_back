import os
import subprocess
import sys

from app.infrastructure.app_config import app_config


def start_scheduler():
    if app_config.scheduler_use_local:
        scheduler_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "app_scheduler.py")
        )
        python_exec = sys.executable  # всегда venv python
        proc = subprocess.Popen([python_exec, scheduler_path])
        return proc
