from flask import current_app, request, jsonify
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

from api.DataAccessObject.Manual import Manual
from api.api_models import ManualCreation, ManualVisited

manuals_ns = Namespace(name="Manuals", path= '/manuals', validate=True,
                       description='Manual information and analysis')

@manuals_ns.route('/', methods=['GET'])
class ManualAll(Resource):
    
    @jwt_required()
    def get(self):
        # Get Pagination Values
        sort = request.args.get("sort", "name")
        order = request.args.get("order", "ASC")
        limit = request.args.get("limit", 6, type=int)
        skip = request.args.get("skip", 0, type=int)

        dao = Manual(current_app.driver)

        output = dao.all(sort, order, limit, skip)

        return jsonify(output)


@manuals_ns.route('/<string:name>')
class ManualByName(Resource):

    def get(self, name):
        dao = Manual(current_app.driver)

        person = dao.findByName(name)

        return jsonify(person)


@manuals_ns.route('/add')
class ManualCreate(Resource):

    @manuals_ns.expect(ManualCreation)
    def post(self):
        dao = Manual(current_app.driver)

        manual = dao.addManual(manuals_ns.payload['name'], manuals_ns.payload['type'])

        return manual, 201

@manuals_ns.route('/visit')
class ManualVisited(Resource):

    @manuals_ns.expect(ManualVisited)
    def post(self):
        dao = Manual(current_app.driver)

        manual = dao.newVisit(manuals_ns.payload['name'], 
                             manuals_ns.payload['type'],
                             manuals_ns.payload['device_id'])

        return manual, 201


