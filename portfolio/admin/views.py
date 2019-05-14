from flask import render_template, url_for, flash, redirect, request, abort
from jinja2 import TemplateNotFound
from flask_login import login_user, logout_user, current_user, login_required,\
                        fresh_login_required, login_fresh, confirm_login
from portfolio.admin import forms
from portfolio import bcrypt, Admin


from flask.views import MethodView

class GeneralView(MethodView):

    def __init__(self, template_name):
        self._template_name = template_name

    def get(self, *args, **kwargs):
        return self.render(*args, **kwargs)

    def post(self, *args, **kwargs):
        return self.render(*args, **kwargs)

    def render(self, *args, **kwargs):
        return render_template(self._template_name, *args, **kwargs)


class Login(GeneralView):

    def __init__(self, template_name):
        super().__init__(template_name)
        self._form = forms.LoginForm()

    def get(self):
        if current_user.is_authenticated and login_fresh():
            return redirect(url_for('admin.dashboard'))
        return super().get(title='Login', form=self._form)

    def post(self):
        if self._form.validate_on_submit():
            admin = Admin.query.filter_by(email=self._form.email.data).first()
            if admin and bcrypt.check_password_hash(admin.password,
                                                    self._form.password.data):
                login_user(admin, remember=self._form.remember.data)
                next_page = request.args.get('next')
                if next_page:
                    flash(f'Welcome {current_user.name}', 'success')
                    confirm_login()
                    return redirect(next_page)
                else:
                    return redirect(url_for('home'))
            else:
                flash('Login failed', 'danger')
        return super().post(title='Login', form=self._form)

class Dashboard(GeneralView):
    decorators = [login_required, fresh_login_required]
