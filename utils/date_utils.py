"""
=========================================================
OmniMind AI Assistant
Date Utilities
=========================================================

Reusable date and time helper functions.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

# =========================================================
# CURRENT DATETIME
# =========================================================


def current_datetime() -> datetime:
    """
    Return current UTC datetime.
    """
    return datetime.now(timezone.utc)


# =========================================================
# CURRENT TIMESTAMP
# =========================================================


def current_timestamp() -> int:
    """
    Return current Unix timestamp.
    """
    return int(current_datetime().timestamp())


# =========================================================
# ISO FORMAT
# =========================================================


def iso_now() -> str:
    """
    Return ISO-8601 datetime.
    """
    return current_datetime().isoformat()


# =========================================================
# FORMAT DATETIME
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
# PARSE DATETIME
# =========================================================


def parse_datetime(
    value: str,
    pattern: str = "%Y-%m-%d %H:%M:%S",
) -> datetime:
    """
    Parse datetime string.
    """
    return datetime.strptime(value, pattern)


# =========================================================
# TODAY
# =========================================================


def today():
    """
    Return today's date.
    """
    return current_datetime().date()


# =========================================================
# YESTERDAY
# =========================================================


def yesterday():
    """
    Return yesterday's date.
    """
    return today() - timedelta(days=1)


# =========================================================
# TOMORROW
# =========================================================


def tomorrow():
    """
    Return tomorrow's date.
    """
    return today() + timedelta(days=1)


# =========================================================
# ADD DAYS
# =========================================================


def add_days(
    value: datetime,
    days: int,
) -> datetime:
    """
    Add days.
    """
    return value + timedelta(days=days)


# =========================================================
# ADD HOURS
# =========================================================


def add_hours(
    value: datetime,
    hours: int,
) -> datetime:
    """
    Add hours.
    """
    return value + timedelta(hours=hours)


# =========================================================
# DIFFERENCE
# =========================================================


def difference(
    start: datetime,
    end: datetime,
) -> timedelta:
    """
    Return time difference.
    """
    return end - start


# =========================================================
# AGE IN DAYS
# =========================================================


def days_between(
    start: datetime,
    end: datetime,
) -> int:
    """
    Days between two dates.
    """
    return abs((end - start).days)


# =========================================================
# RELATIVE TIME
# =========================================================


def relative_time(value: datetime) -> str:
    """
    Human-readable relative time.
    """

    delta = current_datetime() - value

    seconds = int(delta.total_seconds())

    if seconds < 60:
        return f"{seconds} seconds ago"

    minutes = seconds // 60

    if minutes < 60:
        return f"{minutes} minutes ago"

    hours = minutes // 60

    if hours < 24:
        return f"{hours} hours ago"

    days = hours // 24

    if days < 30:
        return f"{days} days ago"

    months = days // 30

    if months < 12:
        return f"{months} months ago"

    years = months // 12

    return f"{years} years ago"


# =========================================================
# START OF DAY
# =========================================================


def start_of_day(
    value: datetime,
) -> datetime:
    """
    Beginning of day.
    """

    return value.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )


# =========================================================
# END OF DAY
# =========================================================


def end_of_day(
    value: datetime,
) -> datetime:
    """
    End of day.
    """

    return value.replace(
        hour=23,
        minute=59,
        second=59,
        microsecond=999999,
    )


# =========================================================
# IS TODAY
# =========================================================


def is_today(
    value: datetime,
) -> bool:
    """
    Check whether date is today.
    """

    return value.date() == today()


# =========================================================
# IS WEEKEND
# =========================================================


def is_weekend(
    value: datetime,
) -> bool:
    """
    Check weekend.
    """

    return value.weekday() >= 5
