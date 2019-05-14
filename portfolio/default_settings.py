import secrets
import os.path as path
from flask import current_app
token = secrets.token_hex(16)

class Config(object):
    DEBUG = False
    TESTING = False
    ENV = 'production'
    SECRETE_KEY = token
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' +\
                                path.join(current_app.instance_path, 'site.db')
    print(Config.SECRETE_KEY)

class TestingConfig(Config):
    TESTING = True
