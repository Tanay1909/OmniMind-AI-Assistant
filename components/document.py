"""
=========================================================
OmniMind AI Assistant
Document Component
=========================================================

Modern document workspace.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import streamlit as st

from agents.document_agent import DocumentAgent


class DocumentComponent:

    SUPPORTED_TYPES = [
        "pdf",
        "docx",
        "txt",
        "md",
    ]

    def __init__(self):

        self.agent = DocumentAgent()

    # =====================================================
    # HEADER
    # =====================================================

    def render_header(self):

        st.title("📄 Document Assistant")

        st.caption("Upload a document, summarize it, analyze it and ask questions.")

    # =====================================================
    # UPLOADER
    # =====================================================

    def upload(self):

        return st.file_uploader(
            "Upload Document",
            type=self.SUPPORTED_TYPES,
        )

    # =====================================================
    # SAVE FILE
    # =====================================================

    def save_uploaded_file(
        self,
        uploaded_file,
    ) -> str:

        suffix = Path(uploaded_file.name).suffix

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as tmp:

            tmp.write(uploaded_file.getbuffer())

            return tmp.name

    # =====================================================
    # METADATA
    # =====================================================

    def metadata(
        self,
        uploaded_file,
    ):

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Filename",
            uploaded_file.name,
        )

        col2.metric(
            "Type",
            Path(uploaded_file.name).suffix,
        )

        col3.metric(
            "Size",
            f"{uploaded_file.size / 1024:.1f} KB",
        )

    # =====================================================
    # PREVIEW
    # =====================================================

    def preview(
        self,
        uploaded_file,
    ):

        extension = Path(uploaded_file.name).suffix.lower()

        if extension in [".txt", ".md"]:

            uploaded_file.seek(0)

            text = uploaded_file.read().decode(
                "utf-8",
                errors="ignore",
            )

            st.subheader("Preview")

            st.text_area(
                "Content",
                text,
                height=300,
            )

    # =====================================================
    # ACTIONS
    # =====================================================

    def action_buttons(self):

        c1, c2, c3 = st.columns(3)

        with c1:
            summarize = st.button(
                "📝 Summarize",
                use_container_width=True,
            )

        with c2:
            extract = st.button(
                "📄 Extract Text",
                use_container_width=True,
            )

        with c3:
            analyze = st.button(
                "🧠 Analyze",
                use_container_width=True,
            )

        return summarize, extract, analyze

    # =====================================================
    # MAIN
    # =====================================================

    def render(self):

        self.render_header()

        uploaded = self.upload()

        if uploaded is None:
            return

        self.metadata(uploaded)

        self.preview(uploaded)

        file_path = self.save_uploaded_file(uploaded)

        try:

            self.agent.load_document(file_path)

        except Exception as e:

            st.error(str(e))

            return

        summarize, extract, analyze = self.action_buttons()

        if summarize:

            with st.spinner("Generating summary..."):

                summary = self.agent.summarize_document()

            st.subheader("Summary")

            st.write(summary)

        if extract:

            with st.spinner("Extracting text..."):

                text = self.agent.extract_text(file_path)

            st.subheader("Extracted Text")

            st.text_area(
                "Document",
                text,
                height=400,
            )

        if analyze:

            with st.spinner("Analyzing document..."):

                result = self.agent.analyze_document()

            st.subheader("Analysis")

            st.write(result)

        st.divider()

        question = st.text_input("Ask a question about this document")

        if st.button("Ask"):

            if question.strip():

                with st.spinner("Searching..."):

                    answer = self.agent.answer_question(question)

                st.subheader("Answer")

                st.write(answer)


document_component = DocumentComponent()
