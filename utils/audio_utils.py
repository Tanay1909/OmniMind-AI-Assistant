"""
=========================================================
OmniMind AI Assistant
Audio Utilities
=========================================================

Reusable audio processing utilities.
"""

from __future__ import annotations

import base64
import io
import wave
from pathlib import Path
from typing import Any

from pydub import AudioSegment

# =========================================================
# LOAD AUDIO
# =========================================================


def load_audio(path: str | Path) -> AudioSegment:
    """
    Load an audio file.
    """
    return AudioSegment.from_file(path)


# =========================================================
# SAVE AUDIO
# =========================================================


def save_audio(
    audio: AudioSegment,
    path: str | Path,
    format: str = "wav",
) -> Path:
    """
    Save an audio file.
    """

    path = Path(path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    audio.export(
        path,
        format=format,
    )

    return path


# =========================================================
# AUDIO DURATION
# =========================================================


def audio_duration(
    audio: AudioSegment,
) -> float:
    """
    Return duration in seconds.
    """

    return len(audio) / 1000.0


# =========================================================
# SAMPLE RATE
# =========================================================


def sample_rate(
    audio: AudioSegment,
) -> int:
    """
    Return sample rate.
    """

    return audio.frame_rate


# =========================================================
# CHANNELS
# =========================================================


def channels(
    audio: AudioSegment,
) -> int:
    """
    Return number of channels.
    """

    return audio.channels


# =========================================================
# CONVERT FORMAT
# =========================================================


def convert_audio(
    source: str | Path,
    destination: str | Path,
    format: str,
) -> Path:
    """
    Convert audio format.
    """

    audio = AudioSegment.from_file(source)

    destination = Path(destination)

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    audio.export(
        destination,
        format=format,
    )

    return destination


# =========================================================
# TRIM AUDIO
# =========================================================


def trim_audio(
    audio: AudioSegment,
    start_ms: int,
    end_ms: int,
) -> AudioSegment:
    """
    Trim audio.
    """

    return audio[start_ms:end_ms]


# =========================================================
# CHANGE VOLUME
# =========================================================


def change_volume(
    audio: AudioSegment,
    db: float,
) -> AudioSegment:
    """
    Increase/decrease volume.
    """

    return audio + db


# =========================================================
# WAV METADATA
# =========================================================


def wav_metadata(
    path: str | Path,
) -> dict[str, Any]:
    """
    Read WAV metadata.
    """

    with wave.open(str(path), "rb") as wav:

        return {
            "channels": wav.getnchannels(),
            "sample_width": wav.getsampwidth(),
            "frame_rate": wav.getframerate(),
            "frames": wav.getnframes(),
            "duration": wav.getnframes() / wav.getframerate(),
        }


# =========================================================
# AUDIO TO BASE64
# =========================================================


def audio_to_base64(
    audio: AudioSegment,
    format: str = "wav",
) -> str:
    """
    Convert audio to Base64.
    """

    buffer = io.BytesIO()

    audio.export(
        buffer,
        format=format,
    )

    return base64.b64encode(buffer.getvalue()).decode("utf-8")


# =========================================================
# BASE64 TO AUDIO
# =========================================================


def base64_to_audio(
    encoded: str,
    format: str = "wav",
) -> AudioSegment:
    """
    Decode Base64 audio.
    """

    data = base64.b64decode(encoded)

    return AudioSegment.from_file(
        io.BytesIO(data),
        format=format,
    )


# =========================================================
# SILENCE
# =========================================================


def create_silence(
    duration_ms: int,
) -> AudioSegment:
    """
    Create silent audio.
    """

    return AudioSegment.silent(duration=duration_ms)


# =========================================================
# CONCATENATE
# =========================================================


def concatenate_audio(
    *segments: AudioSegment,
) -> AudioSegment:
    """
    Merge multiple audio segments.
    """

    output = AudioSegment.empty()

    for segment in segments:

        output += segment

    return output


# =========================================================
# NORMALIZE
# =========================================================


def normalize_audio(
    audio: AudioSegment,
) -> AudioSegment:
    """
    Normalize audio volume.
    """

    return audio.normalize()


# =========================================================
# AUDIO METADATA
# =========================================================


def audio_metadata(
    audio: AudioSegment,
) -> dict[str, Any]:
    """
    Return audio metadata.
    """

    return {
        "duration": audio_duration(audio),
        "sample_rate": sample_rate(audio),
        "channels": channels(audio),
        "sample_width": audio.sample_width,
        "frame_width": audio.frame_width,
        "max_dbfs": audio.max_dBFS,
    }
