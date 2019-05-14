from flask import render_template, url_for, flash, redirect, request, abort
from jinja2 import TemplateNotFound


from flask.views import View

class GeneralView(View):
    methods = ['GET',]
    def __init__(self, template_name):
        self._template_name = template_name

    def render(self, *args, **kwargs):
        try:
            return render_template(self._template_name, *args, **kwargs)
        except TemplateNotFound:
            abort(404)

    def dispatch_request(self, *args, **kwargs):
        return self.render(*args, **kwargs)

class Home(GeneralView):
    pass
