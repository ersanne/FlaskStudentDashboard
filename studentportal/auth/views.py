from flask import render_template, url_for, redirect, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from studentportal import login_manager
from studentportal.models import mongo, User

from studentportal.auth.forms import RegistrationForm, LoginForm, DataSetupForm, RequestPasswordResetForm, \
    ResetPasswordForm
from studentportal.auth import bp


@login_manager.user_loader
def load_user(username):
    user = mongo.db.users.find_one({"_id": username})
    if not user:
        return None
    return User(user)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        if not current_user.data_setup_complete:
            return redirect(url_for('auth.data_setup'))
        return redirect(url_for('frontend.index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        if username.endswith('@live.napier.ac.uk'):
            username = username[:-18]
        user = mongo.db.users.find_one({"_id": username})
        if User.validate_login(user, form.password.data):
            login_user(User(user))
            if not user['data_setup_complete']:
                return redirect(url_for('auth.data_setup'))
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('frontend.index')
            return redirect(next_page)
        else:
          flash('Incorrect Password')
    return render_template('login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        if not current_user.data_setup_complete:
            return redirect(url_for('auth.data_setup'))
        return redirect(url_for('frontend.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = {
            '_id': form.username.data,
            'email': form.username.data + '@live.napier.ac.uk',
            'password_hash': User.hash_password(form.password.data),
            'data_setup_complete': False
        }
        mongo.db.users.insert_one(user)
        return redirect(url_for('auth.data_setup'))
    return render_template('registration.html', title='Sign Up', form=form)


@bp.route('/data-setup', methods=['GET', 'POST'])
@login_required
def data_setup():
    if current_user.data_setup_complete():
        return redirect(url_for('frontend.index'))

    form = DataSetupForm()
    if form.validate_on_submit():
        student = {
            '_id': current_user.username,
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'course_title': form.course_title.data,
            'year_of_study': form.year_of_study.data,
            'current_scqf_level': form.current_scqf_level.data,
            'enrolled_modules': form.enrolled_modules.data,
        }
        mongo.db.students.insert_one(student)
        mongo.db.users.update_one({"_id": current_user.username}, {"$set": {"data_setup_complete": True}})
        return redirect(url_for('frontend.index'))

    return render_template('data-setup.html', form=form)


@bp.route("/reset_password/<token>", methods=['GET', 'POST'])
@bp.route("/reset_password/", methods=['GET', 'POST'])
def reset_password(token=None):
    if current_user.is_authenticated:
        return redirect(url_for('frontend.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        form = RequestPasswordResetForm()
        if form.validate_on_submit():
            token = User(mongo.db.users.find_one({"_id": form.username.data})).get_reset_password_token()
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            flash("No verification available at the moment. Reset here: " + reset_url)
        return render_template('request_password_reset.html', form=form)
    else:
        form = ResetPasswordForm()
        if form.validate_on_submit():
            mongo.db.users.update_one(
                {"_id": user['_id']}, {"$set": {"password_hash": User.hash_password(form.password.data)}})
            flash('Your password has been reset.')
            return redirect(url_for('auth.login'))
        return render_template('password_reset.html', form=form)
