from __future__ import unicode_literals, print_function, division, absolute_import

import arrow
from celery import Celery
from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_migrate import Migrate

from config import config, Config
from models import db, User

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
mail = Mail()
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app(config_level):
    print('Config level: {}'.format(config_level))
    app = Flask(__name__)
    app.config.from_object(config[config_level])
    Bootstrap(app)

    db.init_app(app)
    login_manager.init_app(app)
    migrate = Migrate(app, db)
    mail.init_app(app)
    celery.conf.update(app.config)

    @app.template_filter('datetime')
    def format_datetime(date):
        return arrow.get(date).format('YYYY-MM-DD hh:mm:ss a')

    @app.template_filter('duration')
    def format_duration(minutes):
        hours = int(minutes / 60)
        minutes = int(minutes % 60)
        return '{0} hrs and {1} mins'.format(hours, minutes)

    @app.template_filter('USD')
    def format_usd(val):
        return '${0}'.format(val)

    @app.template_filter('logo')
    def logo(url):
        return '<img class="airline-logo" src="{}">'.format(url)

    # Blueprints
    from main.routes import main
    app.register_blueprint(main)
    from auth.routes import auth
    app.register_blueprint(auth, url_prefix='/auth')
    from profile.routes import profile
    app.register_blueprint(profile, url_prefix='/profile')
    from autocomplete.routes import auto
    app.register_blueprint(auto, url_prefix='/autocomplete')

    return app
