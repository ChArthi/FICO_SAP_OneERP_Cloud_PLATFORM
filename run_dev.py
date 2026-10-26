import os
import runpy
import secrets
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = PROJECT_DIR / "backend"
DATABASE_PATH = BACKEND_DIR / "dev.db"
LOCAL_ENV_PATH = BACKEND_DIR / ".env.local"
SECRET_KEY_PATH = BACKEND_DIR / ".dev-secret-key"

if LOCAL_ENV_PATH.exists():
    for line in LOCAL_ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        os.environ.setdefault(name.strip(), value.strip().strip("\"'"))

try:
    secret_key = SECRET_KEY_PATH.read_text(encoding="utf-8").strip()
except FileNotFoundError:
    secret_key = secrets.token_urlsafe(48)
    try:
        with SECRET_KEY_PATH.open("x", encoding="utf-8") as secret_file:
            secret_file.write(secret_key)
    except FileExistsError:
        secret_key = SECRET_KEY_PATH.read_text(encoding="utf-8").strip()

if not secret_key:
    raise RuntimeError(f"Development signing key is empty: {SECRET_KEY_PATH}")

os.environ.setdefault("APP_ENV", "development")
os.environ.setdefault("DATABASE_URL", f"sqlite:///{DATABASE_PATH.as_posix()}")
os.environ.setdefault("SECRET_KEY", secret_key)

runpy.run_path(str(PROJECT_DIR / "run.py"), run_name="__main__")
