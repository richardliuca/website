from flask import render_template, abort, send_from_directory, current_app
from jinja2 import TemplateNotFound
from flask.views import View, MethodView
import os.path as path

class GeneralView(View):
    methods = ['GET',]
    def __init__(self, template_name=None):
        self._template_name = template_name

    def render(self, *args, **kwargs):
        try:
            return render_template(self._template_name, *args, **kwargs)
        except TemplateNotFound:
            abort(404)

    def dispatch_request(self, *args, **kwargs):
        return self.render(*args, **kwargs)


class GeneralMethodView(MethodView):

    def __init__(self, template_name=None):
        self._template_name = template_name

    def get(self, *args, **kwargs):
        return self.render(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.render(*args, **kwargs)

    def render(self, *args, **kwargs):
        try:
            return render_template(self._template_name, *args, **kwargs)
        except TemplateNotFound:
            abort(404)


class FilesView(View):

    def dispatch_request(self, file):
        try:
            return send_from_directory(
                    directory=path.join(current_app.instance_path),
                                        filename=file)
        except:
            abort(404)

class PostView(MethodView):
    pass
