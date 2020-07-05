import os
from flask import Flask, jsonify
from flask_graphql import GraphQLView

from .api.schemas import schema


# initialize extensions here


def create_app():
    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    app.add_url_rule('/graphql', view_func=GraphQLView.as_view(
        'graphql', schema=schema, graphiql=True)
    )

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({'message': 'The requested URL was not found on the server.'}), 404

    # set up extensions here

    # register blueprints here

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app}

    return app


