import os
from pathlib import Path
from flask import Flask
from portfolio.models import db, bcrypt, login_manager
from portfolio.views import FilesView, DeletePost, PostView, ImgPost
from portfolio.front_page import front_page
from portfolio.admin import admin_portal
from portfolio.blog  import project_hub, notebook

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
    for path in app.config['INSTANCE_STRUCTURE']:
        try:
            os.makedirs(Path(app.instance_path).joinpath(path))
        except OSError:
            continue

    # Initializing app for various extension
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin_portal.login'
    login_manager.login_message_category = 'info'

    login_manager.refresh_view = 'admin_portal.login'
    login_manager.needs_refresh_message = \
        (u'To protect your account, please reauthenticate to access this page.')
    login_manager.needs_refresh_message_category = 'info'

    # Register blueprints
    app.register_blueprint(front_page)
    app.register_blueprint(admin_portal)
    app.register_blueprint(project_hub)
    app.register_blueprint(notebook)
    #
    # # Register url
    app.add_url_rule('/file/<path:file>', view_func=FilesView, endpoint='file')
    app.add_url_rule('/<post>/', view_func=PostView.as_view('preview'))
    app.add_url_rule('/delete', view_func=DeletePost, endpoint='delete')
    app.add_url_rule('/img', view_func=ImgPost.as_view('img'))


    return app
