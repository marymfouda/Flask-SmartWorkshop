from flask import current_app, request, jsonify
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

from api.DataAccessObject.Event import Event
from api.api_models import EventCreation

events_ns = Namespace(name="Events", path= '/events', validate=True,
                       description='Event information and analysis')

@events_ns.route('/', methods=['GET'])
class EventAll(Resource):
    
    @jwt_required()
    def get(self):
        # Get Pagination Values
        sort = request.args.get("sort", "keys")
        order = request.args.get("order", "ASC")
        limit = request.args.get("limit", 6, type=int)
        skip = request.args.get("skip", 0, type=int)

        dao = Event(current_app.driver)

        output = dao.all(sort, order, limit, skip)

        return jsonify(output)
