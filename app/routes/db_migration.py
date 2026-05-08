from flask import Blueprint, jsonify, request
import sqlite3

from db.db_util import get_db_connection, row_get

try:
    import psycopg
    from psycopg import sql
except ImportError:  # pragma: no cover
    psycopg = None
    sql = None


db_migration_bp = Blueprint("db_migration", __name__)
## Data migration routes... 
@db_migration_bp.route("/api/db_migration/reset_tables", methods=["POST", "GET"])
def reset_tables():
    """
    Reset the tables for the database
    """
    try:
        conn = get_db_connection()
        if isinstance(conn, sqlite3.Connection):
            cur = conn.cursor()
            # Drop user tables; keep sqlite internal tables.
            cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            )
            tables = [row_get(r, "name", 0) for r in cur.fetchall()]
            for name in tables:
                cur.execute(f'DROP TABLE IF EXISTS "{name}"')
            conn.commit()
            return jsonify({"message": f"Tables reset successfully ({len(tables)} dropped)"}), 200

        # Postgres (psycopg): rows are dict-like because of row_factory=dict_row.
        with conn.cursor() as cur:
            cur.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
            )
            tables = [row_get(r, "table_name", 0) for r in cur.fetchall()]
            for name in tables:
                # Quote identifiers and cascade to dependent objects (FKs, views, etc.).
                cur.execute(sql.SQL("DROP TABLE IF EXISTS {} CASCADE").format(sql.Identifier(name)))
        conn.commit()
        return jsonify({"message": f"Tables reset successfully ({len(tables)} dropped)"}), 200
    except Exception as e:
        return jsonify({"message": "Error resetting tables: " + str(e)}), 500

