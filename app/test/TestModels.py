from __future__ import unicode_literals, print_function, division, absolute_import

import time

from test.base import BaseTest
from models import db, commit, User


class TestUserModel(BaseTest):

    def test_hash_password(self):
        user = User(
            first_name='Adam',
            last_name='Mertz',
            email='adam@example.com',
            password='pass'
        )

        self.assertTrue(user.check_password(password='pass'), 'check_password should be True')
        self.assertFalse(user.check_password(password='not pass'), 'check_password should be False')

    def test_update_password(self):
        one = 'pass'
        two = 'new pass'

        user = User(
            first_name='Adam',
            last_name='Mertz',
            email='amertz@example.com',
            password=one
        )

        user.update_password(two)
        self.assertTrue(user.check_password(two), 'Update password should be true')
        self.assertFalse(user.check_password(one), 'Update password should be false')

    def test_token_confirmation(self):
        user = User(
            first_name='Adam',
            last_name='Mertz',
            email='amertz@example.com',
            password='pass'
        )

        db.session.add(user)
        commit(db.session)

        token = user.generate_confirmation_token()
        self.assertTrue(user.confirm(token), 'Confirmation token failed')

    def test_token_expiration(self):
        user = User(
            first_name='Adam',
            last_name='Mertz',
            email='amertz@example.com',
            password='pass'
        )

        db.session.add(user)
        commit(db.session)

        token = user.generate_confirmation_token(expiration=1)
        time.sleep(3)
        self.assertFalse(user.confirm(token), 'Token should of expired')
