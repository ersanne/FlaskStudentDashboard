from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField


class FilterModulesForm(FlaskForm):

    school = SelectMultipleField('School', choices=[])
    subject = SelectMultipleField('Subject', choices=[])
    scqf_level = SelectMultipleField('SCQF Level', choices=[])
    delivery_location = SelectMultipleField('Location of delivery', choices=[])
    trimester = SelectMultipleField('Trimester', choices=[])
    term = SelectMultipleField('Term', choices=[])
    delivery_mode = SelectMultipleField('Mode of delivery', choices=[])

    submit = SubmitField('Apply')
