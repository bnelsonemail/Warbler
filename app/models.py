"""SQLAlchemy models for Warbler."""

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


class Likes(db.Model):
    """Mapping user likes to warbles."""

    __tablename__ = 'likes' 

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

    message_id = db.Column(
        db.Integer,
        db.ForeignKey('messages.id', ondelete='cascade'),
        unique=True
    )


class User(db.Model):
    """User in the system.

    This class represents a user, including their details (e.g., username,
    email, bio), relationships (e.g., followers, following), and methods for
    authentication and password management.
    """

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )
    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )
    image_url = db.Column(
        db.Text,
        default="/static/images/default-pic.png",
    )
    header_image_url = db.Column(
        db.Text,
        default="/static/images/warbler-hero.jpg"
    )
    bio = db.Column(
        db.Text,
    )
    location = db.Column(
        db.Text,
    )
    password = db.Column(
        db.Text,
        nullable=False,
    )

    messages = db.relationship('Message')
    followers = db.relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follows.user_being_followed_id == id),
        secondaryjoin=(Follows.user_following_id == id),
        backref="following"
    )
    following = db.relationship(
        "User",
        secondary="follows",
        primaryjoin=(Follows.user_following_id == id),
        secondaryjoin=(Follows.user_being_followed_id == id),
        backref="followers"
    )
    likes = db.relationship(
        'Message',
        secondary="likes"
    )

    def __repr__(self):
        """Provide a string representation of the user.

        Returns:
            str: A string showing the user's ID, username, and email.
        """
        return f"<User #{self.id}: {self.username}, {self.email}>"

    def set_password(self, password):
        """Hash and set the password for the user.

        Args:
            password (str): The plain-text password to hash.
        """
        self.password = bcrypt.generate_password_hash(password).decode('UTF-8')

    def check_password(self, password):
        """Check if the provided password matches the hashed password.

        Args:
            password (str): The plain-text password to verify.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return bcrypt.check_password_hash(self.password, password)

    def is_followed_by(self, other_user):
        """Check if this user is followed by `other_user`.

        Args:
            other_user (User): The user to check as a follower.

        Returns:
            bool: True if `other_user` is a follower, False otherwise.
        """
        return db.session.query(Follows).filter_by(
            user_being_followed_id=self.id,
            user_following_id=other_user.id
        ).first() is not None

    def is_following(self, other_user):
        """Check if this user is following `other_user`.

        Args:
            other_user (User): The user to check as someone being followed.

        Returns:
            bool: True if this user is following `other_user`, False otherwise.
        """
        return db.session.query(Follows).filter_by(
            user_being_followed_id=other_user.id,
            user_following_id=self.id
        ).first() is not None

    @classmethod
    def signup(cls, username, email, password, image_url=None):
        """Sign up a new user.

        This method creates a new user with a hashed password and default
        image URLs if none are provided.

        Args:
            username (str): The username for the user.
            email (str): The email address for the user.
            password (str): The plain-text password for the user.
            image_url (str, optional): The profile image URL. Defaults to None.

        Returns:
            User: The created `User` instance.
        """
        user = cls(
            username=username,
            email=email,
            image_url=image_url or "/static/images/default-pic.png",
        )
        user.set_password(password)
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Authenticate a user with a username and password.

        This method verifies that a user with the provided username exists
        and that the password matches the stored hashed password.

        Args:
            username (str): The username to authenticate.
            password (str): The plain-text password to check.

        Returns:
            User or bool: The authenticated `User` object if credentials are
                          correct, or False otherwise.
        """
        user = cls.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return False



class Message(db.Model):
    """An individual message ("warble")."""

    __tablename__ = 'messages'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    text = db.Column(
        db.String(140),
        nullable=False,
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

    user = db.relationship('User')


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
