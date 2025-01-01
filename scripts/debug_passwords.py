"""scripts/debug_passwords.py"""

from app import create_app
from app.models import db, User

# Initialize Flask app context
app = create_app()

with app.app_context():
    user = User.query.filter_by(username='testuser').first()  # Replace with your test user
    if user:
        user.set_password('newpassword')  # Replace with your desired new password
        db.session.commit()
        print(f"Password for user {user.username} has been updated.")
    else:
        print("User not found.")
