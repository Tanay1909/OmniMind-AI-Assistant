"""
=========================================================
OmniMind AI Assistant
Database Migration Manager
=========================================================

Handles database initialization, reset,
schema inspection and migration utilities.
"""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

from sqlalchemy import inspect

from database.db import DATABASE_FILE
from database.db import Base
from database.db import db


class MigrationManager:
    """
    Database migration manager.
    """

    def __init__(self):

        self.engine = db.engine

    # =====================================================
    # DATABASE
    # =====================================================

    def initialize(self) -> None:
        """
        Create all database tables.
        """

        Base.metadata.create_all(bind=self.engine)

    def drop_all(self) -> None:
        """
        Remove every table.
        """

        Base.metadata.drop_all(bind=self.engine)

    def reset(self) -> None:
        """
        Drop and recreate the schema.
        """

        self.drop_all()

        self.initialize()

    # =====================================================
    # INSPECTION
    # =====================================================

    def table_exists(
        self,
        table_name: str,
    ) -> bool:

        inspector = inspect(self.engine)

        return table_name in inspector.get_table_names()

    def list_tables(self) -> list[str]:

        inspector = inspect(self.engine)

        return inspector.get_table_names()

    def database_exists(self) -> bool:

        return DATABASE_FILE.exists()

    # =====================================================
    # BACKUP
    # =====================================================

    def backup(
        self,
        destination: str | Path,
    ) -> Path:
        """
        Backup SQLite database.
        """

        destination = Path(destination)

        destination.mkdir(
            parents=True,
            exist_ok=True,
        )

        filename = f"backup_" f"{datetime.now():%Y%m%d_%H%M%S}.db"

        backup_path = destination / filename

        shutil.copy2(
            DATABASE_FILE,
            backup_path,
        )

        return backup_path

    def restore(
        self,
        backup_file: str | Path,
    ) -> None:
        """
        Restore SQLite database.
        """

        backup_file = Path(backup_file)

        if not backup_file.exists():

            raise FileNotFoundError(backup_file)

        shutil.copy2(
            backup_file,
            DATABASE_FILE,
        )

    # =====================================================
    # INFORMATION
    # =====================================================

    def summary(self) -> dict:

        return {
            "database_exists": self.database_exists(),
            "tables": self.list_tables(),
            "table_count": len(self.list_tables()),
            "database_path": str(DATABASE_FILE),
        }


migration = MigrationManager()


if __name__ == "__main__":

    migration.initialize()

    print("Database initialized.")

    print(migration.summary())
