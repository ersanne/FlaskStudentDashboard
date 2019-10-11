from flask import Blueprint, render_template, url_for, redirect
from flask_login import current_user

from studentportal.models import User
from studentportal.db import mongo

from studentportal.auth.forms import RegistrationForm, LoginForm

from studentportal.auth import bp


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User(form.username.date, None, form.password.data)
        user_raw = mongo.db.users.find_one({"username": form.username.data})
        print(user_raw)
    return render_template('login.html', title='Sign In', form=form), 200


@bp.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(form.username.data, form.email.data, form.password.data)
        mongo.db.users.insert_one(user.__dict__)
        return redirect(url_for('index'))
    return render_template('registration.html', title='Sign Up', form=form)
