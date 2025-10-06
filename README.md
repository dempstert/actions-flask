# actions-flask
Run github actions w/ flask

## Setup

This project uses Flask with SQLAlchemy and Alembic for database migrations.

### Requirements

- Python 3.12+
- See `requirements.txt` for Python package dependencies

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run database migrations:
```bash
alembic upgrade head
```

3. Run the Flask application:
```bash
python app.py
```

## Project Structure

- `requirements.txt` - Python dependencies (Flask, SQLAlchemy, Flask-SQLAlchemy, Alembic)
- `base.py` - SQLAlchemy DeclarativeBase with metadata naming conventions
- `extensions.py` - Flask extensions (Flask-SQLAlchemy)
- `models.py` - Database models (Example table with id and description)
- `app.py` - Flask application factory
- `alembic/` - Database migration files
- `alembic.ini` - Alembic configuration

## Database Migrations

This project uses Alembic for database migrations.

### Create a new migration
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations
```bash
alembic upgrade head
```

### Rollback migrations
```bash
alembic downgrade -1
```

### View migration history
```bash
alembic history
```

### View current migration
```bash
alembic current
```

## Models

The project includes an example model (`Example`) with:
- `id` - Integer primary key
- `description` - String(255), not null

The DeclarativeBase in `base.py` includes metadata with naming conventions for:
- Indexes: `ix_%(column_0_label)s`
- Unique constraints: `uq_%(table_name)s_%(column_0_name)s`
- Check constraints: `ck_%(table_name)s_%(constraint_name)s`
- Foreign keys: `fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s`
- Primary keys: `pk_%(table_name)s`
