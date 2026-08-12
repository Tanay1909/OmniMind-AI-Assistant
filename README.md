# 🤖 OmniMind AI – Multimodal Intelligent Assistant

## 📌 Overview

OmniMind AI is a powerful **Multimodal Artificial Intelligence Assistant** developed as a **B.Tech Final Year Project**. It combines Large Language Models (LLMs), Computer Vision, Speech Processing, Document Intelligence, and Web Search into a single Streamlit application.

The assistant can understand and process multiple input modalities including text, images, PDFs, audio, and web information to provide intelligent and context-aware responses.

---

# 🚀 Features

### 💬 AI Chat

* Natural language conversations
* Context-aware responses
* Conversation history

### 🖼 Image Understanding

* Image captioning
* OCR (Extract text from images)
* Visual Question Answering
* Object understanding

### 📄 Document Intelligence

* PDF Question Answering
* Document Summarization
* Keyword Extraction
* Semantic Search

### 🎤 Voice Assistant

* Speech-to-Text
* Text-to-Speech
* Voice Conversations

### 🌐 Web Search

* Internet Search
* AI Generated Summaries
* Latest Information Retrieval

### 🧠 Memory

* Chat History
* Long-Term Memory
* Session Management

### 🤖 AI Agents

* Research Agent
* Coding Agent
* Document Agent
* Image Agent

---

# 🏗 Project Architecture

```text
User
      │
      ▼
 Streamlit UI
      │
      ▼
Core Assistant
      │
 ├── Chat Agent
 ├── Vision Agent
 ├── Voice Agent
 ├── Document Agent
 ├── Research Agent
      │
      ▼
LLMs + Vector Database + SQLite + Web Search
```

---

# 📂 Project Structure

```text
OmniMind_AI_Assistant/
│
├── app.py
├── config/
├── pages/
├── models/
├── services/
├── agents/
├── core/
├── utils/
├── database/
├── uploads/
├── exports/
├── assets/
├── tests/
└── docs/
```

---

# 🛠 Technologies Used

* Python
* Streamlit
* OpenAI API
* Google Gemini
* LangChain
* ChromaDB
* FAISS
* Sentence Transformers
* EasyOCR
* Whisper
* PyMuPDF
* SQLite
* Plotly

---

# 💻 Installation

Clone the repository:

```bash
git clone <repository-url>
```

Navigate to the project directory:

```bash
cd OmniMind_AI_Assistant
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file and add your API keys:

```text
OPENAI_API_KEY=your_key
GOOGLE_API_KEY=your_key
```

Run the application:

```bash
streamlit run app.py
```

---

# 📊 Future Scope

* Multi-user authentication
* Cloud deployment
* Mobile application
* Video understanding
* AI workflow automation
* Email and Calendar integration
* Local LLM support (Ollama)
* Advanced RAG
* Multi-agent collaboration

---

# 👨‍💻 Developer

**Tanay Sadhu**

B.Tech – Computer Science & Engineering

Vivekananda Global University, Jaipur

---

# 📄 License

This project is developed for educational and research purposes.
