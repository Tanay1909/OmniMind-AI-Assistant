"""
=========================================================
OmniMind AI Assistant
Administrator Creation Script
=========================================================

Creates a new administrator account.

Usage:
    python scripts/create_admin.py
"""

from pathlib import Path
import getpass
import hashlib
import re
import sqlite3
import sys

DATABASE = Path("database/database.db")


# ==========================================================
# DATABASE
# ==========================================================

def get_connection():

    if not DATABASE.exists():

        print("Database not found.")

        print("Run:")

        print("python scripts/init_db.py")

        sys.exit(1)

    return sqlite3.connect(DATABASE)


# ==========================================================
# PASSWORD HASH
# ==========================================================

def hash_password(password: str) -> str:

    return hashlib.sha256(

        password.encode()

    ).hexdigest()


# ==========================================================
# EMAIL VALIDATION
# ==========================================================

def valid_email(email: str) -> bool:

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    return re.match(pattern, email) is not None


# ==========================================================
# PASSWORD VALIDATION
# ==========================================================

def valid_password(password: str) -> bool:

    if len(password) < 8:

        return False

    return True


# ==========================================================
# CHECK EXISTING USER
# ==========================================================

def email_exists(cursor, email):

    cursor.execute(

        """

        SELECT id

        FROM users

        WHERE email=?

        """,

        (email,),

    )

    return cursor.fetchone() is not None


# ==========================================================
# CREATE ADMIN
# ==========================================================

def create_admin(cursor):

    print("\nCreate Administrator Account")

    print("-" * 40)

    name = input("Full Name : ").strip()

    email = input("Email     : ").strip()

    if not valid_email(email):

        print("Invalid email address.")

        return

    if email_exists(cursor, email):

        print("Email already exists.")

        return

    password = getpass.getpass(

        "Password  : "

    )

    confirm = getpass.getpass(

        "Confirm   : "

    )

    if password != confirm:

        print("Passwords do not match.")

        return

    if not valid_password(password):

        print(

            "Password must contain "

            "at least 8 characters."

        )

        return

    cursor.execute(

        """

        INSERT INTO users

        (

            full_name,

            email,

            password_hash,

            role,

            is_active

        )

        VALUES

        (

            ?, ?, ?, 'admin', 1

        )

        """,

        (

            name,

            email,

            hash_password(password),

        ),

    )

    print("\nAdministrator created successfully.")


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("=" * 60)

    print("OmniMind Administrator Setup")

    print("=" * 60)

    connection = get_connection()

    cursor = connection.cursor()

    create_admin(cursor)

    connection.commit()

    connection.close()

    print("\nDone.")


if __name__ == "__main__":

    main()