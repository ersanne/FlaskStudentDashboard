from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
from flask_login import LoginManager, login_required, current_user

from studentportal.models import User
from studentportal.forms import LoginForm

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/napier-student-portal"
    from models import mongo
    mongo.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    @app.errorhandler(401)
    def page_not_found(error):
        return render_template('404.html', title='404'), 404

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html', title='404'), 404

    @app.route('/')
    @app.route('/index')
    @login_required
    def index():
        return render_template('layout.html'), 200

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = LoginForm()
        return render_template('auth/login.html', title='Sign In', form=form), 200

    @app.route("/signup")
    def signup():
        return render_template('auth/registration.html'), 200

    @app.route("/feed")
    def feed():
        return render_template('feed.html'), 200

    @app.route("/u/profile")
    def profile():
        return render_template('profile.html'), 200

    @app.route("/calender")
    def calender():
        return render_template('calender.html'), 200

    app.jinja_env.auto_reload = True
    app.config['SECRET_KEY'] = 'you-will-never-guess'
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
