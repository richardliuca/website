from flask import Blueprint
from portfolio.admin.views import Login, Dashboard

admin_portal = Blueprint('admin_portal', __name__,
                        template_folder='templates',
                        static_folder='static', static_url_path='/adim/static')

admin_portal.add_url_rule('/login/',
                view_func=Login.as_view('login', template_name='login.html'))
admin_portal.add_url_rule('/dashboard/',
                view_func=Dashboard.as_view('dashboard',
                                            template_name='dashboard.html'))
