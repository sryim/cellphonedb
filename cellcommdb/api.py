import os

from flask import Flask
from flask_restful import Api

from cellcommdb.api_endpoints import routes
from cellcommdb.app import import_config
from cellcommdb.extensions import db

current_dir = os.path.dirname(os.path.realpath(__file__))
output_dir = '%s/../out/' % current_dir
data_dir = '%s/data/' % current_dir
temp_dir = '%s/temp/' % current_dir
query_input_dir = '%s/data/queries' % current_dir


def create_app(environment='local', support='yaml', load_defaults=True):
    app = Flask(__name__)

    flask_config = import_config.flask_config(environment, support, load_defaults)
    app.config.from_mapping(flask_config)
    app.url_map.strict_slashes = False

    with app.app_context():
        db.init_app(app)

    api = Api(app, prefix=flask_config['API_PREFIX'])

    routes.add(api)

    return app
