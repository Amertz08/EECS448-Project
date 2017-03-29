from __future__ import unicode_literals, print_function, absolute_import

from flask import Flask


def create_app(configlvl):
    app = Flask(__name__)

    from app.main import main
    app.register_blueprint(main)

    return app
