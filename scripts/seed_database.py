"""
=========================================================
OmniMind AI Assistant
Database Seed Script
=========================================================

Creates sample records for development and testing.

Usage:
    python scripts/seed_database.py
"""

from pathlib import Path
import hashlib
import random
import sqlite3

DATABASE = Path("database/database.db")


# ==========================================================
# DATABASE CONNECTION
# ==========================================================

def get_connection():

    return sqlite3.connect(DATABASE)


# ==========================================================
# PASSWORD HASH
# ==========================================================

def hash_password(password: str) -> str:

    return hashlib.sha256(

        password.encode()

    ).hexdigest()


# ==========================================================
# SAMPLE USERS
# ==========================================================

def seed_users(cursor):

    users = [

        (

            "Admin User",

            "admin@omnimind.ai",

            hash_password("Admin@123"),

            "admin",

        ),

        (

            "Tanay Sadhu",

            "tanay@example.com",

            hash_password("Password123"),

            "user",

        ),

        (

            "John Smith",

            "john@example.com",

            hash_password("Password123"),

            "user",

        ),

        (

            "Alice Johnson",

            "alice@example.com",

            hash_password("Password123"),

            "user",

        ),

    ]

    cursor.executemany(

        """

        INSERT OR IGNORE INTO users

        (full_name,email,password_hash,role)

        VALUES (?,?,?,?)

        """,

        users,

    )


# ==========================================================
# CONVERSATIONS
# ==========================================================

def seed_conversations(cursor):

    conversations = [

        (1, "Welcome Chat"),

        (2, "Machine Learning"),

        (2, "Resume Review"),

        (3, "Image Analysis"),

        (4, "Python Help"),

    ]

    cursor.executemany(

        """

        INSERT INTO conversations

        (user_id,title)

        VALUES (?,?)

        """,

        conversations,

    )


# ==========================================================
# MESSAGES
# ==========================================================

def seed_messages(cursor):

    messages = []

    sample = [

        "Hello!",

        "Explain AI.",

        "Summarize this PDF.",

        "Generate an image.",

        "Write Python code.",

    ]

    for conversation in range(1, 6):

        messages.append(

            (

                conversation,

                "user",

                random.choice(sample),

            )

        )

        messages.append(

            (

                conversation,

                "assistant",

                "This is a sample AI response.",

            )

        )

    cursor.executemany(

        """

        INSERT INTO messages

        (conversation_id,sender,content)

        VALUES (?,?,?)

        """,

        messages,

    )


# ==========================================================
# DOCUMENTS
# ==========================================================

def seed_documents(cursor):

    docs = [

        (2, "machine_learning.pdf", "pdf", 204800),

        (2, "resume.docx", "docx", 50120),

        (3, "research.pdf", "pdf", 320100),

    ]

    cursor.executemany(

        """

        INSERT INTO documents

        (user_id,filename,file_type,file_size)

        VALUES (?,?,?,?)

        """,

        docs,

    )


# ==========================================================
# IMAGES
# ==========================================================

def seed_images(cursor):

    images = [

        (

            2,

            "future_city.png",

            "Futuristic smart city",

        ),

        (

            3,

            "robot.png",

            "Friendly AI robot",

        ),

    ]

    cursor.executemany(

        """

        INSERT INTO images

        (user_id,filename,prompt)

        VALUES (?,?,?)

        """,

        images,

    )


# ==========================================================
# AUDIO
# ==========================================================

def seed_audio(cursor):

    records = [

        (

            2,

            "meeting.wav",

            "Meeting transcription",

        ),

        (

            3,

            "lecture.mp3",

            "Lecture transcript",

        ),

    ]

    cursor.executemany(

        """

        INSERT INTO audio

        (user_id,filename,transcript)

        VALUES (?,?,?)

        """,

        records,

    )


# ==========================================================
# ACTIVITY LOGS
# ==========================================================

def seed_logs(cursor):

    logs = [

        (

            1,

            "Administrator login",

            "127.0.0.1",

        ),

        (

            2,

            "Generated AI response",

            "127.0.0.1",

        ),

        (

            2,

            "Uploaded PDF",

            "127.0.0.1",

        ),

        (

            3,

            "Generated Image",

            "127.0.0.1",

        ),

    ]

    cursor.executemany(

        """

        INSERT INTO activity_logs

        (user_id,action,ip_address)

        VALUES (?,?,?)

        """,

        logs,

    )


# ==========================================================
# SETTINGS
# ==========================================================

def verify_settings(cursor):

    defaults = [

        ("theme", "light"),

        ("language", "English"),

        ("notifications", "enabled"),

    ]

    cursor.executemany(

        """

        INSERT OR IGNORE INTO settings

        (setting_key,setting_value)

        VALUES (?,?)

        """,

        defaults,

    )


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("=" * 60)

    print("Seeding OmniMind Database")

    print("=" * 60)

    connection = get_connection()

    cursor = connection.cursor()

    seed_users(cursor)

    seed_conversations(cursor)

    seed_messages(cursor)

    seed_documents(cursor)

    seed_images(cursor)

    seed_audio(cursor)

    seed_logs(cursor)

    verify_settings(cursor)

    connection.commit()

    connection.close()

    print("Sample data inserted successfully.")


if __name__ == "__main__":

    main()