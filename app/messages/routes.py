"""app/messages/routes.py"""

from flask import Blueprint, render_template, redirect, flash, url_for, current_app
from flask_login import login_required, current_user
from app.models import db, Message
from app.forms import MessageForm

messages_bp = Blueprint('messages', __name__)


@messages_bp.route('/messages/new', methods=["GET", "POST"])
@login_required
def messages_add() -> str:
    """Add a message."""
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(text=form.text.data, user_id=current_user.id)
        db.session.add(msg)
        db.session.commit()
        flash("Message added successfully!", "success")
        current_app.logger.debug(f"Message added: {msg.text[:20]}...")
        return redirect(url_for('users.users_show', user_id=current_user.id))
    return render_template('messages/new.html', form=form)


@messages_bp.route('/messages/<int:message_id>', methods=["GET"])
def messages_show(message_id: int) -> str:
    """Show a message."""
    current_app.logger.debug(f"Fetching message with ID: {message_id}")
    msg = Message.query.get_or_404(message_id)
    return render_template('messages/show.html', message=msg)


@messages_bp.route('/messages/<int:message_id>/delete', methods=["POST"])
@login_required
def messages_destroy(message_id: int) -> str:
    """Delete a message."""
    msg = Message.query.get_or_404(message_id)
    if msg.user_id != current_user.id:
        flash("Access unauthorized.", "danger")
        current_app.logger.warning(f"Unauthorized delete attempt on message ID: {message_id}")
        return redirect(url_for('homepage'))
    db.session.delete(msg)
    db.session.commit()
    flash(f"Message '{msg.text[:20]}...' deleted.", "success")
    current_app.logger.debug(f"Message deleted with ID: {message_id}")
    return redirect(url_for('users.users_show', user_id=current_user.id))


@main_bp.route('/messages/<int:message_id>/like', methods=['POST'])
@login_required
def like_message(message_id):
    """Like a warble."""
    message = Message.query.get_or_404(message_id)

    # Prevent users from liking their own messages
    if message.user_id == current_user.id:
        flash("You cannot like your own warble!", "danger")
        return redirect(url_for('main.homepage'))

    # Check if already liked
    if message in current_user.likes:
        flash("You already liked this warble.", "info")
    else:
        current_user.likes.append(message)
        db.session.commit()
        flash("Warble liked!", "success")

    return redirect(url_for('main.homepage'))


@main_bp.route('/messages/<int:message_id>/unlike', methods=['POST'])
@login_required
def unlike_message(message_id):
    """Unlike a warble."""
    message = Message.query.get_or_404(message_id)

    if message in current_user.likes:
        current_user.likes.remove(message)
        db.session.commit()
        flash("Warble unliked.", "success")
    else:
        flash("You haven't liked this warble.", "info")

    return redirect(url_for('main.homepage'))
