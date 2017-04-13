from __future__ import unicode_literals, print_function, division, absolute_import

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
