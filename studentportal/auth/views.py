from flask import render_template, url_for, redirect, request, flash
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from studentportal import login_manager
from studentportal.models import mongo, User

from studentportal.auth.forms import RegistrationForm, LoginForm, DataSetupForm
from studentportal.auth import bp


@login_manager.user_loader
def load_user(username):
    user = mongo.db.users.find_one({"_id": username})
    if not user:
        return None
    return User(user['_id'])


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('frontend.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = mongo.db.users.find_one({"_id": form.username.data})
        if User.validate_login(user, form.password.data):
            login_user(User(user['_id']))
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('frontend.index')
            return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = {
            "_id": form.username.data,
            "email": form.username.data + "@live.napier.ac.uk",
            "password_hash": User.hash_password(form.password.data)
        }
        mongo.db.users.insert_one(user)
        return redirect(url_for('frontend.index'))
    return render_template('registration.html', title='Sign Up', form=form)


@bp.route('/data-setup', methods=['GET', 'POST'])
def data_setup():
    if mongo.db.students.find_one({'_id': current_user.username}):
        # User already has completed data setup, continue
        return redirect(url_for('frontend.index'))

    form = DataSetupForm()
    if form.validate_on_submit():
        student = {
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'course_title': form.course_title.data,
            'year_of_study': form.year_of_study,
            'current_scqf_level': form.current_scqf_level,
            'enrolled_modules': form.enrolled_modules,
        }
        mongo.db.students.insert_one(student)

    return render_template('data-setup.html', form=form)


@bp.route("/password_reset")
def password_reset():
    return render_template('login.html')
