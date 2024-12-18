"""app/auth/utils.py"""

from sqlalchemy import exists
from app.models import db, User


def user_exists_by_email(email: str) -> bool:
    """Check if a user exists by email.

    Args:
        email (str): The email to check.

    Returns:
        bool: True if a user with the given email exists, False otherwise.
    """
    return db.session.query(exists().where(User.email == email)).scalar()

def user_exists_by_username(username: str) -> bool:
    """Check if a user exists by username.

    Args:
        username (str): The username to check.

    Returns:
        bool: True if a user with the given username exists, False otherwise.
    """
    return db.session.query(exists().where(User.username == username)).scalar()


