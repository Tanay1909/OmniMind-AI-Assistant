"""
=========================================================
OmniMind AI Assistant
Text Utilities
=========================================================

Reusable text processing utilities.
"""

from __future__ import annotations

import re
import string
from collections import Counter
from typing import Iterable

# =========================================================
# CLEAN TEXT
# =========================================================


def clean_text(text: str) -> str:
    """
    Remove extra whitespace and strip text.
    """

    if not text:
        return ""

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================================================
# NORMALIZE TEXT
# =========================================================


def normalize_text(
    text: str,
    lowercase: bool = True,
) -> str:
    """
    Normalize text.
    """

    text = clean_text(text)

    if lowercase:
        text = text.lower()

    return text


# =========================================================
# REMOVE PUNCTUATION
# =========================================================


def remove_punctuation(text: str) -> str:
    """
    Remove punctuation characters.
    """

    return text.translate(
        str.maketrans(
            "",
            "",
            string.punctuation,
        )
    )


# =========================================================
# REMOVE NUMBERS
# =========================================================


def remove_numbers(text: str) -> str:
    """
    Remove digits.
    """

    return re.sub(r"\d+", "", text)


# =========================================================
# WORD COUNT
# =========================================================


def word_count(text: str) -> int:
    """
    Count words.
    """

    return len(clean_text(text).split())


# =========================================================
# CHARACTER COUNT
# =========================================================


def character_count(
    text: str,
    include_spaces: bool = True,
) -> int:
    """
    Count characters.
    """

    if include_spaces:
        return len(text)

    return len(text.replace(" ", ""))


# =========================================================
# SENTENCE SPLIT
# =========================================================


def sentence_split(text: str) -> list[str]:
    """
    Split text into sentences.
    """

    sentences = re.split(
        r"[.!?]+",
        clean_text(text),
    )

    return [sentence.strip() for sentence in sentences if sentence.strip()]


# =========================================================
# TRUNCATE
# =========================================================


def truncate_text(
    text: str,
    max_length: int = 200,
    suffix: str = "...",
) -> str:
    """
    Truncate text.
    """

    if len(text) <= max_length:
        return text

    return text[:max_length].rstrip() + suffix


# =========================================================
# EXTRACT KEYWORDS
# =========================================================

STOPWORDS = {
    "the",
    "is",
    "a",
    "an",
    "of",
    "and",
    "to",
    "for",
    "in",
    "on",
    "at",
    "by",
    "with",
    "from",
    "that",
    "this",
    "it",
    "be",
    "are",
}


def extract_keywords(
    text: str,
    top_n: int = 10,
) -> list[str]:
    """
    Extract frequent keywords.
    """

    words = normalize_text(text)

    words = remove_punctuation(words)

    tokens = [word for word in words.split() if word not in STOPWORDS]

    counts = Counter(tokens)

    return [word for word, _ in counts.most_common(top_n)]


# =========================================================
# TOKEN ESTIMATE
# =========================================================


def estimate_tokens(text: str) -> int:
    """
    Approximate token count.

    ~1 token ≈ 4 characters.
    """

    return max(
        1,
        len(text) // 4,
    )


# =========================================================
# UNIQUE WORDS
# =========================================================


def unique_words(text: str) -> list[str]:
    """
    Return unique words.
    """

    words = normalize_text(text)

    words = remove_punctuation(words)

    return sorted(set(words.split()))


# =========================================================
# FREQUENCY
# =========================================================


def word_frequency(
    text: str,
) -> dict[str, int]:
    """
    Word frequency dictionary.
    """

    words = normalize_text(text)

    words = remove_punctuation(words)

    return dict(Counter(words.split()))


# =========================================================
# CONTAINS
# =========================================================


def contains_any(
    text: str,
    keywords: Iterable[str],
) -> bool:
    """
    Check whether text contains
    any keyword.
    """

    text = normalize_text(text)

    return any(keyword.lower() in text for keyword in keywords)


# =========================================================
# MARKDOWN
# =========================================================


def strip_markdown(
    text: str,
) -> str:
    """
    Remove common markdown syntax.
    """

    text = re.sub(r"`{1,3}.*?`{1,3}", "", text)

    text = re.sub(r"[*_>#-]", "", text)

    text = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", text)

    return clean_text(text)
