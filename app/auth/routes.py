from __future__ import unicode_literals, print_function, division, absolute_import

from flask import Blueprint, render_template, redirect,\
    url_for, flash, current_app, abort
from flask_login import login_user, login_required, logout_user, current_user
from itsdangerous import URLSafeSerializer

from helpers import send_error_email
from forms import LoginForm, RegistrationForm, ForgotPasswordForm, PasswordResetForm
from models import db, commit, User
from mail import send_email

auth = Blueprint('auth', __name__)


def get_url_serializer(app):
    return URLSafeSerializer(app.config['SECRET_KEY'])


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
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        try:
            commit(db.session)
        except:
            send_error_email()
            flash('There has been an error')
            return render_template('auth/register.html', form=form)

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
        **context
    )
    flash('A new confirmation email has been sent')
    return redirect(url_for('profile.index'))


@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            s = get_url_serializer(current_app)
            token = s.dumps(user.email, salt='recovery-key')
            context = {
                'first_name': user.first_name,
                'token': token
            }
            send_email(
                recipients=[user.email],
                subject='Password Reset',
                template_name='password_reset',
                **context
            )
        flash('Email with link to reset password has been sent')
        return redirect(url_for('auth.login'))
    return render_template('auth/forgot_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def reset(token):
    email = None
    try:
        s = get_url_serializer(current_app)
        email = s.loads(token, salt='recovery-key')
    except:
        abort(404)

    form = PasswordResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first_or_404()
        user.update_password(form.password.data)
        try:
            commit(db.session)
        except:
            send_error_email()
            flash('There has been an error')
            return redirect(url_for('auth.forgot_password'))
        flash('Password updated')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset.html', form=form)
