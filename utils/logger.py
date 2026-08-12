"""
=========================================================
OmniMind AI Assistant
Logger Utilities
=========================================================

Centralized logging configuration.
"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# =========================================================
# CONFIGURATION
# =========================================================

LOG_DIRECTORY = Path("logs")
LOG_DIRECTORY.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIRECTORY / "omnimind.log"

LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | "
    "%(name)s | %(filename)s:%(lineno)d | %(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# =========================================================
# LOGGER FACTORY
# =========================================================


def get_logger(
    name: str,
    level: int = logging.INFO,
) -> logging.Logger:
    """
    Create or retrieve a configured logger.
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(level)

    formatter = logging.Formatter(
        LOG_FORMAT,
        DATE_FORMAT,
    )

    # -------------------------------
    # Console Handler
    # -------------------------------

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    # -------------------------------
    # Rotating File Handler
    # -------------------------------

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    logger.propagate = False

    return logger


# =========================================================
# ROOT LOGGER
# =========================================================

logger = get_logger("OmniMind")


# =========================================================
# LOG FUNCTIONS
# =========================================================


def debug(message: str):
    logger.debug(message)


def info(message: str):
    logger.info(message)


def warning(message: str):
    logger.warning(message)


def error(message: str):
    logger.error(message)


def critical(message: str):
    logger.critical(message)


def exception(message: str):
    """
    Log exception with traceback.
    """

    logger.exception(message)


# =========================================================
# CHANGE LOG LEVEL
# =========================================================


def set_log_level(level: int):
    """
    Update logger level.
    """

    logger.setLevel(level)

    for handler in logger.handlers:
        handler.setLevel(level)


# =========================================================
# LOG SEPARATOR
# =========================================================


def separator(
    character: str = "=",
    length: int = 70,
):
    """
    Print separator into log.
    """

    logger.info(character * length)


# =========================================================
# APPLICATION START
# =========================================================


def log_startup():
    """
    Startup log.
    """

    separator()

    logger.info("OmniMind AI Assistant Started")

    separator()


# =========================================================
# APPLICATION SHUTDOWN
# =========================================================


def log_shutdown():
    """
    Shutdown log.
    """

    separator()

    logger.info("OmniMind AI Assistant Stopped")

    separator()
