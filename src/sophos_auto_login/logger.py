import logging
import sys


def setup_logging(level: str = "INFO") -> None:
    """Configure stdlib logging to stderr."""
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stderr,
    )
