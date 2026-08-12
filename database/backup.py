"""
=========================================================
OmniMind AI Assistant
Database Backup Manager
=========================================================

Handles database backup, restore,
compression, cleanup, and verification.
"""

from __future__ import annotations

import gzip
import shutil
from datetime import datetime
from pathlib import Path

from database.db import DATABASE_FILE


class DatabaseBackupManager:
    """
    Database backup manager.
    """

    def __init__(
        self,
        backup_directory: str | Path = "database/backups",
    ):

        self.backup_dir = Path(backup_directory)

        self.backup_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    # =====================================================
    # BACKUP
    # =====================================================

    def create_backup(
        self,
        compress: bool = False,
    ) -> Path:
        """
        Create database backup.
        """

        if not DATABASE_FILE.exists():

            raise FileNotFoundError("Database not found.")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        backup_file = self.backup_dir / f"omnimind_{timestamp}.db"

        shutil.copy2(
            DATABASE_FILE,
            backup_file,
        )

        if compress:

            compressed = backup_file.with_suffix(".db.gz")

            with (
                open(backup_file, "rb") as source,
                gzip.open(compressed, "wb") as target,
            ):
                shutil.copyfileobj(
                    source,
                    target,
                )

            backup_file.unlink()

            return compressed

        return backup_file

    # =====================================================
    # RESTORE
    # =====================================================

    def restore(
        self,
        backup_file: str | Path,
    ) -> None:
        """
        Restore database.
        """

        backup_file = Path(backup_file)

        if not backup_file.exists():

            raise FileNotFoundError(backup_file)

        if backup_file.suffix == ".gz":

            with gzip.open(
                backup_file,
                "rb",
            ) as source:

                with open(
                    DATABASE_FILE,
                    "wb",
                ) as target:

                    shutil.copyfileobj(
                        source,
                        target,
                    )

        else:

            shutil.copy2(
                backup_file,
                DATABASE_FILE,
            )

    # =====================================================
    # LIST
    # =====================================================

    def list_backups(
        self,
    ) -> list[Path]:
        """
        List available backups.
        """

        backups = []

        backups.extend(self.backup_dir.glob("*.db"))

        backups.extend(self.backup_dir.glob("*.gz"))

        return sorted(
            backups,
            reverse=True,
        )

    # =====================================================
    # DELETE
    # =====================================================

    def delete_backup(
        self,
        backup_file: str | Path,
    ) -> None:
        """
        Delete backup.
        """

        backup_file = Path(backup_file)

        if backup_file.exists():

            backup_file.unlink()

    # =====================================================
    # CLEANUP
    # =====================================================

    def cleanup(
        self,
        keep_last: int = 10,
    ) -> int:
        """
        Keep only newest backups.
        """

        backups = self.list_backups()

        removed = 0

        for backup in backups[keep_last:]:

            backup.unlink()

            removed += 1

        return removed

    # =====================================================
    # VERIFY
    # =====================================================

    def verify(
        self,
        backup_file: str | Path,
    ) -> bool:
        """
        Basic integrity check.
        """

        backup_file = Path(backup_file)

        if not backup_file.exists():
            return False

        return backup_file.stat().st_size > 0

    # =====================================================
    # INFORMATION
    # =====================================================

    def summary(self) -> dict:
        """
        Backup statistics.
        """

        backups = self.list_backups()

        total_size = sum(file.stat().st_size for file in backups)

        return {
            "backup_directory": str(self.backup_dir),
            "backup_count": len(backups),
            "total_size_mb": round(
                total_size / (1024 * 1024),
                2,
            ),
            "latest_backup": str(backups[0]) if backups else None,
        }


backup_manager = DatabaseBackupManager()


if __name__ == "__main__":

    backup = backup_manager.create_backup()

    print("Backup created:", backup)

    print(backup_manager.summary())
