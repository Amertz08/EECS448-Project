from __future__ import unicode_literals, print_function, division, absolute_import

from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

from forms import EditProfileForm
from models import db, commit, User

profile = Blueprint('profile', __name__)


@profile.route('/')
@login_required
def index():
    return render_template('profile/index.html')


@profile.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditProfileForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=current_user.email).first()
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.email = form.email.data
        user.city = form.city.data
        user.state = form.state.data
        user.zip_code = form.zip_code.data
        if form.password.data is not None:
            user.update_password(form.password.data)
        commit(db.session)
        return redirect(url_for('profile.index'))

    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    form.email.data = current_user.email
    form.city.data = current_user.city
    form.state.data = current_user.state
    form.zip_code.data = current_user.zip_code

    return render_template('profile/edit.html', form=form)
