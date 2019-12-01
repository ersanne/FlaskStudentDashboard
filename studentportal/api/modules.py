from studentportal.api import bp
from studentportal.models import mongo
from bson.json_util import dumps


@bp.route('/modules/autocomplete/<search_string>')
def modules(search_string):
    return dumps(mongo.db.modules.find({"$text": {"$search": search_string.strip()}},
                                 {'score': {"$meta": "textScore"}}
                                 ).sort([('score', {'$meta': 'textScore'})]))
