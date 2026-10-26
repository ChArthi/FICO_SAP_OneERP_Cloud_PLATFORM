import os
import runpy
import secrets
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
DATABASE_PATH = PROJECT_DIR / "backend" / "dev.db"

os.environ.setdefault("DATABASE_URL", f"sqlite:///{DATABASE_PATH.as_posix()}")
os.environ.setdefault("SECRET_KEY", secrets.token_urlsafe(32))

runpy.run_path(str(PROJECT_DIR / "run.py"), run_name="__main__")
