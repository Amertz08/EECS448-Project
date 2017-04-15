from __future__ import unicode_literals, print_function, division, absolute_import

import arrow
from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate

from config import config
from models import db, User

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app(config_level):
    app = Flask(__name__)
    app.config.from_object(config[config_level])
    Bootstrap(app)

    db.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app, db)

    @app.add_template_filter
    def format_datetime(date):
        return arrow.get(date).format('YYYY-MM-DD hh:mm:ss a')

    @app.add_template_filter
    def format_duration(minutes):
        hours = int(minutes / 60)
        minutes = int(minutes % 60)
        return '{0} hrs and {1} mins'.format(hours, minutes)

    @app.add_template_filter
    def format_usd(val):
        return '${0}'.format(val)

    @app.add_template_filter
    def logo(url):
        return '<img class="airline-logo" src="{}">'.format(url)

    # Blueprints
    from main import main
    app.register_blueprint(main)
    from auth import auth
    app.register_blueprint(auth, url_prefix='/auth')
    from profile import profile
    app.register_blueprint(profile, url_prefix='/profile')
    from autocomplete import auto
    app.register_blueprint(auto, url_prefix='/autocomplete')

    return app
