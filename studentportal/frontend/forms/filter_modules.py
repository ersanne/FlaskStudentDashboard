from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SelectField, SubmitField


class FilterModulesForm(FlaskForm):
    school = SelectMultipleField('School', choices=[])
    subject = SelectMultipleField('Subject', choices=[])
    scqf_level = SelectMultipleField('SCQF Level', choices=[])
    delivery_location = SelectMultipleField('Location of delivery', choices=[])
    trimester = SelectMultipleField('Trimester', choices=[])
    term = SelectMultipleField('Term', choices=[])
    delivery_mode = SelectMultipleField('Mode of delivery', choices=[])
    sort = SelectField('Sort by',
                       choices=[('module_title:1', 'Title Ascending'),
                                ('module_title:-1', 'Title Descending'),
                                ('subject:1', 'Subject Ascending'),
                                ('subject:-1', 'Subject Descending'),
                                ('scqf_level:1', 'SCQF Level Ascending'),
                                ('scqf_level:-1', 'SCQF Level Descending'),
                                ('teaching_instances.delivery_location:1', 'Location of delivery Ascending'),
                                ('teaching_instances.delivery_location:-1', 'Location of delivery Descending'),
                                ('teaching_instances.trimester:1', 'Trimester Ascending'),
                                ('teaching_instances.trimester:-1', 'Trimester Descending'),
                                ('teaching_instances.term:1', 'Term Ascending'),
                                ('teaching_instances.term:-1', 'Term Descending'),
                                ('teaching_instances.delivery_mode:1', 'Mode of Delivery Ascending'),
                                ('teaching_instances.delivery_mode:-1', 'Mode of Delivery Descending')])
    submit = SubmitField('Apply')
