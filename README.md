# actions-flask

A Flask application with app factory pattern, PostgreSQL database, and Docker support.

## Features

- Flask app factory pattern
- PostgreSQL database with SQLAlchemy
- Configuration management with settings.py
- Docker Compose setup (Flask + PostgreSQL containers)
- Gunicorn for production deployment
- Dependency management with uv
- Pytest suite with testcontainers for isolated testing

## Project Structure

```
actions-flask/
├── app/
│   ├── __init__.py       # App factory
│   ├── models.py         # Database models
│   └── routes.py         # Application routes
├── tests/
│   ├── conftest.py       # Pytest fixtures with testcontainers
│   ├── test_app.py       # Route tests
│   └── test_models.py    # Model tests
├── settings.py           # Configuration settings
├── main.py              # Application entry point
├── Dockerfile           # Docker image definition
├── docker-compose.yml   # Docker Compose configuration
├── pyproject.toml       # Project dependencies
└── uv.lock             # Dependency lock file

```

## Setup

### Prerequisites

- Python 3.12+
- Docker and Docker Compose
- uv (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd actions-flask
```

2. Install dependencies with uv:
```bash
uv sync
```

3. Copy the environment file:
```bash
cp .env.example .env
```

## Running the Application

### With Docker Compose (Recommended)

Start both Flask and PostgreSQL containers:

```bash
docker-compose up --build
```

The application will be available at http://localhost:5000

### Local Development

1. Start PostgreSQL (via Docker or local installation):
```bash
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=flask_db postgres:16-alpine
```

2. Run the Flask app:
```bash
uv run python main.py
```

Or with Gunicorn:
```bash
uv run gunicorn --bind 0.0.0.0:5000 --workers 4 --reload main:app
```

## Testing

Run the test suite with pytest and testcontainers:

```bash
uv run pytest
```

The tests automatically spin up a PostgreSQL container using testcontainers, ensuring isolated and reproducible tests.

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check with database connection status
- `GET /users` - Get all users
- `POST /users` - Create a new user (JSON body: `{"username": "...", "email": "..."}`)
- `GET /users/<id>` - Get a specific user

## Configuration

Configuration is managed in `settings.py` with support for different environments:

- `development` - Development settings with debug enabled
- `testing` - Testing configuration
- `production` - Production settings

Set the environment via the `FLASK_ENV` environment variable.

## Environment Variables

- `FLASK_ENV` - Application environment (development/testing/production)
- `SECRET_KEY` - Flask secret key for sessions
- `DATABASE_URL` - PostgreSQL connection string
- `SQL_ECHO` - Enable SQL query logging (true/false)
