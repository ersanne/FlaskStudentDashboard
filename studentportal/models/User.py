from werkzeug.security import generate_password_hash, check_password_hash
from models import mongo

class User():

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        mongo.db.users.find({"user": self.username})
        return check_password_hash(self.password_hash, password)