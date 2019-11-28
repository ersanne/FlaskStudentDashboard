import os
from sys import platform


class Config:

    def __init__(self):
        pass

    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    WTF_CSRF_ENABLED = True
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://mongo_user:mongo_secret@127.0.0.1:27017/studentportal'
    UPLOAD_FOLDER = '/data/assets'
