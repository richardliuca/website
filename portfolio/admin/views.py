from flask import url_for, flash, redirect, request, abort, jsonify
from flask_login import login_user, logout_user, current_user, login_required,\
                        fresh_login_required, login_fresh, confirm_login
from portfolio.admin import forms
from portfolio import db, bcrypt
from portfolio.models import Admin, Post
from portfolio.views  import GeneralView, GeneralMethodView

class Login(GeneralMethodView):

    def __init__(self, template_name):
        super().__init__(template_name)
        self._form = forms.LoginForm()

    def get(self):
        if current_user.is_authenticated and login_fresh():
            return redirect(url_for('admin_portal.dashboard'))
        return super().get(title='Login', form=self._form)

    def post(self):
        if self._form.validate_on_submit():
            admin = Admin.query.filter_by(email=self._form.email.data).first()
            if admin and bcrypt.check_password_hash(admin.password,
                                                    self._form.password.data):
                login_user(admin, remember=self._form.remember.data)
                next_page = request.args.get('next')
                flash(f'Welcome {current_user.name}', 'success')
                if next_page:
                    confirm_login()
                    return redirect(next_page)
                else:
                    return redirect(url_for('admin_portal.dashboard'))
            else:
                flash('Login failed', 'danger')
        return super().post(title='Login', form=self._form)

class Logout(GeneralView):

    def dispatch_request(self, *args, **kwargs):
        if current_user.is_authenticated:
            try:
                logout_user()
                flash('Logged out', 'success')
                return redirect(url_for('front_page.home'))
            except:
                flash('Logout errored', 'danger')
        else:
            flash('Your were not logged in', 'info')

        if request.referrer:
            return redirect(request.referrer)
        else:
            return redirect(url_for('front_page.home'))

class Dashboard(GeneralMethodView):
    decorators = [login_required, fresh_login_required]

    def get(self):
        return super().get(title='Dashboard')

class NewPost(GeneralMethodView):
    decorators = [login_required, fresh_login_required]

    def __init__(self, template_name):
        super().__init__(template_name)
        self._form = forms.NewPostForm()

    def get(self):
        return super().get(title='New Post', form=self._form)

    def post(self):
        category_choices = _get_category(self._form.post.data).get_json()
        for key, val in category_choices.items():
            self._form.category.choices.append((val, key))

            print(self._form.category.choices)

        if self._form.validate_on_submit():
            if self._form.cancel.data:
                flash('New post cancelled', 'info')
                return redirect(url_for('admin_portal.dashboard'))
            else:
                complete = True if self._form.complete_submit.data else False

            if self._form.new_category.data:
                category = self._form.new_category.data.lower()
            elif self._form.category.data:
                category = self._form.category.data.lower()
            else:
                category = 'none'

            if self._form.post.data:
                kwargs = {'post_type': self._form.post.data,
                        'complete': complete,
                        'title': self._form.title.data,
                        'category': category,
                        'description': self._form.descript.data,
                        'documentation': self._form.doc.data,
                        'author': current_user}
                new = Post(**kwargs)
                flash('Post Saved', 'success')
                db.session.add(new)
                db.session.commit()
            else:
                flash('No post type specified', 'danger')
                return redirect(url_for('admin_portal.new_post'))
            return redirect(url_for('admin_portal.dashboard'))
        else:
            print(self._form.errors)
        return super().post(title='New Post', form=self._form)

class EditPost(GeneralMethodView):
    decorators = [login_required, fresh_login_required]

    def __init__(self, template_name):
        super().__init__(template_name)
        self._form = forms.SelectPost()

    def get(self, **kwargs):
        if not kwargs:
            return super().get(title='Edit Post', form=self._form)
        else:
            self.add_title_choices(kwargs['post'])

            self.add_category_choices(kwargs['post'])
            post_id = request.args.get('id', None)

            if post_id and not(post_id == 'None'):
                post = Post.query.get(post_id)
            else:
                abort(404)

            self._form.post.data = kwargs['post']
            self._form.id_title.data = post_id
            self._form.category.data = post.category
            self._form.title.data = post.title
            self._form.descript.data = post.description
            self._form.doc.data = post.documentation
            return super().get(title=f'Edit {post.title}', form=self._form)

    def post(self, **kwargs):
        self.add_title_choices(self._form.post.data)
        if kwargs:
            self.add_category_choices(kwargs['post'])
            post_id = request.args.get('id', None)

        if self._form.validate_on_submit():
            if not(post_id):
                abort(404)
            post = Post.query.get(post_id)

            if self._form.cancel.data:
                db.session.delete(post)
                db.session.commit()
                flash('Post deleted', 'success')
                return redirect(url_for('admin_portal.edit_post'))
            elif self._form.draft_submit.data:
                post.complete = False
            elif self._form.complete_submit.data:
                post.complete = True
            elif self._form.select.data:
                return redirect(url_for('admin_portal.edit',
                                        post=self._form.post.data,
                                        id=self._form.id_title.data))

            if self._form.new_category.data:
                category = self._form.new_category.data.lower()
            elif self._form.category.data:
                category = self._form.category.data.lower()
            else:
                category = 'none'

            post.title = self._form.title.data
            post.category = category
            post.description = self._form.descript.data
            post.documentation = self._form.doc.data
            db.session.commit()
            flash('Post modified', 'success')
            return redirect(url_for('admin_portal.dashboard'))
        elif self._form.select.data:
            if not(self._form.id_title.data) or \
                                            self._form.id_title.data == 'None':
                print('aborting in post')
                abort(404)
            return redirect(url_for('admin_portal.edit',
                                    post=self._form.post.data,
                                    id=self._form.id_title.data))
        else:
            print(self._form.errors)

        if kwargs:
            return super().post(title=f'Edit {self._form.title.data}',
                                form=self._form)
        else:
            return redirect(url_for('admin_portal.edit_post'))

    def add_title_choices(self, post_type):
        title_choices = _get_title(post_type).get_json()
        title_total = []
        for key, val in title_choices.items():
            title_total.append((str(val), key))
        self._form.id_title.choices = title_total

    def add_category_choices(self, post_type):
        category_choices = _get_category(post_type).get_json()
        choices_total = []
        for key, val in category_choices.items():
            choices_total.append((val, key))
        self._form.category.choices = choices_total

def _get_category(alt_get=None):
    post = request.args.get('post', None)
    post = post if post else alt_get
    output_category = {}
    category = db.session.query(Post.category).filter_by(post_type=post).all()
    # if not(category):
    #     return jsonify(result=None)

    none_sort = lambda pair: pair[0] != 'None'
    pre_json = set(filter(none_sort, category))
    pre_json = set(category)
    for pair in pre_json:
        output_category.update({pair[0].title(): pair[0]})
    return jsonify(**output_category)

def _get_title(alt_get=None):
    post = request.args.get('post', None)
    post = post if post else alt_get
    output_title = {}
    title = db.session.query(Post.title, Post.id).filter_by(post_type=post).all()
    for pair in title:
        output_title.update({pair[0]: pair[1]})
    return jsonify(**output_title)
