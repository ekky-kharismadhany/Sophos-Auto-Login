import logging

import httpx

log = logging.getLogger(__name__)


def check_connectivity(url: str, timeout: int = 10) -> bool:
    """Check internet connectivity by making an HTTP GET request.

    Returns True if internet is reachable, False if blocked (e.g. by Sophos).
    """
    try:
        resp = httpx.get(url, timeout=timeout, follow_redirects=False)
        if resp.status_code in (200, 204):
            log.debug("Connectivity check passed (status %d)", resp.status_code)
            return True
        log.debug(
            "Connectivity check failed: unexpected status %d", resp.status_code
        )
        return False
    except Exception as exc:
        log.debug("Connectivity check failed: %s", exc)
        return False
