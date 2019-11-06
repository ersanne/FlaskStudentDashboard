from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from studentportal.frontend import bp
from studentportal.models import mongo
from studentportal.frontend.forms import CreateProfileForm


@bp.route('/index')
@login_required
def index():
    # TODO
    return render_template('layouts/page-layout.html')


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


@bp.route('/calender')
def calender():
    return render_template('calender.html')


@bp.route('/settings')
def settings():
    return render_template('settings.html')
