# southwest-scraper
Web scraper for southwest airlines

This script gets data using Southwest's Mobile Phone API. Http responses are returned as JSON data through the mobile API, thus this allows for faster scrapping and less bandwidth usage.


##Usage

+ This only returns data as a 1 way flight.
+ You must use the 3 letter airport code.

``` python
flight_r = SouthWestRequest('2017-10-25', # Date of flight in Y-m-d format
                            'LAX',        # Destination airport abbreviation 
                            'EWR')        # Origin airport abbreviation
                            
flights = flight_r.get_results()          # returns a list of dicts
```

##Results
+ Returns a list where the length is the number of different flights for the requested origin and dest airports.
+ Prices are in USD and for Wanna Get Away fares.

An example;
of Newark liberty Airport (EWR) to Los Angeles International Airport (LAX) with a connecting flight to Chiago in between.
+ EWR -> MDW -> LAX

``` json
[
  {
    "connect_depart_date": "2016-11-29T10:15",
    "price": 25100,
    "num_connections": 2,
    "datetime_retrieved": 1475280875322,
    "flights": [
      {
        "dest_airport": "MDW",
        "origin_airport": "EWR",
        "num_stops": 0,
        "arrival_datetime": "2016-11-29T07:30",
        "carrier_code": "WN",
        "flight_number": "374",
        "depart_datetime": "2016-11-29T06:05"
      },
      {
        "dest_airport": "LAX",
        "origin_airport": "MDW",
        "num_stops": 0,
        "arrival_datetime": "2016-11-29T12:50",
        "carrier_code": "WN",
        "flight_number": "2457",
        "depart_datetime": "2016-11-29T10:15"
      }
    ],
    "connect": "2457",
    "seats": "8",
    "duration": 585
  },
```

