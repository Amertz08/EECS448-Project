from __future__ import unicode_literals, print_function, division, absolute_import

import arrow

from flask import Blueprint, render_template

from forms import SearchForm
from skyAPI import flight_service

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    results = None
    if form.validate_on_submit():
        kwargs = {
            'country': 'US',
            'currency': 'USD',
            'locale': 'en-US',
            'originplace': form.origin_place_id.data,
            'destinationplace': form.destination_place_id.data,
            'inbounddate': arrow.get(form.inbound_date.data).format('YYYY-MM-DD'),
            'outbounddate': arrow.get(form.outbound_date.data).format('YYYY-MM-DD'),
            'adults': form.adults.data,
            'children': form.children.data,
            'infants': form.infants.data
        }
        results = flight_service.get_result(**kwargs).json()

    context = {
        'form': form,
        'results': results
    }
    return render_template('index.html', **context)
