"""
=========================================================
OmniMind AI Assistant
User Models
=========================================================

Shared user models used across the application.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import uuid4

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
)

# ==========================================================
# USER ROLE
# ==========================================================


class UserRole(str, Enum):
    """
    User roles.
    """

    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


# ==========================================================
# THEME
# ==========================================================


class Theme(str, Enum):
    """
    UI theme.
    """

    LIGHT = "light"

    DARK = "dark"

    SYSTEM = "system"


# ==========================================================
# API KEYS
# ==========================================================


class APIKeys(BaseModel):
    """
    External API keys.
    """

    model_config = ConfigDict(validate_assignment=True)

    openai: str | None = None

    gemini: str | None = None

    tavily: str | None = None

    huggingface: str | None = None

    groq: str | None = None

    anthropic: str | None = None


# ==========================================================
# USER PREFERENCES
# ==========================================================


class UserPreferences(BaseModel):
    """
    User preferences.
    """

    model_config = ConfigDict(validate_assignment=True)

    theme: Theme = Theme.SYSTEM

    language: str = "en"

    default_model: str = "gpt-4.1"

    temperature: float = Field(
        default=0.7,
        ge=0,
        le=2,
    )

    max_history: int = 20

    auto_save: bool = True

    enable_memory: bool = True

    enable_streaming: bool = True

    show_token_usage: bool = True


# ==========================================================
# USAGE STATISTICS
# ==========================================================


class UsageStatistics(BaseModel):
    """
    User usage statistics.
    """

    model_config = ConfigDict(validate_assignment=True)

    total_conversations: int = 0

    total_messages: int = 0

    documents_uploaded: int = 0

    images_processed: int = 0

    audio_processed: int = 0

    searches: int = 0

    tokens_used: int = 0

    last_active: datetime | None = None


# ==========================================================
# USER PROFILE
# ==========================================================


class UserProfile(BaseModel):
    """
    User profile.
    """

    model_config = ConfigDict(validate_assignment=True)

    id: str = Field(default_factory=lambda: str(uuid4()))

    username: str

    full_name: str | None = None

    email: EmailStr | None = None

    role: UserRole = UserRole.USER

    created_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(default_factory=datetime.utcnow)

    preferences: UserPreferences = Field(default_factory=UserPreferences)

    api_keys: APIKeys = Field(default_factory=APIKeys)

    usage: UsageStatistics = Field(default_factory=UsageStatistics)

    is_active: bool = True

    avatar: str | None = None

    # =====================================================
    # METHODS
    # =====================================================

    def update_last_active(self) -> None:
        """
        Update last activity timestamp.
        """

        self.usage.last_active = datetime.utcnow()

        self.updated_at = datetime.utcnow()

    def increment_messages(self) -> None:
        """
        Increment message count.
        """

        self.usage.total_messages += 1

        self.updated_at = datetime.utcnow()

    def increment_conversations(self) -> None:
        """
        Increment conversation count.
        """

        self.usage.total_conversations += 1

        self.updated_at = datetime.utcnow()

    def increment_documents(self) -> None:
        """
        Increment uploaded documents.
        """

        self.usage.documents_uploaded += 1

        self.updated_at = datetime.utcnow()

    def increment_images(self) -> None:
        """
        Increment processed images.
        """

        self.usage.images_processed += 1

        self.updated_at = datetime.utcnow()

    def increment_audio(self) -> None:
        """
        Increment processed audio.
        """

        self.usage.audio_processed += 1

        self.updated_at = datetime.utcnow()

    def increment_searches(self) -> None:
        """
        Increment search count.
        """

        self.usage.searches += 1

        self.updated_at = datetime.utcnow()

    def add_tokens(
        self,
        tokens: int,
    ) -> None:
        """
        Add token usage.
        """

        self.usage.tokens_used += tokens

        self.updated_at = datetime.utcnow()
