from flask import current_app, request, jsonify
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

from api.DataAccessObject.Kitchen import Kitchen
from api.api_models import KitchenNode, KitchenService

kitchen_ns = Namespace(name="Kitchen", path= '/services/kitchens', validate=True,
                       description='Rolling Shutter information and analysis')

@kitchen_ns.route('/', methods=['GET'])
class KitchenAll(Resource):
    
    @jwt_required()
    def get(self):
        # Get Pagination Values
        sort = request.args.get("sort", "type")
        order = request.args.get("order", "ASC")
        limit = request.args.get("limit", 6, type=int)
        skip = request.args.get("skip", 0, type=int)

        dao = Kitchen(current_app.driver)

        output = dao.all(sort, order, limit, skip)

        return jsonify(output)


@kitchen_ns.route('/nodes/add')
class AddNode(Resource):

    @kitchen_ns.expect(KitchenNode)
    def post(self):
        dao = Kitchen(current_app.driver)

        node = dao.addNode(kitchen_ns.payload['type'])

        return jsonify(node)


@kitchen_ns.route('/new')
class KitchenCreateService(Resource):

    @kitchen_ns.expect(KitchenService)
    def post(self):
        dao = Kitchen(current_app.driver)

        service = dao.newService(**kitchen_ns.payload)

        if service.get('message'):
            return service, 404
        return service, 201


