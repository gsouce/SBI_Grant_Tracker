from flask import Blueprint, jsonify, request
from db.db_util import get_db_connection, is_test_mode


db_migration_bp = Blueprint("db_migration", __name__)
## Data migration routes... 
@db_migration_bp.route("/api/db_migration/reset_tables", methods=["POST", "GET"])
def reset_tables():
    """
    Reset the tables for the database
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
        tables = cursor.fetchall()
        for table in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table[0]}")
        conn.commit()
        return jsonify({"message": "Tables reset successfully"}), 200
    except Exception as e:
        return jsonify({"message": "Error resetting tables: " + str(e)}), 500

