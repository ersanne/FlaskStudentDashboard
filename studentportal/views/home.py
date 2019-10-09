from flask import Blueprint, render_template, redirect
from flask_login import current_user

home = Blueprint('home', __name__)


@home.route('/')
def profile():
    redirect('/dashboard')
    return render_template('profile.html')
