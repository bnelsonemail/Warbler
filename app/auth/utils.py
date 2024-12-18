# app/auth/utils.py

def user_exists_by_email(email):
    """Check if a user exists by email."""
    return User.query.filter_by(email=email).first() is not None

def user_exists_by_username(username):
    """Check if a user exists by username."""
    return User.query.filter_by(username=username).first() is not None
