from __future__ import unicode_literals, print_function, division, absolute_import


from skyscanner.skyscanner import Flights

from local_config import SKYSCANNER_API_KEY

flight_service = Flights(SKYSCANNER_API_KEY)
