"""app/utils/session.py"""

from datetime import datetime, timedelta
from flask import session


SESSION_TIMEOUT = timedelta(minutes=10)

# Add expiration logic for session['password_confirmed']
def is_session_expired() -> bool:
    """Check if the session has expired based on the last confirmed time."""
    last_access = session.get('password_confirmed_at')
    if not last_access:
        return True  # No timestamp means the session is not valid
    return datetime.now() - datetime.fromisoformat(last_access) > SESSION_TIMEOUT

