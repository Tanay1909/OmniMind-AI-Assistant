"""
=========================================================
OmniMind AI Assistant
Database Manager
=========================================================

Centralized database connection and session management.
Supports SQLite using SQLAlchemy.
"""

from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from config.config import settings

# ==========================================================
# DATABASE PATH
# ==========================================================

database_path = Path(settings.DATABASE_PATH)

database_path.parent.mkdir(
    parents=True,
    exist_ok=True,
)

DATABASE_URL = f"sqlite:///{database_path}"

# ==========================================================
# ENGINE
# ==========================================================

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)

# ==========================================================
# SESSION
# ==========================================================

SessionLocal = scoped_session(
    sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )
)

# ==========================================================
# BASE MODEL
# ==========================================================

Base = declarative_base()

# ==========================================================
# DATABASE MANAGER
# ==========================================================


class DatabaseManager:
    """
    Central database manager.
    """

    def __init__(self) -> None:

        self.engine = engine
        self.Session = SessionLocal

    # =====================================================
    # CREATE DATABASE
    # =====================================================

    def create_database(self) -> None:

        Base.metadata.create_all(bind=self.engine)

    # =====================================================
    # DROP DATABASE
    # =====================================================

    def drop_database(self) -> None:

        Base.metadata.drop_all(bind=self.engine)

    # =====================================================
    # SESSION
    # =====================================================

    def get_session(self):

        return self.Session()

    @contextmanager
    def session_scope(self):

        session = self.get_session()

        try:

            yield session

            session.commit()

        except Exception:

            session.rollback()
            raise

        finally:

            session.close()

    # =====================================================
    # CLOSE DATABASE
    # =====================================================

    def dispose(self) -> None:

        self.Session.remove()
        self.engine.dispose()


# ==========================================================
# GLOBAL INSTANCE
# ==========================================================

db = DatabaseManager()

# ==========================================================
# INITIALIZE DATABASE
# ==========================================================


def init_database() -> None:
    """
    Create all database tables.
    """

    Base.metadata.create_all(bind=engine)


# ==========================================================
# DATABASE DEPENDENCY
# ==========================================================


def get_db():

    session = db.get_session()

    try:

        yield session

    finally:

        session.close()
