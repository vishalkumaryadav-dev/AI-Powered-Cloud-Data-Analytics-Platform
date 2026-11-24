import sqlite3
import time
import pandas as pd

from backend.database import get_connection


# Tables that AI-generated SQL is allowed to access
ALLOWED_TABLES = {
    "fact_order_items",
    "dim_customers",
    "dim_products",
    "dim_sellers",
    "dim_date"
}

# Query execution limits
QUERY_TIMEOUT_SECONDS = 5
MAX_RESULT_ROWS = 100



def validate_sql(sql_query: str) -> None:
    """
    Validate that SQL is a meaningful SELECT query
    referencing at least one approved warehouse table.
    """

    if not sql_query or not sql_query.strip():
        raise ValueError("SQL query cannot be empty")

    normalized_sql = sql_query.strip().lower()

    if not normalized_sql.startswith("select"):
        raise ValueError("Only SELECT queries are allowed")

    if not any(
        table in normalized_sql
        for table in ALLOWED_TABLES
    ):
        raise ValueError(
            "Query must reference an approved warehouse table"
        )


def authorizer(action, arg1, arg2, database_name, trigger_name):
    """
    Allow safe read operations and approved SQL functions.
    """

    if action == sqlite3.SQLITE_SELECT:
        return sqlite3.SQLITE_OK

    if action == sqlite3.SQLITE_READ:
        if arg1 in ALLOWED_TABLES:
            return sqlite3.SQLITE_OK

    if action == sqlite3.SQLITE_FUNCTION:
        allowed_functions = {
            "sum", "count", "avg", "min", "max",
            "round", "lower", "upper", "coalesce", "ifnull"
        }

        if (arg2 or "").lower() in allowed_functions:
            return sqlite3.SQLITE_OK

    return sqlite3.SQLITE_DENY


def execute_query(sql_query: str) -> pd.DataFrame:
    """
    Validate and safely execute a read-only SQL query.
    """

    validate_sql(sql_query)

    with get_connection() as connection:

        # Enable read-only query protection
        connection.execute("PRAGMA query_only = ON")

        # Enable SQLite authorizer
        connection.set_authorizer(authorizer)

        # Set execution time limit
        start_time = time.monotonic()

        def query_timeout():
            elapsed = time.monotonic() - start_time
            return int(elapsed > QUERY_TIMEOUT_SECONDS)

        connection.set_progress_handler(query_timeout, 1000)

        # Execute query
        cursor = connection.execute(sql_query)

        # Retrieve column names
        columns = [description[0] for description in cursor.description]

        # Fetch at most 101 rows to detect excess results
        rows = cursor.fetchmany(MAX_RESULT_ROWS + 1)

        if len(rows) > MAX_RESULT_ROWS:
            raise ValueError(
                f"Query returned more than {MAX_RESULT_ROWS} rows. "
                "Please narrow your query."
            )

        return pd.DataFrame(rows, columns=columns)
