from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField, Form
from wtforms.validators import ValidationError, DataRequired, EqualTo
from studentportal.models import mongo


class Select2MultipleField(SelectMultipleField):

    def pre_validate(self, form):
        # Prevent "not a valid choice" error
        pass


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Matriculation Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password',
                              validators=[DataRequired(), EqualTo('password', 'Passwords do not match.')])
    submit = SubmitField('Sign Up')

    def validate_username(form, field):
        if field.data.endswith('@live.napier.ac.uk'):
            field.data = field.data[:-18]
        user = mongo.db.users.find_one({"_id": field.data})
        if user:
            raise ValidationError('User is already registered.')


class DataSetupForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired('First name is required')])
    last_name = StringField('Last name', validators=[DataRequired('Last name is required')])
    course_title = StringField('Course title', validators=[DataRequired('Course Title is required')])
    year_of_study = SelectField('Year of study',
                                choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9),
                                         (10, 10)], coerce=int)
    current_scqf_level = SelectField('Current SCQF level', choices=[(7, 7), (8, 8), (9, 9), (10, 10), (11, 11)], coerce=int)
    enrolled_modules = Select2MultipleField('All currently enrolled modules', choices=[])
    submit = SubmitField('Finish setup')


class RequestPasswordResetForm(FlaskForm):
    username = StringField('Matriculation Number or Email', validators=[DataRequired()])
    submit = SubmitField('Request password reset')

    def validate_username(form, field):
        if field.data.endswith('@live.napier.ac.uk'):
            field.data = field.data[:-18]
        user = mongo.db.users.find_one({"_id": field.data})
        if not user:
            raise ValidationError('User not found!')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm New Password',
                              validators=[DataRequired(), EqualTo('password', 'Passwords do not match.')])
    submit = SubmitField('Reset password')
