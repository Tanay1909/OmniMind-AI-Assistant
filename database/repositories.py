"""
=========================================================
OmniMind AI Assistant
Repository Layer
=========================================================

Repository Pattern implementation using SQLAlchemy.
"""

from __future__ import annotations

from typing import Generic, TypeVar

from sqlalchemy.orm import Session

from database.db import db
from database.models import (
    AnalyticsEvent,
    Conversation,
    Document,
    Memory,
    Message,
    User,
    UserSettings,
    WorkflowExecution,
)

T = TypeVar("T")


# ==========================================================
# BASE REPOSITORY
# ==========================================================


class BaseRepository(Generic[T]):
    """Base repository for CRUD operations."""

    model = None

    def __init__(self, session: Session | None = None):
        self._owns_session = session is None
        self.session = session if session else db.get_session()

    def close(self):
        if self._owns_session:
            self.session.close()

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass

    def get(self, object_id):
        return self.session.get(self.model, object_id)

    def get_all(self):
        return self.session.query(self.model).all()

    def create(self, **kwargs):
        obj = self.model(**kwargs)
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def update(self, obj, **kwargs):
        for key, value in kwargs.items():
            setattr(obj, key, value)

        self.session.commit()
        self.session.refresh(obj)
        return obj

    def delete(self, obj):
        self.session.delete(obj)
        self.session.commit()

    def count(self):
        return self.session.query(self.model).count()


# ==========================================================
# USER REPOSITORY
# ==========================================================


class UserRepository(BaseRepository[User]):
    model = User

    def get_by_username(self, username):
        return self.session.query(User).filter(User.username == username).first()

    def get_by_email(self, email):
        return self.session.query(User).filter(User.email == email).first()


# ==========================================================
# CONVERSATION REPOSITORY
# ==========================================================


class ConversationRepository(BaseRepository[Conversation]):
    model = Conversation

    def get_user_conversations(self, user_id):
        return (
            self.session.query(Conversation)
            .filter(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .all()
        )


# ==========================================================
# MESSAGE REPOSITORY
# ==========================================================


class MessageRepository(BaseRepository[Message]):
    model = Message

    def get_conversation_messages(self, conversation_id):
        return (
            self.session.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .all()
        )


# ==========================================================
# MEMORY REPOSITORY
# ==========================================================


class MemoryRepository(BaseRepository[Memory]):
    model = Memory

    def get_user_memories(self, user_id):
        return self.session.query(Memory).filter(Memory.user_id == user_id).all()


# ==========================================================
# DOCUMENT REPOSITORY
# ==========================================================


class DocumentRepository(BaseRepository[Document]):
    model = Document

    def search_filename(self, keyword):
        return (
            self.session.query(Document)
            .filter(Document.filename.contains(keyword))
            .all()
        )


# ==========================================================
# ANALYTICS REPOSITORY
# ==========================================================


class AnalyticsRepository(BaseRepository[AnalyticsEvent]):
    model = AnalyticsEvent

    def successful_events(self):
        return (
            self.session.query(AnalyticsEvent)
            .filter(AnalyticsEvent.success.is_(True))
            .all()
        )


# ==========================================================
# SETTINGS REPOSITORY
# ==========================================================


class SettingsRepository(BaseRepository[UserSettings]):
    model = UserSettings

    def get_user_settings(self, user_id):
        return (
            self.session.query(UserSettings)
            .filter(UserSettings.user_id == user_id)
            .first()
        )

    def save(self, settings):
        self.session.add(settings)
        self.session.commit()
        self.session.refresh(settings)
        return settings

    def reset(self, user_id):
        settings = self.get_user_settings(user_id)
        if settings:
            self.session.delete(settings)
            self.session.commit()


# ==========================================================
# WORKFLOW REPOSITORY
# ==========================================================


class WorkflowRepository(BaseRepository[WorkflowExecution]):
    model = WorkflowExecution

    def recent(self, limit=20):
        return (
            self.session.query(WorkflowExecution)
            .order_by(WorkflowExecution.created_at.desc())
            .limit(limit)
            .all()
        )


# ==========================================================
# REPOSITORY MANAGER
# ==========================================================


class RepositoryManager:
    """Provides access to all repositories."""

    def __init__(self, session: Session | None = None):
        self.session = session or db.get_session()

        self.users = UserRepository(self.session)
        self.conversations = ConversationRepository(self.session)
        self.messages = MessageRepository(self.session)
        self.memories = MemoryRepository(self.session)
        self.documents = DocumentRepository(self.session)
        self.analytics = AnalyticsRepository(self.session)
        self.settings = SettingsRepository(self.session)
        self.workflows = WorkflowRepository(self.session)
