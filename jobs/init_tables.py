"""
This module contains the tables for the pipeline runs
"""
import sqlite3


def _ensure_postgres_id_defaults(conn):
    """
    If pipeline tables were created earlier without BIGSERIAL (e.g. manual DDL or
    an old schema), id has no default and INSERT ... RETURNING id fails with NOT NULL.
    Attach a sequence + DEFAULT when information_schema shows no default on id.
    """
    if isinstance(conn, sqlite3.Connection):
        return
    fixes = (
        ("pipeline_runs", "pipeline_runs_id_seq"),
        ("pipeline_logs", "pipeline_logs_id_seq"),
    )
    with conn.cursor() as cur:
        for table, seq in fixes:
            cur.execute(
                """
                SELECT column_default
                FROM information_schema.columns
                WHERE table_schema = current_schema()
                  AND table_name = %s
                  AND column_name = 'id'
                """,
                (table,),
            )
            row = cur.fetchone()
            if row is None:
                continue
            default = row["column_default"] if isinstance(row, dict) else row[0]
            if default:
                continue
            cur.execute(f"CREATE SEQUENCE IF NOT EXISTS {seq}")
            cur.execute(
                f"ALTER TABLE {table} ALTER COLUMN id "
                f"SET DEFAULT nextval('{seq}'::regclass)"
            )
            cur.execute(
                f"SELECT setval(%s, COALESCE((SELECT MAX(id) FROM {table}), 0), true)",
                (seq,),
            )
            cur.execute(f"ALTER SEQUENCE {seq} OWNED BY {table}.id")


def create_pipeline_tables(conn):
    """
    Create the pipeline runs table
    """
    # SQLite: one statement per execute(); no BIGSERIAL. Postgres: BIGSERIAL.
    id_pk = (
        "INTEGER PRIMARY KEY AUTOINCREMENT"
        if isinstance(conn, sqlite3.Connection)
        else "BIGSERIAL PRIMARY KEY"
    )
    conn.execute(
        f"""
        CREATE TABLE IF NOT EXISTS pipeline_runs (
            id {id_pk},
            pipeline_name TEXT,
            run_type TEXT,
            status TEXT,
            started_at TIMESTAMP,
            finished_at TIMESTAMP,
            records_processed INTEGER,
            new_records INTEGER,
            updated_records INTEGER,
            error TEXT
        );
        """
    )
    conn.execute(
        f"""
        CREATE TABLE IF NOT EXISTS pipeline_logs (
            id {id_pk},
            job_id INTEGER,
            log_level TEXT,
            message TEXT,
            created_at TIMESTAMP
        );
        """
    )
    _ensure_postgres_id_defaults(conn)
    conn.commit()
