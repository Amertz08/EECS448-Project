from __future__ import unicode_literals, print_function, division, absolute_import

from flask import Blueprint, request

auto = Blueprint('auto', __name__)


@auto.route('/search')
def search():
    args = request.args
    destination = args.get('destination')
    print(destination)
    return 'hello'