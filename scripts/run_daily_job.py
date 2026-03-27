"""
Deployment-friendly daily job entrypoint.
"""
from jobs.daily_jobs import run_daily_jobs


if __name__ == "__main__":
    run_daily_jobs()

