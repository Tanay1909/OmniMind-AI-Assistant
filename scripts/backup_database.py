"""
=========================================================
OmniMind AI Assistant
Database Backup Script
=========================================================

Creates timestamped backups of the SQLite database.

Features
--------
✓ Timestamped backups
✓ Automatic backup directory creation
✓ Optional ZIP compression
✓ Backup verification
✓ Retention policy

Usage:
    python scripts/backup_database.py
"""

from pathlib import Path
from datetime import datetime
import shutil
import zipfile

# ==========================================================
# CONFIGURATION
# ==========================================================

DATABASE = Path("database/database.db")

BACKUP_DIR = Path("backups")

COMPRESS_BACKUP = True

MAX_BACKUPS = 10


# ==========================================================
# CREATE BACKUP DIRECTORY
# ==========================================================

def create_backup_directory():

    BACKUP_DIR.mkdir(

        parents=True,

        exist_ok=True

    )


# ==========================================================
# BACKUP DATABASE
# ==========================================================

def backup_database():

    if not DATABASE.exists():

        print("Database not found.")

        return None

    timestamp = datetime.now().strftime(

        "%Y%m%d_%H%M%S"

    )

    backup_name = (

        f"database_backup_{timestamp}.db"

    )

    destination = BACKUP_DIR / backup_name

    shutil.copy2(

        DATABASE,

        destination

    )

    print(f"Backup created: {destination.name}")

    return destination


# ==========================================================
# COMPRESS BACKUP
# ==========================================================

def compress_backup(backup_file):

    zip_name = backup_file.with_suffix(".zip")

    with zipfile.ZipFile(

        zip_name,

        "w",

        compression=zipfile.ZIP_DEFLATED

    ) as archive:

        archive.write(

            backup_file,

            arcname=backup_file.name

        )

    backup_file.unlink()

    print(f"Compressed: {zip_name.name}")

    return zip_name


# ==========================================================
# VERIFY BACKUP
# ==========================================================

def verify_backup(file_path):

    if file_path.exists():

        size = file_path.stat().st_size

        print(f"Verified ({size} bytes)")

        return True

    print("Backup verification failed.")

    return False


# ==========================================================
# CLEAN OLD BACKUPS
# ==========================================================

def cleanup_old_backups():

    backups = sorted(

        BACKUP_DIR.glob("*"),

        key=lambda item: item.stat().st_mtime,

        reverse=True

    )

    if len(backups) <= MAX_BACKUPS:

        return

    for backup in backups[MAX_BACKUPS:]:

        print(f"Removing: {backup.name}")

        backup.unlink()


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("=" * 60)

    print("OmniMind Database Backup")

    print("=" * 60)

    create_backup_directory()

    backup = backup_database()

    if backup is None:

        return

    if COMPRESS_BACKUP:

        backup = compress_backup(backup)

    verify_backup(backup)

    cleanup_old_backups()

    print("\nBackup completed successfully.")


if __name__ == "__main__":

    main()