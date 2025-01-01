"""app/forms.py"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_login import current_user
from app.models import User
from wtforms.validators import ValidationError



class LikeForm(FlaskForm):
    submit = SubmitField('Like')
    

class MessageForm(FlaskForm):
    """Form for adding/editing messages."""
    text = TextAreaField('Text', validators=[DataRequired(), Length(max=280)])

class UserAddForm(FlaskForm):
    """Form for adding users."""
    username = StringField(
        'Username', 
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your username"}
    )
    email = StringField(
        'E-mail', 
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Enter your email address"}
    )
    password = PasswordField(
        'Password', 
        validators=[DataRequired(), Length(min=6)],
        render_kw={"placeholder": "Enter a password (min. 6 characters)"}
    )
    image_url = StringField('(Optional) Image URL', render_kw={"placeholder": "Optional: Add an image URL"})

class LoginForm(FlaskForm):
    """Login form."""
    username = StringField(
        'Username', 
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your username"}
    )
    password = PasswordField(
        'Password', 
        validators=[DataRequired(), Length(min=6)],
        render_kw={"placeholder": "Enter your password"}
    )

class UserProfileForm(FlaskForm):
    """Form for editing user profiles."""
    username = StringField(
        'Username', 
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your username"}
    )
    email = StringField(
        'E-mail', 
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Enter your email address"}
    )
    bio = TextAreaField(
        'Bio', 
        validators=[Length(max=200)],
        render_kw={"placeholder": "Write a short bio (max. 200 characters)"}
    )
    location = StringField(
        'Location',
        render_kw={"placeholder": "Enter your location"}
    )
    image_url = StringField(
        '(Optional) Image URL',
        render_kw={"placeholder": "Optional: Add an image URL"}
    )
    header_image_url = StringField(
        '(Optional) Header Image URL',
        render_kw={"placeholder": "Optional: Add a header image URL"}
    )

    def validate_username(self, username):
        """validate username is unique"""
        existing_user = User.query.filter_by(username=username.data).first()
        if existing_user and existing_user.id != current_user.id:
            raise ValidationError("This username is already taken. Please choose a different one.")

    def validate_email(self, email):
        """validate email is unique"""
        existing_email = User.query.filter_by(email=email.data).first()
        if existing_email and existing_email.id != current_user.id:
            raise ValidationError("This email is already in use. Please choose a different one.")




class RegistrationForm(FlaskForm):
    """Form for registering a new user."""
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match')
    ])



class PasswordConfirmForm(FlaskForm):
    """Form for confirming password before profile edit."""
    password = PasswordField(
        'Password',
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your password"}
    )
    submit = SubmitField('Confirm Password')
