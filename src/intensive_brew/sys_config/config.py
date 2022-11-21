"""System Configuration package."""

import logging as log
import os


def get_logging_level() -> str:
    """Get desired logging level for the project."""
    logging_level = os.environ.get("LOGGING_LEVEL", default="INFO")
    log.debug(f"{logging_level=}")

    return logging_level.upper()
