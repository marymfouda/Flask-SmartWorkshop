from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager 

from .neo4j import init_driver


#### Swagger Authorization Pattern
authorizations = {
'Bearer Auth': {
    'type': 'apiKey',
    'in': 'header',
    'name': 'Authorization'
    }
}

### Extentions
api = Api(ordered=True, title='Warsha', prefix='/api',
            description='The Smart Workshop Admin Panel APIs',
            security='Bearer Auth', authorizations=authorizations)

jwt = JWTManager()
cors = CORS(resources={r'/*': {'origins': '*'}})


def create_app(object_name):
    app = Flask(__name__)

    app.config.from_object(object_name)

    with app.app_context():
    #### Initiate Neo4j Driver
        init_driver(
            app.config.get('NEO4J_URI'),
            app.config.get('NEO4J_USERNAME'),
            app.config.get('NEO4J_PASSWORD'),
        )
    #### Initiate Extenstions
        api.init_app(app)
        jwt.init_app(app)
        if app.config['ENABLE_CORS']:
            cors.init_app(app)

    

    from .routes.auth import auth_ns
    from .routes.user import users_ns

    from .routes.color import color_ns
    from .routes.event import events_ns
    from .routes.article import articals_ns
    from .routes.exhibition import exhbitions_ns
    from .routes.galleryCategory import gallerycatgorys_ns
    from .routes.image import images_ns
    from .routes.manual import manuals_ns
    from .routes.material import materials_ns
    from .routes.merchant import merchants_ns

    from .routes.rollingshutter import rollingshutter_ns
    from .routes.securit5shutters import securit_ns
    from .routes.foldingsecurit import folding_ns
    from .routes.plissewire import plissewier_ns
    from .routes.window import window_ns
    from .routes.kitchen import kitchen_ns
    from .routes.mobile import ns




    #### Register Namespaces
    api.add_namespace(auth_ns)
    api.add_namespace(users_ns)
    api.add_namespace(color_ns)
    api.add_namespace(events_ns)
    api.add_namespace(articals_ns)
    api.add_namespace(exhbitions_ns)
    api.add_namespace(gallerycatgorys_ns)
    api.add_namespace(images_ns)
    api.add_namespace(manuals_ns)
    api.add_namespace(materials_ns)
    api.add_namespace(merchants_ns)
    api.add_namespace(rollingshutter_ns)
    api.add_namespace(securit_ns)
    api.add_namespace(folding_ns)
    api.add_namespace(plissewier_ns)
    api.add_namespace(window_ns)
    api.add_namespace(kitchen_ns)
    api.add_namespace(ns)


    
    return app
