"""
=========================================================
OmniMind AI Assistant
Formatting Utilities
=========================================================

Reusable formatting helper functions.
"""

from __future__ import annotations

from datetime import datetime, timedelta

# =========================================================
# FILE SIZE
# =========================================================


def format_bytes(size: int) -> str:
    """
    Convert bytes into human-readable format.
    """

    units = ["B", "KB", "MB", "GB", "TB"]

    value = float(size)

    for unit in units:

        if value < 1024 or unit == units[-1]:
            return f"{value:.2f} {unit}"

        value /= 1024


# =========================================================
# DURATION
# =========================================================


def format_duration(seconds: float) -> str:
    """
    Format seconds into HH:MM:SS.
    """

    seconds = int(seconds)

    hours = seconds // 3600

    minutes = (seconds % 3600) // 60

    secs = seconds % 60

    return f"{hours:02}:{minutes:02}:{secs:02}"


# =========================================================
# HUMAN DURATION
# =========================================================


def human_duration(seconds: int) -> str:
    """
    Human-readable duration.
    """

    delta = timedelta(seconds=seconds)

    days = delta.days

    hours, remainder = divmod(delta.seconds, 3600)

    minutes, secs = divmod(remainder, 60)

    parts = []

    if days:
        parts.append(f"{days}d")

    if hours:
        parts.append(f"{hours}h")

    if minutes:
        parts.append(f"{minutes}m")

    if secs or not parts:
        parts.append(f"{secs}s")

    return " ".join(parts)


# =========================================================
# PERCENTAGE
# =========================================================


def format_percentage(
    value: float,
    decimals: int = 2,
) -> str:
    """
    Format percentage.
    """

    return f"{value:.{decimals}f}%"


# =========================================================
# NUMBER
# =========================================================


def format_number(
    value: float,
    decimals: int = 2,
) -> str:
    """
    Format numeric value.
    """

    return f"{value:,.{decimals}f}"


# =========================================================
# INTEGER
# =========================================================


def format_integer(value: int) -> str:
    """
    Format integer with commas.
    """

    return f"{value:,}"


# =========================================================
# CURRENCY
# =========================================================


def format_currency(
    amount: float,
    symbol: str = "$",
    decimals: int = 2,
) -> str:
    """
    Format currency.
    """

    return f"{symbol}{amount:,.{decimals}f}"


# =========================================================
# DATETIME
# =========================================================


def format_datetime(
    value: datetime,
    pattern: str = "%Y-%m-%d %H:%M:%S",
) -> str:
    """
    Format datetime.
    """

    return value.strftime(pattern)


# =========================================================
# DATE
# =========================================================


def format_date(
    value: datetime,
    pattern: str = "%Y-%m-%d",
) -> str:
    """
    Format date.
    """

    return value.strftime(pattern)


# =========================================================
# TIME
# =========================================================


def format_time(
    value: datetime,
    pattern: str = "%H:%M:%S",
) -> str:
    """
    Format time.
    """

    return value.strftime(pattern)


# =========================================================
# ORDINAL
# =========================================================


def ordinal(number: int) -> str:
    """
    Convert integer to ordinal.

    Example:
    1 -> 1st
    """

    if 10 <= number % 100 <= 20:
        suffix = "th"

    else:

        suffix = {
            1: "st",
            2: "nd",
            3: "rd",
        }.get(number % 10, "th")

    return f"{number}{suffix}"


# =========================================================
# ELLIPSIS
# =========================================================


def ellipsis(
    text: str,
    max_length: int = 50,
) -> str:
    """
    Truncate text.
    """

    if len(text) <= max_length:

        return text

    return text[: max_length - 3] + "..."


# =========================================================
# BOOLEAN
# =========================================================


def format_boolean(value: bool) -> str:
    """
    Boolean formatter.
    """

    return "Yes" if value else "No"


# =========================================================
# TITLE CASE
# =========================================================


def title_case(text: str) -> str:
    """
    Convert to title case.
    """

    return text.replace("_", " ").title()


# =========================================================
# SNAKE CASE
# =========================================================


def snake_case(text: str) -> str:
    """
    Convert text to snake_case.
    """

    return "_".join(text.lower().split())


# =========================================================
# KEBAB CASE
# =========================================================


def kebab_case(text: str) -> str:
    """
    Convert text to kebab-case.
    """

    return "-".join(text.lower().split())
