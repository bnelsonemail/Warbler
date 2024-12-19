"""app/routes.py"""

from flask import render_template, flash, current_app, Blueprint, g
from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError
from app.models import Message

##############################################################################
# Homepage and error pages

main_bp = Blueprint('main', __name__)


@main_bp.before_request
def load_logged_in_user():
    """Set g.user to the current user if authenticated."""
    g.user = current_user if current_user.is_authenticated else None


@main_bp.route('/test')
def test_g_user():
    if g.user:
        return f"Logged in as: {g.user.username}"
    return "No user is logged in."


@main_bp.route('/')
def homepage() -> str:
    """Show homepage.

    - Authenticated users: Show the 100 most recent messages.
    - Anonymous users: Show the anonymous homepage.
    """
    current_app.logger.info("Homepage accessed.")
    if current_user.is_authenticated:
        try:
            messages = (Message.query.order_by(Message.timestamp.desc())
                        .limit(100).all())
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error fetching messages: {e}")
            flash("Error loading messages. Please try again later.", "danger")
            messages = []
        return render_template('home.html', messages=messages)
    return render_template('home-anon.html')

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


