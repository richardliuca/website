from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,\
                    TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional,\
                    ValidationError

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
