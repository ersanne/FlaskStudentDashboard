from flask import render_template
from flask_login import login_required

from studentportal.frontend import bp


@bp.route('/index')
@login_required
def index():
    # TODO
    return render_template('layouts/page-layout.html')


@bp.route('/feed')
def feed():
    return render_template('feed.html')


@bp.route('/todo')
def todo():
    return render_template('todo-list.html')


@bp.route('/profile')
def profile():
    return render_template('profile.html')


@bp.route('/calender')
def calender():
    return render_template('calender.html')


@bp.route('/settings')
def settings():
    return render_template('settings.html')