from flask import Blueprint
from portfolio.project_hub.views import Hub

project_hub = Blueprint('project_hub', __name__,
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='/project_hub/static')

project_hub.add_url_rule('/projects/',
                view_func=Hub.as_view('hub', 'projects.html'))
