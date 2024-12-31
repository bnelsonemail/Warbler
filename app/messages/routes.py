"""app/messages/routes.py"""

from flask import Blueprint, render_template, redirect, flash, url_for, current_app, request
from flask_login import login_required, current_user
from app.models import db, Message
from app.forms import MessageForm
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the minimum log level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create a logger
logger = logging.getLogger(__name__)

# Create message blueprint
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


@messages_bp.route('/messages/<int:message_id>/like', methods=['POST'])
@login_required
def like_message(message_id):
    """Like a warble."""
    print("===================================================")
    current_app.logger.debug(f"Received like request for message {message_id} by user {current_user.id}")
    logging.debug(f"User {current_user.id} attempting to like message {message_id}")
    
    
    print(f"Received request to like message ID: {message_id}")
    print(f"Form Data: {request.form}")
    print("====================================================")
    
    # Fetch message
    message = Message.query.get_or_404(message_id)
    liked_message_ids = {message.id for message in current_user.likes}  # Fetch all liked message IDs once
    current_app.logger.debug(f"Received request to like message ID: {message_id}")

    try:
        # Prevent users from liking their own messages
        if message.user_id == current_user.id:
            flash("You cannot like your own warble!", "danger")
            current_app.logger.debug(f"User {current_user.id} attempted to like their own warble {message_id}.")
            return redirect(request.referrer or url_for('main.homepage'))

        # Check if already liked
        if message.id in liked_message_ids:
            flash("You already liked this warble.", "info")
            current_app.logger.debug(f"User {current_user.id} has already liked message {message_id}.")
        else:
            # Add the like
            print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            current_app.logger.debug(f"Current user likes before: {[msg.id for msg in current_user.likes]}")
            current_user.likes.append(message)
            db.session.commit()
            current_app.logger.debug(f"Current user likes after: {[msg.id for msg in current_user.likes]}")
            print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            flash("Warble liked!", "success")
            current_app.logger.debug(f"User {current_user.id} liked message {message_id}.")

    except Exception as e:
        db.session.rollback()  # Ensure rollback if the transaction fails
        current_app.logger.error(f"Error processing like for message {message_id}: {e}")
        flash("An error occurred while liking the warble.", "danger")
        return redirect(request.referrer or url_for('main.homepage'))

    return redirect(request.referrer or url_for('main.homepage'))



@messages_bp.route('/messages/<int:message_id>/unlike', methods=['POST'])
@login_required
def unlike_message(message_id):
    """Unlike a warble."""
    message = Message.query.get_or_404(message_id)
    
    # Log the current liked messages
    liked_message_ids = [msg.id for msg in current_user.likes]
    current_app.logger.debug(f"User {current_user.id} has liked message IDs: {liked_message_ids}")

    # Check if the like exists before attempting to remove it
    if current_user.has_liked_message(message):
        try:
            current_user.likes.remove(message)
            db.session.commit()
            flash("Warble unliked.", "success")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error unliking message {message_id}: {e}")
            flash("An error occurred while unliking the warble.", "danger")
    else:
        flash("You haven't liked this warble.", "info")

    return redirect(request.referrer or url_for('main.homepage'))


@messages_bp.route('/messages/<int:message_id>/delete', methods=['POST'])
@login_required
def delete_message(message_id):
    """Delete a message."""
    message = Message.query.get_or_404(message_id)

    # Check if the current user owns the message
    if message.user_id != current_user.id:
        flash("Access unauthorized.", "danger")
        return redirect(url_for('main.homepage'))  # Or redirect to another page

    try:
        db.session.delete(message)
        db.session.commit()
        flash("Message deleted.", "success")
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while trying to delete the message.", "danger")
    
    return redirect(request.referrer or url_for('main.homepage'))