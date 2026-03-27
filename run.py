"""
Runs the Flask application/starts the server
"""
import os
from app import create_app

app = create_app()

def run_web() -> None:
    host = os.getenv("FLASK_RUN_HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "False").strip().lower() in {"true", "1", "yes", "y"}
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    run_web()