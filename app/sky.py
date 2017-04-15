from __future__ import unicode_literals, print_function, division, absolute_import

from skywrapper.api import LiveFlights
from local_config import SKYSCANNER_API_KEY

live_flights = LiveFlights(SKYSCANNER_API_KEY)
