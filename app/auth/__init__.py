"""app/auth/__init__.py"""

from flask import Blueprint



auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth",
    template_folder="templates"  # Points to `app/auth/templates`
)


from .routes import *
