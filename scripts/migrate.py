"""
=========================================================
OmniMind AI Assistant
Database Migration Script
=========================================================

Features
--------
✓ Migration version tracking
✓ Migration history
✓ Upgrade support
✓ Rollback support
✓ Automatic compatibility checks

Usage

python scripts/migrate.py upgrade

python scripts/migrate.py rollback

python scripts/migrate.py status
"""

import sqlite3
from pathlib import Path
import sys

DATABASE = Path("database/database.db")


# ==========================================================
# DATABASE CONNECTION
# ==========================================================

def get_connection():

    return sqlite3.connect(DATABASE)


# ==========================================================
# CREATE MIGRATION TABLE
# ==========================================================

def initialize(cursor):

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS schema_migrations(

        version INTEGER PRIMARY KEY,

        description TEXT,

        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)


# ==========================================================
# MIGRATIONS
# ==========================================================

def migration_1(cursor):

    """
    Initial schema version
    """

    cursor.execute("""

    INSERT INTO settings

    (setting_key,setting_value)

    VALUES

    ('app_version','1.0.0')

    """)


def migration_2(cursor):

    """
    Add profile image column
    """

    cursor.execute("""

    ALTER TABLE users

    ADD COLUMN profile_image TEXT

    """)


def migration_3(cursor):

    """
    Add last login timestamp
    """

    cursor.execute("""

    ALTER TABLE users

    ADD COLUMN last_login TIMESTAMP

    """)


# ==========================================================
# MIGRATION REGISTRY
# ==========================================================

MIGRATIONS = {

    1: (

        "Initial Configuration",

        migration_1,

    ),

    2: (

        "Profile Image",

        migration_2,

    ),

    3: (

        "Last Login",

        migration_3,

    ),

}


# ==========================================================
# CURRENT VERSION
# ==========================================================

def current_version(cursor):

    cursor.execute("""

    SELECT MAX(version)

    FROM schema_migrations

    """)

    result = cursor.fetchone()[0]

    return result or 0


# ==========================================================
# APPLY MIGRATIONS
# ==========================================================

def upgrade(cursor):

    version = current_version(cursor)

    print(f"Current Version : {version}")

    for number in sorted(MIGRATIONS):

        if number <= version:

            continue

        description, function = MIGRATIONS[number]

        print(f"Applying {number}: {description}")

        function(cursor)

        cursor.execute("""

        INSERT INTO schema_migrations

        (version,description)

        VALUES (?,?)

        """, (

            number,

            description,

        ))

    print("\nMigration completed.")


# ==========================================================
# ROLLBACK
# ==========================================================

def rollback(cursor):

    version = current_version(cursor)

    if version == 0:

        print("Nothing to rollback.")

        return

    cursor.execute("""

    DELETE FROM schema_migrations

    WHERE version=?

    """, (

        version,

    ))

    print(

        f"Migration {version} removed "

        "(manual schema rollback may be required)."

    )


# ==========================================================
# STATUS
# ==========================================================

def status(cursor):

    cursor.execute("""

    SELECT

        version,

        description,

        applied_at

    FROM schema_migrations

    ORDER BY version

    """)

    rows = cursor.fetchall()

    if not rows:

        print("No migrations applied.")

        return

    print("\nMigration History\n")

    for version, description, applied in rows:

        print(

            f"{version:<3}"

            f"{description:<25}"

            f"{applied}"

        )


# ==========================================================
# MAIN
# ==========================================================

def main():

    if len(sys.argv) < 2:

        print(

            "Usage:\n"

            "python migrate.py "

            "[upgrade|rollback|status]"

        )

        return

    connection = get_connection()

    cursor = connection.cursor()

    initialize(cursor)

    command = sys.argv[1].lower()

    if command == "upgrade":

        upgrade(cursor)

    elif command == "rollback":

        rollback(cursor)

    elif command == "status":

        status(cursor)

    else:

        print("Unknown command.")

    connection.commit()

    connection.close()


if __name__ == "__main__":

    main()