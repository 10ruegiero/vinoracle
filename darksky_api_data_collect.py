import json
import requests
import pprint


def api_get_request():
    # API Manual for Time Machine Request
    # url : https: // api.darksky.net / forecast / [key] / [latitude], [longitude], [time]
    # A Time Machine Request returns the observed (in the past) or forecasted (in the future) hour - by - hour weather and daily weather conditions
    # for a particular date.A Time Machine request is identical in structure to a Forecast Request, except:
    #   - The currently data point will refer to the time provided, rather than the current time.
    #   - The minutely data block will be omitted, unless you are requesting a time within an hour of the present.
    #   - The hourly data block will contain data points starting at midnight (local time) of the day requested, and continuing until midnight (local time) of the following day.
    #   - The daily data block will contain a single data point referring to the requested date.
    #   - The alerts data block will be omitted.




    # Secret API Key
    key = '82ed529296a9e4d16d85f95242f3f3b2'

    url =

    print(url)
    # Get data from API Method
    data = requests.get(url).text
    data = json.loads(data)

    # Used to print JSON format data
    pp = pprint.PrettyPrinter()
    pp.pprint(type(data))
    pp.pprint(data)

    # Query for Top Artist in the list [the first one]


    pp.pprint(top_artist)

    return data  # return the top artist in Spain




url = 'http://ws.audioscrobbler.com/2.0/?method=geo.gettopartists&country=spain&api_key=4beab33cc6d65b05800d51f5e83bde1b&format=json'
api_get_request(url)