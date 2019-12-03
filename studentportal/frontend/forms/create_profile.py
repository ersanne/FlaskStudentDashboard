from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, FileField, SelectMultipleField
from wtforms.validators import ValidationError
from flask_wtf.file import FileAllowed

from studentportal.models import mongo


class Select2MultipleField(SelectMultipleField):

    def pre_validate(self, form):
        # Prevent "not a valid choice" error
        pass


class CreateProfileForm(FlaskForm):

    # User details
    location = StringField('City')
    home_location = StringField('Home City')
    company = StringField('Work')
    website = StringField('Website')
    linked_in = StringField('LinkedIn')
    facebook = StringField('Facebook')
    twitter = StringField('Twitter')
    instagram = StringField('Instagram')
    about = TextAreaField('About')

    # Skills select2 field
    skills = Select2MultipleField('Skills', choices=[])

    # Picture
    profile_picture = FileField('Upload file', validators=[FileAllowed(['jpg', 'jpe', 'jpeg', 'png', 'gif', 'svg', 'bmp'], 'Only images allowed!')])

    # Feature options
    enable_portfolio = BooleanField('Enable Portfolio')
    enable_activity = BooleanField('Enable Activity/Timeline')

    submit = SubmitField('Create Profile')

    def validate_email(self, email):
        user = mongo.db.users.find_one({"email": email.data})
        if user is not None:
            raise ValidationError('Email already in use.')
