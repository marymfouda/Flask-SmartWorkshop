from flask import current_app, request, jsonify
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

from api.DataAccessObject.Material import Material
from api.api_models import MaterialCreation, MaterialSelected

materials_ns = Namespace(name="Materials", path= '/materials', validate=True,
                       description='Material information and analysis')

@materials_ns.route('/', methods=['GET'])
class MaterialAll(Resource):
    
    # @jwt_required()
    def get(self):
        # Get Pagination Values
        sort = request.args.get("sort", "id")
        order = request.args.get("order", "ASC")
        limit = request.args.get("limit", 6, type=int)
        skip = request.args.get("skip", 0, type=int)

        dao = Material(current_app.driver)

        output = dao.all(sort, order, limit, skip)

        return jsonify(output)


@materials_ns.route('/<string:name>')
class MaterialByName(Resource):

    def get(self, name):
        dao = Material(current_app.driver)

        material = dao.findByName(name)

        return jsonify(material)


@materials_ns.route('/add')
class MaterialCreate(Resource):

    @materials_ns.expect(MaterialCreation)
    def post(self):
        dao = Material(current_app.driver)

        material = dao.addMaterial(materials_ns.payload['name'])

        return material, 201

@materials_ns.route('/select')
class MaterialCreate(Resource):

    @materials_ns.expect(MaterialSelected)
    def post(self):
        dao = Material(current_app.driver)

        material = dao.newSelection(materials_ns.payload['device_id'], materials_ns.payload['name'])

        return material, 201

