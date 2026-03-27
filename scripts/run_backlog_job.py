"""
Deployment-friendly backlog ingestion entrypoint.
"""
from pipelines.gran_gov.backlog_ingestion import ingest_backlog
from pipelines.gran_gov.init_tables import create_tables
from db.db_util import get_db_connection
from config.runtime import get_runtime_settings


def run_backlog_job() -> None:
    settings = get_runtime_settings()
    conn = get_db_connection(test_mode=settings.test_mode)
    try:
        create_tables(conn)
        ingest_backlog(conn, test_mode=1 if settings.test_mode else 0)
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    run_backlog_job()

