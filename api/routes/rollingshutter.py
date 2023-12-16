from flask import current_app, request, jsonify
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

from api.DataAccessObject.RollingShutter import RollingShutter
from api.api_models import RollingShutterNode, RollingShutterService

rollingshutter_ns = Namespace(name="Rolling Shutter", path= '/services/rollingshutter', validate=True,
                       description='Rolling Shutter information and analysis')

@rollingshutter_ns.route('/', methods=['GET'])
class RollingShutterAll(Resource):
    
    # @jwt_required()
    def get(self):
        # Get Pagination Values
        sort = request.args.get("sort", "type")
        order = request.args.get("order", "ASC")
        limit = request.args.get("limit", 6, type=int)
        skip = request.args.get("skip", 0, type=int)

        dao = RollingShutter(current_app.driver)

        output = dao.all(sort, order, limit, skip)

        return jsonify(output)


@rollingshutter_ns.route('/node/add')
class AddNode(Resource):

    @rollingshutter_ns.expect(RollingShutterNode)
    def post(self):
        dao = RollingShutter(current_app.driver)

        node = dao.addNode(rollingshutter_ns.payload['type'])

        return jsonify(node)


@rollingshutter_ns.route('/new')
class RollingShutterCreateService(Resource):

    @rollingshutter_ns.expect(RollingShutterService)
    def post(self):
        dao = RollingShutter(current_app.driver)

        service = dao.newService(rollingshutter_ns.payload['device_id'], 
                                  rollingshutter_ns.payload['type'],
                                  rollingshutter_ns.payload['height'],
                                  rollingshutter_ns.payload['width'],
                                  rollingshutter_ns.payload['piece_count'])
        if service.get('message'):
            return service, 404
        return service, 201


