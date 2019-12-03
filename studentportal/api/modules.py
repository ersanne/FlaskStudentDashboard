from flask import request
from studentportal.api import bp
from studentportal.models import mongo
from bson.json_util import dumps
from json import dumps as json_dumps

@bp.route('/modules/autocomplete')
def modules_autocomplete():
    search = request.args.get('search')
    page = request.args.get('page', 1, type=int)
    skips = (page - 1) * 10
    try:
        return dumps(mongo.db.modules.find({"$text": {"$search": search.strip()}},
                                           {'score': {"$meta": "textScore"}}
                                           ).sort([('score', {'$meta': 'textScore'})]).skip(skips).limit(10))
    except:
        return json_dumps({"error": "Could not run search query."})
