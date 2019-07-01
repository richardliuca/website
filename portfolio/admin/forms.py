from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,\
                    TextAreaField, SelectField, SelectMultipleField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import InputRequired, DataRequired, Length, Email,\
                                EqualTo, Optional, ValidationError
from portfolio.models import Post, Tag

class LoginForm(FlaskForm):
    email = StringField(u'Email Address', validators=[InputRequired(),
                                                    DataRequired(),
                                                    Email()])
    password = PasswordField(u'Password', validators=[InputRequired(),
                                                    DataRequired()])
    remember = BooleanField(u'Remember Me')
    submit = SubmitField(u'Login')

class NewPostForm(FlaskForm):
    post = SelectField(u'Post', choices=[])
    tags = SelectMultipleField(u'Tag', choices=[], validators=[Optional()])
    new_tag = StringField(u'New Tag', validators=[Optional()])
    post_datetime = StringField(u'Date Time', validators=[InputRequired(),
                                                            DataRequired()])
    title = StringField(u'Title', validators=[InputRequired(), DataRequired()])
    body = TextAreaField(u'Content', validators=[InputRequired(),
                                                DataRequired()])
    cover = FileField(u'Cover Photo', validators=[FileAllowed(
                                                ['png', 'jpg', 'jpeg', 'gif'],
                                                 'Images Only!')])
    draft_submit = SubmitField(u'Save as Draft', validators=[Optional()])
    complete_submit = SubmitField(u'Publish', validators=[Optional()])
    cancel = SubmitField(u'Cancel', validators=[Optional()])

    def validate_title(form, field):
        get_title = Post.query.filter_by(**{field.name: field.data}).first()
        if get_title:
            raise ValidationError(f'{field.data} is already taken or in used')

    def validate_new_tag(form, field):
        get_tag = Tag.query.filter_by(name=field.data).first()
        if get_tag:
            raise ValidationError(f'{field.data} is already taken or in used')
