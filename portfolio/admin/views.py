from flask import url_for, flash, redirect, request, abort, jsonify
from flask_login import login_user, logout_user, current_user, login_required,\
                        fresh_login_required, login_fresh, confirm_login
from portfolio.admin import forms
from portfolio import db, bcrypt
from portfolio.models import db, Admin, Post, Tag
from portfolio.views  import GeneralView, GeneralMethodView
from portfolio.catalog import Catalog

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
        self._post_tags = get_tags(get_list=['project', 'note'])
        self._tags = get_tags(filter_con=['project', 'note'])
        self._form.post.choices.extend(list(map(
            lambda val: (val[0], val[1]), self._post_tags.items()
            )))
        self._form.tags.choices.extend(list(map(
            lambda val: (val[0], val[1]), self._tags.items()
            )))

    def get(self):
        return super().get(title='New Post', form=self._form)

    def post(self):
        if self._form.cancel.data:
            flash('New post cancelled', 'info')
            return redirect(url_for('admin_portal.dashboard'))
        elif self._form.validate_on_submit():
            tags = []
            tags.append(Tag.query.get(int(self._form.post.data)))
            complete = True if self._form.complete_submit.data else False
            if self._form.tags.data:
                [tags.append(Tag.query.get(int(id))) for id in self._form.tags.data]
            if self._form.new_tag.data:
                tags.append(Tag(name=self._form.new_tag.data))

            kwargs = {'complete': complete, 'title': self._form.title.data,
                    'tags': tags, 'body': self._form.body.data,
                    'author': current_user}
            new_post = Post(**kwargs)
            flash('Post Saved', 'success')
            print(kwargs)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('admin_portal.dashboard'))
        else:
            print(self._form.errors)
        return super().post(title='New Post', form=self._form)

def get_tags(filter_con=[], get_list=[]):
    tags = Tag.query
    choices = {}
    if filter_con:
        for filter in filter_con:
            tags = tags.filter(Tag.name != filter)
    elif get_list:
        tags = tags.filter(db.or_(*[Tag.name == filter for filter in get_list]))
    tags = tags.all()
    list(map(lambda x: choices.update({str(x.id) : x.name.capitalize()}), tags))
    return choices
