import json
from werkzeug.security import generate_password_hash, check_password_hash
from studentportal.models import mongo
from studentportal import login_manager


class User:
    def __init__(self, username):
        self.username = username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

