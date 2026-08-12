"""
=========================================================
OmniMind AI Assistant
Settings Component
=========================================================

Application settings page.
"""

from __future__ import annotations

import streamlit as st

from models.settings import ThemeMode, LLMProvider
from database.repositories import SettingsRepository


class SettingsComponent:
    """User settings interface."""

    def __init__(self):
        try:
            self.repository = SettingsRepository()
        except Exception as e:
            self.repository = None
            self.error = str(e)
        else:
            self.error = None

    # =====================================================
    # HEADER
    # =====================================================

    def render_header(self):
        st.header("⚙ Settings")
        st.caption("Customize OmniMind AI according to your preferences.")

    # =====================================================
    # AI SETTINGS
    # =====================================================

    def ai_settings(self):
        st.subheader("AI Configuration")

        provider = st.selectbox(
            "Provider",
            [p.value for p in LLMProvider],
            index=0,
        )

        model = st.text_input(
            "Default Model",
            value="GPT-4.1",
        )

        temperature = st.slider(
            "Temperature",
            0.0,
            2.0,
            0.7,
            0.1,
        )

        max_tokens = st.number_input(
            "Maximum Tokens",
            min_value=256,
            value=4096,
            step=256,
        )

        return {
            "provider": provider,
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

    # =====================================================
    # APPEARANCE
    # =====================================================

    def appearance(self):
        st.subheader("Appearance")

        theme = st.selectbox(
            "Theme",
            [t.value for t in ThemeMode],
            index=0,
        )

        animations = st.checkbox(
            "Enable Animations",
            value=True,
        )

        wide_layout = st.checkbox(
            "Wide Layout",
            value=True,
        )

        return {
            "theme": theme,
            "animations": animations,
            "wide_layout": wide_layout,
        }

    # =====================================================
    # FEATURES
    # =====================================================

    def features(self):
        st.subheader("Features")

        return {
            "memory": st.checkbox("Conversation Memory", True),
            "web_search": st.checkbox("Web Search", True),
            "rag": st.checkbox("RAG", True),
            "vision": st.checkbox("Vision", True),
            "speech": st.checkbox("Speech", True),
        }

    # =====================================================
    # SECURITY
    # =====================================================

    def security(self):
        st.subheader("Security")

        return {
            "save_history": st.checkbox(
                "Save Conversation History",
                True,
            ),
            "encrypt_data": st.checkbox(
                "Encrypt Local Data",
                False,
            ),
            "auto_delete": st.checkbox(
                "Auto Delete Temporary Files",
                True,
            ),
        }

    # =====================================================
    # SAVE
    # =====================================================

    def save(self, settings):

        if st.button(
            "💾 Save Settings",
            use_container_width=True,
        ):

            if self.repository is None:
                st.error(f"Database error: {self.error}")
                return

            if hasattr(self.repository, "save"):
                self.repository.save(settings)
                st.success("Settings saved successfully.")
            else:
                st.warning("SettingsRepository.save() is not implemented.")

    # =====================================================
    # MAIN
    # =====================================================

    def render(self):

        self.render_header()

        ai = self.ai_settings()

        st.divider()

        appearance = self.appearance()

        st.divider()

        features = self.features()

        st.divider()

        security = self.security()

        settings = {
            **ai,
            **appearance,
            **features,
            **security,
        }

        self.save(settings)


settings_component = SettingsComponent()
