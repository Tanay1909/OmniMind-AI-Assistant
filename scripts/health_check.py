"""
=========================================================
OmniMind AI Assistant
System Health Check
=========================================================

Features
--------
✓ Python version verification
✓ Dependency validation
✓ Database connectivity
✓ Environment file validation
✓ Directory verification
✓ Disk space check
✓ Write permission check
✓ Overall system report

Usage:
    python scripts/health_check.py
"""

from pathlib import Path
import shutil
import sqlite3
import sys
import importlib

# ==========================================================
# CONFIGURATION
# ==========================================================

MINIMUM_PYTHON = (3, 11)

DATABASE = Path("database/database.db")

REQUIRED_DIRECTORIES = [

    "logs",

    "uploads",

    "database",

    "assets",

    "config",

    "services",

    "agents",

    "models",

]

REQUIRED_PACKAGES = [

    "streamlit",

    "pandas",

    "numpy",

    "sklearn",

]

CHECKS = []


# ==========================================================
# RESULT
# ==========================================================

def record(name, passed, message):

    CHECKS.append(

        (

            name,

            passed,

            message,

        )

    )


# ==========================================================
# PYTHON
# ==========================================================

def check_python():

    passed = sys.version_info >= MINIMUM_PYTHON

    record(

        "Python Version",

        passed,

        sys.version.split()[0]

    )


# ==========================================================
# DEPENDENCIES
# ==========================================================

def check_packages():

    missing = []

    for package in REQUIRED_PACKAGES:

        try:

            importlib.import_module(

                package

            )

        except ImportError:

            missing.append(package)

    if missing:

        record(

            "Dependencies",

            False,

            "Missing: " + ", ".join(missing)

        )

    else:

        record(

            "Dependencies",

            True,

            "All required packages installed"

        )


# ==========================================================
# DATABASE
# ==========================================================

def check_database():

    if not DATABASE.exists():

        record(

            "Database",

            False,

            "Database file not found"

        )

        return

    try:

        connection = sqlite3.connect(

            DATABASE

        )

        connection.execute(

            "SELECT 1"

        )

        connection.close()

        record(

            "Database",

            True,

            "Connection successful"

        )

    except Exception as error:

        record(

            "Database",

            False,

            str(error)

        )


# ==========================================================
# DIRECTORIES
# ==========================================================

def check_directories():

    missing = []

    for folder in REQUIRED_DIRECTORIES:

        if not Path(folder).exists():

            missing.append(folder)

    if missing:

        record(

            "Directories",

            False,

            ", ".join(missing)

        )

    else:

        record(

            "Directories",

            True,

            "All directories found"

        )


# ==========================================================
# ENVIRONMENT
# ==========================================================

def check_environment():

    env = Path(".env")

    record(

        ".env",

        env.exists(),

        "Present" if env.exists()

        else "Missing"

    )


# ==========================================================
# DISK SPACE
# ==========================================================

def check_disk():

    usage = shutil.disk_usage(".")

    free_gb = usage.free / (1024 ** 3)

    passed = free_gb > 1

    record(

        "Disk Space",

        passed,

        f"{free_gb:.2f} GB free"

    )


# ==========================================================
# WRITE ACCESS
# ==========================================================

def check_permissions():

    test = Path("health_check.tmp")

    try:

        test.write_text("test")

        test.unlink()

        record(

            "Write Permission",

            True,

            "Writable"

        )

    except Exception:

        record(

            "Write Permission",

            False,

            "Cannot write to project directory"

        )


# ==========================================================
# SUMMARY
# ==========================================================

def print_summary():

    print("\n")

    print("=" * 70)

    print("SYSTEM HEALTH REPORT")

    print("=" * 70)

    passed = 0

    failed = 0

    for name, status, message in CHECKS:

        icon = "PASS" if status else "FAIL"

        print(

            f"{icon:5}"

            f"{name:<20}"

            f"{message}"

        )

        if status:

            passed += 1

        else:

            failed += 1

    print("-" * 70)

    print(f"Passed : {passed}")

    print(f"Failed : {failed}")

    print(f"Total  : {passed + failed}")

    print("=" * 70)

    if failed == 0:

        print("Overall Status : HEALTHY")

    else:

        print("Overall Status : ATTENTION REQUIRED")


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("=" * 70)

    print("OmniMind AI Assistant Health Check")

    print("=" * 70)

    check_python()

    check_packages()

    check_database()

    check_directories()

    check_environment()

    check_disk()

    check_permissions()

    print_summary()


if __name__ == "__main__":

    main()