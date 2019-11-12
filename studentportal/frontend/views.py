from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from studentportal.frontend import bp
from studentportal.models import mongo
from studentportal.frontend.forms import CreateProfileForm


@bp.route('/')
@bp.route('/index')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('frontend.dashboard'))
    return render_template('guest_home.html')


@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


@bp.route('/feed')
@login_required
def feed():
    return render_template('feed.html')


@bp.route('/todo')
@login_required
def todo():
    return render_template('todo-list.html')


@bp.route('/u/<username>', methods=['GET', 'POST'])
def profile(username):
    profile_data = mongo.db.profiles.find_one({"_id": username})
    if profile_data is None:
        if current_user.is_authenticated and current_user.get_id() == username:
            form = CreateProfileForm()
            return render_template('create_profile.html', form=form)
        else:
            return redirect(url_for('auth.login'))
    return render_template('profile.html', profile=profile_data)


@bp.route('/calendar')
def calendar():
    return render_template('calendar.html')


@bp.route('/settings')
@login_required
def settings():
    return render_template('settings.html')
