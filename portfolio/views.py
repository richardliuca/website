from flask import render_template, request, abort, send_from_directory, \
                current_app, jsonify, make_response, url_for, flash
from jinja2 import TemplateNotFound
from flask_login import login_required, fresh_login_required, current_user
from flask.views import View, MethodView
from portfolio.models import db, Post, Tag, Image
import os.path as path
from werkzeug.utils import secure_filename
import uuid

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


def FilesView(file):

    try:
        return send_from_directory(
                directory=path.join(current_app.instance_path),
                                    filename=file)
    except:
        abort(404)

class PostSearch(GeneralView):

    def dispatch_request(self):
        page = request.args.get('page', 1, type=int)
        tags = [name.lower() for name in request.args.getlist('tag') if not(name.lower() in self.target)]
        or_search = request.args.get('or', 0, type=int)

        if self.complete == True or self.complete == False:
            self.posts = Post.query.filter(Post.complete == self.complete)
        else:
            self.posts = Post.query

        self.posts = self.posts.filter(db.or_(*[Post.tags.any(Tag.name == tag) for tag in self.target]))

        if or_search:
            self.posts = self.posts.filter(db.or_(*[Post.tags.any(Tag.name == tag) for tag in tags]))
        else:
            for tag in tags:
                self.posts = self.posts.filter(Post.tags.any(Tag.name == tag))
            or_search = None

        self.posts = self.posts.order_by(Post.id.desc())

        if self.max_page:
            self.posts = self.posts.paginate(page=page, per_page=self.max_page)
        else:
            self.posts = self.posts.all()

        return super().dispatch_request(title=self.title,
                                        catalog=self.posts,
                                        source=self.target,
                                        tags=tags,
                                        or_search=or_search)

class PostView(GeneralView):

    def dispatch_request(self, **kwargs):
        id = request.args.get('id', None)
        post = Post.query.get(id) if id else None

        if not(kwargs and post):
            abort(404)
        elif kwargs['post'] == 'project':
            title = 'Project Hub'
        elif kwargs['post'] == 'note':
            title = 'Notebook'
        elif kwargs['post'] == 'preview':
            if current_user.is_authenticated:
                return make_response(jsonify({
                        'title': post.title,
                        'date_posted': post.date_posted.strftime("%B, %d %Y"),
                        'content': post.body,
                        'tags': [tag.name for tag in post.tags]}))
            else:
                abort(404)
        else:
            abort(404)

        return super().dispatch_request(
                            title=title,
                            post_title=post.title,
                            post_date=post.date_posted.strftime("%B, %d %Y"),
                            post_content=post.body,
                            post_tags=post.tags)

def DeletePost(**kwargs):

    if current_user.is_authenticated:
        try:
            id = request.args.get('id', -1, type=int)
            if id == -1:
                raise Exception('No id argument passed')
            post = Post.query.get(id)
            data = {'message': f'Post: {post.title} is deleted', 'id': post.id}
            db.session.delete(post)
            db.session.commit()
            return make_response(jsonify(data), 200)
        except:
            data = {'message': 'An error has occured'}
            return make_response(jsonify(data), 500)
    else:
        abort(404)

def allowed_file(filename):
    if '.' in filename:
        name, ext = path.splitext(filename)
        return ext[1:].lower() in current_app.config['ALLOWED_EXTENSIONS']
    return False

class ImgPost(MethodView):
    methods = ['GET', 'POST']

    def get(self):
        if current_user.is_authenticated:
            id = request.args.get('id', 0, type=int)
            image = Image.query.get(id)
            if id and image:
                return send_from_directory(directory=current_app.config['UPLOAD_FOLDER'], filename=image.name)
        abort(404)

    def post(self):
        if 'imgFile' in request.files:
            img_file = request.files['imgFile']
            if img_file and allowed_file(img_file.filename):
                img_filename = secure_filename(img_file.filename)
                _, ext = path.splitext(img_filename)
                unique_name = str(uuid.uuid5(uuid.NAMESPACE_DNS, img_filename))

                img_file_path = path.join(current_app.config['UPLOAD_FOLDER'], unique_name + ext)
                image_to_save = Image(name=unique_name + ext)
                try:
                    db.session.add(image_to_save)
                    db.session.commit()
                    img_file.save(img_file_path)
                    return make_response(jsonify({'source': url_for('img',
                                        id=image_to_save.id, _external=True)}))
                except:
                    return make_response(jsonify({'msg': 'Image filename is already used'}), 400)
            else:
                return make_response(jsonify({'msg': 'Image file extension is not allowed'}), 400)
        return make_response(500)
