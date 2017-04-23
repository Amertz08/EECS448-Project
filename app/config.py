from __future__ import unicode_literals, print_function, division, absolute_import

import os

from local_config import SMTP_USER, SMTP_PASSWORD


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY') or '))aos47#z9%t&fwx=jqcf+yo9&&7s&(+4@(gt9gl70i-_4mh*p'

    CONFIG_LVL = 'default'
    ADMIN_EMAIL = 'admin@example.com'

    MYSQL_USER = 'EECS448'
    MYSQL_PASS = 'z81mL2eJgK5y'
    MYSQL_DB = 'EECS448_dev'
    MYSQL_HOST = 'localhost'

    # Database info
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{usr}:{passwd}@{host}/{db}'.format(
        usr=MYSQL_USER, passwd=MYSQL_PASS, host=MYSQL_HOST, db=MYSQL_DB
    )

    CELERY_BROKER_URL = 'redis://localhost:6379/0'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = True
    MAIL_DEFAULT_SENDER = 'no-reply@example.com'
    MAIL_USER = SMTP_USER
    MAIL_PASSWORD = SMTP_PASSWORD

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    CONFIG_LVL = 'DEV'


class TestingConfig(Config):
    CONFIG_LVL = 'TESTING'
    TESTING = True
    MYSQL_USER = 'EECS448'
    MYSQL_PASS = 'z81mL2eJgK5y'
    MYSQL_DB = 'EECS448_test'
    MYSQL_HOST = 'localhost'

    # Database info
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{usr}:{passwd}@{host}/{db}'.format(
        usr=MYSQL_USER, passwd=MYSQL_PASS, host=MYSQL_HOST, db=MYSQL_DB
    )


class ProductionConfig(Config):
    PRODUCTION = True
    CONFIG_LVL = 'PRODUCTION'


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
