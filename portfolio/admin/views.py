from flask import url_for, flash, redirect, request, abort
from flask_login import login_user, logout_user, current_user, login_required,\
                        fresh_login_required, login_fresh, confirm_login
from portfolio.admin import forms
from portfolio import db, bcrypt
from portfolio.models import Admin, Project, Note
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
        if self._form.validate_on_submit():
            complete = False
            if self._form.cancel.data:
                flash('New post cancelled', 'info')
                return redirect(url_for('admin_portal.dashboard'))
            elif self._form.draft_submit.data:
                flash('New post drafted', 'info')
            elif self._form.complete_submit.data:
                flash('New post publish', 'info')
                complete = True
            else:
                flash('Error has occurred', 'danger')

            if self._form.new_category.data:
                category = self._form.category.data
            elif self._form.category.data:
                category = self._form.category.data
            else:
                category = None

            if self._form.post.data:
                if form.post.data == 'projects':
                    new = Project(complete=complete,
                                    title=self._form.title.data,
                                    category=category,
                                    description=self._form.descript.data,
                                    documentation=self._form.doc.data,
                                    template=self._form.template.data,
                                    lead=current_user)
                elif form.post.data == 'notes':
                    new = Note(complete=complete,
                                    title=self._form.title.data,
                                    category=category,
                                    description=self._form.descript.data,
                                    documentation=self._form.doc.data,
                                    template=self._form.template.data,
                                    author=current_user)
                else:
                    pass

                db.session.add(new)
                db.session.commit()
            else:
                flash('No post type specified', 'danger')
                return redirect(url_for('admin_portal.new_post'))
            return redirect(url_for('admin_portal.dashboard'))

        return super().post(title='New Post', form=self._form)

class EditPost(GeneralMethodView):
    pass

class Database(GeneralView):
    pass
