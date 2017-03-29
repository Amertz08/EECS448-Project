from __future__ import unicode_literals, print_function, absolute_import

from flask import Flask

from config import config
from models import db


def create_app(config_level):
    app = Flask(__name__)
    app.config.from_object(config[config_level])

    db.init_app(app)

    # Blueprints
    from main import main
    app.register_blueprint(main)

    return app
