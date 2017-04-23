from __future__ import unicode_literals, print_function, division, absolute_import

import datetime
import time

from sqlalchemy.exc import IntegrityError

from test.base import BaseTest
from models import db, commit, User, FavoritePlace


class TestUserModel(BaseTest):

    def test_default_values_for_attributes(self):
        user = User(
            first_name='Adam',
            last_name='Mertz',
            email='amertz@example.com',
            password='pass'
        )
        db.session.add(user)
        commit(db.session)

        self.assertEqual(user.city, '', 'city should default to an empty string')
        self.assertEqual(user.state, '', 'state should default to an empty string')
        self.assertIsNone(user.zip_code, 'zip_code has no default')
        self.assertFalse(user.validated, 'validated should default to False')

    def test_email_uniqueness(self):
        user_one = User(
            first_name='Adam',
            last_name='Mertz',
            email='amertz@example.com',
            password='pass'
        )
        user_two = User(
            first_name='Steve',
            last_name='McQueen',
            email='amertz@example.com',
            password='another pass'
        )

        db.session.add(user_one)
        commit(db.session)
        db.session.add(user_two)
        self.assertRaises(IntegrityError, commit, db.session)

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


class TestFavoritePlaceModel(BaseTest):

    def test_default_attribute_values(self):
        user = User(
            first_name='Adam',
            last_name='Mertz',
            email='amertz@example.com',
            password='pass'
        )
        db.session.add(user)
        commit(db.session)

        place = FavoritePlace(user_id=user.id)

        db.session.add(place)
        commit(db.session)

        self.assertIsNotNone(place.added, 'added should have a value')
        self.assertIsInstance(place.added, datetime.datetime, 'added should be datetime object')
        self.assertEqual(place.city, '', 'city should default to empty string')
        self.assertEqual(place.country, '', 'country should default to empty string')
        self.assertEqual(place.place_id, '', 'place_id should default to empty string')

    def test_equality(self):
        user = User(
            first_name='Adam',
            last_name='Mertz',
            email='amertz@example.com',
            password='pass'
        )
        db.session.add(user)
        commit(db.session)

        place_one = FavoritePlace(user_id=user.id)
        db.session.add(place_one)
        commit(db.session)

        place_two = FavoritePlace.query.first()
        self.assertEqual(place_one, place_two, '__eq__ does not work properly')

        place_three = FavoritePlace(user_id=user.id, place_id='blah')
        db.session.add(place_three)
        commit(db.session)
        self.assertNotEqual(place_one, place_three, '__ne__ does not work properly')
