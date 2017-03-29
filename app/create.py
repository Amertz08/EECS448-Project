from __future__ import unicode_literals, print_function, absolute_import

from flask import Flask

from app.config import config
from app.models import db


def create_app(config_level):
    app = Flask(__name__)
    app.config.from_object(config[config_level])

    db.init_app(app)

    # Blueprints
    from app.main import main
    app.register_blueprint(main)

    return app
