import requests
from parse_page import ParsePage
import time


class RequestPage(object):

    def __init__(self):
        self.url = 'https://www.southwest.com/flight/search-flight.html?int=HOMEQBOMAIR'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}

    def request_page(self):
        session = requests.Session()
        time.sleep(.05)
        session.get('https://www.southwest.com/')

        time.sleep(.01)
        payload = {'returnAirport': '',
                   'twoWayTrip': 'false',
                   'fareType': 'DOLLARS',
                   'originAirport': 'LGA',
                   'destinationAirport': 'LAX',
                   'outboundDateString': '12/8/2016',
                   'returnDateString': '',
                   'adultPassengerCount': 1,
                   'seniorPassengerCount': 0,
                   'promoCode': '',
                   'submitButton': True}

        req = session.post(self.url,
                           data=payload,
                           headers=self.headers,
                           allow_redirects=True)

        #with open('test.html', 'w') as f:
         #   f.writelines(req.content)

        return req.content

rr = RequestPage()
parse = ParsePage(rr.request_page())


