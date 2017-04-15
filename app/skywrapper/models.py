from __future__ import unicode_literals, print_function, division, absolute_import

import datetime

import arrow

from skyscanner.skyscanner import Flights


def format_datetime(time, is_datetime=True):
    if is_datetime:
        return arrow.get(time).datetime
    else:
        return arrow.get(time).date()


class LiveFlights(Flights):
    def query_flights(self, params):
        """

        :param params: 
        :return: 
        """
        query = Query(**params)
        response = self.get_result(**query.serialize)
        return QueryResults(query, response)


class EqualityMixin(object):
    id = None

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id


class BaseModel(object):
    @property
    def serialize(self):
        return {k: v for k, v in self._serialize_gen()}

    def _serialize_gen(self):
        for k, v in self.__dict__.items():
            yield k, self._filter_serialization(v)

    @staticmethod
    def _filter_serialization(value):
        if isinstance(value, BaseModel):
            return value.serialize
        elif isinstance(value, datetime.datetime):
            return value.strftime('%Y-%m-%d %H-%M-%S')
        elif isinstance(value, datetime.date):
            return value.strftime('%Y-%m-%d')
        elif isinstance(value, list):
            return [val.serialize for val in value]
        else:
            return value


class QueryResults(BaseModel):
    def __init__(self, query, response):
        """

        :param query: 
        :param response: 
        """
        self.query = query
        self.status = response.status_code
        self.results = self._parse_response(response)

    def __repr__(self):
        return '<QueryResults status: {}>'.format(self.status)

    def _parse_response(self, response):
        """

        :param response: 
        :return: 
        """
        if self.status == 200:
            return [result for result in self._parse_response_generator(response)]
        else:
            return []

    def _parse_response_generator(self, response):
        """

        :param response: 
        :return: 
        """
        results = response.json()

        segments = results['Segments']
        for leg in results['Legs']:
            segment_ids = leg['SegmentIds']
            relevant_data = {
                'places': results['Places'],
                'carriers': results['Carriers']
            }
            yield Result(
                _id=leg['Id'],
                departure_time=leg['Departure'],
                arrival_time=leg['Arrival'],
                segments=[segment for segment in self._parse_segments_generator(segments, segment_ids)],
                relevant_data=relevant_data
            )

    @staticmethod
    def _parse_segments_generator(segments, segment_ids):
        """

        :param segments: 
        :param segment_ids: 
        :return: 
        """
        for segment_id in segment_ids:
            for segment in segments:
                if segment['Id'] == segment_id:
                    yield {
                        'id': segment_id,
                        'origin_id': segment['OriginStation'],
                        'destination_id': segment['DestinationStation'],
                        'flight_number': segment['FlightNumber'],
                        'directionality': segment['Directionality'],
                        'departure_time': format_datetime(segment['DepartureDateTime']),
                        'arrival_time': format_datetime(segment['ArrivalDateTime']),
                        'carrier_id': segment['Carrier'],
                        'duration': segment['Duration']
                    }
                    break


class Query(BaseModel):
    def __init__(self, **kwargs):
        if kwargs:
            self.set_query(**kwargs)

    def __repr__(self):
        return '<Query origin: {0} destination: {1}>'.format(self.originplace, self.destinationplace)

    def set_query(self, **kwargs):
        """

        :param kwargs: 
        :return: 
        """
        self.originplace = kwargs['originplace']
        self.destinationplace = kwargs['destinationplace']
        self.outbounddate = kwargs['outbounddate']
        self.inbounddate = kwargs['inbounddate']
        self.adults = kwargs.get('adults') if kwargs.get('adults') else 0
        self.children = kwargs.get('adults') if kwargs.get('adults') else 0
        self.infants = kwargs.get('infants') if kwargs.get('infants') else 0
        self.country = kwargs.get('country') if kwargs.get('country') else 'US'
        self.currency = kwargs.get('currency') if kwargs.get('currency') else 'USD'
        self.locale = kwargs.get('locale') if kwargs.get('locale') else 'en-US'


