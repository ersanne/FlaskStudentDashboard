from flask import Blueprint

bp = Blueprint('api', __name__)

from studentportal.api import modules
