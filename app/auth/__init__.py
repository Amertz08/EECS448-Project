from __future__ import unicode_literals, print_function, division, absolute_import

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user

from forms import LoginForm
from models import User

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('main.index'))
    return render_template('auth/login.html', form=form)


@auth.route('/register')
def register():
    pass