"""
=========================================================
OmniMind AI Assistant
File Utilities
=========================================================

Reusable file and directory helper functions.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from typing import Any

# =========================================================
# PATH
# =========================================================


def to_path(path: str | Path) -> Path:
    """
    Convert string to Path object.
    """
    return Path(path)


# =========================================================
# EXISTS
# =========================================================


def file_exists(path: str | Path) -> bool:
    """
    Check whether a file exists.
    """
    return to_path(path).is_file()


def directory_exists(path: str | Path) -> bool:
    """
    Check whether a directory exists.
    """
    return to_path(path).is_dir()


# =========================================================
# CREATE DIRECTORY
# =========================================================


def ensure_directory(path: str | Path) -> Path:
    """
    Create directory if it doesn't exist.
    """
    directory = to_path(path)

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return directory


# =========================================================
# FILE SIZE
# =========================================================


def file_size(path: str | Path) -> int:
    """
    Return file size in bytes.
    """
    return to_path(path).stat().st_size


# =========================================================
# READ TEXT
# =========================================================


def read_text(
    path: str | Path,
    encoding: str = "utf-8",
) -> str:
    """
    Read text file.
    """
    return to_path(path).read_text(
        encoding=encoding,
    )


# =========================================================
# WRITE TEXT
# =========================================================


def write_text(
    path: str | Path,
    content: str,
    encoding: str = "utf-8",
) -> Path:
    """
    Write text file.
    """
    file = to_path(path)

    ensure_directory(file.parent)

    file.write_text(
        content,
        encoding=encoding,
    )

    return file


# =========================================================
# JSON
# =========================================================


def read_json(path: str | Path) -> Any:
    """
    Read JSON file.
    """
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def write_json(
    path: str | Path,
    data: Any,
) -> Path:
    """
    Write JSON file.
    """
    file = to_path(path)

    ensure_directory(file.parent)

    with open(file, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False,
        )

    return file


# =========================================================
# COPY
# =========================================================


def copy_file(
    source: str | Path,
    destination: str | Path,
) -> Path:
    """
    Copy file.
    """
    destination = to_path(destination)

    ensure_directory(destination.parent)

    shutil.copy2(
        source,
        destination,
    )

    return destination


# =========================================================
# MOVE
# =========================================================


def move_file(
    source: str | Path,
    destination: str | Path,
) -> Path:
    """
    Move file.
    """
    destination = to_path(destination)

    ensure_directory(destination.parent)

    shutil.move(
        source,
        destination,
    )

    return destination


# =========================================================
# DELETE
# =========================================================


def delete_file(path: str | Path) -> bool:
    """
    Delete file if it exists.
    """
    file = to_path(path)

    if file.exists():
        file.unlink()
        return True

    return False


# =========================================================
# HASH
# =========================================================


def file_hash(
    path: str | Path,
    algorithm: str = "sha256",
) -> str:
    """
    Calculate file hash.
    """
    hasher = hashlib.new(algorithm)

    with open(path, "rb") as file:
        while chunk := file.read(8192):
            hasher.update(chunk)

    return hasher.hexdigest()


# =========================================================
# EXTENSION
# =========================================================


def extension(path: str | Path) -> str:
    """
    Return file extension.
    """
    return to_path(path).suffix.lower()


# =========================================================
# STEM
# =========================================================


def filename(path: str | Path) -> str:
    """
    Return filename without extension.
    """
    return to_path(path).stem


# =========================================================
# LIST FILES
# =========================================================


def list_files(
    directory: str | Path,
    pattern: str = "*",
) -> list[Path]:
    """
    List files matching a pattern.
    """
    directory = to_path(directory)

    if not directory.exists():
        return []

    return sorted(directory.glob(pattern))


# =========================================================
# CLEAR DIRECTORY
# =========================================================


def clear_directory(
    directory: str | Path,
) -> None:
    """
    Delete all files inside a directory.
    """
    directory = to_path(directory)

    if not directory.exists():
        return

    for item in directory.iterdir():

        if item.is_file():
            item.unlink()

        elif item.is_dir():
            shutil.rmtree(item)


# =========================================================
# METADATA
# =========================================================


def metadata(
    path: str | Path,
) -> dict:
    """
    Return file metadata.
    """
    file = to_path(path)

    stat = file.stat()

    return {
        "name": file.name,
        "stem": file.stem,
        "suffix": file.suffix,
        "size": stat.st_size,
        "created": stat.st_ctime,
        "modified": stat.st_mtime,
        "absolute_path": str(file.resolve()),
    }
