from __future__ import unicode_literals, print_function, absolute_import

from flask import Blueprint

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return 'hello'
