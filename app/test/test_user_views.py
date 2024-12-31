"""app/test/test_user_views.py"""

import pytest

class TestUserViews:
    def test_follower_following_pages_logged_in(self, client, user1, user2):
        """Can logged-in users view follower/following pages?"""
        client.post('/auth/login', data={"email": user1.email, "password": "password123"}, follow_redirects=True)
        response = client.get(f'/users/{user2.id}/following', follow_redirects=True)
        assert response.status_code == 200
        assert b"Following" in response.data

    def test_follower_following_pages_logged_out(self, client, user2):
        """Are logged-out users prohibited from viewing follower/following pages?"""
        response = client.get(f'/users/{user2.id}/following', follow_redirects=True)
        assert response.status_code == 302
        assert b"Please log in to access this page." in response.data
