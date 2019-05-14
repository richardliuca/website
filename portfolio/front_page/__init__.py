from flask import Blueprint

front_page = Blueprint('front_page', __name__,
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='/front_page/static')
