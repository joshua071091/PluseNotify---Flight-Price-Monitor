# PulseNotify - Flight Price Alert System

## Overview

PulseNotify is a Django REST Framework application that allows users to create flight price alerts and receive notifications when flight prices fall below their configured threshold.

The application includes:

- JWT Authentication
- User Registration and Login
- Flight Price Alerts
- Mock Flight Price Feed API
- Celery Background Tasks
- Celery Beat Scheduler
- Redis Message Broker
- PostgreSQL Database
- Admin Analytics API
- Unit Tests

---

# Tech Stack

- Python 3.11+
- Django
- Django REST Framework
- JWT Authentication (SimpleJWT)
- PostgreSQL
- Redis
- Celery
- Celery Beat
- Docker Compose

---

# Project Structure

```text
pulsenotify/
│
├── manage.py
├── requirements.txt
├── docker-compose.yml
├── .env
│
├── pulse/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── permissions.py
│   ├── signals.py
│   ├── tasks.py
│   ├── tests.py
│   └── apps.py
│
└── pulsenotify/
    ├── __init__.py
    ├── celery.py
    ├── urls.py
    │
    └── settings/
        ├── __init__.py
        ├── base.py
        ├── local.py
        └── production.py
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone https://github.com/joshua071091/PluseNotify---Flight-Price-Monitor
cd pulsenotify
```

---

## 2. Create Virtual Environment

Linux/Mac:

```bash
python -m venv venv
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Create Environment File

Create `.env` in project root:

```env
SECRET_KEY=your_secret_key

DB_NAME=pulsenotify
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5433

DJANGO_SETTINGS_MODULE=pulsenotify.settings.local
```

---

# Docker Setup

## Start PostgreSQL and Redis

```bash
docker compose up -d
```

Verify containers:

```bash
docker ps
```

Expected containers:

```text
pulse_postgres
pulse_redis
```

---

# Database Setup

## Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---
# Running the Application

The application requires THREE separate processes:

1. Django Server
2. Celery Worker
3. Celery Beat Scheduler

Open three terminal windows.

---

## Terminal 1 – Django Server

```bash
python manage.py runserver
```

Expected:

```text
Starting development server at http://127.0.0.1:8000/
```

Application URL:

```text
http://127.0.0.1:8000/
```

---

## Terminal 2 – Celery Worker

```bash
celery -A pulsenotify worker --loglevel=info
```

Expected:

```text
celery@hostname ready
```

Purpose:

- Executes background tasks
- Sends notifications
- Processes queued jobs

---

## Terminal 3 – Celery Beat

```bash
celery -A pulsenotify beat --loglevel=info
```

Expected:

```text
Scheduler: Sending due task
```

Purpose:

- Runs scheduled jobs
- Triggers price checks every 60 seconds

---

# Running Tests

Execute all tests:

```bash
python manage.py test
```

Expected:

```text
Ran 5 tests

OK
```

Tests Covered:

- Price Threshold Logic
- Notification Log Creation
- User Alert Scoping

---

# Authentication

JWT Authentication is used.

Header format:

```http
Authorization: Bearer <access_token>
```

---

# API Endpoints

## Register

### POST

```http
/api/auth/register/
```

Request:

```json
{
  "username": "alice",
  "password": "securepass",
  "email": "alice@example.com"
}
```

---

## Login

### POST

```http
/api/auth/login/
```

Request:

```json
{
  "username": "alice",
  "password": "securepass"
}
```

Response:

```json
{
  "access": "jwt_token"
}
```

---

## Create Alert

### POST

```http
/api/alerts/
```

Request:

```json
{
  "origin": "DEL",
  "destination": "BOM",
  "threshold_price": 4500
}
```

---

## List Alerts

### GET

```http
/api/alerts/
```

---

## Deactivate Alert

### DELETE

```http
/api/alerts/<id>/
```

---

## Mock Flight Price Feed

### GET

```http
/api/flights/price/?route=DEL-BOM
```

Response:

```json
{
  "route": "DEL-BOM",
  "price": 4200
}
```

---

## Admin Summary

### GET

```http
/api/admin/summary/
```

Admin users only.

Response:

```json
{
  "total_alerts": 10,
  "active_alerts": 6,
  "triggered_alerts": 3,
  "total_notifications": 3,
  "top_routes": [
    {
      "route": "DEL-BOM",
      "alert_count": 5
    }
  ]
}
```

---

# Celery Workflow

1. User creates alert
2. Alert stored as ACTIVE
3. Celery Beat runs every 60 seconds
4. Beat triggers check_prices task
5. Task calls mock flight API
6. Price compared with threshold
7. If price <= threshold:
   - send_notification task executed
   - NotificationLog created
   - Alert status changed to TRIGGERED

---

# Required Submission Files

Include:

- Source Code
- README.md
- requirements.txt
- docker-compose.yml
- Postman Collection JSON
- Unit Tests

---

# Assignment Requirements Covered

- JWT Authentication
- PostgreSQL
- Redis
- Celery Worker
- Celery Beat
- Django Signals
- Custom Permissions
- DRF Serializers
- Unit Tests
- Docker Support
- REST APIs
- Admin Analytics

---

# Author

Joshua Rajkumar

Senior Backend Developer