"""
Initializes the Flask application and registers the blueprints.
"""
import os

from flask import Flask

from app.routes.api import api_bp
from app.routes.auth import auth_bp
from app.routes.dashboard import dashboard_bp
from app.routes.db_migration import db_migration_bp
from app.routes.user_activity import user_activity_bp

from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "dev-secret-change-in-production")

    CORS(
        app,
        origins=["https://sbi.vercel.app"],
        supports_credentials=True,  # needed if you use sessions/cookies
    )

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_activity_bp)
    app.register_blueprint(db_migration_bp)
    return app