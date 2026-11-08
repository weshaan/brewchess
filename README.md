# Brewchess

Brewchess is a chess intelligence platform. This repository currently contains the Django backend foundation: project configuration, PostgreSQL wiring, and a lightweight health-check API. Chess features will be added in later increments.

## Technology stack

- Python 3.12+ (developed with Python 3.14)
- Django 5.2 LTS
- Django REST Framework
- PostgreSQL 16
- psycopg (PostgreSQL driver)
- django-environ
- pytest and pytest-django

## Backend structure

```text
brewchess/
├── backend/
│   ├── manage.py
│   ├── config/                 # Django project package
│   │   └── settings/           # base, local, production
│   ├── apps/
│   │   └── core/               # Shared infrastructure (health check)
│   ├── requirements.txt
│   └── pytest.ini
├── docker-compose.yml          # PostgreSQL service
├── .env.example
├── .gitignore
└── README.md
```

Reusable application code lives under `backend/apps/`. Project-level configuration lives under `backend/config/`.

## Prerequisites (macOS)

- Python 3.12 or newer (`python3 --version`)
- Docker Desktop (or Docker Engine) with Compose
- Git

Confirm Docker Compose is available with one of:

```bash
docker compose version
# or, on some macOS installs:
docker-compose version
```

## Setup

### 1. Create a virtual environment

From the repository root:

```bash
cd /path/to/brewchess
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install --upgrade pip
pip install -r backend/requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` if needed. At minimum, keep a non-empty `DJANGO_SECRET_KEY` and matching PostgreSQL values. Never commit `.env`.

### 4. Start PostgreSQL

```bash
docker compose up -d db
```

If your Docker install only provides the standalone binary:

```bash
docker-compose up -d db
```

Check that the container is healthy:

```bash
docker compose ps
# or: docker-compose ps
```

Stop the database when finished:

```bash
docker compose stop db
```

### 5. Run database migrations

```bash
cd backend
python manage.py migrate
```

### 6. Start Django

Still inside `backend/` with the virtual environment activated:

```bash
python manage.py runserver
```

The API listens on [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Test the health endpoint

```bash
curl http://127.0.0.1:8000/api/v1/health/
```

Expected response:

```json
{"status":"ok","service":"brewchess-api"}
```

## Run automated tests

From `backend/` with the virtual environment activated and `.env` configured:

```bash
cd backend
pytest
```

These foundation tests cover the health endpoint and a 404 for unknown API routes. They do not require a live PostgreSQL connection.

## Settings modules

Select the settings module with `DJANGO_SETTINGS_MODULE`:

| Value | Purpose |
| --- | --- |
| `config.settings.local` | Local development (default) |
| `config.settings.production` | Production |

`manage.py`, `wsgi.py`, and `asgi.py` default to `config.settings.local` when the variable is unset.

## Useful commands

```bash
# Django system checks
cd backend
python manage.py check

# Show migrations
python manage.py showmigrations
```
