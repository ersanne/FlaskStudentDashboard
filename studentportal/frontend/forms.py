from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, InputRequired, Email, EqualTo

from studentportal.models import mongo


class CreateProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    location = StringField('City')
    home_location = StringField('Home City')
    company = StringField('Work')
    website = StringField('Website')
    linked_in = StringField('LinkedIn')
    facebook = StringField('Facebook')
    twitter = StringField('Twitter')
    instagram = StringField('Instagram')
    about = TextAreaField('About')
    submit = SubmitField('Create Profile')

    def validate_email(self, email):
        user = mongo.db.users.find_one({"email": email.data})
        if user is not None:
            raise ValidationError('Email already in use.')
