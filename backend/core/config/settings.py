from dotenv import load_dotenv
from pathlib import Path
import os

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT_DIR / ".env")

def env_path(key: str) -> Path:
    value = os.getenv(key)
    if value is None:
        raise ValueError(f"Environment variable {key} is required")
    return Path(value)


ERP_MDB = ROOT_DIR / env_path("ERP_MDB")
ERP_SQLITE_DB = ROOT_DIR / env_path("ERP_SQLITE_DB")
SQLITE_DB = ROOT_DIR / env_path("SQLITE_DB")
OUTPUT_DIR = ROOT_DIR / env_path("OUTPUT_DIR")
INPUT_DIR = ROOT_DIR / env_path("INPUT_DIR")

ENCODING = os.getenv("ENCODING")

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)
