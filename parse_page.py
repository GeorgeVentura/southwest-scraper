from lxml import etree
import re


class ParsePage(object):

    def __init__(self, page_html):
        self.tree = etree.HTML(page_html)
        self.flights = self.get_flight_rows()
        self.flight_data = []
        for flight in self.flights:
            print self.parse_flight(flight)
        print 'done'

    def parse_flight(self, row):
        return {'depart': self._depart_time(row),
                'arrival': self._arrive_time(row),
                'flight_number': self._flight_number(row),
                'price': self._get_price(row)}

    def get_flight_rows(self):
        return self.tree.xpath('//*[contains(@id, "outbound_flightRow")]')

    def _depart_time(self, row):
        time = row.find('td/div/span/span/[@class="time"]').text
        part = row.find('td/div/span/span/[@class="indicator"]').text
        return time + part

    def _arrive_time(self, row):
        time = row.find('td[2]/div/span/span[@class="time"]').text
        part = row.find('td[2]/div/span/span[@class="indicator"]').text
        return time + part

    def _get_price(self, row):
        price = row.find('td[8]/div/div/div/div[2]/div/label/span')
        if price is None:
            price = row.find('td[8]/div/span').text
        else:
            return re.sub('[^0-9]','', price.tail)
        #return re.sub(r'([^\s\w]|_)+', '', price)
        return re.sub("[^a-zA-Z]+", "", price)

    def _get_travel_time(self, row):
        hours = row.find('td[5]/div/').text
        min = row.find('td[5]/div/span/span').tail
        return {'hour': hours,
                'min': min}

    def _flight_number(self, row):
        flight_numbers = []
        flight_num = row.find('td[3]/div/span/span/span/a')
        link = flight_num.get("href")
        links = link.split('FlightNumber=')
        for index, val in enumerate(links):
            if index >= 1:
                values = val.split('&')
                flight_numbers.append(values[0])
        return flight_numbers


def open_file():
    with open('test.html', 'r') as f:
        return str(f.readlines())

if __name__ == "__main__":
    parse = ParsePage(open_file())