class Result(EqualityMixin, BaseModel):
    def __init__(self, _id, departure_time, arrival_time, segments, relevant_data):
        """

        :param _id: 
        :param departure_time: 
        :param arrival_time: 
        :param segments: 
        """
        self.id = _id
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.segments = self._parse_segments(segments, relevant_data)

    def __repr__(self):
        return '<Result id: {0}>'.format(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def _parse_segments(self, segments, relevant_data):
        """

        :param segments: 
        :param relevant_data: 
        :return: 
        """
        return [segment for segment in self._parse_segments_generator(segments, relevant_data)]

    def _parse_segments_generator(self, segments, relevant_data):
        """

        :param segments: 
        :param relevant_data: 
        :return: 
        """
        places = relevant_data['places']
        carriers = relevant_data['carriers']
        origin = None
        destination = None
        for segment in segments:
            for place in places:
                if place['Id'] == segment['origin_id']:
                    origin = Place(
                        _id=place['Id'],
                        name=place['Name'],
                        code=place['Code'],
                        type=place['Type']
                    )
                    if destination is not None:
                        break
                elif place['Id'] == segment['destination_id']:
                    destination = Place(
                        _id=place['Id'],
                        name=place['Name'],
                        code=place['Code'],
                        type=place['Type']
                    )
                    if origin is not None:
                        break
            flight = Flight(
                number=segment['flight_number'],
                carrier=self._build_carrier(segment['carrier_id'], carriers)
            )
            segment = Segment(
                _id=segment['id'],
                origin=origin,
                destination=destination,
                departure_time=segment['departure_time'],
                arrival_time=segment['arrival_time'],
                duration=segment['duration'],
                flight=flight,
                directionality=segment['directionality']
            )
            yield segment

    @staticmethod
    def _build_carrier(carrier_id, carriers):
        """

        :param carrier_id: 
        :param carriers: 
        :return: 
        """
        for carrier in carriers:
            if carrier['Id'] == carrier_id:
                return Carrier(
                    _id=carrier['Id'],
                    name=carrier['Name'],
                    code=carrier['Code'],
                    display_code=carrier['DisplayCode'],
                    image_url=carrier['ImageUrl']
                )


class Segment(EqualityMixin, BaseModel):
    def __init__(self, _id, origin, destination, departure_time,
                 arrival_time, duration, flight, directionality):
        """

        :param _id: 
        :param origin: 
        :param destination: 
        :param departure_time: 
        :param arrival_time: 
        :param duration: 
        :param flight: 
        :param directionality: 
        """
        self.id = _id
        self.origin = origin
        self.destination = destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.duration = duration
        self.flight = flight
        self.directionality = directionality

    def __repr__(self):
        return '<Segment id: {0} flight_number: {1}>'.format(self.id, self.flight.number)

    @property
    def duration_to_string(self):
        hrs = int(self.duration / 60)
        mins = int(self.duration % 60)
        return '{0} hrs and {1} mins'.format(hrs, mins)


class Place(EqualityMixin, BaseModel):
    def __init__(self, _id, name, code, type):
        """

        :param _id: 
        :param name: 
        :param code: 
        :param type: 
        """
        self.id = _id
        self.name = name
        self.code = code
        self.type = type

    def __repr__(self):
        return '<Place id: {0} name: {1}>'.format(self.id, self.name)


class Carrier(EqualityMixin, BaseModel):
    def __init__(self, _id, name, code, display_code, image_url):
        """

        :param _id: 
        :param name: 
        :param code: 
        :param display_code: 
        :param image_url: 
        """
        self.id = _id
        self.name = name
        self.code = code
        self.display_code = display_code
        self.image_url = image_url

    def __repr__(self):
        return '<Carrier id: {0} name: {1}>'.format(self.id, self.name)


class Flight(EqualityMixin, BaseModel):
    def __init__(self, number, carrier):
        """

        :param number: 
        :param carrier: 
        """
        self.number = number
        self.carrier = carrier

    def __repr__(self):
        return '<Flight id: {0} carrier: {1}>'.format(self.number, self.carrier)

