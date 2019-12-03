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
    password2 = PasswordField('Confirm Password',
                              validators=[DataRequired(), EqualTo('password', 'Passwords do not match.')])
    submit = SubmitField('Sign Up')

    def validate_username(form, field):
        user = mongo.db.users.find_one({"_id": field.data})
        if user:
            raise ValidationError('User is already registered.')


class DataSetupForm(FlaskForm):
    first_name = StringField('First name', validators=[InputRequired('First name is required')])
    last_name = StringField('Last name', validators=[InputRequired('Last name is required')])
    course_title = StringField('Course title', validators=[InputRequired('Course Title is required')])
    year_of_study = SelectField('Year of study', choices=[(1, 1), (8, 8)],
                                validators=[InputRequired('Year of study is required')])
    current_scqf_level = SelectField('Current SCQF level', choices=[(7, 7), (8, 8)], validators=[InputRequired('')])
    enrolled_modules = SelectMultipleField('All currently enrolled modules', choices=[], validators=[InputRequired()])
    submit = SubmitField('Finish setup')


class UsernameForm(FlaskForm):
    username = StringField('Matriculation Number', validators=[InputRequired(), username()])


class RequestPasswordResetForm(FlaskForm):
    username = StringField('Matriculation Number or Email', validators=[InputRequired()])
    submit = SubmitField('Request password reset')

    def validate_username(form, field):
        user = mongo.db.users.find_one({"_id": field.data})
        if not user:
            raise ValidationError('User not found!')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[InputRequired()])
    password2 = PasswordField('Confirm New Password',
                              validators=[InputRequired(), EqualTo('password', 'Passwords do not match.')])
    submit = SubmitField('Reset password')