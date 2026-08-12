"""
=========================================================
OmniMind AI Assistant
Cleanup Logs Script
=========================================================

Features
--------
✓ Remove old log files
✓ Archive logs before deletion
✓ Clean temporary files
✓ Clean cache folders
✓ Cleanup statistics

Usage:
    python scripts/cleanup_logs.py
"""

from pathlib import Path
from datetime import datetime, timedelta
import shutil
import zipfile

# ==========================================================
# CONFIGURATION
# ==========================================================

LOG_DIR = Path("logs")
TEMP_DIR = Path("uploads/temp")
CACHE_DIR = Path("__pycache__")
ARCHIVE_DIR = Path("archives")

LOG_RETENTION_DAYS = 30

ARCHIVE_LOGS = True


# ==========================================================
# CREATE ARCHIVE DIRECTORY
# ==========================================================

def create_archive_directory():

    ARCHIVE_DIR.mkdir(

        parents=True,

        exist_ok=True

    )


# ==========================================================
# ARCHIVE LOG FILE
# ==========================================================

def archive_log(log_file):

    timestamp = datetime.now().strftime(

        "%Y%m%d_%H%M%S"

    )

    archive_name = (

        ARCHIVE_DIR /

        f"{log_file.stem}_{timestamp}.zip"

    )

    with zipfile.ZipFile(

        archive_name,

        "w",

        compression=zipfile.ZIP_DEFLATED

    ) as archive:

        archive.write(

            log_file,

            arcname=log_file.name

        )

    return archive_name


# ==========================================================
# CLEAN OLD LOGS
# ==========================================================

def cleanup_logs():

    deleted = 0

    archived = 0

    if not LOG_DIR.exists():

        return deleted, archived

    cutoff = datetime.now() - timedelta(

        days=LOG_RETENTION_DAYS

    )

    for log in LOG_DIR.glob("*.log"):

        modified = datetime.fromtimestamp(

            log.stat().st_mtime

        )

        if modified < cutoff:

            if ARCHIVE_LOGS:

                archive_log(log)

                archived += 1

            log.unlink()

            deleted += 1

    return deleted, archived


# ==========================================================
# CLEAN TEMP DIRECTORY
# ==========================================================

def cleanup_temp():

    removed = 0

    if not TEMP_DIR.exists():

        return removed

    for item in TEMP_DIR.iterdir():

        if item.is_file():

            item.unlink()

            removed += 1

        elif item.is_dir():

            shutil.rmtree(item)

            removed += 1

    return removed


# ==========================================================
# CLEAN CACHE
# ==========================================================

def cleanup_cache():

    removed = 0

    for cache in Path(".").rglob("__pycache__"):

        shutil.rmtree(cache)

        removed += 1

    return removed


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("=" * 60)

    print("OmniMind Cleanup Utility")

    print("=" * 60)

    create_archive_directory()

    logs_deleted, logs_archived = cleanup_logs()

    temp_removed = cleanup_temp()

    cache_removed = cleanup_cache()

    print("\nCleanup Summary")

    print("-" * 40)

    print(f"Archived Logs : {logs_archived}")

    print(f"Deleted Logs  : {logs_deleted}")

    print(f"Temp Removed  : {temp_removed}")

    print(f"Cache Removed : {cache_removed}")

    print("\nCleanup completed successfully.")


if __name__ == "__main__":

    main()