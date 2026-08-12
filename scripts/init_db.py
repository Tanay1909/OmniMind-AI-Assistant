"""
=========================================================
OmniMind AI Assistant
Database Initialization Script
=========================================================

Creates the SQLite database and required tables.

Usage:
    python scripts/init_db.py
"""

from pathlib import Path
import sqlite3

# ==========================================================
# CONFIGURATION
# ==========================================================

DATABASE_DIR = Path("database")
DATABASE_FILE = DATABASE_DIR / "database.db"


# ==========================================================
# DATABASE CONNECTION
# ==========================================================

def get_connection():

    DATABASE_DIR.mkdir(exist_ok=True)

    connection = sqlite3.connect(DATABASE_FILE)

    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# ==========================================================
# CREATE TABLES
# ==========================================================

def create_tables(cursor):

    # Users
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        full_name TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password_hash TEXT NOT NULL,

        role TEXT DEFAULT 'user',

        is_active INTEGER DEFAULT 1,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Conversations
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversations (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        title TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
    )
    """)

    # Messages
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        conversation_id INTEGER NOT NULL,

        sender TEXT NOT NULL,

        content TEXT NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(conversation_id)
        REFERENCES conversations(id)
        ON DELETE CASCADE
    )
    """)

    # Documents
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        filename TEXT,

        file_type TEXT,

        file_size INTEGER,

        upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE SET NULL
    )
    """)

    # Images
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS images (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        filename TEXT,

        prompt TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE SET NULL
    )
    """)

    # Audio
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audio (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        filename TEXT,

        transcript TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE SET NULL
    )
    """)

    # Settings
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        setting_key TEXT UNIQUE,

        setting_value TEXT
    )
    """)

    # Activity Logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activity_logs (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        action TEXT,

        ip_address TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE SET NULL
    )
    """)


# ==========================================================
# CREATE INDEXES
# ==========================================================

def create_indexes(cursor):

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_users_email
    ON users(email)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_messages_conversation
    ON messages(conversation_id)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_documents_user
    ON documents(user_id)
    """)

    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_logs_user
    ON activity_logs(user_id)
    """)


# ==========================================================
# DEFAULT SETTINGS
# ==========================================================

def insert_defaults(cursor):

    defaults = [

        ("theme", "light"),

        ("language", "English"),

        ("ai_provider", "OpenAI"),

        ("notifications", "enabled"),
    ]

    cursor.executemany("""
    INSERT OR IGNORE INTO settings
    (setting_key, setting_value)
    VALUES (?, ?)
    """, defaults)


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("=" * 60)
    print("Initializing OmniMind Database")
    print("=" * 60)

    connection = get_connection()

    cursor = connection.cursor()

    create_tables(cursor)

    create_indexes(cursor)

    insert_defaults(cursor)

    connection.commit()

    connection.close()

    print("Database initialized successfully.")
    print(f"Database location: {DATABASE_FILE}")


if __name__ == "__main__":

    main()