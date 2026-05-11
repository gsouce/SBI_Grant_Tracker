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
@db_migration_bp.route("/api/db_migration/add_unbookmarked_grants", methods=["POST", "GET"])
def add_unbookmarked_grants():
    """
    Add unbookmarked grants to the database
    """
    try:
        conn = get_db_connection()

        cursor = conn.cursor()
        cursor.execute(
            "ADD COLUMN unbookmarked BOOLEAN NOT NULL DEFAULT FALSE TO user_grant_activity"
        )
        conn.commit()
        return jsonify({"message": "Unbookmarked grants added successfully"}), 200
    except Exception as e:
        return jsonify({"message": "Error adding unbookmarked grants: " + str(e)}), 500

