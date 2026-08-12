"""
=========================================================
OmniMind AI Assistant
Uploader Component
=========================================================

Reusable file uploader for documents, images,
audio, and video.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import streamlit as st


class FileUploader:
    """
    Reusable upload component.
    """

    DOCUMENT_TYPES = [
        "pdf",
        "docx",
        "txt",
        "md",
    ]

    IMAGE_TYPES = [
        "png",
        "jpg",
        "jpeg",
        "webp",
    ]

    AUDIO_TYPES = [
        "mp3",
        "wav",
        "m4a",
    ]

    VIDEO_TYPES = [
        "mp4",
        "mov",
        "avi",
    ]

    def __init__(
        self,
        max_size_mb: int = 25,
    ) -> None:

        self.max_size_mb = max_size_mb

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate(
        self,
        uploaded_file,
        allowed_types: Iterable[str],
    ) -> bool:
        """
        Validate uploaded file.
        """

        if uploaded_file is None:
            return False

        extension = Path(uploaded_file.name).suffix.lower().replace(".", "")

        if extension not in allowed_types:

            st.error(f"Unsupported file type: {extension}")

            return False

        size_mb = uploaded_file.size / (1024 * 1024)

        if size_mb > self.max_size_mb:

            st.error(f"Maximum upload size is " f"{self.max_size_mb} MB.")

            return False

        return True

    # =====================================================
    # UPLOADER
    # =====================================================

    def upload(
        self,
        label: str,
        file_types: list[str],
        multiple: bool = False,
    ):
        """
        Render file uploader.
        """

        return st.file_uploader(
            label=label,
            type=file_types,
            accept_multiple_files=multiple,
        )

    # =====================================================
    # METADATA
    # =====================================================

    def metadata(
        self,
        uploaded_file,
    ) -> None:
        """
        Display metadata.
        """

        suffix = Path(uploaded_file.name).suffix

        size = uploaded_file.size / 1024

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Filename",
            uploaded_file.name,
        )

        col2.metric(
            "Type",
            suffix,
        )

        col3.metric(
            "Size",
            f"{size:.1f} KB",
        )

    # =====================================================
    # PREVIEW
    # =====================================================

    def preview(
        self,
        uploaded_file,
    ) -> None:
        """
        Preview supported files.
        """

        extension = Path(uploaded_file.name).suffix.lower()

        if extension in [
            ".png",
            ".jpg",
            ".jpeg",
            ".webp",
        ]:

            st.image(
                uploaded_file,
                use_container_width=True,
            )

        elif extension in [
            ".mp3",
            ".wav",
            ".m4a",
        ]:

            st.audio(uploaded_file)

        elif extension in [
            ".mp4",
            ".mov",
            ".avi",
        ]:

            st.video(uploaded_file)

        elif extension in [
            ".txt",
            ".md",
        ]:

            text = uploaded_file.read().decode(
                "utf-8",
                errors="ignore",
            )

            st.text_area(
                "Preview",
                text,
                height=300,
            )

        else:

            st.info("Preview unavailable.")

    # =====================================================
    # PROGRESS
    # =====================================================

    def progress(
        self,
        value: float,
    ) -> None:
        """
        Upload progress.
        """

        st.progress(value, text="Uploading...")

    # =====================================================
    # SAVE
    # =====================================================

    def save(
        self,
        uploaded_file,
        destination: str | Path,
    ) -> Path:
        """
        Save uploaded file.
        """

        destination = Path(destination)

        destination.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path = destination / uploaded_file.name

        with open(
            file_path,
            "wb",
        ) as file:

            file.write(uploaded_file.getbuffer())

        return file_path

    # =====================================================
    # COMPLETE WORKFLOW
    # =====================================================

    def render(
        self,
        title: str,
        allowed_types: list[str],
        destination: str = "uploads",
    ) -> Path | None:
        """
        Complete upload workflow.
        """

        uploaded = self.upload(
            title,
            allowed_types,
        )

        if uploaded is None:
            return None

        if not self.validate(
            uploaded,
            allowed_types,
        ):
            return None

        self.metadata(uploaded)

        self.preview(uploaded)

        self.progress(100)

        return self.save(
            uploaded,
            destination,
        )


uploader = FileUploader()
