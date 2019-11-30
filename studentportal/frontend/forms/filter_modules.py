from flask_uploads import UploadSet, IMAGES
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, FileField, SelectMultipleField

from studentportal.models import mongo


class FilterModulesForm(FlaskForm):
    test = BooleanField('Test')


for school in mongo.db.modules.distinct('school'):
    setattr(FilterModulesForm, school.replace(" ", "_").lower(), BooleanField(school))
