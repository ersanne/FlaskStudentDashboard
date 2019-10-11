from flask import render_template

from studentportal.admin import bp


@bp.route('/')
@bp.route('/index')
def profile():
    return render_template('base.html')
