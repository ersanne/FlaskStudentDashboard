from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, InputRequired, DataRequired, EqualTo
from studentportal.models import mongo


class Username(object):
    def __init__(self, error_message=None):
        if not error_message:
            error_message = 'Username not valid'
        self.error_message = error_message

    def __call__(self, form, field):
        user = mongo.db.users.find_one({"_id": field.data})
        if not user:
            raise ValidationError(self.error_message)


username = Username


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Matriculation Number', validators=[InputRequired(), username()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class UsernameForm(FlaskForm):
    username = StringField('Matriculation Number', validators=[InputRequired(), username()])


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[InputRequired()])
    password2 = PasswordField('Confirm New Password', validators=[InputRequired(), EqualTo('password')])
