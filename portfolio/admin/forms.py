from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,\
                    TextAreaField, SelectField, SelectMultipleField,DateTimeField
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
    title = StringField(u'Title', validators=[InputRequired(), DataRequired()])
    body = TextAreaField(u'Content', validators=[InputRequired(), DataRequired()])
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

class SelectPost(NewPostForm):
    id_title = SelectField(u'Title', choices=[], validators=[Optional()])
    select = SubmitField(u'Select')
