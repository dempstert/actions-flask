"""Pytest configuration and fixtures."""
import os
import pytest
from testcontainers.postgres import PostgresContainer
from app import create_app, db as _db


@pytest.fixture(scope='session')
def postgres_container():
    """Create a PostgreSQL container for testing."""
    postgres = PostgresContainer("postgres:16-alpine")
    postgres.start()
    
    yield postgres
    
    postgres.stop()


@pytest.fixture(scope='session')
def app(postgres_container):
    """Create application for testing."""
    # Set the test database URL from the container
    db_url = postgres_container.get_connection_url()
    os.environ['TEST_DATABASE_URL'] = db_url
    
    # Create the app with testing configuration
    app = create_app('testing')
    
    # Establish an application context
    ctx = app.app_context()
    ctx.push()
    
    yield app
    
    ctx.pop()


@pytest.fixture(scope='session')
def db(app):
    """Create database for testing."""
    _db.create_all()
    
    yield _db
    
    _db.drop_all()


@pytest.fixture(scope='function')
def session(db, app):
    """Create a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()
    
    # Bind the session to the connection
    session_options = dict(bind=connection, binds={})
    session = db.session
    session.configure(**session_options)
    
    yield session
    
    # Rollback transaction
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()
