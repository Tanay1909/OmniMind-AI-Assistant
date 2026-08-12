"""
=========================================================
OmniMind AI Assistant
Audio Models
=========================================================

Shared audio models used across the application.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

# ==========================================================
# AUDIO FORMAT
# ==========================================================


class AudioFormat(str, Enum):
    """
    Supported audio formats.
    """

    MP3 = "mp3"
    WAV = "wav"
    M4A = "m4a"
    FLAC = "flac"
    AAC = "aac"
    OGG = "ogg"
    WEBM = "webm"
    UNKNOWN = "unknown"


# ==========================================================
# AUDIO METADATA
# ==========================================================


class AudioMetadata(BaseModel):
    """
    General audio information.
    """

    model_config = ConfigDict(validate_assignment=True)

    id: str = Field(default_factory=lambda: str(uuid4()))

    filename: str

    format: AudioFormat = AudioFormat.UNKNOWN

    duration: float = 0.0

    sample_rate: int = 16000

    channels: int = 1

    bitrate: int | None = None

    language: str | None = None

    file_size: int = 0

    created_at: datetime = Field(default_factory=datetime.utcnow)

    metadata: dict[str, Any] = Field(default_factory=dict)


# ==========================================================
# SPEAKER
# ==========================================================


class Speaker(BaseModel):
    """
    Speaker information.
    """

    model_config = ConfigDict(validate_assignment=True)

    speaker_id: str

    name: str | None = None

    confidence: float = 1.0


# ==========================================================
# TRANSCRIPTION SEGMENT
# ==========================================================


class TranscriptionSegment(BaseModel):
    """
    A single speech segment.
    """

    model_config = ConfigDict(validate_assignment=True)

    id: str = Field(default_factory=lambda: str(uuid4()))

    start_time: float

    end_time: float

    text: str

    confidence: float = 1.0

    speaker: Speaker | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)

    @property
    def duration(self) -> float:
        return round(self.end_time - self.start_time, 2)


# ==========================================================
# TRANSCRIPTION RESULT
# ==========================================================


class TranscriptionResult(BaseModel):
    """
    Complete transcription.
    """

    model_config = ConfigDict(validate_assignment=True)

    audio: AudioMetadata

    transcript: str

    language: str | None = None

    segments: list[TranscriptionSegment] = Field(default_factory=list)

    processing_time: float | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)

    @property
    def segment_count(self) -> int:
        return len(self.segments)

    @property
    def word_count(self) -> int:
        return len(self.transcript.split())


# ==========================================================
# TEXT TO SPEECH RESULT
# ==========================================================


class SpeechSynthesisResult(BaseModel):
    """
    Result returned by TTS engines.
    """

    model_config = ConfigDict(validate_assignment=True)

    text: str

    output_path: str

    duration: float | None = None

    voice: str | None = None

    language: str | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)
