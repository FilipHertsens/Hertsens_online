from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, HiddenField, IntegerField, MultipleFileField, TextAreaField
from wtforms.validators import InputRequired, Email, Length


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')
