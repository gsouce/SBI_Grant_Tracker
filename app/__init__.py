"""
Initializes the Flask application and registers the blueprints.
"""
from flask import Flask
from app.routes.dashboard import dashboard_bp
from app.routes.api import api_bp
from app.routes.user_activity import user_activity_bp
from app.routes.db_migration import db_migration_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(user_activity_bp)
    app.register_blueprint(db_migration_bp)
    return app