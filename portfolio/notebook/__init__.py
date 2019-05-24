from flask import Blueprint
from portfolio.notebook.views import Notebook
from portfolio.views import PostView

notebook = Blueprint('notebook', __name__,
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='/notes/static')

notebook.add_url_rule('/notebook/',
                view_func=Notebook.as_view('notebook', 'notebook.html'))
notebook.add_url_rule('/notebook/<post>/',
                view_func=PostView.as_view('note_post', 'post.html'))
