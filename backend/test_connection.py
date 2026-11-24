import sqlite3
from pathlib import Path
from contextlib import contextmanager

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR.parent / "ecommerce-cloud-data-warehouse" / "ecommerce.db"


def get_db_connection():

    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    connection = sqlite3.connect(
        f"file:{DB_PATH.as_posix()}?mode=ro",
        uri=True
    )

    connection.row_factory = sqlite3.Row

    return connection


@contextmanager
def get_connection():

    connection = get_db_connection()

    try:
        yield connection
    finally:
        connection.close()