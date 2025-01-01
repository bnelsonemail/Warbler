"""scripts/fix_plaintext_passwords.py"""

from app import create_app
from app.models import db, User

app = create_app()

with app.app_context():
    users = User.query.all()
    for user in users:
        if not user.password.startswith("$2b$"):  # Check for bcrypt hash
            print(f"Fixing password for user: {user.username}")
            user.set_password(user.password)  # Rehash the plaintext password
            db.session.add(user)

    db.session.commit()
    print("All plaintext passwords have been hashed.")
