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

def api_get_request(timesec):
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

    # Date
    print("Date : ", datetime.datetime.utcfromtimestamp(timesec).strftime('%d-%m-%Y %H:%M:%S'))

    # Excluding datas
    exclusion = '?exclude=currently,hourly,flags'

    # URL de requête
    url = base_url + key + latitude + longitude + str(timesec) + exclusion
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


def init_dict(request,data_dict):
    # Transforme un dictionnaire json, en un dictionnaire de listes
    for key in request['daily']['data'][0]:
        value = request['daily']['data'][0][key]
        data_dict[key] = [value]
    return data_dict

def add_data(request,data_dict):
    # Transforme un dictionnaire json, en un dictionnaire de listes
    for key in request['daily']['data'][0]:
        value = request['daily']['data'][0][key]
        data_dict[key].append(value)
    return data_dict

def main():
    data_dict = {}

    # Date de début de la période et durée de la période
    date_init = time_stamp(2017, 6, 30)
    duree = 5
    periode = time_table(date_init, duree)

    # Requêtes successives
    count = 0
    for date_time_stamp in periode:
        request = api_get_request(date_time_stamp)
        # print_json(request)
        if (count == 0):
            init_dict(request,data_dict)
        else:
            add_data(request, data_dict)
        count +=1

    print(data_dict)

    # Creating a pandas data frame
    df = pandas.DataFrame(dict([(k,pandas.Series(v)) for k,v in data_dict.items()]))
    print(df)
    file_name = 'darksky_data_' + str(date_init) + '_' + str(duree) + '.csv'
    df.to_csv(file_name)

# Exécution principale
if __name__ == '__main__':
    main()