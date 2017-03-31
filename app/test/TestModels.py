from __future__ import unicode_literals, print_function, division, absolute_import

from test.base import BaseTest
from models import User

class TestUserModel(BaseTest):

    def test_hash_password(self):
        user = User(
            first_name='Adam',
            last_name='Mertz',
            email='adam@example.com',
            password='pass'
        )

        self.assertTrue(user.check_password(password='pass'), 'Password was incorrect')
