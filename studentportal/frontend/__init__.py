from flask import Blueprint

bp = Blueprint('frontend', __name__, template_folder='templates')

from studentportal.frontend import views