from flask import url_for, flash, redirect, request, abort, jsonify, current_app
from flask_login import login_user, logout_user, current_user, login_required,\
                        fresh_login_required, login_fresh, confirm_login
from portfolio.admin import forms
from portfolio import db, bcrypt
from portfolio.models import db, Admin, Post, Tag, Image
from portfolio.views  import GeneralView, GeneralMethodView
from portfolio.tools import get_tags, file_upload_handler, image_resize
from datetime import datetime
import os.path as path
import os

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
        self._form = forms.PostForm()
        self._post_tags = get_tags(get_list=['project', 'note'])
        self._tags = get_tags(filter_con=['project', 'note'])
        self._form.post.choices.extend(list(map(
            lambda val: (val[0], val[1]), self._post_tags.items())))
        self._form.tags.choices.extend(list(map(
            lambda val: (val[0], val[1]), self._tags.items())))

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
                tags.append(Tag(name=self._form.new_tag.data.lower()))

            cover_to_save = None
            if self._form.cover.data:
                cover_img = self._form.cover.data
                save_path = file_upload_handler(cover_img,
                                                current_app.config['IMAGE_PATH'])
                if save_path:
                    _, img_filename = path.split(save_path)
                    try:
                        cover_to_save = Image(name=img_filename)
                        db.session.add(cover_to_save)
                        cover_img = image_resize(cover_img, (174, 232))
                        cover_img.save(save_path)
                    except:
                        flash('Image filename is already used', 'danger')
                        return super().post(title='New Post', form=self._form)
                elif cover_img and not(save_path):
                    flash('Cover image extension not allowed', 'danger')
                    return super().post(title='New Post', form=self._form)

            kwargs = {'complete': complete, 'title': self._form.title.data,
                    'tags': tags, 'body': self._form.body.data,
                    'author': current_user,
                    'date_posted': datetime.strptime(
                    self._form.post_datetime.data,
                    '%B/%d/%Y %H:%M:%S.%f'),
                    'cover': cover_to_save}
            new_post = Post(**kwargs)
            flash('Post Saved', 'success')
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('admin_portal.dashboard'))
        else:
            print(self._form.errors)
        return super().post(title='New Post', form=self._form)

class EditPost(GeneralMethodView):
    decorators = [login_required, fresh_login_required]

    def __init__(self, template_name):
        super().__init__(template_name)
        self._form = forms.PostForm()
        self._post_tags = get_tags(get_list=['project', 'note'])
        self._tags = get_tags(filter_con=['project', 'note'])
        self._form.post.choices.extend(list(map(
            lambda val: (val[0], val[1]), self._post_tags.items())))
        self._form.tags.choices.extend(list(map(
            lambda val: (val[0], val[1]), self._tags.items())))

        self._post_id = request.args.get('id', 0, type=int)
        self._post = Post.query.get(self._post_id) if self._post_id else None
        self._cover_name = self._post.cover.name if self._post.cover else None

    def get(self):
        if self._post_id and self._post:
            tags = tuple(map(lambda tag: str(tag.id), self._post.tags))

            self._form.post.data = list(filter(lambda tag_id: tag_id in tags,
                                                self._post_tags.keys() )).pop()
            self._form.tags.data = list(filter(lambda tag_id: tag_id in tags,
                                                self._tags.keys()))
            self._form.post_datetime.data = self._post.date_posted.strftime(
                                                        '%B/%d/%Y %H:%M:%S.%f')
            self._form.title.data = self._post.title
            self._form.body.data = self._post.body
            return super().get(title='Edit Post', form=self._form,
                            cover=self._cover_name)
        abort(404)

    def post(self):
        if self._post:
            if self._form.cancel.data:
                flash('Edit discarded', 'info')
                return redirect(url_for('admin_portal.dashboard'))
            elif self._form.validate_on_submit():
                tags = []
                tags.append(Tag.query.get(int(self._form.post.data)))
                complete = True if self._form.complete_submit.data else False
                if self._form.tags.data:
                    [tags.append(Tag.query.get(int(id))) for id in self._form.tags.data]
                if self._form.new_tag.data:
                    tags.append(Tag(name=self._form.new_tag.data.lower()))

                cover_to_save = self._post.cover
                if self._form.cover.data:
                    cover_img = self._form.cover.data
                    save_path = file_upload_handler(cover_img,
                                                    current_app.config['IMAGE_PATH'])
                    if save_path:
                        _, img_filename = path.split(save_path)
                        try:
                            if cover_to_save:
                                os.remove(path.abspath(path.join(
                                    current_app.instance_path,
                                    current_app.config['IMAGE_PATH'],
                                    cover_to_save.name)))
                                db.session.delete(cover_to_save)
                            cover_to_save = Image(name=img_filename)
                            db.session.add(cover_to_save)
                            cover_img = image_resize(cover_img, (174, 232))
                            cover_img.save(save_path)
                        except:
                            flash('Image filename is already used', 'danger')
                            return super().post(title='New Post', form=self._form)
                    elif cover_img and not(save_path):
                        flash('Cover image extension not allowed', 'danger')
                        return super().post(title='New Post', form=self._form)

                kwargs = {'complete': complete, 'title': self._form.title.data,
                        'tags': tags, 'body': self._form.body.data,
                        'author': current_user,
                        'date_posted': datetime.strptime(
                        self._form.post_datetime.data,
                        '%B/%d/%Y %H:%M:%S.%f'),
                        'cover': cover_to_save}
                [ setattr(self._post, key, value) for key, value in kwargs.items()]
                flash('Post Saved', 'success')
                db.session.commit()
                return redirect(url_for('admin_portal.dashboard'))

            else:
                print(self._form.errors)
            return super().post(title='Edit Post', form=self._form,
                            cover=self._cover_name)
        abort(404)

class PostsLog(GeneralView):
    decorators = [login_required, fresh_login_required]
    title = 'Posts'

    def dispatch_request(self):
        posts = Post.query.order_by(Post.id.desc()).all()
        return super().dispatch_request(title=self.title, catalog=posts)
