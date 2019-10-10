from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, InputRequired, Email, EqualTo

from studentportal.mongo import mongo


class RegistrationForm(FlaskForm):
    username = StringField('Matriculation Number', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    password2 = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = mongo.db.users.find_one({"email": email.data})
        if user is not None:
            raise ValidationError('Email already in use.')
