import sqlite3

from flask import Blueprint, jsonify

from db.db_util import get_db_connection, is_test_mode, row_get

try:
    from psycopg import sql
except ImportError:  # pragma: no cover
    sql = None


db_migration_bp = Blueprint("db_migration", __name__)


@db_migration_bp.route("/api/db_migration/add_unbookmarked_grants", methods=["POST", "GET"])
def add_unbookmarked_grants():
    """
    Idempotently add ``unbookmarked`` to ``user_grant_activity`` if missing.
    """
    conn = None
    try:
        conn = get_db_connection(test_mode=is_test_mode())
        if isinstance(conn, sqlite3.Connection):
            cur = conn.cursor()
            try:
                cur.execute(
                    "ALTER TABLE user_grant_activity ADD COLUMN unbookmarked INTEGER NOT NULL DEFAULT 0"
                )
                added = True
            except sqlite3.OperationalError as e:
                if "duplicate column" in str(e).lower():
                    added = False
                else:
                    raise
            conn.commit()
            msg = (
                "Column unbookmarked added to user_grant_activity"
                if added
                else "Column unbookmarked already exists (no change)"
            )
            return jsonify({"message": msg, "added": added}), 200

        if sql is None:
            return jsonify({"message": "psycopg.sql required for Postgres migrations"}), 500
        with conn.cursor() as cur:
            cur.execute(
                "ALTER TABLE user_grant_activity ADD COLUMN IF NOT EXISTS "
                "unbookmarked BOOLEAN NOT NULL DEFAULT FALSE"
            )
        conn.commit()
        return jsonify(
            {
                "message": "Column unbookmarked ensured on user_grant_activity (Postgres IF NOT EXISTS)",
                "added": True,
            }
        ), 200
    except Exception as e:
        return jsonify({"message": "Error adding unbookmarked column: " + str(e)}), 500
    finally:
        if conn is not None:
            conn.close()


@db_migration_bp.route("/api/db_migration/reset_tables", methods=["POST", "GET"])
def reset_tables():
    """
    Drop all application tables. Destructive: use only in dev or with backups.
    """
    conn = None
    try:
        conn = get_db_connection(test_mode=is_test_mode())
        if isinstance(conn, sqlite3.Connection):
            cur = conn.cursor()
            cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            )
            tables = [row_get(r, "name", 0) for r in cur.fetchall()]
            for name in tables:
                cur.execute(f'DROP TABLE IF EXISTS "{name}"')
            conn.commit()
            return jsonify({"message": f"Tables reset successfully ({len(tables)} dropped)"}), 200

        if sql is None:
            return jsonify({"message": "psycopg.sql required for Postgres reset"}), 500
        with conn.cursor() as cur:
            cur.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
            )
            tables = [row_get(r, "table_name", 0) for r in cur.fetchall()]
            for name in tables:
                cur.execute(
                    sql.SQL("DROP TABLE IF EXISTS {} CASCADE").format(sql.Identifier(name))
                )
        conn.commit()
        return jsonify({"message": f"Tables reset successfully ({len(tables)} dropped)"}), 200
    except Exception as e:
        return jsonify({"message": "Error resetting tables: " + str(e)}), 500
    finally:
        if conn is not None:
            conn.close()
