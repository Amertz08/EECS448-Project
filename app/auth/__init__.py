from __future__ import unicode_literals, print_function, division, absolute_import

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user

from forms import LoginForm, RegistrationForm
from models import db, commit, User
from mail import send_email

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            if user.check_password(form.password.data):
                login_user(user, form.remember_me.data)
                return redirect(url_for('profile.index'))
            else:
                flash('Email/Password combination incorrect')
        else:
            flash('Email/Password combination incorrect')
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
            flash('You are now registered.')
            context = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'token': user.generate_confirmation_token()
            }
            send_email(
                recipients=[user.email],
                subject='Confirm your email address',
                template_name='confirmation',
                context=context
            )
            flash('We sent you a verification email.')
            login_user(user)
            return redirect(url_for('profile.index'))
        else:
            flash('Email is already registered')
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.validated:
        return redirect(url_for('profile.index'))
    if current_user.confirm(token):
        flash('Thank you for confirming your account.')
    else:
        flash('The confirmation link is invalid or has expired')
    return redirect(url_for('profile.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    context = {
        'first_name': current_user.first_name,
        'last_name': current_user.last_name,
        'token': current_user.generate_confirmation_token()
    }
    send_email(
        recipients=[current_user.email],
        subject='Confirm your email address',
        template_name='confirmation',
        context=context
    )
    flash('A new confirmation email has been sent')
    return redirect(url_for('profile.index'))
