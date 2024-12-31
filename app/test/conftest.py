"""app/test/conftest.py"""

import pytest
from app import create_app, db
from app.models import User, Message

@pytest.fixture(scope="module")
def app():
    """Set up Flask app for testing."""
    app = create_app("testing")  # Ensure 'testing' config uses a test database
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="module")
def client(app):
    """Set up Flask test client."""
    return app.test_client()

@pytest.fixture(scope="function")
def setup_db():
    """Ensure clean database before each test."""
    db.session.rollback()  # Rollback any open transactions
    db.session.query(User).delete()
    db.session.query(Message).delete()
    db.session.commit()


@pytest.fixture
def setup_users():
    user1 = User(username="user1", email="user1@example.com")
    user1.set_password("password")
    user2 = User(username="user2", email="user2@example.com")
    user2.set_password("password")
    db.session.add_all([user1, user2])
    db.session.commit()
    return user1, user2
