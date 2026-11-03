"""Test database models."""
import pytest
from app.models import User


def test_user_creation(session):
    """Test creating a user model."""
    user = User(username='modeluser', email='model@example.com')
    session.add(user)
    session.commit()
    
    assert user.id is not None
    assert user.username == 'modeluser'
    assert user.email == 'model@example.com'
    assert user.created_at is not None


def test_user_repr(session):
    """Test user string representation."""
    user = User(username='repruser', email='repr@example.com')
    assert repr(user) == '<User repruser>'


def test_user_to_dict(session):
    """Test user to_dict method."""
    user = User(username='dictuser', email='dict@example.com')
    session.add(user)
    session.commit()
    
    user_dict = user.to_dict()
    
    assert user_dict['username'] == 'dictuser'
    assert user_dict['email'] == 'dict@example.com'
    assert 'id' in user_dict
    assert 'created_at' in user_dict


def test_user_query(session):
    """Test querying users."""
    # Create multiple users
    user1 = User(username='queryuser1', email='query1@example.com')
    user2 = User(username='queryuser2', email='query2@example.com')
    
    session.add(user1)
    session.add(user2)
    session.commit()
    
    # Query all users
    users = User.query.all()
    assert len(users) >= 2
    
    # Query specific user
    found_user = User.query.filter_by(username='queryuser1').first()
    assert found_user is not None
    assert found_user.username == 'queryuser1'


def test_user_unique_constraints(session):
    """Test unique constraints on username and email."""
    user1 = User(username='uniqueuser', email='unique@example.com')
    session.add(user1)
    session.commit()
    
    # Try to create another user with the same username
    user2 = User(username='uniqueuser', email='different@example.com')
    session.add(user2)
    
    with pytest.raises(Exception):
        session.commit()
