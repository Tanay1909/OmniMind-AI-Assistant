"""
=========================================================
OmniMind AI Assistant
Settings Models
=========================================================

Shared settings models used across the application.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

# ==========================================================
# LLM PROVIDERS
# ==========================================================


class LLMProvider(str, Enum):
    """
    Supported LLM providers.
    """

    OPENAI = "openai"
    GEMINI = "gemini"
    GROQ = "groq"
    OLLAMA = "ollama"
    ANTHROPIC = "anthropic"


# ==========================================================
# APPLICATION THEME
# ==========================================================


class ThemeMode(str, Enum):
    """
    UI Theme.
    """

    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"


# ==========================================================
# MODEL SETTINGS
# ==========================================================


class ModelSettings(BaseModel):
    """
    LLM configuration.
    """

    model_config = ConfigDict(validate_assignment=True)

    provider: LLMProvider = LLMProvider.OPENAI

    model_name: str = "gpt-4.1"

    temperature: float = Field(
        default=0.7,
        ge=0,
        le=2,
    )

    max_tokens: int = Field(
        default=4096,
        gt=0,
    )

    top_p: float = Field(
        default=1.0,
        ge=0,
        le=1,
    )

    frequency_penalty: float = Field(
        default=0.0,
        ge=-2,
        le=2,
    )

    presence_penalty: float = Field(
        default=0.0,
        ge=-2,
        le=2,
    )

    stream: bool = True


# ==========================================================
# UI SETTINGS
# ==========================================================


class UISettings(BaseModel):
    """
    Streamlit UI configuration.
    """

    model_config = ConfigDict(validate_assignment=True)

    theme: ThemeMode = ThemeMode.SYSTEM

    page_title: str = "OmniMind AI"

    page_icon: str = "🤖"

    layout: str = "wide"

    sidebar_state: str = "expanded"

    show_token_usage: bool = True

    show_latency: bool = True

    enable_chat_history: bool = True

    enable_markdown: bool = True


# ==========================================================
# FEATURE FLAGS
# ==========================================================


class FeatureFlags(BaseModel):
    """
    Enable or disable application modules.
    """

    model_config = ConfigDict(validate_assignment=True)

    chat: bool = True

    memory: bool = True

    vision: bool = True

    speech: bool = True

    web_search: bool = True

    rag: bool = True

    coding: bool = True

    research: bool = True

    analytics: bool = True

    export: bool = True


# ==========================================================
# SECURITY SETTINGS
# ==========================================================


class SecuritySettings(BaseModel):
    """
    Security configuration.
    """

    model_config = ConfigDict(validate_assignment=True)

    max_upload_size_mb: int = 25

    allowed_file_types: list[str] = Field(
        default_factory=lambda: [
            "pdf",
            "docx",
            "txt",
            "png",
            "jpg",
            "jpeg",
            "mp3",
            "wav",
        ]
    )

    enable_rate_limit: bool = False

    enable_api_key_validation: bool = True

    enable_file_validation: bool = True


# ==========================================================
# CACHE SETTINGS
# ==========================================================


class CacheSettings(BaseModel):
    """
    Cache configuration.
    """

    model_config = ConfigDict(validate_assignment=True)

    enabled: bool = True

    ttl_seconds: int = 3600

    max_entries: int = 1000


# ==========================================================
# APPLICATION SETTINGS
# ==========================================================


class UserSettings(BaseModel):
    """
    Complete application settings.
    """

    model_config = ConfigDict(validate_assignment=True)

    model: ModelSettings = Field(default_factory=ModelSettings)

    ui: UISettings = Field(default_factory=UISettings)

    features: FeatureFlags = Field(default_factory=FeatureFlags)

    security: SecuritySettings = Field(default_factory=SecuritySettings)

    cache: CacheSettings = Field(default_factory=CacheSettings)
