
"""
=========================================================
OmniMind AI Assistant
Logging Configuration
=========================================================
"""

from __future__ import annotations

import logging
import logging.handlers
from pathlib import Path

# ==========================================================
# DIRECTORIES
# ==========================================================

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "omnimind.log"

# ==========================================================
# LOG FORMAT
# ==========================================================

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(name)s | "
    "%(filename)s:%(lineno)d | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# ==========================================================
# LOGGER CONFIGURATION
# ==========================================================

def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """
    Configure the application logger.

    Returns:
        logging.Logger
    """

    logger = logging.getLogger("OmniMind")

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(level)

    formatter = logging.Formatter(
        fmt=LOG_FORMAT,
        datefmt=DATE_FORMAT
    )

    # -------------------------
    # Console Logger
    # -------------------------
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    # -------------------------
    # File Logger
    # -------------------------
    file_handler = logging.handlers.RotatingFileHandler(
        filename=LOG_FILE,
        maxBytes=5 * 1024 * 1024,   # 5 MB
        backupCount=5,
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.propagate = False

    return logger


# ==========================================================
# GLOBAL LOGGER
# ==========================================================

logger = setup_logging()


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def get_logger(name: str) -> logging.Logger:
    """
    Return a child logger.

    Example:
        log = get_logger(__name__)
    """

    return logger.getChild(name)
