from flask import Blueprint, render_template, redirect


auth = Blueprint('auth', __name__)


@auth.route('/login')
def profile():
    return render_template('profile.html')


@auth.route('/register')
def profile():
    return render_template('auth/registration.html')


@auth.route('/logout')
def logout():
    logout_user()
    return redirect('/login')
