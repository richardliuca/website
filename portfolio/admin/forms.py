from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,\
                    TextAreaField, SelectField, DateTimeField
from wtforms.validators import InputRequired, DataRequired, Length, Email,\
                                EqualTo, Optional, ValidationError
from portfolio.models import Project, Note

class LoginForm(FlaskForm):
    email = StringField(u'Email Address', validators=[InputRequired(),
                                                    DataRequired(),
                                                    Email()])
    password = PasswordField(u'Password', validators=[InputRequired(),
                                                    DataRequired()])
    remember = BooleanField(u'Remember Me')
    submit = SubmitField(u'Login')

def unique_post(form, field):
    if unique_post.post.data:
        if unique_post.post.data == 'projects':
            get_field = Project.query.filter_by(**{field.name: field.data}).first()
        else:
            get_field = Note.query.filter_by(**{field.name: field.data}).first()
        if get_field:
            raise ValueError(f'{field.data} is already taken or in used')
    else:
        raise ValidationError('No post type specified')


class NewPostForm(FlaskForm):
    post = SelectField(u'Post', choices=[('projects', 'Project'),
                                        ('notes', 'Note')])
    category = SelectField(u'Category')
    date = DateTimeField(u'Date', validators=[Optional()])
    title = StringField(u'Title', validators=[InputRequired(),
                                            DataRequired(),
                                            unique_post])
    descript = StringField(u'Short Summary', validators=[InputRequired(),
                                                        DataRequired()])
    doc = TextAreaField(u'More', validators=[InputRequired(), DataRequired()])
    template = StringField(u'Html File', validators=[Optional(), unique_post])
    draft_submit = SubmitField(u'Save as Draft', validators=[Optional()])
    complete_submit = SubmitField(u'Publish', validators=[Optional()])
    cancel = SubmitField(u'Cancel', validators=[Optional()])
