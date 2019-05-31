from flask import Blueprint
from portfolio.blog.views import Hub, Notebook
from portfolio.views import PostView

project_hub = Blueprint('project_hub', __name__,
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='/blog/static')

project_hub.add_url_rule('/project_hub/',
                view_func=Hub.as_view('hub', 'projects.html'))
project_hub.add_url_rule('/project_hub/<post>/',
                view_func=PostView.as_view('proj_post', 'post.html'))

notebook = Blueprint('notebook', __name__,
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='/blog/static')

notebook.add_url_rule('/notebook/',
                view_func=Notebook.as_view('notebook', 'notebook.html'))
notebook.add_url_rule('/notebook/<post>/',
                view_func=PostView.as_view('note_post', 'post.html'))
