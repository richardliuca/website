import secrets
import os.path as path
from flask import current_app
token = secrets.token_hex(16)

class Config(object):
    DEBUG = False
    TESTING = False
    ENV = 'production'
    SECRET_KEY = token
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    IMAGE_PATH = 'static/images/'
    INSTANCE_STRUCTURE = [
        'static/',
        IMAGE_PATH,
    ]
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://richard:liu@localhost/flask_dev'

class TestingConfig(Config):
    TESTING = True
