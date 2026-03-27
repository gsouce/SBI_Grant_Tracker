from db.db_util import get_db_connection
from datetime import datetime


def add_last_seen_at_column(conn) -> None:
    """
    Add the last_seen_at column to the grants table
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute(f"ALTER TABLE grants ADD COLUMN IF NOT EXISTS last_seen_at TIMESTAMP NOT NULL DEFAULT '{now}'")

if __name__ == "__main__":
    conn = get_db_connection(test_mode=False)
    add_last_seen_at_column(conn)
    conn.commit()
    conn.close()