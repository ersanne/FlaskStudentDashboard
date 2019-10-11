from flask import Flask
from flask_login import LoginManager


def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/napier-student-portal"
    from db import mongo
    mongo.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)

    from studentportal.errors import bp as error_bp
    app.register_blueprint(error_bp)

    from studentportal.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from studentportal.frontend import bp as frontend_bp
    app.register_blueprint(frontend_bp)

    from studentportal.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    app.jinja_env.auto_reload = True
    app.config['SECRET_KEY'] = 'you-will-never-guess'
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
