from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from time import time
import jwt

from . import mongo


class User:
    def __init__(self, user):
        self.username = user['_id']
        self.user = user

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user['_id']

    def data_setup_complete(self):
        return self.user['data_setup_complete']

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.user['_id'], 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def validate_login(user, password):
        if user and password:
            return check_password_hash(user['password_hash'], password)

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    @staticmethod
    def verify_reset_password_token(token):
        try:
            _id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return mongo.db.users.find_one({"_id":_id})
