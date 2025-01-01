"""app/users/routes.py"""

import os
import sys
import logging
from flask import Blueprint, render_template, redirect, flash, url_for, request, current_app, session, g
from flask_login import login_required, current_user
from app.models import db, User, Message
from app.forms import UserProfileForm, PasswordConfirmForm, FollowForm
from werkzeug.security import check_password_hash
from app.utils.session import is_session_expired


users_bp = Blueprint('users', __name__, url_prefix='/users')



@users_bp.route('/users', methods=['GET'])
@login_required
def list_users():
    """List all users."""
    form = FollowForm()  # Create an instance of the FollowForm
    users = User.query.paginate(page=request.args.get('page', 1, type=int), per_page=20)
    return render_template('users/index.html', users=users.items, pagination=users, form=form)





@users_bp.route('/<int:user_id>')
def users_show(user_id: int) -> str:
    """Show user profile."""
    user = User.query.get_or_404(user_id)
    follow_form = FollowForm()
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

    return render_template('users/show.html', user=user, messages=messages.items, pagination=messages, follow_form=follow_form)





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


@users_bp.route('/follow/<int:user_id>', methods=['POST'])
@login_required
def follow_user(user_id):
    """Follow a user."""
    user_to_follow = User.query.get_or_404(user_id)
    print('=============================================')
    current_app.logger.debug(f"User {g.user.username} attempting to follow {user_to_follow.username}.")
    print('=============================================')
    
    if not g.user:
        flash("You must be logged in to follow users.", "danger")
        return redirect(url_for('auth.login'))

    if user_to_follow in g.user.following:
        flash(f"You are already following {user_to_follow.username}.", "warning")
    else:
        g.user.following.append(user_to_follow)
        db.session.commit()
        flash(f"You are now following {user_to_follow.username}!", "success")

    return redirect(request.referrer or url_for('users.list_users'))

# @users_bp.route('/follow/<int:user_id>', methods=['POST'])
# @login_required
# def follow_user(user_id):
#     user_to_follow = User.query.get_or_404(user_id)
#     success, message = toggle_follow(user_to_follow, 'follow')
#     flash(message, "success" if success else "warning")
#     return redirect(request.referrer or url_for('users.list_users'))



@users_bp.route('/unfollow/<int:user_id>', methods=['POST'])
@login_required
def unfollow_user(user_id):
    """Unfollow a user."""
    user_to_unfollow = User.query.get_or_404(user_id)
    print('=============================================')
    current_app.logger.debug(f"User {g.user.username} attempting to unfollow {user_to_unfollow.username}.")
    print('=============================================')

    if not g.user:
        flash("You must be logged in to unfollow users.", "danger")
        return redirect(url_for('auth.login'))

    if user_to_unfollow not in g.user.following:
        flash(f"You are not following {user_to_unfollow.username}.", "warning")
    else:
        g.user.following.remove(user_to_unfollow)
        db.session.commit()
        flash(f"You have unfollowed {user_to_unfollow.username}.", "success")

    return redirect(request.referrer or url_for('users.list_users'))



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
            session['password_confirmed_at'] = datetime.now().isoformat()  # Store timestamp
            return redirect(url_for('users.edit_user', user_id=user_id))
        else:
            flash("Incorrect password. Please try again.", "danger")
            return render_template('users/confirm_password.html', form=form)

    return render_template('users/confirm_password.html', form=form)


@users_bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    """Edit the user's profile after password confirmation."""
    current_app.logger.debug(f"Accessing edit_user for user_id: {user_id}")
    current_app.logger.debug(f"Session password_confirmed: {session.get('password_confirmed')}")

    # Check if the session variable exists
    if not session.get('password_confirmed') or is_session_expired():
        flash("Session expired. Please confirm your password again.", "warning")
        return redirect(url_for('users.confirm_password', user_id=user_id))

    user = User.query.get_or_404(user_id)
    if user.id != current_user.id:
        flash("You are not authorized to edit this profile.", "danger")
        return redirect(url_for('users.list_users'))

    form = UserProfileForm(obj=user)

    if form.validate_on_submit():
        session.pop('password_confirmed', None)  # Clear only after form submission
        user.username = form.username.data
        user.email = form.email.data
        user.bio = form.bio.data
        user.location = form.location.data
        user.image_url = form.image_url.data
        user.header_image_url = form.header_image_url.data
        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('main.homepage', user_id=user_id))

    # Pass user_id explicitly to the template
    return render_template('users/edit.html', form=form, user=user, user_id=user.id)


@users_bp.route('/search', methods=['GET', 'POST'])
def search_users():
    """Search for users by username or email."""
    query = request.args.get('query', '').strip()

    if not query:
        flash("Please enter a search term.", "warning")
        return redirect(url_for('users.list_users'))

    # Search for users by username or email
    users = User.query.filter(
        (User.username.ilike(f"%{query}%")) | (User.email.ilike(f"%{query}%"))
    ).all()

    follow_form = FollowForm()  # Pass a form to the template
    return render_template('users/search_results.html', users=users, query=query, follow_form=follow_form)



@users_bp.route('/users/<int:user_id>/likes')
@login_required
def show_liked_warbles(user_id):
    """Show all warbles liked by the user."""
    user = User.query.get_or_404(user_id)
    return render_template('users/likes.html', user=user)


