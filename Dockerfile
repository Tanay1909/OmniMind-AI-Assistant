
# ======================================================
# OmniMind AI - Dockerfile
# ======================================================

# ---------- Base Image ----------
FROM python:3.11-slim

# ---------- Environment ----------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# ---------- Working Directory ----------
WORKDIR /app

# ---------- System Dependencies ----------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    curl \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# ---------- Install Python Dependencies ----------
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# ---------- Copy Project ----------
COPY . .

# ---------- Create Required Directories ----------
RUN mkdir -p \
    database \
    uploads/images \
    uploads/audio \
    uploads/documents \
    uploads/temporary \
    exports/pdf \
    exports/csv \
    exports/chats \
    logs

# ---------- Streamlit ----------
EXPOSE 8501

# ---------- Health Check ----------
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# ---------- Start Application ----------
CMD ["streamlit", "run", "app.py", \
     "--server.address=0.0.0.0", \
     "--server.port=8501", \
     "--server.headless=true"]

