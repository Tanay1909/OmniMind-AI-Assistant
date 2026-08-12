"""
=========================================================
OmniMind AI Assistant
Database Models
=========================================================

SQLAlchemy ORM models for persistent storage.
"""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from database.db import Base

# ==========================================================
# USER
# ==========================================================


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    full_name: Mapped[str | None] = mapped_column(
        String(200),
    )

    email: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
    )

    role: Mapped[str] = mapped_column(
        String(20),
        default="user",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    conversations = relationship(
        "Conversation",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    memories = relationship(
        "Memory",
        back_populates="user",
        cascade="all, delete-orphan",
    )


# ==========================================================
# CONVERSATION
# ==========================================================


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    title: Mapped[str] = mapped_column(
        String(255),
        default="New Conversation",
    )

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    user = relationship(
        "User",
        back_populates="conversations",
    )

    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
    )


# ==========================================================
# MESSAGE
# ==========================================================


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    conversation_id: Mapped[str] = mapped_column(
        ForeignKey("conversations.id"),
    )

    role: Mapped[str] = mapped_column(
        String(20),
    )

    content: Mapped[str] = mapped_column(
        Text,
    )

    token_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    conversation = relationship(
        "Conversation",
        back_populates="messages",
    )


# ==========================================================
# MEMORY
# ==========================================================


class Memory(Base):
    __tablename__ = "memories"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
    )

    memory_type: Mapped[str] = mapped_column(
        String(50),
    )

    content: Mapped[str] = mapped_column(
        Text,
    )

    importance: Mapped[str] = mapped_column(
        String(20),
        default="medium",
    )

    memory_metadata: Mapped[dict] = mapped_column(
        "metadata",
        JSON,
        default=dict,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    user = relationship(
        "User",
        back_populates="memories",
    )


# ==========================================================
# DOCUMENT
# ==========================================================


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    filename: Mapped[str] = mapped_column(
        String(255),
    )

    file_type: Mapped[str] = mapped_column(
        String(50),
    )

    file_size: Mapped[int] = mapped_column(
        Integer,
    )

    path: Mapped[str] = mapped_column(
        String(500),
    )

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )


# ==========================================================
# ANALYTICS
# ==========================================================


class AnalyticsEvent(Base):
    __tablename__ = "analytics"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    event_type: Mapped[str] = mapped_column(
        String(100),
    )

    duration: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    success: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    event_metadata: Mapped[dict] = mapped_column(
        "metadata",
        JSON,
        default=dict,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )


# ==========================================================
# SETTINGS
# ==========================================================


class UserSettings(Base):
    __tablename__ = "user_settings"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
    )

    settings: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )


# ==========================================================
# WORKFLOW EXECUTION
# ==========================================================


class WorkflowExecution(Base):
    __tablename__ = "workflow_executions"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    workflow_name: Mapped[str] = mapped_column(
        String(255),
    )

    status: Mapped[str] = mapped_column(
        String(30),
    )

    execution_time: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    workflow_metadata: Mapped[dict] = mapped_column(
        "metadata",
        JSON,
        default=dict,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )
