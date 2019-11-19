from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, FileField, SelectField
from wtforms.validators import ValidationError, InputRequired
from flask_wtf.file import FileAllowed

from studentportal.models import mongo


class CreateProfileForm(FlaskForm):

    # User details
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

    # Skills select2 field
    skills = SelectField('Skills', choices=[])

    # Picture
    images = UploadSet('images', IMAGES)
    profile_picture = FileField('Upload file', validators=[FileAllowed(images, 'Only images allowed!')])

    # Feature options
    enable_portfolio = BooleanField('Enable Portfolio')
    enable_activity = BooleanField('Enable Activity/Timeline')

    submit = SubmitField('Create Profile')

    def validate_email(self, email):
        user = mongo.db.users.find_one({"email": email.data})
        if user is not None:
            raise ValidationError('Email already in use.')
