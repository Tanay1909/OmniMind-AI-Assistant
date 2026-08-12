"""
=========================================================
OmniMind AI Assistant
Speech Page
=========================================================

Speech-to-Text, Text-to-Speech and Translation
workspace powered by SpeechAgent.
"""

from __future__ import annotations

import streamlit as st

from agents.speech_agent import SpeechAgent

from components.footer import footer
from components.navbar import navbar
from components.notifications import notifications
from components.sidebar import sidebar
from components.uploader import uploader


class SpeechPage:
    """
    Speech AI Workspace.
    """

    def __init__(self):

        self.agent = SpeechAgent()

    # =====================================================
    # PAGE CONFIG
    # =====================================================

    def configure(self):

        st.set_page_config(
            page_title="Speech",
            page_icon="🎤",
            layout="wide",
            initial_sidebar_state="expanded",
        )

    # =====================================================
    # SIDEBAR
    # =====================================================

    def render_sidebar(self):

        return sidebar.render()

    # =====================================================
    # HEADER
    # =====================================================

    def render_header(
        self,
        model: str,
    ):

        navbar.render(
            page_title="🎤 Speech Workspace",
            model_name=model,
        )

    # =====================================================
    # AUDIO UPLOAD
    # =====================================================

    def upload_audio(self):

        return uploader.render(
            title="Upload Audio",
            allowed_types=uploader.AUDIO_TYPES,
            destination="uploads/audio",
        )

    # =====================================================
    # ACTIONS
    # =====================================================

    def action_buttons(self):

        col1, col2, col3 = st.columns(3)

        with col1:

            transcribe = st.button(
                "📝 Speech → Text",
                use_container_width=True,
            )

        with col2:

            translate = st.button(
                "🌍 Translate",
                use_container_width=True,
            )

        with col3:

            summarize = st.button(
                "📄 Summarize",
                use_container_width=True,
            )

        return {
            "transcribe": transcribe,
            "translate": translate,
            "summarize": summarize,
        }

    # =====================================================
    # TEXT TO SPEECH
    # =====================================================

    def text_to_speech(self):

        st.subheader("Text to Speech")

        text = st.text_area(
            "Enter Text",
            height=150,
        )

        if st.button(
            "🔊 Generate Speech",
            use_container_width=True,
        ):

            with st.spinner("Generating audio..."):

                audio_path = self.agent.text_to_speech(text)

            st.audio(audio_path)

            notifications.success("Speech", "Audio generated successfully.")

    # =====================================================
    # AUDIO WORKSPACE
    # =====================================================

    def workspace(
        self,
        audio_file,
        actions,
    ):

        if audio_file is None:

            st.info("Upload an audio file to begin.")

            return

        st.audio(str(audio_file))

        if actions["transcribe"]:

            with st.spinner("Transcribing..."):

                transcript = self.agent.transcribe(audio_file)

            st.subheader("Transcript")

            st.text_area(
                "",
                transcript,
                height=250,
            )

            notifications.success("Speech", "Transcription completed.")

        if actions["translate"]:

            with st.spinner("Translating..."):

                translated = self.agent.translate(audio_file)

            st.subheader("Translation")

            st.write(translated)

        if actions["summarize"]:

            with st.spinner("Summarizing..."):

                summary = self.agent.summarize(audio_file)

            st.subheader("Summary")

            st.write(summary)

    # =====================================================
    # FOOTER
    # =====================================================

    def render_footer(self):

        footer.render()

    # =====================================================
    # MAIN
    # =====================================================

    def render(self):

        self.configure()

        config = self.render_sidebar()

        self.render_header(config["model"])

        actions = self.action_buttons()

        st.divider()

        audio = self.upload_audio()

        self.workspace(
            audio,
            actions,
        )

        st.divider()

        self.text_to_speech()

        st.divider()

        self.render_footer()


speech_page = SpeechPage()


def main():

    speech_page.render()


if __name__ == "__main__":

    main()
