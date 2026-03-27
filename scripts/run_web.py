"""
Deployment-friendly web entrypoint.
"""
import os
from run import app


if __name__ == "__main__":
    # Keep this script simple; production should prefer gunicorn:
    # gunicorn -w 2 -b 0.0.0.0:$PORT scripts.run_web:app
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)

