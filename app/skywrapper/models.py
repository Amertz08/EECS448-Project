from __future__ import unicode_literals, print_function, division, absolute_import

import datetime

import arrow

from skywrapper.enums import Direction
from skywrapper.helpers import format_datetime


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
    currency = None

    def __init__(self, query, response):
        """

        :param query: Query object
        :param response: response object
        """
        self.query = query
        self.status = response.status_code
        self.results = self._parse_response(response)

    def __repr__(self):
        return '<QueryResults status: {}>'.format(self.status)

    def __iter__(self):
        for result in self.results:
            yield result

    def _parse_response(self, response):
        """
        Returns list of Result objects from API response
        :param response: response object 
        :return: [] or list of Result objects
        """
        if self.status == 200:
            return [result for result in self._parse_response_generator(response)]
        else:
            return []

    def _parse_response_generator(self, response):
        """
        Yields Response objects after translating API data into python objects
        :param response: response object
        :return: generates Result object
        """
        results = response.json()

        self.currency = Currency(**results['Currencies'].pop())
        itineraries = results['Itineraries']
        legs = results['Legs']
        segments = results['Segments']
        relevant_data = {
            'places': results['Places'],
            'carriers': results['Carriers']
        }
        outbound_leg = None
        outbound_times = {}
        inbound_leg = None
        inbound_times = {}
        for l in legs:
            for i in itineraries:
                if i['OutboundLegId'] == l['Id']:
                    segment_ids = l['SegmentIds']
                    filtered_segments = [
                        segment for segment in self._segment_generator(segments) if segment['id'] in segment_ids
                    ]
                    outbound_leg = Leg(
                        _id=l['Id'],
                        directionality=Direction.outbound,
                        segments=[
                            segment for segment in self._parse_segments_generator(filtered_segments, relevant_data)
                        ]
                    )
                    outbound_times['departure'] = l['Departure']
                    outbound_times['arrival'] = l['Arrival']
                    if inbound_leg is not None:
                        break
                elif i['InboundLegId'] == l['Id']:
                    segment_ids = l['SegmentIds']
                    filtered_segments = [
                        segment for segment in self._segment_generator(segments) if segment['id'] in segment_ids
                    ]
                    inbound_leg = Leg(
                        _id=l['Id'],
                        directionality=Direction.inbound,
                        segments=[
                            segment for segment in self._parse_segments_generator(filtered_segments, relevant_data)
                        ]
                    )
                    inbound_times['departure'] = l['Departure']
                    inbound_times['arrival'] = l['Arrival']
                    if outbound_leg is not None:
                        break
            yield Result(
                outbound_times=outbound_times,
                inbound_times=inbound_times,
                outbound_leg=outbound_leg,
                inbound_leg=inbound_leg
            )

    @staticmethod
    def _segment_generator(segments):
        """
        Yields segment data translated from API response
        :param segments: list of dictionaries returned from 'Segments' key on API response
        :return: generates dictionary from data stored in dictionaries in 'Segments' key on API response
        """
        for segment in segments:
            yield {
                'id': segment['Id'],
                'origin_id': segment['OriginStation'],
                'destination_id': segment['DestinationStation'],
                'flight_number': segment['FlightNumber'],
                'directionality': segment['Directionality'],
                'departure_time': format_datetime(segment['DepartureDateTime']),
                'arrival_time': format_datetime(segment['ArrivalDateTime']),
                'carrier_id': segment['Carrier'],
                'duration': segment['Duration']
            }

    def _parse_segments_generator(self, segments, relevant_data):
        """
        Yields Segment object with only applicable data
        :param segments: List of dictionaries that have been preparse by _segment_generator
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
                        _type=place['Type']
                    )
                    if destination is not None:
                        break
                elif place['Id'] == segment['destination_id']:
                    destination = Place(
                        _id=place['Id'],
                        name=place['Name'],
                        code=place['Code'],
                        _type=place['Type']
                    )
                    if origin is not None:
                        break
            flight = Flight(
                _id=segment['flight_number'],
                carrier=self._build_carrier(segment['carrier_id'], carriers)
            )
            segment = Segment(
                _id=segment['id'],
                origin=origin,
                destination=destination,
                departure_time=segment['departure_time'],
                arrival_time=segment['arrival_time'],
                duration=segment['duration'],
                flight=flight
            )
            yield segment

    @staticmethod
    def _build_carrier(carrier_id, carriers):
        """
        Returns Carrier object with relevant data
        :param carrier_id: id we care about
        :param carriers: List of carrier data
        :return: Carrier Object
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


