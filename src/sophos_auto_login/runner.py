import logging
import time

from sophos_auto_login.config import Config
from sophos_auto_login.connectivity import check_connectivity
from sophos_auto_login.portal import perform_login

log = logging.getLogger(__name__)

POST_LOGIN_WAIT = 3  # seconds to wait before re-checking after login


def _attempt_login(config: Config) -> bool:
    """Attempt login and verify connectivity was restored."""
    log.info("Internet appears blocked. Attempting Sophos portal login...")
    success = perform_login(config)

    if not success:
        log.error("Login script execution failed.")
        return False

    log.info("Waiting %ds before re-checking connectivity...", POST_LOGIN_WAIT)
    time.sleep(POST_LOGIN_WAIT)

    if check_connectivity(config.connectivity_url):
        log.info("Connectivity restored successfully.")
        return True

    log.warning("Login completed but connectivity still not restored.")
    return False


def run(config: Config) -> int:
    """Run the auto-login tool in the configured mode.

    Returns exit code: 0 = ok, 1 = login failed.
    """
    if config.run_mode == "cron":
        return _run_cron(config)
    return _run_periodic(config)


def _run_cron(config: Config) -> int:
    """Single check-and-login cycle for cron mode."""
    if check_connectivity(config.connectivity_url):
        log.info("Internet is reachable. Nothing to do.")
        return 0

    if _attempt_login(config):
        return 0

    return 1


def _run_periodic(config: Config) -> int:
    """Continuous loop for periodic mode."""
    log.info(
        "Starting periodic mode (checking every %ds)...", config.check_interval
    )

    while True:
        try:
            if check_connectivity(config.connectivity_url):
                log.debug("Internet is reachable.")
            else:
                _attempt_login(config)
        except Exception:
            log.exception("Unexpected error in periodic loop (will retry).")

        time.sleep(config.check_interval)
