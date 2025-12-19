# Quizly Backend – Django REST API

## Table of Contents

1. Introduction
2. Legal & Hosting Notice
3. Tech Stack
4. Architecture Overview
5. Authentication Concept
6. API Endpoints
7. CORS & CSRF Configuration
8. Local Development Setup
9. Requirements
10. Checklist / Definition of Done
11. Contact

---

## Introduction

This repository contains the **Django REST backend** for **Quizly**, an educational quiz application that allows users to generate quizzes from YouTube videos.

The backend is responsible for:

- User registration and authentication
- Secure session handling using JWT and HttpOnly cookies
- Quiz creation, storage, and management
- Integration with AI services for transcription and quiz generation
- Providing a REST API consumed by a separate frontend application

The frontend is **not included** in this repository and communicates exclusively via HTTP requests.

## Tech Stack

- Python 3.12
- Django
- Django REST Framework
- JWT Authentication (SimpleJWT)
- HttpOnly Cookies
- django-cors-headers
- SQLite (development)
- Postgresql (production)

---

## Architecture Overview

The backend follows a **clean and modular architecture**:

- `views.py`  
  Handles HTTP requests and responses only.
- `serializers.py`  
  Responsible for input validation and data transformation.
- `utils.py` / `services.py`  
  Contains business logic (e.g. token handling, helpers).
- `models.py`  
  Database models.
- `urls.py`  
  API routing.

This separation ensures readability, testability, and maintainability.

---

## Authentication Concept

Authentication is implemented using **JWT tokens stored in HttpOnly cookies**.

### Key principles

- No tokens are stored in localStorage or sessionStorage
- No Authorization headers are used by the frontend
- Tokens are inaccessible to JavaScript (HttpOnly)
- Cross-origin authentication is enabled via proper CORS configuration

### Token types

- **Access Token**
  - Short-lived
  - Used to authenticate protected API routes
- **Refresh Token**
  - Long-lived
  - Used to obtain new access tokens
  - Sent only via HttpOnly cookies

---

## API Endpoints

### Authentication

#### Register

```
POST /api/register/
```

Creates a new user account.

#### Login

```
POST /api/login/
```

Authenticates a user and sets access & refresh tokens as HttpOnly cookies.

#### Refresh Token

```
POST /api/token/refresh/
```

Renews the access token using the refresh token stored in an HttpOnly cookie.

**Success Response**

```json
{
  "detail": "Token refreshed",
  "access": "new_access_token"
}
```

Status Codes:

- 200 – Token refreshed
- 401 – Invalid or missing refresh token
- 500 – Internal server error

#### Logout

```
POST /api/logout/
```

Invalidates tokens and clears authentication cookies.

---

## CORS & CSRF Configuration

To support cookie-based authentication across origins, the backend uses:

- `django-cors-headers`
- Explicitly allowed origins (including port)
- `CORS_ALLOW_CREDENTIALS = True`
- Trusted CSRF origins for POST requests

Correct middleware ordering is essential for CORS to work properly.

---

## Local Development Setup

### 1. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run migrations

```bash
python manage.py migrate
```

### 4. Start development server

```bash
python manage.py runserver
```

Backend runs at:

```
http://127.0.0.1:8000
```

---

## Requirements

All Python dependencies are listed in `requirements.txt`.

Important runtime requirements:

- Python 3.12
- FFmpeg (required for audio processing via Whisper)
- Internet access for external AI services (Gemini API)

---

## Checklist / Definition of Done

- Clean code principles applied
- Functions limited in size and responsibility
- Snake_case naming conventions
- No unused or commented-out code
- Documentation via docstrings
- JWT authentication via HttpOnly cookies
- Backend & frontend separated via REST API
- Proper CORS & CSRF handling
- Admin panel supports quiz and question management

---

## Contact

\*\*Ahmet-Nafi Müftüoglus

- Portfolio: https://nafi.com
- Email: mail@nafi.com
- LinkedIn: https://www.linkedin.com/in/ahmet-nafi-m%C3%BCft%C3%BCoglu-9602aa398/

**Benjamin Tietz**

- Portfolio: https://benjamin-tietz.com
- Email: mail@benjamin-tietz.com
- LinkedIn: https://www.linkedin.com/in/benjamin-tietz/
