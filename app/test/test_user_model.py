"""app/test/test_user_model.py"""

import pytest
from app.models import User, db

class TestUserModel:
    @pytest.fixture
    def user1(self):
        user = User(username="testuser1", email="test1@example.com")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        return user

    @pytest.fixture
    def user2(self):
        user = User(username="testuser2", email="test2@example.com")
        user.set_password("password456")
        db.session.add(user)
        db.session.commit()
        return user

    def test_repr(self, user1):
        """Does the __repr__ method work as expected?"""
        assert repr(user1) == f"<User #{user1.id}: testuser1, test1@example.com, Location: None>"

    def test_is_following(self, user1, user2):
        """Does is_following detect when user1 is following user2?"""
        user1.following.append(user2)
        db.session.commit()
        assert user1.is_following(user2) is True

    def test_is_not_following(self, user1, user2):
        """Does is_following detect when user1 is not following user2?"""
        assert user1.is_following(user2) is False

    def test_is_followed_by(self, user1, user2):
        """Does is_followed_by detect when user1 is followed by user2?"""
        user2.following.append(user1)
        db.session.commit()
        assert user1.is_followed_by(user2) is True

    def test_is_not_followed_by(self, user1, user2):
        """Does is_followed_by detect when user1 is not followed by user2?"""
        assert user1.is_followed_by(user2) is False

    def test_user_creation(self):
        """Does User.create successfully create a new user?"""
        user = User.signup(username="newuser", email="new@example.com", password="password789")
        assert user.id is not None

    def test_user_creation_validation_failure(self):
        """Does User.create fail with invalid data?"""
        with pytest.raises(ValueError):
            User.signup(username=None, email="invalid@example.com", password="password789")

    def test_user_authenticate_success(self, user1):
        """Does User.authenticate return a user with valid credentials?"""
        authenticated_user = User.authenticate(username="testuser1", password="password123")
        assert authenticated_user == user1

    def test_user_authenticate_invalid_username(self, user1):
        """Does User.authenticate fail with an invalid username?"""
        assert User.authenticate(username="wronguser", password="password123") is False

    def test_user_authenticate_invalid_password(self, user1):
        """Does User.authenticate fail with an invalid password?"""
        assert User.authenticate(username="testuser1", password="wrongpassword") is False
