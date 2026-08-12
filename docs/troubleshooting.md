# OmniMind AI Assistant

# Troubleshooting Guide

Version: 1.0.0

---

# Table of Contents

1. Introduction
2. Installation Issues
3. Python Environment Issues
4. Dependency Problems
5. Streamlit Issues
6. Database Issues
7. Authentication Issues
8. AI Service Issues
9. Document Processing Issues
10. Image Processing Issues
11. Audio Processing Issues
12. Deployment Issues
13. Docker Issues
14. Performance Issues
15. Logging and Debugging
16. Frequently Used Commands
17. Support

---

# 1. Introduction

This guide provides solutions for the most common problems encountered while using or developing OmniMind AI Assistant.

Before troubleshooting:

✔ Verify your Python version

✔ Check environment variables

✔ Confirm internet connectivity

✔ Review application logs

✔ Ensure all dependencies are installed

---

# 2. Installation Issues

## Problem

ModuleNotFoundError

Example

ModuleNotFoundError: No module named 'streamlit'

Solution

```bash
pip install -r requirements.txt
```

----------------------------------------

## Problem

Python version not supported

Solution

Check version

```bash
python --version
```

Recommended

Python 3.11+

----------------------------------------

## Problem

Virtual environment not activated

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

---

# 3. Python Environment Issues

## Multiple Python versions

Check

```bash
where python
```

Linux

```bash
which python3
```

----------------------------------------

## Pip not found

Solution

```bash
python -m ensurepip

python -m pip install --upgrade pip
```

---

# 4. Dependency Problems

## Missing package

Install

```bash
pip install package_name
```

----------------------------------------

## Reinstall everything

```bash
pip uninstall -r requirements.txt -y

pip install -r requirements.txt
```

----------------------------------------

## Dependency conflict

```bash
pip check
```

Upgrade

```bash
pip install --upgrade pip setuptools wheel
```

---

# 5. Streamlit Issues

## Application won't start

Run

```bash
streamlit run app.py
```

----------------------------------------

## Port already in use

```bash
streamlit run app.py --server.port 8502
```

----------------------------------------

## Blank page

Possible causes

- Browser cache
- JavaScript disabled
- Runtime error

Solution

Refresh browser

Restart Streamlit

Review terminal logs

---

# 6. Database Issues

## Database connection failed

Check

DATABASE_URL

----------------------------------------

SQLite

Delete corrupted database

Reinitialize

```bash
python database/init_db.py
```

----------------------------------------

PostgreSQL

Verify

- Username
- Password
- Host
- Port

Test

```bash
psql
```

---

# 7. Authentication Issues

## Login failed

Verify

- Email
- Password

----------------------------------------

## JWT expired

Generate new login token.

----------------------------------------

## Invalid credentials

Reset password.

Clear browser cookies if necessary.

---

# 8. AI Service Issues

## API key missing

Verify

.env

Contains

OPENAI_API_KEY

----------------------------------------

## Rate limit exceeded

Wait a few minutes.

Reduce request frequency.

----------------------------------------

## AI response timeout

Possible causes

- Slow network
- Provider outage
- Large prompt

Retry request.

---

# 9. Document Processing Issues

## PDF upload fails

Verify

Supported format

PDF

----------------------------------------

Maximum file size

Check application configuration.

----------------------------------------

OCR not working

Verify

Tesseract installed

Correct language packs installed

---

# 10. Image Processing Issues

## Unsupported image format

Supported

PNG

JPG

JPEG

WEBP

----------------------------------------

## Image analysis failed

Check

- Image quality
- File corruption
- File size

---

# 11. Audio Processing Issues

## Microphone unavailable

Verify browser permission.

----------------------------------------

## Speech recognition failed

Speak clearly.

Check microphone.

Verify internet connection.

----------------------------------------

## No audio output

Check speakers.

Verify TTS configuration.

---

# 12. Deployment Issues

## Application inaccessible

Check

Firewall

Reverse Proxy

Port

----------------------------------------

## HTTPS not working

Verify

SSL certificate

DNS records

Nginx configuration

---

# 13. Docker Issues

## Container won't start

Check logs

```bash
docker logs container_name
```

----------------------------------------

Restart

```bash
docker compose down

docker compose up -d
```

----------------------------------------

Rebuild

```bash
docker compose build
```

---

# 14. Performance Issues

Symptoms

- Slow response
- High CPU
- High RAM
- Delayed AI responses

Solutions

✔ Cache repeated requests

✔ Optimize prompts

✔ Reduce image size

✔ Use GPU when available

✔ Monitor database performance

✔ Archive old logs

---

# 15. Logging and Debugging

Application logs

```bash
logs/application.log
```

Enable debug

.env

```env
DEBUG=True
```

Python logging example

```python
import logging

logger = logging.getLogger(__name__)

logger.info("Application Started")

logger.error("Unexpected Error")
```

---

# 16. Frequently Used Commands

Run application

```bash
streamlit run app.py
```

Run tests

```bash
pytest
```

Coverage

```bash
pytest --cov=.
```

Install dependencies

```bash
pip install -r requirements.txt
```

Update packages

```bash
pip install --upgrade -r requirements.txt
```

Docker

```bash
docker compose up -d
```

View logs

```bash
docker logs container_name
```

---

# Troubleshooting Checklist

✔ Python version correct

✔ Virtual environment active

✔ Dependencies installed

✔ Environment variables configured

✔ Database running

✔ AI API keys configured

✔ Internet available

✔ Streamlit running

✔ Docker healthy (if used)

✔ Logs reviewed

---

# Support

If the issue persists:

1. Review application logs.
2. Search existing project issues.
3. Contact the project maintainer.
4. Include:
   - Error message
   - Operating system
   - Python version
   - Steps to reproduce

---

# Conclusion

Most issues can be resolved by checking the Python environment, dependencies, configuration, logs, and API credentials. Always verify the environment before investigating application logic.

---

© 2026 OmniMind AI Assistant