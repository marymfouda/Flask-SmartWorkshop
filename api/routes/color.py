from flask import current_app, request, jsonify
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

from api.DataAccessObject.Color import Color
from api.api_models import ColorCreation , ColorSelected

color_ns = Namespace(name="Color", path= '/colors', validate=True,
                       description='Color information and analysis')

@color_ns.route('/', methods=['GET'])
class colorAll(Resource):
    
    @jwt_required()
    def get(self):
        # Get Pagination Values
        sort = request.args.get("sort", "code")
        order = request.args.get("order", "ASC")
        limit = request.args.get("limit", 6, type=int)
        skip = request.args.get("skip", 0, type=int)

        dao = Color(current_app.driver)

        output = dao.all(sort, order, limit, skip)

        return jsonify(output)


@color_ns.route('/<int:code>')
class colorBycode(Resource):

    def get(self, code):
        dao = Color(current_app.driver)

        color = dao.findByCode(code)

        return jsonify(color)


@color_ns.route('/add')
class UserCreate(Resource):

    @color_ns.expect(ColorCreation)
    def post(self):
        dao = Color(current_app.driver)

        color = dao.addColor(color_ns.payload['code'], color_ns.payload['type'])

        return color, 201
@color_ns.route('/select')
class ColorSelected(Resource):

    @color_ns.expect(ColorSelected)
    def post(self):
        dao = Color(current_app.driver)

        color = dao.NewSelectedColor( color_ns.payload['device_id'], color_ns.payload['code'], color_ns.payload['type'] )

        return color, 201