from flask import render_template, request, abort, \
                send_from_directory, current_app
from jinja2 import TemplateNotFound
from flask.views import View, MethodView
from portfolio.models import Project, Note
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

class PostView(GeneralView):

    def dispatch_request(self, **kwargs):
        id = request.args.get('id', None)
        if not(kwargs):
            abort(404)
        elif kwargs['post'] == 'projects':
            post = Project.query.get(id) if id else None
            title = 'Project Hub'
        elif kwargs['post'] == 'notes':
            post = Note.query.get(id) if id else None
            title = 'Notebook'
        else:
            abort(404)

        if not(post):
            abort(404)
        else:
            return super().dispatch_request(title=title,
                                            post_title=post.title,
                                            post_date=post.date_posted.strftime("%B, %w %Y"),
                                            post_content=post.documentation,
                                            post_category=post.category)
