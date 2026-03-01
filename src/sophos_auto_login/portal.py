import logging
from pathlib import Path

from sophos_auto_login.config import Config

log = logging.getLogger(__name__)


def perform_login(config: Config) -> bool:
    """Load the recorded login script, substitute credentials, and execute it.

    Returns True on success, False on failure.
    """
    script_file = Path(config.script_path)

    if not script_file.exists():
        log.error(
            "Recorded script not found at '%s'. "
            "Run 'python -m sophos_auto_login record' first to record your login steps.",
            script_file,
        )
        return False

    log.info("Loading recorded script from %s", script_file)
    script_text = script_file.read_text()

    # Substitute placeholders with real credentials
    script_text = script_text.replace("__USERNAME__", config.username)
    script_text = script_text.replace("__PASSWORD__", config.password)

    # Run headless during automated execution
    script_text = script_text.replace("headless=False", "headless=True")

    try:
        namespace: dict = {}
        exec(compile(script_text, str(script_file), "exec"), namespace)

        # Playwright codegen generates a run(playwright) function + a __main__ block
        # that calls sync_playwright. The exec above runs the entire script including
        # the __main__ block, which performs the login.
        log.info("Login script executed successfully.")
        return True
    except Exception:
        log.exception("Login script execution failed.")
        return False
