from flask import current_app, request, jsonify
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

from api.DataAccessObject.Window import Window
from api.api_models import WindowNode, WindowService

window_ns = Namespace(name="Window", path= '/services/window', validate=True,
                       description='Rolling Shutter information and analysis')

@window_ns.route('/', methods=['GET'])
class WindowAll(Resource):
    
    # @jwt_required()
    def get(self):
        # Get Pagination Values
        sort = request.args.get("sort", "type")
        order = request.args.get("order", "ASC")
        limit = request.args.get("limit", 6, type=int)
        skip = request.args.get("skip", 0, type=int)

        dao = Window(current_app.driver)

        output = dao.all(sort, order, limit, skip)

        return jsonify(output)


@window_ns.route('/node/add')
class AddNode(Resource):

    @window_ns.expect(WindowNode)
    def post(self):
        dao = Window(current_app.driver)

        node = dao.addNode(window_ns.payload['type'])

        return jsonify(node)


@window_ns.route('/new')
class WindowCreateService(Resource):

    @window_ns.expect(WindowService)
    def post(self):
        dao = Window(current_app.driver)

        service = dao.newService(**window_ns.payload)

        if service.get('message'):
            return service, 404
        return service, 201


