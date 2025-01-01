"""app/users/routes.py"""

import os
import sys
import logging
from flask import Blueprint, render_template, redirect, flash, url_for, request, current_app, session
from flask_login import login_required, current_user
from app.models import db, User, Message
from app.forms import UserProfileForm, PasswordConfirmForm
from werkzeug.security import check_password_hash

users_bp = Blueprint('users', __name__, url_prefix='/users')



@users_bp.route('/')
def list_users() -> str:
    """Page with listing of users."""
    search = request.args.get('q')
    page = request.args.get('page', 1, type=int)
    per_page = 20  # Number of users per page

    query = User.query.filter(User.username.like(f"%{search}%")) if search else User.query
    users = query.paginate(page=page, per_page=per_page)

    return render_template('users/index.html', users=users.items, pagination=users)




@users_bp.route('/<int:user_id>')
def users_show(user_id: int) -> str:
    """Show user profile."""
    print("================================")
    print(f"Requested user_id: {user_id}")
    user = User.query.get_or_404(user_id)
    print("User fetched:", user)
    print("+++++++++++++++++++++++++++")
    print(f"Header Image URL: {user.header_image_url}")
    print(f"Profile Image URL: {user.image_url}")
    print("================================")
    page = request.args.get('page', 1, type=int)
    per_page = 20

    messages = (Message.query.filter_by(user_id=user_id)
                .order_by(Message.timestamp.desc())
                .paginate(page=page, per_page=per_page))

    try:
        # Explicitly find the template path
        template = current_app.jinja_env.get_or_select_template('users/show.html')
        current_app.logger.debug(f"Template found at: {template.filename}")
    except Exception as e:
        current_app.logger.error(f"Error finding template: {e}")
        raise

    return render_template('users/show.html', user=user, messages=messages.items, pagination=messages)





@users_bp.route('/<int:user_id>/following')
@login_required
def show_following(user_id: int) -> str:
    """Show list of people this user is following."""
    user = User.query.get_or_404(user_id)
    return render_template('users/following.html', user=user)


@users_bp.route('/<int:user_id>/followers')
@login_required
def users_followers(user_id: int) -> str:
    """Show list of followers of this user."""
    user = User.query.get_or_404(user_id)
    return render_template('users/followers.html', user=user)


@users_bp.route('/follow/<int:follow_id>', methods=['POST'])
@login_required
def add_follow(follow_id: int) -> str:
    """Add a follow for the currently-logged-in user."""
    followed_user = User.query.get_or_404(follow_id)
    current_user.following.append(followed_user)
    db.session.commit()
    flash(f"You are now following {followed_user.username}.", "success")
    current_app.logger.debug(f"{current_user.username} started following {followed_user.username}")
    return redirect(url_for('users.show_following', user_id=current_user.id))


@users_bp.route('/stop-following/<int:follow_id>', methods=['POST'])
@login_required
def stop_following(follow_id: int) -> str:
    """Stop following this user."""
    followed_user = User.query.get(follow_id)
    current_user.following.remove(followed_user)
    db.session.commit()
    flash(f"You have unfollowed {followed_user.username}.", "info")
    current_app.logger.debug(f"{current_user.username} unfollowed {followed_user.username}")
    return redirect(url_for('users.show_following', user_id=current_user.id))


@users_bp.route('/delete', methods=["POST"])
@login_required
def delete_user() -> str:
    """Delete current user."""
    db.session.delete(current_user)
    db.session.commit()
    flash("User deleted.", "info")
    current_app.logger.debug(f"User {current_user.username} deleted their account.")
    return redirect(url_for('auth.login'))


@users_bp.route('/<int:user_id>/confirm-password', methods=['GET', 'POST'])
@login_required
def confirm_password(user_id):
    """Route to confirm password before allowing profile edit."""
    if user_id != current_user.id:
        flash("Unauthorized access.", "danger")
        return redirect(url_for('users.users_show', user_id=current_user.id))

    form = PasswordConfirmForm()
    if form.validate_on_submit():
        if current_user.check_password(form.password.data):
            # Store a session variable to indicate the user is authorized to edit
            session['password_confirmed'] = True
            return redirect(url_for('users.edit_user', user_id=user_id))
        else:
            flash("Incorrect password. Please try again.", "danger")
            return render_template('users/confirm_password.html', form=form)

    return render_template('users/confirm_password.html', form=form)


@users_bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    """Edit the user's profile after password confirmation."""
    print('=====================================================')
    current_app.logger.debug(f"Accessing edit_user for user_id: {user_id}")
    print('======================================================')
    # Check if the session variable exists
    if not session.get('password_confirmed'):
        flash("You must confirm your password before editing your profile.", "warning")
        return redirect(url_for('users.confirm_password', user_id=user_id))

    session.pop('password_confirmed', None)  # Clear the session variable after use

    user = User.query.get_or_404(user_id)
    if user.id != current_user.id:
        flash("You are not authorized to edit this profile.", "danger")
        return redirect(url_for('users.list_users'))

    form = UserProfileForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.bio = form.bio.data
        user.location = form.location.data
        user.image_url = form.image_url.data
        user.header_image_url = form.header_image_url.data
        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('users.users_show', user_id=user_id))

    # Pass user_id explicitly to the template
    return render_template('users/edit.html', form=form, user=user, user_id=user.id)




@users_bp.route('/users/<int:user_id>/likes')
@login_required
def show_liked_warbles(user_id):
    """Show all warbles liked by the user."""
    user = User.query.get_or_404(user_id)
    return render_template('users/likes.html', user=user)


