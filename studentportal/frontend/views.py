from flask import render_template

from studentportal.frontend import bp


@bp.route("/feed")
def feed():
    return render_template('feed.html'), 200


@bp.route("/profile")
def profile():
    return render_template('profile.html'), 200


@bp.route("/calender")
def calender():
    return render_template('calender.html'), 200
