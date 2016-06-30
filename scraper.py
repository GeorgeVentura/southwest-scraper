from datetime import datetime, timedelta as td
from request_page import RequestPage
from parse_page import ParsePage


class Scraper(object):

    def __init__(self, origin_airports, destination_airports, start_date, end_date):
        self.origin_airports = origin_airports
        self.destination_airports = destination_airports
        self.start_date = start_date
        self.end_date = end_date
        self.date_range = self.get_date_range()

    def get_date_range(self):
        start_date_obj = datetime.strptime(self.start_date, '%m/%d/%Y').date()
        end_date_obj = datetime.strptime(self.end_date, '%m/%d/%Y').date()

        delta = end_date_obj - start_date_obj
        date_range = []
        for i in range(delta.days + 1):
            date_range.append(start_date_obj + td(days=i))
        return date_range

    def start(self):
        for origin_airport in self.origin_airports:
            for destination_airport in self.destination_airports:
                for depart_date in self.date_range:
                        req = RequestPage(origin_airport,
                                          destination_airport,
                                          depart_date)
                        parse = ParsePage(req.request_page())
                        print parse.get_flight_data()


originx_airports = ['PHX']
dest_airports = ['LAX']

scrap = Scraper(originx_airports, dest_airports, '08/01/2016', '08/05/2016')
scrap.start()


