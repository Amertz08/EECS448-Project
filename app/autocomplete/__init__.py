from __future__ import unicode_literals, print_function, division, absolute_import

from flask import Blueprint, request, jsonify

from sky import live_flights

auto = Blueprint('auto', __name__)


def _search_data_gen(results):
    for result in results:
        yield {
            'label': '{city}, {country}'.format(city=result['PlaceName'], country=result['CountryName']),
            'value': '{city}, {country}'.format(city=result['PlaceName'], country=result['CountryName']),
            'data': {
                'place_id': result['PlaceId']
            }
        }


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
            'query': destination
        }
        response = live_flights.location_autosuggest(**kwargs)
        places = response.json()['Places']
        results = [place for place in _search_data_gen(places)]
    return jsonify(results)
