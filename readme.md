# Quizly Backend – Django REST API

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Deployment with Docker Compose](#deployment-with-docker-compose)
4. [Quickstart](#quickstart)
5. [Usage](#usage)
6. [Tech Stack](#tech-stack)
7. [Architecture Overview](#architecture-overview)
8. [Authentication Concept](#authentication-concept)
9. [API Documentation](#api-documentation)
10. [CORS & CSRF Configuration](#cors--csrf-configuration)
11. [Local Development (without Docker)](#local-development-without-docker)
12. [Requirements](#requirements)
13. [Contact](#contact)

---

## Introduction

This repository contains the **Django REST backend** for **Quizly**, an educational quiz application that allows users to generate quizzes from YouTube videos using AI-based transcription and question generation.

The backend is responsible for:

- User registration and authentication
- Secure session handling using JWT stored in HttpOnly cookies
- Quiz creation, storage, and evaluation
- Integration with external AI services
- Providing a REST API consumed by a separate frontend

The frontend is **not included** in this repository and communicates exclusively via HTTP requests.

---

## Prerequisites

- Linux server (Ubuntu/Debian recommended)
- Docker & Docker Compose
- Git

Install Docker if not already available:

```bash
sudo apt update && sudo apt install -y docker.io docker-compose
```

---

## Deployment with Docker Compose

The backend is deployed using **Docker Compose** with two isolated services:

- **backend** – Django + Gunicorn
- **db** – PostgreSQL database

All configuration is handled via environment variables defined in a `.env` file.

### Services Overview

- Backend listens on **port 8000**
- PostgreSQL runs inside the Docker network (not publicly exposed)
- Static files are served using **WhiteNoise**
- A Django superuser is created automatically on first startup (optional)

---

## Quickstart

### 1. Clone the repository

```bash
git clone https://github.com/BenjaminTietz/quizzly-backend.git
cd quizzly-backend
```

### 2. Create environment file

```bash
cp .env.template .env
```

Adjust values if needed (database credentials, superuser, secrets).

### 3. Build and start containers

```bash
docker compose build
docker compose up -d
```

### 4. Verify running containers

```bash
docker compose ps
```

### 5. Access the application

- Backend API:  
  `http://<your-server-ip>:8000`

- Django Admin Panel:  
  `http://<your-server-ip>:8000/admin/`

If configured in `.env`, a superuser is created automatically.

---

## Usage

### Create a superuser manually (optional)

```bash
docker compose exec backend python manage.py createsuperuser
```

### View logs

```bash
docker compose logs -f backend
docker compose logs -f db
```

### Stop the application

```bash
docker compose down
```

---

## Tech Stack

- Python 3.11
- Django
- Django REST Framework
- PostgreSQL
- Gunicorn
- WhiteNoise (static files)
- JWT Authentication (SimpleJWT)
- HttpOnly Cookies
- Docker & Docker Compose

---

## Architecture Overview

The backend follows a **clean and modular architecture**:

- `views.py` – HTTP request/response handling
- `serializers.py` – Input validation and transformation
- `services.py` – Business logic
- `models.py` – Database models
- `urls.py` – API routing

This structure ensures readability, testability, and scalability.

---

## Authentication Concept

Authentication is implemented using **JWT tokens stored in HttpOnly cookies**.

### Key principles

- No tokens in localStorage or sessionStorage
- No Authorization headers required
- Tokens inaccessible to JavaScript
- Secure cross-origin authentication via CORS & CSRF configuration

### Token types

- **Access Token** – short-lived, protects API endpoints
- **Refresh Token** – long-lived, renews access tokens

---

## API Documentation

Detailed API documentation is available here:

➡️ [API.md](./api.md)

---

## CORS & CSRF Configuration

- `django-cors-headers`
- Explicit allowed origins
- `CORS_ALLOW_CREDENTIALS = True`
- Trusted CSRF origins
- Correct middleware order enforced

---

## Local Development (without Docker)

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Backend runs at:

```
http://127.0.0.1:8000
```

---

## Requirements

- Python 3.11 (local development)
- Docker & Docker Compose (deployment)
- FFmpeg (audio processing)
- Internet access for external AI services

---

## Contact

### 👤 Contributors

**Ahmet-Nafi Müftüoglu**

- Portfolio: https://nafi.com
- Mail: mail@nafi.com
- LinkedIn: https://www.linkedin.com/in/ahmet-nafi-m%C3%BCft%C3%BCoglu-9602aa398/

**Benjamin Tietz**

- Portfolio: https://benjamin-tietz.com
- Mail: mail@benjamin-tietz.com
- LinkedIn: https://www.linkedin.com/in/benjamin-tietz/
