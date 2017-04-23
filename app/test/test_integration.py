from __future__ import unicode_literals, print_function, division, absolute_import

import os


def test_app_config():
    assert os.getenv('APP_CONFIG') is not None, 'APP_CONFIG not set'


def test_secret_key():
    assert os.getenv('SECRET_KEY') is not None, 'SECRET_KEY not set'


def test_skyscanner_api_key():
    assert os.getenv('SKYSCANNER_API_KEY') is not None, 'SKYSCANNER_API_KEY not set'


def test_mysql_user():
    assert os.getenv('MYSQL_USER') is not None, 'MYSQL_USER is not set'


def test_mysql_pass():
    assert os.getenv('MYSQL_PASS') is not None, 'MYSQL_PASS is not set'
