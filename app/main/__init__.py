from __future__ import unicode_literals, print_function, division, absolute_import

import arrow

from flask import Blueprint, render_template

from forms import SearchForm
from sky import live_flights

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    query_results = None
    if form.validate_on_submit():
        kwargs = {
            'originplace': form.origin_place_id.data,
            'destinationplace': form.destination_place_id.data,
            'inbounddate': arrow.get(form.inbound_date.data).format('YYYY-MM-DD'),
            'outbounddate': arrow.get(form.outbound_date.data).format('YYYY-MM-DD'),
            'adults': form.adults.data,
            'children': form.children.data,
            'infants': form.infants.data,
        }
        query_results = live_flights.query_flights(kwargs)

    context = {
        'form': form,
        'results': query_results.results if query_results else query_results
    }
    return render_template('index.html', **context)
