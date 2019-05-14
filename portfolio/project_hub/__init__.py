from flask import Blueprint

project_hub = Blueprint('project_hub', __name__,
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='/project_hub/static')
