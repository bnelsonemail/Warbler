"""app/users/routes.py"""

from flask import Blueprint, render_template, redirect, flash, url_for, request
from flask_login import login_required, current_user
from app.models import db, User


users_bp = Blueprint('users', __name__)


@users_bp.route('/users')
def list_users():
    """Page with listing of users."""
    search = request.args.get('q')
    users = User.query.filter(User.username.like(f"%{search}%")).all() if search else User.query.all()
    return render_template('users/index.html', users=users)


@users_bp.route('/users/<int:user_id>')
def users_show(user_id):
    """Show user profile."""
    user = User.query.get_or_404(user_id)
    messages = (Message.query.filter_by(user_id=user_id)
                .order_by(Message.timestamp.desc())
                .limit(100).all())
    return render_template('users/show.html', user=user, messages=messages)


@users_bp.route('/users/<int:user_id>/following')
@login_required
def show_following(user_id):
    """Show list of people this user is following."""
    user = User.query.get_or_404(user_id)
    return render_template('users/following.html', user=user)


@users_bp.route('/users/<int:user_id>/followers')
@login_required
def users_followers(user_id):
    """Show list of followers of this user."""
    user = User.query.get_or_404(user_id)
    return render_template('users/followers.html', user=user)


@users_bp.route('/users/follow/<int:follow_id>', methods=['POST'])
@login_required
def add_follow(follow_id):
    """Add a follow for the currently-logged-in user."""
    followed_user = User.query.get_or_404(follow_id)
    current_user.following.append(followed_user)
    db.session.commit()
    flash(f"You are now following {followed_user.username}.", "success")
    return redirect(url_for('users.show_following', user_id=current_user.id))


@users_bp.route('/users/stop-following/<int:follow_id>', methods=['POST'])
@login_required
def stop_following(follow_id):
    """Stop following this user."""
    followed_user = User.query.get(follow_id)
    current_user.following.remove(followed_user)
    db.session.commit()
    flash(f"You have unfollowed {followed_user.username}.", "info")
    return redirect(url_for('users.show_following', user_id=current_user.id))


@users_bp.route('/users/delete', methods=["POST"])
@login_required
def delete_user():
    """Delete current user."""
    db.session.delete(current_user)
    db.session.commit()
    flash("User deleted.", "info")
    return redirect(url_for('auth.login'))
