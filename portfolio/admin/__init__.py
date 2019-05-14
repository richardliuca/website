from flask import Blueprint
from portfolio.admin.views import Login

admin_portal = Blueprint('admin_portal', __name__,
                        template_folder='templates',
                        static_folder='static')

admin_portal.add_url_rule('/login/',
                view_func=Login.as_view('login', template_name='login.html'))
