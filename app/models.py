"""app/models.py"""

from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class Follows(db.Model):
    """Connection of a follower <-> followed_user."""
    __tablename__ = 'follows'

    user_being_followed_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        primary_key=True,
    )
    user_following_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        primary_key=True,
    )

    def __repr__(self) -> str:
        return f"<Follows {self.user_being_followed_id} follows {self.user_following_id}>"


class Likes(db.Model):
    """Mapping user likes to warbles."""
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id', ondelete='cascade'))

    def __repr__(self) -> str:
        return f"<Likes User {self.user_id} likes Message {self.message_id}>"


class User(db.Model):
    """User in the system."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    image_url = db.Column(db.Text, default="/static/images/default-pic.png")
    header_image_url = db.Column(db.Text, default="/static/images/warbler-hero.jpg")
    bio = db.Column(db.Text)
    location = db.Column(db.Text)
    password = db.Column(db.Text, nullable=False)

    messages = db.relationship('Message', backref="user")
    followers = db.relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follows.user_being_followed_id == id),
        secondaryjoin=(Follows.user_following_id == id),
        backref="following"
    )
    likes = db.relationship('Message', secondary="likes")

    def __repr__(self) -> str:
        return f"<User #{self.id}: {self.username}, {self.email}>"

    def set_password(self, password: str) -> None:
        """Hash and set the password for the user."""
        self.password = bcrypt.generate_password_hash(password).decode('UTF-8')

    def check_password(self, password: str) -> bool:
        """Check if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    def is_followed_by(self, other_user: "User") -> bool:
        """Check if this user is followed by `other_user`."""
        return other_user in self.followers

    def is_following(self, other_user: "User") -> bool:
        """Check if this user is following `other_user`."""
        return other_user in self.following

    @classmethod
    def signup(cls, username: str, email: str, password: str, image_url: str = None) -> "User":
        """Sign up a new user."""
        if not username or not email or not password:
            raise ValueError("Username, email, and password are required.")
        user = cls(
            username=username,
            email=email,
            image_url=image_url or "/static/images/default-pic.png",
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def authenticate(cls, username: str, password: str) -> "User | bool":
        """Authenticate a user with a username and password."""
        user = cls.query.filter_by(username=username).first()
        return user if user and user.check_password(password) else False


class Message(db.Model):
    """An individual message ("warble")."""
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(140), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self) -> str:
        return f"<Message #{self.id}: {self.text[:20]} by User #{self.user_id}>"


def connect_db(app):
    """Connect this database to provided Flask app."""
    db.app = app
    db.init_app(app)
