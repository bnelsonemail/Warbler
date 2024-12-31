"""app/test/test_message_model.py"""

import pytest
from app.models import Message, db

class TestMessageModel:
    @pytest.fixture
    def message(self, user1):
        message = Message(text="This is a test message.", user_id=user1.id)
        db.session.add(message)
        db.session.commit()
        return message

    def test_message_creation(self, message):
        """Does creating a message work as expected?"""
        assert message.text == "This is a test message."
        assert message.user.username == "testuser1"
