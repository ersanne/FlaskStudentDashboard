from flask import Flask
from flask_login import LoginManager

login_manager = LoginManager()


def create_app():

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')
    app.config.from_pyfile('config.py')

    from studentportal.models import mongo
    mongo.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from studentportal.errors import bp as error_bp
    app.register_blueprint(error_bp)

    from studentportal.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from studentportal.frontend import bp as frontend_bp
    app.register_blueprint(frontend_bp)

    from studentportal.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app
