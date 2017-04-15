from __future__ import unicode_literals, print_function, division, absolute_import


from skyscanner.skyscanner import Flights

from skywrapper.models import Query, QueryResults


class LiveFlights(Flights):
    def query_flights(self, params):
        """

        :param params: 
        :return: 
        """
        query = Query(**params)
        response = self.get_result(**query.serialize)
        return QueryResults(query, response)
