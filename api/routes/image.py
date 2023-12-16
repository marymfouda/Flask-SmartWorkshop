from flask import current_app, request, jsonify
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

from api.DataAccessObject.Image import Image
from api.api_models import ImageNodeCreation, ImageClicked

images_ns = Namespace(name="Images", path= '/images', validate=True,
                       description='Image information and analysis')

@images_ns.route('/', methods=['GET'])
class ImageAll(Resource):
    
    @jwt_required()
    def get(self):
        # Get Pagination Values
        sort = request.args.get("sort", "url")
        order = request.args.get("order", "ASC")
        limit = request.args.get("limit", 6, type=int)
        skip = request.args.get("skip", 0, type=int)

        dao = Image(current_app.driver)

        output = dao.all(sort, order, limit, skip)

        return jsonify(output)


@images_ns.route('/<string:url>')
class ImageByUrl(Resource):

    def get(self, url):
        dao = Image(current_app.driver)

        person = dao.findByURL(url)

        return jsonify(person)


@images_ns.route('/add')
class ImageCreate(Resource):

    @images_ns.expect(ImageNodeCreation)
    def post(self):
        dao = Image(current_app.driver)

        user = dao.addImage(images_ns.payload['url'])

        return user, 201

@images_ns.route('/click')
class ImageCreate(Resource):

    @images_ns.expect(ImageClicked)
    def post(self):
        dao = Image(current_app.driver)

        user = dao.newClick(images_ns.payload['url'], 
                            images_ns.payload['device_id'])

        return user, 201


