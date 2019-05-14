import os
from flask import Flask
from portfolio.models import db, bcrypt, Admin
from portfolio.admin import admin_portal
from flask_login import LoginManager

def create_app(test_config=None):
    # Creating Flask appication object
    app = Flask(__name__)
    with app.app_context():
        # Configuration
        # Loading default development configurations
        from portfolio import default_settings
    # Apply default development configurations
    app.config.from_object(default_settings.DevelopmentConfig)

    if test_config is not None:
        # Loading testing configurations
        app.config.from_object(default_settings.TestingConfig)
    elif os.environ.get('APPLICATION_SETTINGS', default=None):
        # Environment variable : APPLICATION_SETTINGS points to a python file
        # The pointed files contain configurations for application instance
        # Inside the config file, values must be in all uppercase
        app.config.from_envvar('APPLICATION_SETTINGS')
        # Alternative with json config file is also valid
        # app.config.from_json(filename)
    else:
        print('WARNING!!!')
        print('Proceeding with development mode')

    # Creating instance folder if not exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        print('Instance path exist, proceeding ...')

    # Initializing app for various extension
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'

    # Register blueprints
    app.register_blueprint(admin_portal)


    return app
