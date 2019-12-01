from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField
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
    username = StringField('Matriculation Number', validators=[InputRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class DataSetupForm(FlaskForm):
    first_name = StringField('First name', validators=[InputRequired()])
    last_name = StringField('Last name', validators=[InputRequired()])
    course_title = StringField('Course title', validators=[InputRequired()])
    year_of_study = SelectField('Year of study', choices=[(1, 1), (8, 8)], validators=[InputRequired()])
    current_scqf_level = SelectField('Current SCQF level', choices=[(7, 7), (8, 8)], validators=[InputRequired()])
    # enrolled_modules = SelectMultipleField('All currently enrolled modules', choices=[], validators=[InputRequired()])
    submit = SubmitField('Finish setup')


class UsernameForm(FlaskForm):
    username = StringField('Matriculation Number', validators=[InputRequired(), username()])


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[InputRequired()])
    password2 = PasswordField('Confirm New Password', validators=[InputRequired(), EqualTo('password')])
