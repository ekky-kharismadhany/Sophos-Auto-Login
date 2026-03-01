from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    portal_url: str
    username: str
    password: str
    run_mode: str = "cron"
    check_interval: int = 60
    connectivity_url: str = "https://www.google.com/generate_204"
    log_level: str = "INFO"
    script_path: str = "./recorded_login.py"

    def __repr__(self) -> str:
        return (
            f"Config(portal_url={self.portal_url!r}, "
            f"username={self.username!r}, "
            f"password='***', "
            f"run_mode={self.run_mode!r}, "
            f"check_interval={self.check_interval}, "
            f"connectivity_url={self.connectivity_url!r}, "
            f"log_level={self.log_level!r}, "
            f"script_path={self.script_path!r})"
        )


def load_config() -> Config:
    """Load configuration from environment variables. Fails fast on missing required vars."""
    missing = []
    portal_url = os.environ.get("SOPHOS_PORTAL_URL", "")
    if not portal_url:
        missing.append("SOPHOS_PORTAL_URL")

    username = os.environ.get("SOPHOS_USERNAME", "")
    if not username:
        missing.append("SOPHOS_USERNAME")

    password = os.environ.get("SOPHOS_PASSWORD", "")
    if not password:
        missing.append("SOPHOS_PASSWORD")

    if missing:
        raise SystemExit(
            f"Missing required environment variables: {', '.join(missing)}\n"
            "Set them in your .env file or export them in your shell."
        )

    run_mode = os.environ.get("SOPHOS_RUN_MODE", "cron").lower()
    if run_mode not in ("cron", "periodic"):
        raise SystemExit(
            f"SOPHOS_RUN_MODE must be 'cron' or 'periodic', got '{run_mode}'"
        )

    try:
        check_interval = int(os.environ.get("SOPHOS_CHECK_INTERVAL", "60"))
    except ValueError:
        raise SystemExit("SOPHOS_CHECK_INTERVAL must be an integer (seconds)")

    return Config(
        portal_url=portal_url,
        username=username,
        password=password,
        run_mode=run_mode,
        check_interval=check_interval,
        connectivity_url=os.environ.get(
            "SOPHOS_CONNECTIVITY_URL", "https://www.google.com/generate_204"
        ),
        log_level=os.environ.get("SOPHOS_LOG_LEVEL", "INFO").upper(),
        script_path=os.environ.get("SOPHOS_SCRIPT_PATH", "./recorded_login.py"),
    )
