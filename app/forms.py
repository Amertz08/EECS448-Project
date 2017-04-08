from __future__ import unicode_literals, print_function, division, absolute_import

from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Required, Length, Email


class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Login')


class RegistrationForm(Form):
    first_name = StringField('First Name', validators=[Required()])
    last_name = StringField('Last Name', validators=[Required()])
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required])
    submit = SubmitField('Register')
