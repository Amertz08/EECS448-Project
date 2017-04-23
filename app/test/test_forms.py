from __future__ import unicode_literals, print_function, division, absolute_import

from wtforms import ValidationError
from wtforms.validators import Email

from test.base import BaseTest
from forms import LoginForm, RegistrationForm,\
    EditProfileForm, FlightSearchForm, PlaceSearchForm
from models import db, commit, User


class TestLoginForm(BaseTest):

    def test_email_required(self):
        form = LoginForm(
            password='pass',
            remember_me=True
        )

        self.assertFalse(form.validate(), 'validation should be false: Email required')

    def test_email_length(self):
        domain = '@example.com'
        email = ''.join('a' for x in range(64 - len(domain)))
        email += domain
        form = LoginForm(
            email=email,
            password='pass'
        )
        self.assertFalse(form.validate(), 'email field should validate for length')

    def test_invalid_email(self):
        form = LoginForm(
            email='blah',
            password='blah'
        )
        self.assertFalse(form.validate(), 'email field should validate valid email input')


class TestRegistrationForm(BaseTest):

    def test_first_name_required(self):
        form = RegistrationForm(
            last_name='blah',
            email='adam@example.com',
            password='pass',
            confirm='pass'
        )
        self.assertFalse(form.validate(), 'first_name should be required')

    def test_last_name_required(self):
        form = RegistrationForm(
            first_name='blah',
            email='adam@example.com',
            password='pass',
            confirm='pass'
        )
        self.assertFalse(form.validate(), 'last_name should be required')

    def test_email_required(self):
        form = RegistrationForm(
            first_name='blah',
            last_name='blah',
            password='pass',
            confirm='pass'
        )
        self.assertFalse(form.validate(), 'email should be required')

    def test_invalid_email(self):
        form = RegistrationForm(
            first_name='blah',
            last_name='blah',
            email='blah',
            password='pass',
            confirm='pass'
        )
        self.assertFalse(form.validate(), 'email should be required')

    def test_unique_email_validation(self):
        user = User(
            first_name='Steve',
            last_name='Sanchez',
            email='a@example.com',
            password='pass'
        )

        db.session.add(user)
        commit(db.session)

        form = RegistrationForm(
            first_name='Adam',
            last_name='Mertz',
            email='a@example.com',
            password='test',
            confirm='test'
        )

        self.assertFalse(form.validate(), 'email should be validated as unique')

    def test_passwords(self):
        form = RegistrationForm(
            first_name='Adam',
            last_name='Mertz',
            email='a@example.com',
            password='pass',
            confirm='not pass'
        )

        self.assertFalse(form.validate(), 'password and conform must be the same')
