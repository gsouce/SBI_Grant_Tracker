import os
import sqlite3

try:
    import psycopg
except ImportError:  # pragma: no cover
    psycopg = None

def is_test_mode() -> bool:
    """
    Resolve TEST_MODE from environment.
    Truthy: true, 1, yes, y (case-insensitive)
    """
    raw = (os.getenv("TEST_MODE") or "").strip().lower()
    return raw in {"true", "1", "yes", "y"}

def get_db_connection(test_mode: bool = False):
    """
    Get a connection to the database
    """
    database_url = (os.getenv("DATABASE_URL") or "").strip()
    if database_url:
        if psycopg is None:
            raise RuntimeError("psycopg is required for DATABASE_URL connections.")
        print("Connecting to Postgres via DATABASE_URL")
        return psycopg.connect(database_url)

    if test_mode:
        print("Connecting to grants_test.db")
        conn = sqlite3.connect("grants_test.db")
        conn.row_factory = sqlite3.Row
        return conn
    else:
        print("Connecting to grants.db")
        conn = sqlite3.connect("grants.db")
        conn.row_factory = sqlite3.Row
        return conn