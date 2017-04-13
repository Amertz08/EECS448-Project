from __future__ import unicode_literals, print_function, division, absolute_import

from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, \
    BooleanField, IntegerField, HiddenField
from wtforms.fields.html5 import DateField
from wtforms.validators import Required, Length, Email, EqualTo


class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Login')


class RegistrationForm(Form):
    first_name = StringField('First Name', validators=[Required()])
    last_name = StringField('Last Name', validators=[Required()])
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required(), EqualTo('confirm', 'Passwords must match')])
    confirm = PasswordField('Repeat Password', validators=[Required()])
    submit = SubmitField('Register')


class EditProfileForm(Form):
    first_name = StringField('First Name', validators=[Required()])
    last_name = StringField('Last Name', validators=[Required()])
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[EqualTo('confirm', 'Passwords must match')])
    confirm = PasswordField('Repeat Password')
    city = StringField('City')
    state = StringField('State', validators=[Length(1, 2)])
    zip_code = IntegerField('Zip code')
    submit = SubmitField('Update')


class SearchForm(Form):
    origin = StringField('Origin', validators=[Required()])
    destination = StringField('Destination', validators=[Required()])
    dest_place_id = HiddenField('dest_place_id')
    origin_place_id = HiddenField('origin_place_id')
    outbound_date = DateField('Fly out date')
    inbound_date = DateField('Return date')
    submit = SubmitField('Search')
