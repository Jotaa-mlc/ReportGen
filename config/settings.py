from dotenv import load_dotenv
from pathlib import Path
import os

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")


MDB_PATH = Path(os.getenv("MDB_PATH"))
BASE_DIR = Path(os.getenv("BASE_DIR"))
SCHEMA_FILE = Path(BASE_DIR / os.getenv("SCHEMA_FILE"))
SQLITE_DB = Path(BASE_DIR / os.getenv("SQLITE_DB"))
XLSX_DIR = Path(BASE_DIR / os.getenv("XLSX_DIR"))
TABLE_DIR = Path(BASE_DIR / os.getenv("TABLE_DIR"))

ENCODING = os.getenv("ENCODING")

TABLE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

XLSX_DIR.mkdir(
    parents=True,
    exist_ok=True
)
