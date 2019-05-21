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
    if form.post.data:
        field_name = field.name if not(field.name == 'new_category') else 'category'
        field_value = field.data.lower()
        if form.post.data == 'projects':
            get_field = Project.query.filter_by(**{field_name: field_value}).first()
        else:
            get_field = Note.query.filter_by(**{field_name: field_value}).first()
        if get_field:
            raise ValidationError(f'{field.data} is already taken or in used')
    else:
        raise ValidationError('No post type specified')


class NewPostForm(FlaskForm):
    post = SelectField(u'Post', choices=[('projects', 'Project'),
                                        ('notes', 'Note')])
    category = SelectField(u'Category', choices=[], validators=[Optional()])
    new_category = StringField(u'New Category', validators=[Optional(), unique_post])
    title = StringField(u'Title', validators=[InputRequired(),
                                            DataRequired(),
                                            unique_post])
    descript = StringField(u'Brief Summary', validators=[InputRequired(),
                                                        DataRequired()])
    doc = TextAreaField(u'Documentation', validators=[InputRequired(), DataRequired()])
    template = StringField(u'Html File', validators=[Optional(), unique_post])
    draft_submit = SubmitField(u'Save as Draft', validators=[Optional()])
    complete_submit = SubmitField(u'Publish', validators=[Optional()])
    cancel = SubmitField(u'Cancel', validators=[Optional()])

class SelectPost(FlaskForm):
    post = SelectField(u'Post', choices=[('projects', 'Project'),
                                        ('notes', 'Note')])
    title = SelectField(u'Title', choices=[], validators=[Optional()])
    select = SubmitField(u'Select')
