"""app/messages/routes.py"""

from flask import Blueprint, render_template, redirect, flash, url_for
from flask_login import login_required, current_user
from app.models import db, Message
from app.forms import MessageForm

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/messages/new', methods=["GET", "POST"])
@login_required
def messages_add():
    """Add a message."""
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(text=form.text.data, user_id=current_user.id)
        db.session.add(msg)
        db.session.commit()
        flash("Message added successfully!", "success")
        return redirect(url_for('users.users_show', user_id=current_user.id))
    return render_template('messages/new.html', form=form)

@messages_bp.route('/messages/<int:message_id>', methods=["GET"])
def messages_show(message_id):
    """Show a message."""
    msg = Message.query.get_or_404(message_id)
    return render_template('messages/show.html', message=msg)

@messages_bp.route('/messages/<int:message_id>/delete', methods=["POST"])
@login_required
def messages_destroy(message_id):
    """Delete a message."""
    msg = Message.query.get_or_404(message_id)
    if msg.user_id != current_user.id:
        flash("Access unauthorized.", "danger")
        return redirect(url_for('homepage'))
    db.session.delete(msg)
    db.session.commit()
    flash("Message deleted.", "success")
    return redirect(url_for('users.users_show', user_id=current_user.id))
