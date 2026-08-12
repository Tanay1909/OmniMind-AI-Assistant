"""
=========================================================
OmniMind AI Assistant
Helper Utilities
=========================================================

Generic helper functions used throughout the application.
"""

from __future__ import annotations

import json
import time
import uuid
from functools import wraps
from pathlib import Path
from typing import Any, Callable, Iterable

# =========================================================
# UUID
# =========================================================


def generate_uuid() -> str:
    """
    Generate a random UUID.

    Returns
    -------
    str
    """
    return str(uuid.uuid4())


# =========================================================
# SAFE EXECUTION
# =========================================================


def safe_execute(
    func: Callable,
    *args,
    default: Any = None,
    **kwargs,
) -> Any:
    """
    Execute a function safely.

    Returns default value if execution fails.
    """
    try:
        return func(*args, **kwargs)
    except Exception:
        return default


# =========================================================
# FLATTEN LIST
# =========================================================


def flatten(items: Iterable) -> list:
    """
    Flatten nested lists.

    Example
    -------
    [[1,2],[3,4]]
        ->
    [1,2,3,4]
    """
    result = []

    for item in items:

        if isinstance(item, (list, tuple, set)):

            result.extend(flatten(item))

        else:

            result.append(item)

    return result


# =========================================================
# CHUNK LIST
# =========================================================


def chunk_list(
    items: list,
    chunk_size: int,
) -> list[list]:
    """
    Split list into chunks.
    """

    if chunk_size <= 0:

        raise ValueError("chunk_size must be greater than zero.")

    return [
        items[i : i + chunk_size]
        for i in range(
            0,
            len(items),
            chunk_size,
        )
    ]


# =========================================================
# DICTIONARY MERGE
# =========================================================


def merge_dicts(
    *dictionaries: dict,
) -> dict:
    """
    Merge multiple dictionaries.
    """

    merged = {}

    for dictionary in dictionaries:

        merged.update(dictionary)

    return merged


# =========================================================
# REMOVE NONE VALUES
# =========================================================


def remove_none(data: dict) -> dict:
    """
    Remove None values from dictionary.
    """

    return {key: value for key, value in data.items() if value is not None}


# =========================================================
# JSON SERIALIZATION
# =========================================================


def to_json(
    obj: Any,
    indent: int = 4,
) -> str:
    """
    Convert object to JSON string.
    """

    return json.dumps(
        obj,
        indent=indent,
        default=str,
        ensure_ascii=False,
    )


# =========================================================
# LOAD JSON
# =========================================================


def from_json(
    text: str,
) -> Any:
    """
    Parse JSON string.
    """

    return json.loads(text)


# =========================================================
# TIMER DECORATOR
# =========================================================


def timer(func: Callable):
    """
    Measure execution time.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):

        start = time.perf_counter()

        result = func(
            *args,
            **kwargs,
        )

        end = time.perf_counter()

        print(f"{func.__name__} executed in " f"{end-start:.4f} seconds")

        return result

    return wrapper


# =========================================================
# FILE SIZE
# =========================================================


def file_size(path: str | Path) -> int:
    """
    Return file size in bytes.
    """

    return Path(path).stat().st_size


# =========================================================
# PATH EXISTS
# =========================================================


def path_exists(path: str | Path) -> bool:
    """
    Check whether a path exists.
    """

    return Path(path).exists()


# =========================================================
# ENSURE DIRECTORY
# =========================================================


def ensure_directory(
    directory: str | Path,
) -> Path:
    """
    Create directory if it does not exist.
    """

    directory = Path(directory)

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return directory


# =========================================================
# UNIQUE ITEMS
# =========================================================


def unique(items: Iterable) -> list:
    """
    Remove duplicates while preserving order.
    """

    seen = set()

    output = []

    for item in items:

        if item not in seen:

            seen.add(item)

            output.append(item)

    return output


# =========================================================
# CLAMP VALUE
# =========================================================


def clamp(
    value: float,
    minimum: float,
    maximum: float,
) -> float:
    """
    Clamp numeric value.
    """

    return max(
        minimum,
        min(
            value,
            maximum,
        ),
    )


# =========================================================
# IS EMPTY
# =========================================================


def is_empty(value: Any) -> bool:
    """
    Check whether value is empty.
    """

    return value is None or value == ""


# =========================================================
# DEFAULT VALUE
# =========================================================


def default_if_none(
    value: Any,
    default: Any,
) -> Any:
    """
    Replace None with default.
    """

    return default if value is None else value
