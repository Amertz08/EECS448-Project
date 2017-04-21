from __future__ import unicode_literals, print_function, division, absolute_import


from skyscanner.skyscanner import Flights

from skywrapper.models import Query, QueryResults


class LiveFlights(Flights):
    params = None

    def query_flights(self, params):
        """
        Returns QueryResults object with results data
        :param params: 
        :return: 
        """
        self.params = params
        query = Query(**params)
        response = self.get_result(**query.serialize)
        return QueryResults(query, response)

    def update_result(self):
        """
        Returns QueryResults object with updated data
        :return: 
        """
        if self.params is None:
            raise AttributeError('params not set')
        return self.query_flights(self.params)
