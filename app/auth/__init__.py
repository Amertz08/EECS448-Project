from __future__ import unicode_literals, print_function, division, absolute_import

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user

from forms import LoginForm, RegistrationForm
from models import db, commit, User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('main.index'))
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=form.password.data
            )
            db.session.add(user)
            commit(db.session)
            flash('You are now registered')
            return redirect(url_for('main.index'))
        else:
            flash('Email is already registered')
            return render_template('auth/register.html', form=form)
    return render_template('auth/register.html', form=form)
