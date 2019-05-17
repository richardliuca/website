from flask import Blueprint
from portfolio.notebook.views import Notebook

notebook = Blueprint('notebook', __name__,
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='/notes/static')

notebook.add_url_rule('/notes/',
                view_func=Notebook.as_view('notebook', 'notebook.html'))
