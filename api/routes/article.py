from flask import current_app, request, jsonify
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

from api.DataAccessObject.Article import Article
from api.api_models import ArticleCreation , ArticleViewed

articals_ns = Namespace(name="Articles", path= '/articles', validate=True,
                       description='Article information and analysis')

@articals_ns.route('/', methods=['GET'])
class ArticleAll(Resource):
    
    @jwt_required()
    def get(self):
        # Get Pagination Values
        sort = request.args.get("sort", "title")
        order = request.args.get("order", "ASC")
        limit = request.args.get("limit", 6, type=int)
        skip = request.args.get("skip", 0, type=int)

        dao = Article(current_app.driver)

        output = dao.all(sort, order, limit, skip)

        return jsonify(output)


@articals_ns.route('/<string:title>')
class ArticleByTitle(Resource):

    def get(self, title):
        dao = Article(current_app.driver)

        article = dao.findByTitle(title)

        return jsonify(article)


@articals_ns.route('/add')
class ArticleCreate(Resource):

    @articals_ns.expect(ArticleCreation)
    def post(self):
        dao = Article(current_app.driver)

        artical = dao.addArticle(articals_ns.payload['title'], articals_ns.payload['text'])

        return artical, 201
@articals_ns.route('/viewedarticle')
class ArticleViewed(Resource):

    @articals_ns.expect(ArticleViewed)
    def post(self):
        dao = Article(current_app.driver)

        artical = dao.NewViewedArticle( articals_ns.payload['device_id'], articals_ns.payload['title'], articals_ns.payload['text'] )

        return artical, 201

