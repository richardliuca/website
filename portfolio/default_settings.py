import secrets
token = secrets.token_hex(16)

class Config(object):
    DEBUG = False
    TESTING = False
    ENV = 'production'
    SECRETE_KEY = token

class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'
    print(Config.SECRETE_KEY)

class TestingConfig(Config):
    TESTING = True
