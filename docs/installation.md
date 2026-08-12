# OmniMind AI Assistant

## Installation Guide

Version: 1.0.0

---

# Table of Contents

1. Introduction
2. System Requirements
3. Project Structure
4. Clone Repository
5. Create Virtual Environment
6. Install Dependencies
7. Environment Variables
8. Database Setup
9. Running the Project
10. Running Tests
11. Common Installation Errors
12. Updating the Project

---

# 1. Introduction

OmniMind AI Assistant is an enterprise-grade multimodal AI assistant built with Python and Streamlit.

Features include:

- AI Chat
- Vision AI
- Voice Assistant
- Document QA
- OCR
- Image Generation
- Speech Recognition
- Translation
- PDF Analysis
- Database Support
- Authentication
- Analytics Dashboard

---

# 2. System Requirements

Minimum Requirements

- Windows 10 / Ubuntu 22.04 / macOS
- Python 3.11+
- Git
- pip
- 8 GB RAM
- 5 GB Free Disk Space

Recommended

- Python 3.11
- 16 GB RAM
- SSD Storage
- NVIDIA GPU (Optional)

---

# 3. Clone Repository

```bash
git clone https://github.com/yourusername/OmniMind_AI_Assistant.git

cd OmniMind_AI_Assistant
```

---

# 4. Create Virtual Environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

# 5. Install Dependencies

Upgrade pip

```bash
python -m pip install --upgrade pip
```

Install project packages

```bash
pip install -r requirements.txt
```

---

# 6. Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
OPENAI_API_KEY=your_api_key

GOOGLE_API_KEY=your_google_key

DATABASE_URL=sqlite:///database.db

SECRET_KEY=change_this_secret

DEBUG=True
```

---

# 7. Database Setup

SQLite

```bash
python database/init_db.py
```

PostgreSQL

Update the `.env` file:

```env
DATABASE_URL=postgresql://user:password@localhost/omnimind
```

Run migrations

```bash
alembic upgrade head
```

---

# 8. Run the Application

```bash
streamlit run app.py
```

Open

```
http://localhost:8501
```

---

# 9. Run Unit Tests

Run all tests

```bash
pytest
```

Generate coverage report

```bash
pytest --cov=.
```

Verbose mode

```bash
pytest -v
```

---

# 10. Verify Installation

The following features should work:

- Login Screen
- Dashboard
- AI Chat
- File Upload
- PDF Analysis
- Voice Assistant
- Image Processing
- Database Connection
- Settings Page

---

# 11. Common Installation Errors

### ModuleNotFoundError

Solution

```bash
pip install -r requirements.txt
```

---

### OpenAI API Key Missing

Solution

Create

```
.env
```

Add

```env
OPENAI_API_KEY=your_key
```

---

### Streamlit Not Found

```bash
pip install streamlit
```

---

### Database Error

Run

```bash
python database/init_db.py
```

---

### Port Already in Use

```bash
streamlit run app.py --server.port 8502
```

---

# 12. Updating Project

Pull latest version

```bash
git pull origin main
```

Update packages

```bash
pip install -r requirements.txt --upgrade
```

Run migrations

```bash
alembic upgrade head
```

---

# Installation Checklist

- Python Installed
- Virtual Environment Created
- Dependencies Installed
- Environment Variables Configured
- Database Initialized
- Streamlit Running
- Tests Passing

---

# Support

GitHub Issues

Create an issue for bugs and feature requests.

---

# License

MIT License

---

© 2026 OmniMind AI Assistant