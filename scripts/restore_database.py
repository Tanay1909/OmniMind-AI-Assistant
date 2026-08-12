"""
=========================================================
OmniMind AI Assistant
Database Restore Script
=========================================================

Restores the SQLite database from a backup.

Features
--------
✓ Supports .db backups
✓ Supports .zip backups
✓ Creates safety backup before restore
✓ Backup verification
✓ Rollback on failure

Usage:
    python scripts/restore_database.py
"""

from pathlib import Path
from datetime import datetime
import shutil
import sqlite3
import tempfile
import zipfile

# ==========================================================
# CONFIGURATION
# ==========================================================

DATABASE = Path("database/database.db")

BACKUP_DIR = Path("backups")

TEMP_DIR = Path("temp_restore")


# ==========================================================
# CREATE SAFETY BACKUP
# ==========================================================

def create_safety_backup():

    if not DATABASE.exists():

        return None

    BACKUP_DIR.mkdir(

        exist_ok=True

    )

    timestamp = datetime.now().strftime(

        "%Y%m%d_%H%M%S"

    )

    safety_backup = (

        BACKUP_DIR /

        f"safety_backup_{timestamp}.db"

    )

    shutil.copy2(

        DATABASE,

        safety_backup

    )

    print(

        f"Safety backup created: {safety_backup.name}"

    )

    return safety_backup


# ==========================================================
# VERIFY DATABASE
# ==========================================================

def verify_database(file_path):

    try:

        connection = sqlite3.connect(file_path)

        connection.execute(

            "PRAGMA integrity_check"

        )

        connection.close()

        return True

    except Exception:

        return False


# ==========================================================
# EXTRACT ZIP
# ==========================================================

def extract_zip(zip_file):

    TEMP_DIR.mkdir(

        exist_ok=True

    )

    with zipfile.ZipFile(

        zip_file,

        "r"

    ) as archive:

        archive.extractall(

            TEMP_DIR

        )

    db_files = list(

        TEMP_DIR.glob("*.db")

    )

    if not db_files:

        raise FileNotFoundError(

            "No database found inside ZIP."

        )

    return db_files[0]


# ==========================================================
# RESTORE
# ==========================================================

def restore_database(backup_file):

    source = backup_file

    if backup_file.suffix == ".zip":

        source = extract_zip(

            backup_file

        )

    if not verify_database(source):

        raise ValueError(

            "Backup integrity verification failed."

        )

    shutil.copy2(

        source,

        DATABASE

    )


# ==========================================================
# CLEAN TEMP FILES
# ==========================================================

def cleanup():

    if TEMP_DIR.exists():

        shutil.rmtree(

            TEMP_DIR

        )


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("=" * 60)

    print("OmniMind Database Restore")

    print("=" * 60)

    backups = sorted(

        BACKUP_DIR.glob("*")

    )

    if not backups:

        print(

            "No backups found."

        )

        return

    print("\nAvailable Backups:\n")

    for index, backup in enumerate(backups, start=1):

        print(

            f"{index}. {backup.name}"

        )

    choice = int(

        input(

            "\nSelect backup number: "

        )

    )

    selected = backups[choice - 1]

    safety_backup = create_safety_backup()

    try:

        restore_database(

            selected

        )

        print(

            "\nDatabase restored successfully."

        )

    except Exception as error:

        print(

            f"\nRestore failed: {error}"

        )

        if safety_backup:

            shutil.copy2(

                safety_backup,

                DATABASE

            )

            print(

                "Rollback completed."

            )

    finally:

        cleanup()


if __name__ == "__main__":

    main()