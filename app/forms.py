"""app/forms.py"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo


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


class RegistrationForm(FlaskForm):
    """Form for registering a new user."""
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match')
    ])
