from flask import Blueprint, jsonify, request
from db.db_util import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    """
    Login the user
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        email = request.json["email"]
        password = generate_password_hash(request.json["password"])
        cursor.execute("SELECT user_id, password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["user_id"]
            return jsonify({"message": "User logged in successfully"}), 200
        else:
            return jsonify({"message": "Invalid email or password"}), 401
    except Exception as e:
        return jsonify({"message": "Error logging in: " + str(e)}), 500

@auth_bp.route("/api/auth/logout", methods=["POST"])
def logout():
    """
    Logout the user
    """
    try:
        session.pop("user_id", None)
        return jsonify({"message": "User logged out successfully"}), 200
    except Exception as e:
        return jsonify({"message": "Error logging out: " + str(e)}), 500