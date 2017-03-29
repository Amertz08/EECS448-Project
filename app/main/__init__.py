from __future__ import unicode_literals, print_function, division, absolute_import

from flask import Blueprint, render_template

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')
