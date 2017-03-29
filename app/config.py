from __future__ import unicode_literals, print_function, absolute_import

import os


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY') or '))aos47#z9%t&fwx=jqcf+yo9&&7s&(+4@(gt9gl70i-_4mh*p'

    MYSQL_USER = 'EECS448'
    MYSQL_PASS = 'z81mL2eJgK5y'
    MYSQL_DB = 'EECS448_dev'
    MYSQL_HOST = 'localhost'

    # Database info
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{usr}:{passwd}@{host}/{db}'.format(
        usr=MYSQL_USER, passwd=MYSQL_PASS, host=MYSQL_HOST, db=MYSQL_DB
    )

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
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


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
