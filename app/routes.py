"""app/routes.py"""

import os

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import UserAddForm, LoginForm, MessageForm
from models import db, connect_db, User, Message


##############################################################################
# Homepage and error pages


@app.route('/')
def homepage():
    """Show homepage."""
    if current_user.is_authenticated:
        messages = (Message.query.order_by(Message.timestamp.desc())
                    .limit(100).all())
        return render_template('home.html', messages=messages)
    return render_template('home-anon.html')

@app.after_request
def add_header(response):
    """Add non-caching headers."""
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


