"""
=========================================================
OmniMind AI Assistant
Retry Utilities
=========================================================

Reusable retry decorators with exponential backoff.
"""

from __future__ import annotations

import functools
import random
import time
from collections.abc import Callable
from typing import Any, TypeVar

T = TypeVar("T")


# =========================================================
# RETRY DECORATOR
# =========================================================


def retry(
    exceptions: tuple[type[Exception], ...] = (Exception,),
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    max_delay: float | None = None,
    jitter: bool = True,
):
    """
    Retry decorator with exponential backoff.

    Parameters
    ----------
    exceptions:
        Exception types that trigger retries.
    max_attempts:
        Maximum retry attempts.
    delay:
        Initial delay in seconds.
    backoff:
        Delay multiplier after each retry.
    max_delay:
        Maximum allowed delay.
    jitter:
        Add random jitter to reduce retry storms.
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:

            current_delay = delay
            last_exception = None

            for attempt in range(1, max_attempts + 1):

                try:
                    return func(*args, **kwargs)

                except exceptions as exc:

                    last_exception = exc

                    if attempt == max_attempts:
                        raise

                    wait = current_delay

                    if jitter:
                        wait += random.uniform(0, 0.5)

                    time.sleep(wait)

                    current_delay *= backoff

                    if max_delay is not None:
                        current_delay = min(
                            current_delay,
                            max_delay,
                        )

            raise last_exception

        return wrapper

    return decorator


# =========================================================
# RETRY FUNCTION
# =========================================================


def retry_call(
    function: Callable[..., T],
    *args: Any,
    exceptions: tuple[type[Exception], ...] = (Exception,),
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    max_delay: float | None = None,
    jitter: bool = True,
    **kwargs: Any,
) -> T:
    """
    Retry a callable directly.
    """

    wrapped = retry(
        exceptions=exceptions,
        max_attempts=max_attempts,
        delay=delay,
        backoff=backoff,
        max_delay=max_delay,
        jitter=jitter,
    )(function)

    return wrapped(*args, **kwargs)


# =========================================================
# RETRY FOREVER
# =========================================================


def retry_forever(
    exceptions: tuple[type[Exception], ...] = (Exception,),
    delay: float = 5.0,
):
    """
    Retry indefinitely until success.
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:

            while True:

                try:
                    return func(*args, **kwargs)

                except exceptions:

                    time.sleep(delay)

        return wrapper

    return decorator


# =========================================================
# WAIT UNTIL SUCCESS
# =========================================================


def wait_until_success(
    function: Callable[..., T],
    interval: float = 2.0,
    *args: Any,
    **kwargs: Any,
) -> T:
    """
    Execute until successful.
    """

    while True:

        try:
            return function(*args, **kwargs)

        except Exception:

            time.sleep(interval)


# =========================================================
# SIMPLE RETRY
# =========================================================


def simple_retry(
    function: Callable[..., T],
    attempts: int = 3,
) -> T:
    """
    Simple retry without backoff.
    """

    last_exception = None

    for _ in range(attempts):

        try:
            return function()

        except Exception as exc:

            last_exception = exc

    raise last_exception
