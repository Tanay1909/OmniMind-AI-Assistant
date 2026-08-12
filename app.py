import streamlit as st
from config.config import PAGE_TITLE, PAGE_ICON

# -----------------------------
# Streamlit Page Configuration
# -----------------------------
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Custom CSS
# -----------------------------
try:
    with open("assets/css/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# -----------------------------
# Session State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "GPT-5.5"

# -----------------------------
# Home Page
# -----------------------------
st.title("🤖 OmniMind AI Assistant")

st.markdown("""
### Your Intelligent Multimodal AI Assistant

OmniMind AI is capable of understanding:

- 💬 Text Chat
- 🖼 Image Analysis
- 📄 Document Question Answering
- 🎤 Voice Assistant
- 🌐 Web Search
- 🧠 Long-Term Memory
- 🔍 RAG (Retrieval-Augmented Generation)
- 🤖 AI Agents
""")

st.info("Use the sidebar to navigate through the different modules.")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Supported Models", "3+")

with col2:
    st.metric("Input Types", "5")

with col3:
    st.metric("AI Features", "10+")

st.divider()

st.subheader("🚀 Quick Start")

st.markdown("""
1. Select a feature from the sidebar.
2. Upload an image, document, or audio file—or start chatting.
3. Choose your preferred AI model in the Settings page.
4. View and export your conversation history anytime.
""")

st.success("OmniMind AI is ready!")
