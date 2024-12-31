"""app/test/test_message_views.py"""

import pytest

class TestMessageViews:
    def test_add_message_logged_in(self, client, user1):
        """Can logged-in users add a message?"""
        client.post('/auth/login', data={"email": user1.email, "password": "password123"}, follow_redirects=True)
        response = client.post('/messages/new', data={"text": "New message!"}, follow_redirects=True)
        assert response.status_code == 200
        assert b"Message added successfully!" in response.data

    def test_add_message_logged_out(self, client):
        """Are logged-out users prohibited from adding messages?"""
        response = client.post('/messages/new', data={"text": "New message!"}, follow_redirects=True)
        assert response.status_code == 302
        assert b"Please log in to access this page." in response.data

    def test_delete_message_logged_in(self, client, user1, message):
        """Can logged-in users delete their own messages?"""
        client.post('/auth/login', data={"email": user1.email, "password": "password123"}, follow_redirects=True)
        response = client.post(f'/messages/{message.id}/delete', follow_redirects=True)
        assert response.status_code == 200
        assert b"Message deleted." in response.data

    def test_delete_message_logged_out(self, client, message):
        """Are logged-out users prohibited from deleting messages?"""
        response = client.post(f'/messages/{message.id}/delete', follow_redirects=True)
        assert response.status_code == 302
        assert b"Please log in to access this page." in response.data
