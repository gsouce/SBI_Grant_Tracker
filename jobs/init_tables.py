"""
This module contains the tables for the pipeline runs
"""
import sqlite3


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
    conn.commit()
