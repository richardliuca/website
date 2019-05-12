import os
from flask import Flask

def create_app(test_config=None):
    # Creating Flask appication object
    app = Flask(__name__)
    # Loading default development configurations
    from portfolio import default_settings
    # Apply default development configurations
    app.config.from_object(default_settings)


    if os.environ.get('APPLICATION_SETTINGS', default=None):
        # Environment variable : APPLICATION_SETTINGS points to a python file
        # The pointed files contain configurations for application instance
        # Inside the config file, values must be in all uppercase
        app.config.from_envvar('APPLICATION_SETTINGS')
        # Alternative with json config file is also valid
        # app.config.from_json(filename)
    else:
        print('WARNING!!!')
        print('Proceeding with development mode')


    if test_config is not None:
        app.config.update(test_config)

    import portfolio.views
    return app
