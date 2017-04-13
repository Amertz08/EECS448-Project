from __future__ import unicode_literals, print_function, division, absolute_import

from flask import Blueprint, request, jsonify

from skyAPI import flight_service

auto = Blueprint('auto', __name__)


@auto.route('/search')
def search():
    args = request.args
    destination = args.get('destination')
    results = []
    if destination != '':
        kwargs = {
            'currency': 'USD',
            'market': 'US',
            'locale': 'en-US',
            'id': destination
        }
        response = flight_service.location_autosuggest(**kwargs)
        results = response.json()

    return jsonify(results)
