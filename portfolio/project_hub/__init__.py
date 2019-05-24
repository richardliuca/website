from flask import Blueprint
from portfolio.project_hub.views import Hub
from portfolio.views import PostView

project_hub = Blueprint('project_hub', __name__,
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='/project_hub/static')

project_hub.add_url_rule('/project_hub/',
                view_func=Hub.as_view('hub', 'projects.html'))
project_hub.add_url_rule('/project_hub/<post>/',
                view_func=PostView.as_view('proj_post', 'post.html'))
