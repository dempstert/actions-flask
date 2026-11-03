"""Test Flask application routes."""
import pytest


def test_index(client):
    """Test the index route."""
    response = client.get('/')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['message'] == 'Welcome to Flask App'
    assert data['status'] == 'running'


def test_health(client):
    """Test the health check route."""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['database'] == 'connected'


def test_get_users_empty(client, session):
    """Test getting users when database is empty."""
    response = client.get('/users')
    assert response.status_code == 200
    
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_create_user(client, session):
    """Test creating a new user."""
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com'
    }
    
    response = client.post('/users', json=user_data)
    assert response.status_code == 201
    
    data = response.get_json()
    assert data['username'] == 'testuser'
    assert data['email'] == 'test@example.com'
    assert 'id' in data
    assert 'created_at' in data


def test_create_user_missing_data(client, session):
    """Test creating a user with missing data."""
    response = client.post('/users', json={'username': 'testuser'})
    assert response.status_code == 400
    
    data = response.get_json()
    assert 'error' in data


def test_get_users_with_data(client, session):
    """Test getting users after creating one."""
    # Create a user
    user_data = {
        'username': 'testuser2',
        'email': 'test2@example.com'
    }
    client.post('/users', json=user_data)
    
    # Get all users
    response = client.get('/users')
    assert response.status_code == 200
    
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1
    
    # Check the user we created is in the list
    usernames = [user['username'] for user in data]
    assert 'testuser2' in usernames


def test_get_user_by_id(client, session):
    """Test getting a specific user by ID."""
    # Create a user
    user_data = {
        'username': 'testuser3',
        'email': 'test3@example.com'
    }
    create_response = client.post('/users', json=user_data)
    created_user = create_response.get_json()
    user_id = created_user['id']
    
    # Get the user by ID
    response = client.get(f'/users/{user_id}')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['id'] == user_id
    assert data['username'] == 'testuser3'
    assert data['email'] == 'test3@example.com'


def test_get_user_not_found(client, session):
    """Test getting a non-existent user."""
    response = client.get('/users/99999')
    assert response.status_code == 404
