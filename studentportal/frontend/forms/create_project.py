from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, FileField, SelectMultipleField
from wtforms.validators import ValidationError, InputRequired
from flask_wtf.file import FileAllowed

from studentportal.models import mongo
from .util import Select2MultipleField


class CreateProfileForm(FlaskForm):

    # User details
    project_title = StringField('Title', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[])
    members = Select2MultipleField('Members')

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
