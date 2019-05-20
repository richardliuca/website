from flask import url_for, flash, redirect, request, abort
from flask_login import login_user, logout_user, current_user, login_required,\
                        fresh_login_required, login_fresh, confirm_login
from portfolio.admin import forms
from portfolio import bcrypt, Admin
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
        print(self._form.errors)
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
        pass

class EditPost(GeneralMethodView):
    pass

class Database(GeneralView):
    pass
