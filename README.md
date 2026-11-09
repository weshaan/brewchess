# Brewchess

Brewchess is a chess intelligence platform. This repository currently contains the Django backend foundation plus core database models for users and chess games. Authentication APIs, PGN upload flows, and analysis features will be added in later increments.

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
│   │   ├── core/               # Shared infrastructure (health check)
│   │   ├── users/              # Custom user model
│   │   └── games/              # Chess game model
│   ├── requirements.txt
│   └── pytest.ini
├── docker-compose.yml          # PostgreSQL service
├── .env.example
├── .gitignore
└── README.md
```

Reusable application code lives under `backend/apps/`. Project-level configuration lives under `backend/config/`.

## Applications and models

### `users`

Owns the custom user model (`AUTH_USER_MODEL = users.User`), based on Django's `AbstractUser`.

Key fields:

- `username` (unique), `email` (unique), `password`
- `first_name`, `last_name`
- `is_active`, `is_staff`, `date_joined`
- `created_at`, `updated_at`

Passwords use Django's built-in hashing. This app does not yet expose registration or login APIs.

### `games`

Owns the `ChessGame` model. Each game belongs to one user (`ForeignKey`, `CASCADE` on delete). A user may own many games.

Key fields:

- UUID primary key
- `white_player`, `black_player`, `result`, `pgn`
- Optional metadata: `played_at`, `event`, `site`, `time_control`
- `variant` (currently `standard` only)
- `created_at`, `updated_at`

Supported results: `1-0`, `0-1`, `1/2-1/2`, `*`.

Indexes support listing a user's games by `played_at` and `created_at`.

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

If you previously migrated Feature 1 before the custom user model existed, recreate the local Postgres volume once, then migrate:

```bash
docker-compose down -v
docker-compose up -d db
cd backend
python manage.py migrate
```

This deletes local database data only. It is expected for early local development.

### 6. Create a Django superuser

```bash
cd backend
python manage.py createsuperuser
```

Follow the prompts for username, email, and password.

### 7. Start Django

Still inside `backend/` with the virtual environment activated:

```bash
python manage.py runserver
```

The API listens on [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

Django Admin is available at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) after you create a superuser.

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

Foundation tests cover the health endpoint. Model tests cover the custom user and `ChessGame` behaviour and require PostgreSQL (pytest-django creates a test database).

```bash
# Run only model tests
pytest apps/users apps/games
```

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
