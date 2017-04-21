from __future__ import unicode_literals, print_function, division, absolute_import

from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, \
    BooleanField, IntegerField, HiddenField, SelectField
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


class FlightSearchForm(Form):
    origin = StringField('Origin', validators=[Required()])
    destination = StringField('Destination', validators=[Required()])
    destination_place_id = HiddenField('destination_place_id')
    origin_place_id = HiddenField('origin_place_id')
    outbound_date = DateField('Fly out date')
    inbound_date = DateField('Return date')
    adults = SelectField('Adults (16+)', choices=[(n, n) for n in range(1, 9)], coerce=int)
    children = SelectField('Children (1-16)', choices=[(n, n) for n in range(9)], coerce=int)
    infants = SelectField('Infants (under 12 months)', choices=[(n, n) for n in range(9)], coerce=int)
    submit = SubmitField('Search')


class PlaceSearchForm(Form):
    destination = StringField('Destination', validators=[Required()])
    destination_place_id = HiddenField('destination_place_id')
    city = HiddenField('city')
    country = HiddenField('country')
    submit = SubmitField('Add')

