# OmniMind AI Assistant

# API Reference

Version: 1.0.0

---

# Table of Contents

1. Overview
2. Base URL
3. Authentication
4. Common Response Format
5. Authentication APIs
6. Chat APIs
7. Document APIs
8. Image APIs
9. Audio APIs
10. OCR APIs
11. Translation APIs
12. Analytics APIs
13. User APIs
14. Health Check
15. Error Codes
16. Rate Limiting

---

# 1. Overview

OmniMind AI Assistant exposes REST APIs for AI services.

Supported Features:

- Authentication
- AI Chat
- Image Analysis
- Voice Processing
- OCR
- PDF Analysis
- Translation
- User Management
- Analytics

---

# 2. Base URL

Development

http://localhost:8000/api/v1

Production

https://your-domain.com/api/v1

---

# 3. Authentication

Every protected request must include:

Authorization: Bearer <JWT_TOKEN>

Example

Authorization: Bearer eyJhbGc...

---

# 4. Common Response Format

Success

{
    "success": true,
    "message": "Operation completed",
    "data": {}
}

Error

{
    "success": false,
    "message": "Invalid request",
    "error": "Detailed error"
}

---

# 5. Authentication APIs

## Login

POST /auth/login

Request

{
    "email":"user@example.com",
    "password":"password123"
}

Response

{
    "success":true,
    "token":"JWT_TOKEN",
    "user":{
        "id":1,
        "name":"Tanay"
    }
}

--------------------------------------

## Register

POST /auth/register

Request

{
    "name":"John",
    "email":"john@email.com",
    "password":"password"
}

Response

201 Created

--------------------------------------

## Logout

POST /auth/logout

Authorization Required

Response

200 OK

---

# 6. Chat APIs

## Generate AI Response

POST /chat

Request

{
    "prompt":"Explain Machine Learning"
}

Response

{
    "response":"Machine Learning is..."
}

--------------------------------------

## Conversation History

GET /chat/history

Response

[
    {
        "id":1,
        "message":"Hello"
    }
]

--------------------------------------

## Delete Conversation

DELETE /chat/{conversation_id}

---

# 7. Document APIs

## Upload PDF

POST /documents/upload

Multipart/Form-Data

Field

file

Response

{
    "document_id":45
}

--------------------------------------

## Ask Question

POST /documents/query

Request

{
    "document_id":45,
    "question":"Summarize this document"
}

Response

{
    "answer":"..."
}

--------------------------------------

## Delete Document

DELETE /documents/{id}

---

# 8. Image APIs

## Analyze Image

POST /image/analyze

Multipart/Form-Data

Response

{
    "objects":[
        "Laptop",
        "Person"
    ]
}

--------------------------------------

## Generate Image

POST /image/generate

Request

{
    "prompt":"Cyberpunk City"
}

Response

{
    "image_url":"..."
}

---

# 9. Audio APIs

## Speech To Text

POST /audio/transcribe

Multipart/Form-Data

Response

{
    "text":"Hello World"
}

--------------------------------------

## Text To Speech

POST /audio/speak

Request

{
    "text":"Hello"
}

Response

Audio File

---

# 10. OCR APIs

## Extract Text

POST /ocr

Multipart/Form-Data

Response

{
    "text":"Detected text..."
}

---

# 11. Translation APIs

POST /translate

Request

{
    "text":"Hello",
    "target_language":"Hindi"
}

Response

{
    "translation":"नमस्ते"
}

---

# 12. Analytics APIs

GET /analytics/dashboard

Response

{
    "users":125,
    "documents":95,
    "requests":5021
}

--------------------------------------

GET /analytics/activity

Returns recent user activity.

---

# 13. User APIs

GET /users/profile

Returns logged-in user.

--------------------------------------

PUT /users/profile

Update user profile.

--------------------------------------

DELETE /users/profile

Delete account.

---

# 14. Health Check

GET /health

Response

{
    "status":"healthy",
    "database":"connected",
    "ai_service":"online"
}

---

# 15. HTTP Status Codes

200 OK

201 Created

400 Bad Request

401 Unauthorized

403 Forbidden

404 Not Found

409 Conflict

422 Validation Error

429 Too Many Requests

500 Internal Server Error

503 Service Unavailable

---

# 16. Error Response

{
    "success":false,
    "message":"Authentication failed",
    "error_code":"AUTH_001"
}

---

# Rate Limiting

Default

100 requests/minute

Authenticated Users

500 requests/minute

Premium Users

Unlimited

---

# API Versioning

Current Version

v1

Future

v2

---

# Security

JWT Authentication

HTTPS

Input Validation

Password Hashing

API Rate Limiting

XSS Protection

SQL Injection Prevention

---

# Example cURL

Login

curl -X POST http://localhost:8000/api/v1/auth/login \
-H "Content-Type: application/json" \
-d '{
"email":"user@example.com",
"password":"password123"
}'

--------------------------------------

Generate Chat Response

curl -X POST http://localhost:8000/api/v1/chat \
-H "Authorization: Bearer TOKEN" \
-H "Content-Type: application/json" \
-d '{
"prompt":"Explain Artificial Intelligence"
}'

---

# API Best Practices

• Always use HTTPS in production

• Validate input before sending

• Refresh expired JWT tokens

• Handle HTTP status codes properly

• Implement retries for temporary failures

• Respect API rate limits

---

© 2026 OmniMind AI Assistant