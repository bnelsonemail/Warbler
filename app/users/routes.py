"""app/users/routes.py"""

from flask import Blueprint, render_template, redirect, flash, url_for, request, current_app
from flask_login import login_required, current_user
from app.models import db, User, Message

users_bp = Blueprint('users', __name__)

@users_bp.route('/users')
def list_users() -> str:
    """Page with listing of users."""
    search = request.args.get('q')
    page = request.args.get('page', 1, type=int)
    per_page = 20  # Number of users per page

    query = User.query.filter(User.username.like(f"%{search}%")) if search else User.query
    users = query.paginate(page=page, per_page=per_page)

    return render_template('users/index.html', users=users.items, pagination=users)


@users_bp.route('/users/<int:user_id>')
def users_show(user_id: int) -> str:
    """Show user profile."""
    user = User.query.get_or_404(user_id)
    page = request.args.get('page', 1, type=int)
    per_page = 20  # Number of messages per page

    messages = (Message.query.filter_by(user_id=user_id)
                .order_by(Message.timestamp.desc())
                .paginate(page=page, per_page=per_page))

    return render_template('users/show.html', user=user, messages=messages.items, pagination=messages)


@users_bp.route('/users/<int:user_id>/following')
@login_required
def show_following(user_id: int) -> str:
    """Show list of people this user is following."""
    user = User.query.get_or_404(user_id)
    return render_template('users/following.html', user=user)


@users_bp.route('/users/<int:user_id>/followers')
@login_required
def users_followers(user_id: int) -> str:
    """Show list of followers of this user."""
    user = User.query.get_or_404(user_id)
    return render_template('users/followers.html', user=user)


@users_bp.route('/users/follow/<int:follow_id>', methods=['POST'])
@login_required
def add_follow(follow_id: int) -> str:
    """Add a follow for the currently-logged-in user."""
    followed_user = User.query.get_or_404(follow_id)
    current_user.following.append(followed_user)
    db.session.commit()
    flash(f"You are now following {followed_user.username}.", "success")
    current_app.logger.debug(f"{current_user.username} started following {followed_user.username}")
    return redirect(url_for('users.show_following', user_id=current_user.id))


@users_bp.route('/users/stop-following/<int:follow_id>', methods=['POST'])
@login_required
def stop_following(follow_id: int) -> str:
    """Stop following this user."""
    followed_user = User.query.get(follow_id)
    current_user.following.remove(followed_user)
    db.session.commit()
    flash(f"You have unfollowed {followed_user.username}.", "info")
    current_app.logger.debug(f"{current_user.username} unfollowed {followed_user.username}")
    return redirect(url_for('users.show_following', user_id=current_user.id))


@users_bp.route('/users/delete', methods=["POST"])
@login_required
def delete_user() -> str:
    """Delete current user."""
    db.session.delete(current_user)
    db.session.commit()
    flash("User deleted.", "info")
    current_app.logger.debug(f"User {current_user.username} deleted their account.")
    return redirect(url_for('auth.login'))
