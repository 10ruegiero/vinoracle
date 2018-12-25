import datetime
import calendar
import requests
import json
import pprint
import pandas


def time_stamp(year,month,day):
    date = datetime.datetime(year,month,day)
    # print("Date : ", date)
    timesec = calendar.timegm(date.utctimetuple())
    # print("Timestamp équivalent :", timesec)
    return timesec

def time_table(init_stamp,duree_periode):
    daysec = 86400
    time_table = range(init_stamp, init_stamp + duree_periode*daysec, daysec)
    return time_table

def api_get_request(latitude, longitude, timesec):
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

    # Coordonnées géographiques
    print("Location : ", latitude, longitude)

    # Date
    print("Date : ", datetime.datetime.utcfromtimestamp(timesec).strftime('%d-%m-%Y %H:%M:%S'))

    # Excluding datas
    exclusion = '?exclude=currently,hourly,flags'

    # URL de requête
    url = base_url + key + latitude + "," + longitude + "," + str(timesec) + exclusion
    print(url)

    # Get data from API Method
    data = requests.get(url).text
    data = json.loads(data)

    return data


def print_json(json):
    # Used to print JSON format data
    pp = pprint.PrettyPrinter()
    pp.pprint(type(json))
    pp.pprint(json)


def init_dict():
    data_dict = {
        'latitude': [],
        'longitude': [],
        'timezone': [],
        'time': [],
        'apparentTemperature': [],
        'apparentTemperatureHigh': [],
        'apparentTemperatureHighTime': [],
        'apparentTemperatureLow': [],
        'apparentTemperatureLowTime': [],
        'apparentTemperatureMax': [],
        'apparentTemperatureMaxTime': [],
        'apparentTemperatureMin': [],
        'apparentTemperatureMinTime': [],
        'cloudCover': [],
        'dewPoint': [],
        'humidity': [],
        'icon': [],
        'moonPhase': [],
        'nearestStormBearing': [],
        'nearestStormDistance': [],
        'ozone': [],
        'precipAccumulation': [],
        'precipIntensity': [],
        'precipIntensityError': [],
        'precipIntensityMax': [],
        'precipIntensityMaxTime': [],
        'precipProbability': [],
        'precipType': [],
        'pressure': [],
        'summary': [],
        'sunriseTime': [],
        'sunsetTime': [],
        'temperature': [],
        'temperatureHigh': [],
        'temperatureHighTime': [],
        'temperatureLow': [],
        'temperatureLowTime': [],
        'temperatureMax': [],
        'temperatureMaxTime': [],
        'temperatureMin': [],
        'temperatureMinTime': [],
        'uvIndex': [],
        'uvIndexTime': [],
        'visibility': [],
        'windBearing': [],
        'windGust': [],
        'windGustTime': [],
        'windSpeed': []
    }

    return data_dict

def add_data(request,data_dict):
    # Transforme un dictionnaire json, en un dictionnaire de listes
    data_dict['latitude'].append(request['latitude'])
    data_dict['longitude'].append(request['longitude'])
    data_dict['timezone'].append(request['timezone'])

    for key in request['daily']['data'][0]:
        value = request['daily']['data'][0][key]
        data_dict[key].append(value)
    return data_dict

def main():
    # Initialisation du dictionnaire
    data_dict = init_dict()

    # Coordonnées géographiques
    # Coordonnées de la vigne à Mireval 43.50885, 3.79118
    latitude = '43.50885'
    longitude = '3.79118'

    # Période temporelle
    # Date de début de la période et durée de la période
    date_init = time_stamp(2017, 1, 1)
    duree = 365
    periode = time_table(date_init, duree)

    # Requêtes successives
    for date_time_stamp in periode:
        request = api_get_request(latitude, longitude, date_time_stamp)
        # print_json(request)
        add_data(request, data_dict)

    print(data_dict)

    # Creating a pandas data frame
    df = pandas.DataFrame(dict([(k,pandas.Series(v)) for k,v in data_dict.items()]))
    print(df)
    date_name = str(datetime.datetime.utcfromtimestamp(date_init).strftime('%d-%m-%Y'))
    file_name = 'darksky_data_' + latitude[:4] + '_' + longitude[:4] + '_' + date_name + '_' + str(duree) + '.csv'
    df.to_csv(file_name, "w")

# Exécution principale
if __name__ == '__main__':
    main()