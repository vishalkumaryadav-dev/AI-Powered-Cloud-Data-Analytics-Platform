
import sqlite3
import gzip
import shutil
import os

from pathlib import Path
from contextlib import contextmanager


# Project 2 root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Original database from Project 1 (local development)
LOCAL_DB_PATH = (
    BASE_DIR.parent
    / "ecommerce-cloud-data-warehouse"
    / "ecommerce.db"
)

# Compressed database bundled with Project 2 (deployment)
DB_ARCHIVE_PATH = BASE_DIR / "data" / "ecommerce.db.gz"

# Extracted database location
DEPLOYED_DB_PATH = BASE_DIR / "data" / "ecommerce.db"


def get_database_path():
    """
    Locate the database.

    Prefer the original Project 1 database locally.
    Otherwise, extract the bundled compressed database.
    """

    if LOCAL_DB_PATH.exists():
        return LOCAL_DB_PATH

    if DEPLOYED_DB_PATH.exists():
        return DEPLOYED_DB_PATH

    if not DB_ARCHIVE_PATH.exists():
        raise FileNotFoundError(
            "Neither the original database nor the "
            "compressed database archive was found."
        )

    DEPLOYED_DB_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    temp_path = DEPLOYED_DB_PATH.with_suffix(".db.tmp")

    try:
        with gzip.open(DB_ARCHIVE_PATH, "rb") as source:
            with open(temp_path, "wb") as destination:
                shutil.copyfileobj(source, destination)

        os.replace(temp_path, DEPLOYED_DB_PATH)

    finally:
        if temp_path.exists():
            temp_path.unlink()

    return DEPLOYED_DB_PATH


def get_db_connection():
    """
    Create and return a read-only SQLite connection.
    """

    db_path = get_database_path()

    connection = sqlite3.connect(
        f"file:{db_path.as_posix()}?mode=ro",
        uri=True
    )

    connection.row_factory = sqlite3.Row

    return connection


@contextmanager
def get_connection():
    """
    Automatically manage database connection lifecycle.
    """

    connection = get_db_connection()

    try:
        yield connection
    finally:
        connection.close()
