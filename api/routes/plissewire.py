from flask import current_app, request, jsonify
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

from api.DataAccessObject.PlisseWire import PlisseWire
from api.api_models import  PlisseWireNode, PlisseWireService

plissewier_ns = Namespace(name="Plisse Wire", path= '/services/plissewire', validate=True,
                       description='Plisse Wire information and analysis')

@plissewier_ns.route('/', methods=['GET'])
class PlisseWireAll(Resource):
    
    # @jwt_required()
    def get(self):
        # Get Pagination Values
        sort = request.args.get("sort", "sector_type")
        order = request.args.get("order", "ASC")
        limit = request.args.get("limit", 6, type=int)
        skip = request.args.get("skip", 0, type=int)

        dao = PlisseWire(current_app.driver)

        output = dao.all(sort, order, limit, skip)

        return jsonify(output)


@plissewier_ns.route('/node/add')
class AddNode(Resource):

    @plissewier_ns.expect(PlisseWireNode)
    def post(self):
        dao = PlisseWire(current_app.driver)

        node = dao.addNode(**plissewier_ns.payload)

        return jsonify(node)


@plissewier_ns.route('/new')
class PlisseWireCreateService(Resource):

    @plissewier_ns.expect(PlisseWireService)
    def post(self):
        dao = PlisseWire(current_app.driver)

        service = dao.newService(**plissewier_ns.payload)
        
        if service.get('message'):
            return service, 404
        return service, 201


