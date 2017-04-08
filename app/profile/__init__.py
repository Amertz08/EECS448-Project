from __future__ import unicode_literals, print_function, division, absolute_import

from flask import Blueprint, render_template
from flask_login import login_required

profile = Blueprint('profile', __name__)


@profile.route('/')
@login_required
def index():
    return render_template('profile/index.html')
