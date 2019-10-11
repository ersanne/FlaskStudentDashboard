from flask import Blueprint, render_template

from studentportal.errors import bp


@bp.errorhandler(401)
def page_not_found(error):
    return render_template('404.html', title='404'), 404


@bp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='404'), 404
