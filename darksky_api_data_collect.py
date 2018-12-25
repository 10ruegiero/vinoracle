import datetime
import calendar
import requests
import json
import pprint
import pandas


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

    # Request preparation
    print("#### Dark Sky API Request ####")

    # Dark Sky URL
    base_url = 'https://api.darksky.net/forecast/'

    # Secret API Key
    key = '82ed529296a9e4d16d85f95242f3f3b2/'

    # Coordonnées de la vigne à Mireval 43.50885, 3.79118
    latitude = '43.50885,'
    longitude = '3.79118,'
    print("Location : ", latitude, longitude)

    # Date demandée 30 juin 2017
    date_text = "30JUN2017"
    date = datetime.datetime.strptime(date_text, "%d%b%Y")
    print("Date : ",date)
    timesec = calendar.timegm(date.utctimetuple())
    print("Timestamp équivalent :", timesec)

    # URL de requête
    url = base_url + key + latitude + longitude + str(timesec)
    print(url)

    # Get data from API Method
    data = requests.get(url).text
    data = json.loads(data)

    return data



def main():
    data_json = api_get_request()
    # Used to print JSON format data
    pp = pprint.PrettyPrinter()
    pp.pprint(type(data_json))
    pp.pprint(data_json)

    # Creating a pandas data frame


# Exécution principale
if __name__ == '__main__':
    main()