class Query(BaseModel):
    originplace = None
    destinationplace = None
    outbounddate = None
    inbounddate = None
    adults = None
    children = None
    infants = None
    country = None
    currency = None
    locale = None

    def __init__(self, **kwargs):
        if kwargs:
            self.init(**kwargs)

    def __repr__(self):
        return '<Query origin: {0} destination: {1}>'.format(self.originplace, self.destinationplace)

    def init(self, **kwargs):
        """
        Initializes all attributes
        :param kwargs: parameters used in API call 
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
    def __init__(self, outbound_times, outbound_leg, inbound_times, inbound_leg=None):
        """
        
        :param outbound_times: dictionary with departure/arrival times for outbound leg
        :param outbound_leg: Leg object for outbound leg
        :param inbound_times: dictionary with departure/arrival times for inbound leg
        :param inbound_leg: Leg obejct for inbound leg
        """
        self.outbound_times = outbound_times
        self.outbound_leg = outbound_leg
        self.inbound_times = inbound_times
        self.inbound_leg = inbound_leg
        self.outbound_duration = self._calc_duration(outbound_times)
        self.inbound_duration = self._calc_duration(inbound_times) if inbound_times else 0
        self.price = 0.00

    def __repr__(self):
        return '<Result>'

    @staticmethod
    def _calc_duration(times):
        """
        Calculates trip duration in minutes
        :param times: dictionary with departure/arrival times for leg
        :return: None or minutes for total trip
        """
        if times is not None:
            start = arrow.get(times['departure'])
            end = arrow.get(times['arrival'])
            return int((end - start).seconds / 60)
        return None


class Leg(EqualityMixin, BaseModel):
    def __init__(self, _id, directionality, segments):
        """
        
        :param _id: 
        :param directionality: 
        :param segments: 
        """
        self.id = _id
        self.directionality = directionality
        self.segments = segments

    def __repr__(self):
        return '<Leg id: {0} directionality: {1}>'.format(self.id, self.directionality)


class Segment(EqualityMixin, BaseModel):
    def __init__(self, _id, origin, destination, departure_time,
                 arrival_time, duration, flight):
        """
        
        :param _id: 
        :param origin: 
        :param destination: 
        :param departure_time: 
        :param arrival_time: 
        :param duration: 
        :param flight: 
        """
        self.id = _id
        self.origin = origin
        self.destination = destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.duration = duration
        self.flight = flight

    def __repr__(self):
        return '<Segment id: {0} flight_number: {1}>'.format(self.id, self.flight.id)


class Place(EqualityMixin, BaseModel):
    def __init__(self, _id, name, code, _type):
        """

        :param _id: 
        :param name: 
        :param code: 
        :param type: 
        """
        self.id = _id
        self.name = name
        self.code = code
        self.type = _type

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
    def __init__(self, _id, carrier):
        """

        :param _id: 
        :param carrier: 
        """
        self.id = _id
        self.carrier = carrier

    def __repr__(self):
        return '<Flight id: {0} carrier: {1}>'.format(self.id, self.carrier)


class Currency(BaseModel):
    code = None
    symbol = None
    space_between_amount_and_symbol = None
    symbol_on_left = True
    decimal_separator = None
    thousands_separator = None
    rounding_coefficient = 0
    decimal_digits = 0

    def __init__(self, **kwargs):
        if kwargs:
            self.init(**kwargs)

    def __repr__(self):
        return '<Currency {}>'.format(self.code)

    def __eq__(self, other):
        return self.code == other.code

    def __ne__(self, other):
        return self.code != other.code

    def init(self, **kwargs):
        """
        Initializes attributes for object
        :param kwargs: 
        :return: 
        """
        self.code = kwargs.get('Code')
        self.symbol = kwargs.get('Symbol')
        self.space_between_amount_and_symbol = kwargs.get('SpaceBetweenAmountAndSymbol')
        self.symbol_on_left = kwargs.get('SymbolOnLeft')
        self.decimal_separator = kwargs.get('DecimalSeparator')
        self.thousands_separator = kwargs.get('ThousandsSeparator')
        self.rounding_coefficient = kwargs.get('RoundingCoefficent')
        self.decimal_digits = kwargs.get('DecimalDigitis')


class PriceOption(BaseModel):
    def __init__(self, age, price, url, agents=None):
        """
        
        :param age: 
        :param price: 
        :param url: 
        :param agents: 
        """
        self.age = age
        self.price = price
        self.url = url
        if agents:  # TODO: will a price option ever have more than 1 agent?
            self.agents = agents
        else:
            self.agents = []

    def __repr__(self):
        return '<PriceOption {}>'.format(self.price)


class Agent(EqualityMixin, BaseModel):
    id = None
    name = None
    image_url = None
    status = None
    optimize_for_mobile = False
    booking_number = None
    type = None

    def __iter__(self, **kwargs):
        if kwargs:
            self.init(**kwargs)

    def __repr__(self):
        return '<Agent name: {0} type: {1}>'.format(self.name, self.type)

    def init(self, **kwargs):
        """
        Initializes attributes for object
        :param kwargs: 
        :return: 
        """
        self.id = kwargs.get('Id')
        self.name = kwargs.get('Name')
        self.image_url = kwargs.get('ImageUrl')
        self.status = kwargs.get('Status')
        self.optimize_for_mobile = kwargs.get('OptimizedForMobile')
        self.booking_number = kwargs.get('BookingNumber')
        self.type = kwargs.get('Type')

