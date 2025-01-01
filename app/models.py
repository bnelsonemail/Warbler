"""app/models.py"""

from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


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

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Ensure auto-increment
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), nullable=False)
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id', ondelete='cascade'), nullable=False)

    def __repr__(self) -> str:
        return f"<Likes User {self.user_id} likes Message {self.message_id}>"



# Association tables
likes = db.Table(
    'likes',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), primary_key=True),
    db.Column('message_id', db.Integer, db.ForeignKey('messages.id', ondelete="CASCADE"), primary_key=True),
    extend_existing=True  # Prevent re-declaration error
)

follows = db.Table(
    'follows',
    db.Column('user_following_id', db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), primary_key=True),
    db.Column('user_being_followed_id', db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), primary_key=True),
    extend_existing=True  # Prevent re-declaration error
)

class User(db.Model, UserMixin):
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

    messages = db.relationship('Message', backref="user", cascade="all, delete")
    followers = db.relationship(
        "User",
        secondary="follows",
        primaryjoin=(follows.c.user_being_followed_id == id),
        secondaryjoin=(follows.c.user_following_id == id),
        backref="following"
    )
    likes = db.relationship(
        'Message',
        secondary="likes",
        backref=db.backref('liked_by', lazy='dynamic'),
        lazy='joined'
    )


    def __repr__(self) -> str:
        return f"<User #{self.id}: {self.username}, {self.email}, Location: {self.location}>"

    def debug_password(self, plain_password: str):
        """Debug the password matching process."""
        is_valid = bcrypt.check_password_hash(self.password, plain_password)
        current_app.logger.debug(f"Debug Password Match for {self.username}: {is_valid}")
        return is_valid

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

    def has_liked_message(self, message: "Message") -> bool:
        """Check if the user has liked a specific message."""
        return message.id in {msg.id for msg in self.likes}


    def like_message(self, message: "Message") -> None:
        """Like a message if not already liked."""
        if not self.has_liked_message(message):
            self.likes.append(message)

    def unlike_message(self, message: "Message") -> None:
        """Unlike a message if already liked."""
        current_app.logger.debug(f"Current user likes: {[msg.id for msg in current_user.likes]}")
        if self.has_liked_message(message):
            self.likes.remove(message)

    # Flask-Login required methods
    @property
    def is_active(self) -> bool:
        """Return True if the user is active."""
        return True

    @property
    def is_authenticated(self) -> bool:
        """Return True if the user is authenticated."""
        return True

    @property
    def is_anonymous(self) -> bool:
        """Return False for authenticated users."""
        return False

    def get_id(self) -> str:
        """Return the unique ID for the user."""
        return str(self.id)

    @classmethod
    def signup(cls, username: str, email: str, password: str, image_url: str = None) -> "User":
        """Sign up a new user."""
        if not username or not email or not password:
            raise ValueError("Username, email, and password are required.")
        if cls.query.filter_by(username=username).first() or cls.query.filter_by(email=email).first():
            raise ValueError("Username or email already exists.")

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
