"""
=========================================================
OmniMind AI Assistant
Custom Exceptions
=========================================================

Defines custom exception classes used throughout
the application.
"""

from __future__ import annotations

# ==========================================================
# Base Exception
# ==========================================================


class OmniMindError(Exception):
    """
    Base exception for OmniMind AI.
    """

    default_message = "An unknown OmniMind error occurred."

    def __init__(self, message: str | None = None):
        super().__init__(message or self.default_message)


# ==========================================================
# Configuration
# ==========================================================


class ConfigurationError(OmniMindError):
    default_message = "Configuration is invalid."


class MissingAPIKeyError(ConfigurationError):
    default_message = "Required API key is missing."


# ==========================================================
# Model Errors
# ==========================================================


class ModelError(OmniMindError):
    default_message = "AI model failed."


class ModelInitializationError(ModelError):
    default_message = "Unable to initialize AI model."


class ModelResponseError(ModelError):
    default_message = "Model failed to generate a response."


# ==========================================================
# Validation
# ==========================================================


class ValidationError(OmniMindError):
    default_message = "Validation failed."


class UnsupportedFileTypeError(ValidationError):
    default_message = "Unsupported file type."


class FileTooLargeError(ValidationError):
    default_message = "Uploaded file exceeds the allowed size."


# ==========================================================
# Database
# ==========================================================


class DatabaseError(OmniMindError):
    default_message = "Database operation failed."


class MemoryError(DatabaseError):
    default_message = "Conversation memory error."


class CacheError(DatabaseError):
    default_message = "Cache operation failed."


# ==========================================================
# Search / RAG
# ==========================================================


class RetrievalError(OmniMindError):
    default_message = "Failed to retrieve relevant information."


class EmbeddingError(OmniMindError):
    default_message = "Embedding generation failed."


# ==========================================================
# OCR / Vision
# ==========================================================


class VisionError(OmniMindError):
    default_message = "Image analysis failed."


class OCRError(VisionError):
    default_message = "OCR extraction failed."


# ==========================================================
# Audio
# ==========================================================


class AudioError(OmniMindError):
    default_message = "Audio processing failed."


class SpeechRecognitionError(AudioError):
    default_message = "Speech recognition failed."


class TextToSpeechError(AudioError):
    default_message = "Text-to-speech generation failed."


# ==========================================================
# Web Search
# ==========================================================


class SearchError(OmniMindError):
    default_message = "Web search failed."


# ==========================================================
# Authentication
# ==========================================================


class AuthenticationError(OmniMindError):
    default_message = "Authentication failed."


class AuthorizationError(AuthenticationError):
    default_message = "Permission denied."


# ==========================================================
# Workflow
# ==========================================================


class WorkflowError(OmniMindError):
    default_message = "Workflow execution failed."


class ToolExecutionError(WorkflowError):
    default_message = "Tool execution failed."


# ==========================================================
# Agent
# ==========================================================


class AgentException(OmniMindError):
    """
    Raised when an AI agent fails to complete its task.
    """

    default_message = "Agent execution failed."
