"""
=========================================================
OmniMind AI Assistant
Pytest Configuration
=========================================================

Shared fixtures used across the entire test suite.
"""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

import pytest

# ==========================================================
# TEMP DIRECTORY
# ==========================================================


@pytest.fixture(scope="session")
def temp_directory():
    """
    Create a temporary directory for tests.
    """

    directory = Path(tempfile.mkdtemp())

    yield directory

    shutil.rmtree(directory, ignore_errors=True)


# ==========================================================
# SAMPLE TEXT
# ==========================================================


@pytest.fixture
def sample_text():
    """
    Sample text fixture.
    """

    return "Artificial Intelligence is transforming " "software development."


# ==========================================================
# SAMPLE DOCUMENT
# ==========================================================


@pytest.fixture
def sample_document():
    """
    Sample document fixture.
    """

    return {
        "title": "AI Research",
        "author": "OpenAI",
        "pages": 12,
        "language": "English",
    }


# ==========================================================
# SAMPLE USER
# ==========================================================


@pytest.fixture
def sample_user():
    """
    Sample user data.
    """

    return {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "role": "admin",
    }


# ==========================================================
# SAMPLE CHAT HISTORY
# ==========================================================


@pytest.fixture
def sample_chat_history():
    """
    Example conversation.
    """

    return [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi! How can I help you?"},
    ]


# ==========================================================
# SAMPLE CONFIG
# ==========================================================


@pytest.fixture
def sample_config():
    """
    Sample configuration.
    """

    return {
        "temperature": 0.7,
        "max_tokens": 1024,
        "stream": False,
    }


# ==========================================================
# SAMPLE FILE
# ==========================================================


@pytest.fixture
def sample_file(temp_directory):
    """
    Create a sample text file.
    """

    path = temp_directory / "sample.txt"

    path.write_text(
        "This is a sample file.",
        encoding="utf-8",
    )

    return path


# ==========================================================
# SAMPLE JSON
# ==========================================================


@pytest.fixture
def sample_json():
    """
    Example JSON object.
    """

    return {
        "name": "OmniMind",
        "version": "1.0.0",
        "status": "active",
    }


# ==========================================================
# SAMPLE IMAGE PATH
# ==========================================================


@pytest.fixture
def sample_image(temp_directory):
    """
    Empty placeholder image.
    """

    image = temp_directory / "image.png"

    image.touch()

    return image


# ==========================================================
# SAMPLE AUDIO PATH
# ==========================================================


@pytest.fixture
def sample_audio(temp_directory):
    """
    Empty placeholder audio.
    """

    audio = temp_directory / "audio.wav"

    audio.touch()

    return audio


# ==========================================================
# SAMPLE PDF PATH
# ==========================================================


@pytest.fixture
def sample_pdf(temp_directory):
    """
    Empty placeholder PDF.
    """

    pdf = temp_directory / "sample.pdf"

    pdf.touch()

    return pdf


# ==========================================================
# RANDOM TEXT
# ==========================================================


@pytest.fixture
def random_text():
    """
    Random reusable string.
    """

    return "Lorem ipsum dolor sit amet, " "consectetur adipiscing elit."


# ==========================================================
# API RESPONSE
# ==========================================================


@pytest.fixture
def api_success_response():
    """
    Mock successful API response.
    """

    return {
        "success": True,
        "status": 200,
        "message": "Success",
        "data": {},
    }


# ==========================================================
# API ERROR RESPONSE
# ==========================================================


@pytest.fixture
def api_error_response():
    """
    Mock error response.
    """

    return {
        "success": False,
        "status": 500,
        "message": "Internal Server Error",
    }
