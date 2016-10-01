'''
    Author: George Ventura
    Date:   9/30/2016

    http://github.com/GeorgeVentura/southwest-scraper

'''

import requests
import json
import datetime


class SouthWestRequest(object):

    def __init__(self, depart_date, destination_airport, origin_airport):
        self.API_KEY = 'l7xx8d8bfce4ee874269bedc02832674129a'
        self.headers = {'X-API-Key': 'l7xx8d8bfce4ee874269bedc02832674129b',
                        'User-Agent': 'Southwest/3.6.16 (iPhone; iOS 9.3.2; Scale/2.00)'}

        self.URL = 'https://mobile.southwest.com/api/extensions/v1/mobile/flights/products?currency-type=Dollars&departure-date={0}&destination-airport={1}&number-adult-passengers=1&number-senior-passengers=0&origination-airport={2}&promo-code='.format(depart_date, destination_airport, origin_airport)
        self.flights = self.parse_response(self.make_request())

    def make_request(self):
        session = requests.Session()
        session.headers = self.headers
        try:
            req = session.get(self.URL)
            if req.status_code == 200:
                json_response = json.loads(req.content)
                return json_response
            else:
                print "Status Code http: " + req.status_code
        except Exception as e:
            print e

    def parse_response(self, reps):
        if 'message' in reps:
            return 0
        flights = []
        if len(reps['trips']) == 0:
            return 0
        dat = reps['trips'][0]['airProducts']
        for flight in dat:
            flights.append(self.extract_data(flight))
        return flights

    def extract_data(self, flight):
        record = dict()
        record['flights'] = self.get_flights(flight['segments'])
        record['duration'] = flight['durationMinutes']
        record['price'] = flight['fareProducts'][2]['currencyPrice']['totalFareCents']
        record['seats'] = flight['fareProducts'][2]['seatsAvailable']
        datetime_retrieved = datetime.datetime.now()
        record['datetime_retrieved'] = datetime_retrieved
        record['num_connections'] = len(flight['segments'])
        if len(flight['segments']) > 1:
            connect_flight = self.get_connecting_flight(flight)
            record['connect'] = connect_flight[0]
            record['connect_depart_date'] = connect_flight[1]
        else:
            record['connect'] = None
            record['connect_depart_date'] = None
        return record

    def get_connecting_flight(self, flight):
        if len(flight['segments']) > 1:
            flight_number_connect = flight['segments'][1]['operatingCarrierInfo']['flightNumber']
            depart_datetime = flight['segments'][1]['departureDateTime']
            return flight_number_connect, depart_datetime

    def get_flights(self, flights):
        flight_data = []
        for flight in flights:
            flight_data.append({'depart_datetime': flight['departureDateTime'],
                                'arrival_datetime': flight['arrivalDateTime'],
                                'dest_airport': flight['destinationAirportCode'],
                                'origin_airport': flight['originationAirportCode'],
                                'num_stops': flight['numberOfStops'],
                                'flight_number': flight['operatingCarrierInfo']['flightNumber'],
                                'carrier_code': flight['operatingCarrierInfo']['carrierCode']})
        return flight_data

    def get_results(self):
        return self.flights

    def get_results_json(self):
        return json.dumps(self.flights, default=SouthWestRequest.default)

    @staticmethod
    def default(obj):
        """Default JSON serializer."""
        import calendar, datetime

        if isinstance(obj, datetime.datetime):
            if obj.utcoffset() is not None:
                obj = obj - obj.utcoffset()
            millis = int(
                calendar.timegm(obj.timetuple()) * 1000 +
                obj.microsecond / 1000
            )
            return millis
        raise TypeError('Not sure how to serialize %s' % (obj,))
