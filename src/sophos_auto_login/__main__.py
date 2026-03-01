import argparse
import os

from dotenv import load_dotenv

from sophos_auto_login.config import load_config
from sophos_auto_login.logger import setup_logging
from sophos_auto_login.recorder import record
from sophos_auto_login.runner import run


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(
        prog="sophos-auto-login",
        description="Automatic re-authentication for Sophos captive portal.",
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("record", help="Record login steps via Playwright codegen")
    sub.add_parser("run", help="Check connectivity and login if needed (default)")

    args = parser.parse_args()
    command = args.command or "run"

    if command == "record":
        portal_url = os.environ.get("SOPHOS_PORTAL_URL", "")
        if not portal_url:
            raise SystemExit(
                "SOPHOS_PORTAL_URL is required for recording. "
                "Set it in .env or export it."
            )
        script_path = os.environ.get("SOPHOS_SCRIPT_PATH", "./recorded_login.py")
        log_level = os.environ.get("SOPHOS_LOG_LEVEL", "INFO").upper()
        setup_logging(log_level)
        record(portal_url, script_path)
    else:
        config = load_config()
        setup_logging(config.log_level)
        raise SystemExit(run(config))


if __name__ == "__main__":
    main()
