 
"""
=========================================================
OmniMind AI Assistant
Session Manager
=========================================================

Centralized Streamlit session state management.
"""

from __future__ import annotations

from typing import Any

import streamlit as st


class SessionManager:
    """
    Manages Streamlit session state.
    """

    DEFAULT_STATE = {
        "messages": [],
        "chat_history": [],
        "current_chat": None,
        "selected_model": "GPT-5.5",
        "temperature": 0.7,
        "uploaded_files": [],
        "memory": {},
        "theme": "Light",
        "language": "English",
        "user_preferences": {},
        "analytics": {},
        "authenticated": False,
    }

    @classmethod
    def initialize(cls) -> None:
        """Initialize session state."""

        for key, value in cls.DEFAULT_STATE.items():
            if key not in st.session_state:
                if isinstance(value, (list, dict)):
                    st.session_state[key] = value.copy()
                else:
                    st.session_state[key] = value

    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """Get a session value."""

        return st.session_state.get(key, default)

    @staticmethod
    def set(key: str, value: Any) -> None:
        """Set a session value."""

        st.session_state[key] = value

    @staticmethod
    def exists(key: str) -> bool:
        """Check if a key exists."""

        return key in st.session_state

    @staticmethod
    def delete(key: str) -> None:
        """Delete a session key."""

        if key in st.session_state:
            del st.session_state[key]

    @staticmethod
    def clear() -> None:
        """Clear the entire session."""

        st.session_state.clear()

    # =====================================================
    # CHAT
    # =====================================================

    @classmethod
    def add_message(
        cls,
        role: str,
        content: str,
    ) -> None:
        """Add a chat message."""

        messages = cls.get("messages", [])

        messages.append({
            "role": role,
            "content": content,
        })

        cls.set("messages", messages)

    @classmethod
    def get_messages(cls):
        """Return chat messages."""

        return cls.get("messages", [])

    @classmethod
    def clear_chat(cls):
        """Clear chat history."""

        cls.set("messages", [])

    # =====================================================
    # FILES
    # =====================================================

    @classmethod
    def add_uploaded_file(cls, file_name: str):
        files = cls.get("uploaded_files", [])

        files.append(file_name)

        cls.set("uploaded_files", files)

    # =====================================================
    # MODEL
    # =====================================================

    @classmethod
    def get_model(cls):
        return cls.get("selected_model")

    @classmethod
    def set_model(cls, model: str):
        cls.set("selected_model", model)

    # =====================================================
    # TEMPERATURE
    # =====================================================

    @classmethod
    def set_temperature(cls, value: float):
        cls.set("temperature", value)

    @classmethod
    def get_temperature(cls):
        return cls.get("temperature")

    # =====================================================
    # MEMORY
    # =====================================================

    @classmethod
    def set_memory(cls, key: str, value: Any):
        memory = cls.get("memory", {})
        memory[key] = value
        cls.set("memory", memory)

    @classmethod
    def get_memory(cls):
        return cls.get("memory", {})

    # =====================================================
    # USER PREFERENCES
    # =====================================================

    @classmethod
    def set_preference(cls, key: str, value: Any):
        prefs = cls.get("user_preferences", {})
        prefs[key] = value
        cls.set("user_preferences", prefs)

    @classmethod
    def get_preferences(cls):
        return cls.get("user_preferences", {})