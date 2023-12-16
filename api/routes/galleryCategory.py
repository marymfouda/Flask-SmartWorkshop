from flask import current_app, request, jsonify
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

from api.DataAccessObject.GalleryCategory import GalleryCategory
from api.api_models import GalleryCategoryCreation

gallerycatgorys_ns = Namespace(name="Gallery Category", path= '/gallerycategories', validate=True,
                       description='Gallery Category information and analysis')

@gallerycatgorys_ns.route('/', methods=['GET'])
class GalleryCategoryAll(Resource):
    
    @jwt_required()
    def get(self):
        # Get Pagination Values
        sort = request.args.get("sort", "name")
        order = request.args.get("order", "ASC")
        limit = request.args.get("limit", 6, type=int)
        skip = request.args.get("skip", 0, type=int)

        dao = GalleryCategory(current_app.driver)

        output = dao.all(sort, order, limit, skip)

        return jsonify(output)


@gallerycatgorys_ns.route('/<string:name>')
class GalleryCategoryById(Resource):

    def get(self, name):
        dao = GalleryCategory(current_app.driver)

        person = dao.findByName(name)

        return jsonify(person)


@gallerycatgorys_ns.route('/add')
class GalleryCategoryCreate(Resource):

    @gallerycatgorys_ns.expect(GalleryCategoryCreation)
    def post(self):
        dao = GalleryCategory(current_app.driver)

        user = dao.addGalleryCategory(gallerycatgorys_ns.payload['name'])

        return user, 201


