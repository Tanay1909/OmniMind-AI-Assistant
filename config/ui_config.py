"""
=========================================================
OmniMind AI Assistant
UI Configuration
=========================================================
"""

from dataclasses import dataclass

# ==========================================================
# APP INFORMATION
# ==========================================================

APP_TITLE = "🤖 OmniMind AI"

APP_SUBTITLE = (
    "An Intelligent Multimodal AI Assistant powered by " "Large Language Models"
)

APP_ICON = "🤖"

APP_LOGO = "assets/logo/logo.png"

FAVICON = "🤖"

# ==========================================================
# PAGE SETTINGS
# ==========================================================

PAGE_LAYOUT = "wide"

SIDEBAR_STATE = "expanded"

# ==========================================================
# THEME
# ==========================================================

PRIMARY_COLOR = "#4F46E5"

SECONDARY_COLOR = "#7C3AED"

SUCCESS_COLOR = "#16A34A"

WARNING_COLOR = "#F59E0B"

ERROR_COLOR = "#DC2626"

INFO_COLOR = "#2563EB"

BACKGROUND_COLOR = "#F8FAFC"

CARD_BACKGROUND = "#FFFFFF"

TEXT_COLOR = "#111827"

# ==========================================================
# FONTS
# ==========================================================

FONT_FAMILY = "Inter"

TITLE_SIZE = 36

HEADER_SIZE = 28

TEXT_SIZE = 16

# ==========================================================
# SIDEBAR
# ==========================================================

SIDEBAR_WIDTH = 320

# ==========================================================
# CHAT
# ==========================================================

USER_AVATAR = "👤"

BOT_AVATAR = "🤖"

WELCOME_MESSAGE = """
Welcome to **OmniMind AI** 👋

I can help you with:

• 💬 AI Chat

• 🖼 Image Analysis

• 📄 Document Question Answering

• 🎤 Voice Assistant

• 🌐 Web Search

• 🤖 AI Agents

Ask me anything!
"""

# ==========================================================
# DASHBOARD CARDS
# ==========================================================

METRIC_CARDS = [
    "AI Models",
    "Documents",
    "Images",
    "Voice",
    "Memory",
    "Analytics",
]

# ==========================================================
# SIDEBAR MENU
# ==========================================================

NAVIGATION = [
    ("🏠", "Home"),
    ("💬", "AI Chat"),
    ("📄", "Document Chat"),
    ("🖼", "Image Analysis"),
    ("🎤", "Voice Assistant"),
    ("🌐", "Web Search"),
    ("🤖", "AI Agents"),
    ("📊", "Analytics"),
    ("📜", "History"),
    ("⚙", "Settings"),
]

# ==========================================================
# FILE UPLOAD
# ==========================================================

UPLOAD_HELP = "Supported formats: PDF, DOCX, TXT, PNG, JPG, JPEG, " "WEBP, MP3, WAV"

# ==========================================================
# ANIMATIONS
# ==========================================================

ENABLE_ANIMATIONS = True

ENABLE_SPINNER = True

ENABLE_PROGRESS_BAR = True

# ==========================================================
# BUTTON LABELS
# ==========================================================

BUTTONS = {
    "send": "🚀 Send",
    "upload": "📤 Upload",
    "clear": "🗑 Clear Chat",
    "download": "⬇ Download",
    "analyze": "🔍 Analyze",
    "summarize": "📝 Summarize",
    "search": "🌐 Search",
    "record": "🎙 Record",
}

# ==========================================================
# FOOTER
# ==========================================================

FOOTER = "Built with ❤️ using Streamlit • Gemini • Groq " "© 2026 Tanay Sadhu"

# ==========================================================
# CSS
# ==========================================================

CUSTOM_CSS = "assets/css/style.css"

# ==========================================================
# LOADING TEXT
# ==========================================================

LOADING_MESSAGES = [
    "Thinking...",
    "Analyzing...",
    "Understanding your request...",
    "Searching relevant information...",
    "Generating response...",
]

# ==========================================================
# DATACLASS
# ==========================================================


@dataclass(frozen=True)
class UIConfig:
    title: str = APP_TITLE
    icon: str = APP_ICON
    layout: str = PAGE_LAYOUT
    sidebar: str = SIDEBAR_STATE


UI = UIConfig()
