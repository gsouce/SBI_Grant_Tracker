"""
Centralized environment-driven runtime settings.
"""
from dataclasses import dataclass
import os


def _env_bool(name: str, default: bool = False) -> bool:
    raw = (os.getenv(name) or "").strip().lower()
    if not raw:
        return default
    return raw in {"true", "1", "yes", "y", "on"}


def _env_int(name: str, default: int) -> int:
    raw = (os.getenv(name) or "").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


@dataclass(frozen=True)
class RuntimeSettings:
    test_mode: bool
    max_grants_per_run: int
    max_failures: int
    max_rate_limit_retries: int
    retry_sleep_default_seconds: float


def get_runtime_settings() -> RuntimeSettings:
    return RuntimeSettings(
        test_mode=_env_bool("TEST_MODE", False),
        max_grants_per_run=_env_int("MAX_GRANTS_PER_RUN", 300),
        max_failures=_env_int("MAX_FAILURES_PER_RUN", 25),
        max_rate_limit_retries=_env_int("MAX_RATE_LIMIT_RETRIES", 3),
        retry_sleep_default_seconds=float(os.getenv("RETRY_SLEEP_DEFAULT_SECONDS", "10.0")),
    )

