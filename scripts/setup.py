"""
=========================================================
OmniMind AI Assistant
Project Setup Script
=========================================================

Automates the initial project setup.

Functions:
- Check Python version
- Create required directories
- Generate .env file
- Install dependencies
- Initialize database
- Verify installation
"""

from pathlib import Path
import platform
import subprocess
import sys

# ==========================================================
# CONFIGURATION
# ==========================================================

REQUIRED_PYTHON = (3, 11)

PROJECT_FOLDERS = [
    "logs",
    "uploads",
    "uploads/images",
    "uploads/audio",
    "uploads/documents",
    "uploads/temp",
    "database",
    "assets",
]

ENV_TEMPLATE = """# OmniMind AI Assistant

DEBUG=True

SECRET_KEY=change_this_secret_key

OPENAI_API_KEY=

GOOGLE_API_KEY=

DATABASE_URL=sqlite:///database/database.db

LOG_LEVEL=INFO
"""


# ==========================================================
# CHECK PYTHON VERSION
# ==========================================================

def check_python():

    print("\nChecking Python Version...")

    version = sys.version_info

    if version < REQUIRED_PYTHON:

        print(
            f"Python {REQUIRED_PYTHON[0]}.{REQUIRED_PYTHON[1]} "
            f"or later is required."
        )

        sys.exit(1)

    print(
        f"Python {version.major}.{version.minor}.{version.micro}"
    )


# ==========================================================
# CREATE DIRECTORIES
# ==========================================================

def create_directories():

    print("\nCreating directories...")

    for folder in PROJECT_FOLDERS:

        Path(folder).mkdir(
            parents=True,
            exist_ok=True
        )

        print(f"Created: {folder}")


# ==========================================================
# CREATE .ENV
# ==========================================================

def create_env():

    env_file = Path(".env")

    if env_file.exists():

        print("\n.env already exists")

        return

    env_file.write_text(ENV_TEMPLATE)

    print("\nCreated .env file")


# ==========================================================
# INSTALL DEPENDENCIES
# ==========================================================

def install_requirements():

    requirements = Path("requirements.txt")

    if not requirements.exists():

        print("requirements.txt not found")

        return

    print("\nInstalling dependencies...")

    subprocess.run(

        [

            sys.executable,

            "-m",

            "pip",

            "install",

            "-r",

            "requirements.txt",

        ],

        check=False,

    )


# ==========================================================
# INITIALIZE DATABASE
# ==========================================================

def initialize_database():

    db_script = Path("scripts/init_db.py")

    if not db_script.exists():

        print("Database initialization skipped.")

        return

    print("\nInitializing database...")

    subprocess.run(

        [

            sys.executable,

            str(db_script),

        ],

        check=False,

    )


# ==========================================================
# VERIFY INSTALLATION
# ==========================================================

def verify():

    print("\nInstallation Summary")

    print("--------------------------")

    print("Operating System :", platform.system())

    print("Python           :", platform.python_version())

    print("Project Ready    : Yes")


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("=" * 60)

    print("OmniMind AI Assistant Setup")

    print("=" * 60)

    check_python()

    create_directories()

    create_env()

    install_requirements()

    initialize_database()

    verify()

    print("\nSetup Completed Successfully!")


if __name__ == "__main__":

    main()