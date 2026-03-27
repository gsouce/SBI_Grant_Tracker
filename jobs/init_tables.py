"""
This module contains the tables for the pipeline runs
"""
def create_pipeline_tables(conn):
    """
    Create the pipeline runs table
    """
    conn.execute("""
        CREATE TABLE IF NOT EXISTS pipeline_runs (
            id BIGSERIAL PRIMARY KEY,
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

        CREATE TABLE IF NOT EXISTS pipeline_logs (
            id BIGSERIAL PRIMARY KEY,
            job_id INTEGER,
            log_level TEXT,
            message TEXT,
            created_at TIMESTAMP
        );
    """)
    conn.commit()
