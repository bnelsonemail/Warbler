"""app/routes.py"""

from flask import render_template, flash, current_app, Blueprint, g
from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError
from app.models import Message
from app.forms import LikeForm


##############################################################################
# Homepage and error pages

main_bp = Blueprint('main', __name__)


# @main_bp.before_request
# def load_logged_in_user():
#     """Set g.user to the current user if authenticated."""
#     g.user = current_user if current_user.is_authenticated else None



@main_bp.route('/')
def homepage():
    """Show homepage for logged-in users or anonymous users."""
    form = LikeForm()  # Create an instance of the LikeForm
    if current_user.is_authenticated:
        try:
            # Fetch messages from the logged-in user and the users they follow
            messages = (Message.query
                        .filter((Message.user_id == current_user.id) |
                                (Message.user_id.in_([user.id for user in current_user.following])))
                        .order_by(Message.timestamp.desc())
                        .limit(100)
                        .all())
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error fetching messages: {e}")
            flash("Error loading messages. Please try again later.", "danger")
            messages = []

        # Pass current_user as 'user' to match the template
        return render_template('home.html', messages=messages, form=form, user=current_user)

    return render_template('home-anon.html', form=form)




@main_bp.after_request
def add_header(response):
    """Add non-caching headers.

    Disables caching for all requests if caching is disabled in the config.
    """
    if not current_app.config.get("ENABLE_CACHING", False):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response





##############################################################################
# Turn off all caching in Flask
#   (useful for dev; in production, this kind of stuff is typically
#   handled elsewhere)
#
# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask


