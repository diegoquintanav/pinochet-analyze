__version__ = "0.1.1"

import os
from flask import Flask, jsonify
from flask_graphql import GraphQLView

from project.api.schemas import schema
from project.api.models import graph

# resolve what configuration will be used
config_dispatcher = {
    "development": "config.DevelopmentConfig",
    "testing": "config.TestingConfig",
    "production": "config.ProductionConfig",
    "default": "config.DevelopmentConfig"
    # add more dispatchers here
}


def create_app():
    # instantiate the app
    app = Flask(__name__)

    # set config
    configure_app(app, os.environ.get("FLASK_ENV", "default"))
    print("app.debug inside create_app")
    print(app.debug)
    app.add_url_rule('/graphql',
                     view_func=GraphQLView.as_view('graphql',
                                                   schema=schema,
                                                   graphiql=True)
                     )

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({'message': 'The requested URL was not found on the server.'}), 404

    # set up extensions here

    # register blueprints here

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "graph": graph}

    return app


def configure_app(app, config_name):
    # configures the app importing an object from /config/default.py
    # http://flask.pocoo.org/docs/2.0/config/
    # http://exploreflask.com/en/latest/configuration.html#configuring-based-on-environment-variables
    app.config.from_object(config_dispatcher[config_name])
    print("app.debug inside configure_app")
    print(app.debug)