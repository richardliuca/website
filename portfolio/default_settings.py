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
    INSTANCE_STRUCTURE = [
        'static/',
    ]

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://richard:liu@localhost/flask_dev'
    # SQLALCHEMY_BINDS = {
    #     'security': 'sqlite:///' + path.join(current_app.instance_path, 'security.db'),
    # }

class TestingConfig(Config):
    TESTING = True
