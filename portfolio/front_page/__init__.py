from flask import Blueprint
from portfolio.front_page.views import Home, About

front_page = Blueprint('front_page', __name__,
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='/front_page/static')

front_page.add_url_rule('/',
            view_func=Home.as_view('home', template_name='home.html'))
front_page.add_url_rule('/home/', endpoint='home')
front_page.add_url_rule('/about/',
            view_func=About.as_view('about', template_name='about.html'))
