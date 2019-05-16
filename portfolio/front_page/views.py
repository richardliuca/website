from flask import url_for, flash, redirect, request, abort, current_app
from jinja2 import TemplateNotFound
from portfolio.views import GeneralView
import os, pathlib
import os.path as path

class Home(GeneralView):
    def dispatch_request(self):
        cover_dir = path.join(current_app.instance_path, pathlib.Path('static/Home/'))
        cover_path = url_for('front_page.static', filename='cover.jpeg', _external=True)
        try:
            for file in os.listdir(cover_dir):
                if path.isfile(path.join(cover_dir, file)):
                    name, ext = path.splitext(file)
                    if name.lower() == 'cover':
                        cover_path = url_for('file',
                                            file='static/Home/'+file)
                        break
        except:
            pass
        return super().dispatch_request(title='Home', cover=cover_path)

class About(GeneralView):
        def dispatch_request(self):
            return super().dispatch_request(title='About Me')
