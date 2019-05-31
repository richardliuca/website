from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,\
                    TextAreaField, SelectField, DateTimeField
from wtforms.validators import InputRequired, DataRequired, Length, Email,\
                                EqualTo, Optional, ValidationError
from portfolio.models import Post

class LoginForm(FlaskForm):
    email = StringField(u'Email Address', validators=[InputRequired(),
                                                    DataRequired(),
                                                    Email()])
    password = PasswordField(u'Password', validators=[InputRequired(),
                                                    DataRequired()])
    remember = BooleanField(u'Remember Me')
    submit = SubmitField(u'Login')

def unique_post(form, field):
    if form.post.data:
        field_name = field.name if not(field.name == 'new_category') else 'category'
        field_value = field.data.lower()

        get_field = Post.query.filter_by(post_type=form.post.data,
                                            **{field_name: field_value}).first()

        if get_field:
            raise ValidationError(f'{field.data} is already taken or in used')
    else:
        raise ValidationError('No post type specified')


class NewPostForm(FlaskForm):
    post = SelectField(u'Post', choices=[('project', 'Project'),
                                        ('note', 'Note')])
    category = SelectField(u'Category', choices=[], validators=[Optional()])
    new_category = StringField(u'New Category', validators=[Optional(), unique_post])
    title = StringField(u'Title', validators=[InputRequired(),
                                            DataRequired(),
                                            unique_post])
    descript = StringField(u'Brief Summary', validators=[InputRequired(),
                                                        DataRequired()])
    doc = TextAreaField(u'Documentation', validators=[InputRequired(), DataRequired()])
    draft_submit = SubmitField(u'Save as Draft', validators=[Optional()])
    complete_submit = SubmitField(u'Publish', validators=[Optional()])
    cancel = SubmitField(u'Cancel', validators=[Optional()])

class SelectPost(NewPostForm):
    id_title = SelectField(u'Title', choices=[], validators=[Optional()])
    select = SubmitField(u'Select')
