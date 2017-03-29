from __future__ import unicode_literals, print_function, absolute_import

from create import create_app
from models import db

from flask_testing import TestCase


class BaseTest(TestCase):

    def create_app(self):
        return create_app('testing')

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
