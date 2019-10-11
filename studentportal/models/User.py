import json
from werkzeug.security import generate_password_hash, check_password_hash
from db import mongo


class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = self.hash_password(password)

    def hash_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        mongo.db.users.find({"user": self.username})
        return check_password_hash(self.password_hash, password)
