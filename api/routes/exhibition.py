from flask import current_app, request, jsonify
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

from api.DataAccessObject.Exhibition import Exhibition
from api.api_models import ExhibitionCreation , ExhibitionViewed

exhbitions_ns = Namespace(name="Exhibitions", path= '/exhbitions', validate=True,
                       description='Exhibition information and analysis')

@exhbitions_ns.route('/', methods=['GET'])
class ExhibitionAll(Resource):
    
    @jwt_required()
    def get(self):
        # Get Pagination Values
        sort = request.args.get("sort", "name")
        order = request.args.get("order", "ASC")
        limit = request.args.get("limit", 6, type=int)
        skip = request.args.get("skip", 0, type=int)

        dao = Exhibition(current_app.driver)

        output = dao.all(sort, order, limit, skip)

        return jsonify(output)


@exhbitions_ns.route('/<string:name>')
class ExhibitionById(Resource):

    def get(self, name):
        dao = Exhibition(current_app.driver)

        ex = dao.findByName(name)

        return jsonify(ex)


@exhbitions_ns.route('/add')
class ExhibitionCreate(Resource):

    @exhbitions_ns.expect(ExhibitionCreation)
    def post(self):
        dao = Exhibition(current_app.driver)

        ex = dao.addExhibition(**exhbitions_ns.payload)

        return ex, 201
    
@exhbitions_ns.route('/viewed')
class ViewedGallery(Resource):

    @exhbitions_ns.expect(ExhibitionViewed)
    def post(self):
        dao = Exhibition(current_app.driver)

        exhbition = dao.NewViewedGallery(**exhbitions_ns.payload)

        return exhbition, 201


