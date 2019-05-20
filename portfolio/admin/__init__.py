from flask import Blueprint
from portfolio.admin.views import Login, Logout, Dashboard, NewPost, EditPost, Database

admin_portal = Blueprint('admin_portal', __name__,
                        template_folder='templates',
                        static_folder='static', static_url_path='/adim/static')

admin_portal.add_url_rule('/login/',
                view_func=Login.as_view('login', template_name='login.html'))
admin_portal.add_url_rule('/home/login/', endpoint='login')
admin_portal.add_url_rule('/logout/',
                view_func=Logout.as_view('logout'))
admin_portal.add_url_rule('/dashboard/',
                view_func=Dashboard.as_view('dashboard',
                                            template_name='dashboard.html'))
admin_portal.add_url_rule('/dashboard/new_post',
                view_func=NewPost.as_view('new_post',
                                            template_name='new_post.html'))
admin_portal.add_url_rule('/dashboard/edit_post',
                view_func=EditPost.as_view('edit_post',
                                            template_name='edit_post.html'))
admin_portal.add_url_rule('/dashboard/database',
                view_func=EditPost.as_view('database',
                                            template_name='database.html'))
