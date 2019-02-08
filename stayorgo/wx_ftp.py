import urllib.request
from datetime import datetime
from dateutil import tz
import json
import os

from . import cache


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(BASE_DIR, 'wx_source.json')) as json_data_file:
    wx_data = json.load(json_data_file)


def wx_read_json(f_string):
    f = urllib.request.urlopen(f_string)

    json_string = f.read()
    json_parsed = json.loads(json_string.decode('utf-8'))
    f.close()

    return json_parsed


def wx_connect(station_name, flag, source):
    global wx_data
    # connect to the <source> forecast api
    # Time format required = 2019-02-08T21:00:00+11:00
    # Done: http://api.wunderground.com/api/a0288eb1235df557/hourly/q/-37.914,145.369.json

    list_split = station_name.split(',')
    latlon = False
    if len(list_split) == 2:
        try:
            float(list_split[0])
            latlon = True
        except ValueError:
            pass

    # need to modify slightly if the lat lon notation is being used
    # Can combine call to reduce access requirements
    # http://api.wunderground.com/api/<key>/forecast10day/hourly/q/AU/Selby.json

    # request = urllib.request.urlopen(
    #     'https://api.aerisapi.com/forecasts/ferny creek,australia?&format=json&filter=day&limit=10&
    #     fields=periods.dateTimeISO,loc,periods.maxTempC,periods.minHumidity,periods.windSpeedMaxKPH,
    #     periods.windSpeedMinKPH&client_id=xxx&client_secret=XXXXXXX')
    # response = request.read()
    # json = json.loads(response)
    # if json['success']:
    #     print
    #     json
    # else:
    #     print("An error occurred: %s" % (json['error']['description']))
    #     request.close()

    # if latlon:
    final = []
    cache_hour = 30
    cache_daily = 90
    cache_time = None
    if source == "aeris":
        if not latlon:
            station_name = "%s, australia" % station_name
        tail = ""
        if flag == "hourly":
            cache_time = cache_hour
            tail = "&filter=1hr&limit=36"
        if flag == 'forecast10day':
            cache_time = cache_daily
            tail = "&filter=day&limit=10"
        url = "{}{}?format=json&client_id={}&client_secret={}&fields={}{}".format(wx_data[source]['base_url'],
                                                                                  station_name,
                                                                                  wx_data[source]['key'],
                                                                                  wx_data[source]['secret'],
                                                                                  wx_data[source]['fields'],
                                                                                  tail)
        # url = "https://api.aerisapi.com/forecasts/%s?format=json&client_id=%s&client_secret=%s&fields=%s%s" \
        #                            % (station_name, "xxx", "XXXXXXXXX",
        #                               "periods.dateTimeISO,loc,periods.maxTempC,periods.minHumidity,
        #                               periods.windSpeedMaxKPH,periods.windSpeedMinKPH", tail)
        # print(url)
        result = wx_read_json(url)

        # print(result)

        if result['success']:
            for value in result['response'][0]['periods']:
                tmp = dict()
                tmp['maxTemp'] = value['maxTempC']
                tmp['minRH'] = value['minHumidity']
                # tmp['avgWindSpd'] = (value['windSpeedMaxKPH'] + value['windSpeedMinKPH']) / 2.0
                tmp['avgWindSpd'] = value['windSpeedMaxKPH']
                tmp['datetime'] = value['dateTimeISO']
                final.append(tmp)
        else:
            final.append({"error": result['error']['description']})
    elif source == "darksky":
        # https://api.darksky.net/forecast/xxxxxxx/-37.9176,145.3782?units=ca&exclude=[currently,minutely,alerts,flags]
        #
        tail = ""
        if flag == "hourly":
            cache_time = cache_hour
        if flag == 'forecast10day':
            cache_time = cache_daily

        url = "{}{}/{}?{}{}".format(wx_data[source]['base_url'], wx_data[source]['key'], station_name,
                                 wx_data[source]['fields'], tail)
        # print(url)
        result = wx_read_json(url)

        if result:
            if flag == "hourly":
                for value in result['hourly']['data']:
                    tmp = dict()
                    tmp['maxTemp'] = value['temperature']
                    tmp['avgWindSpd'] = value['windSpeed']
                    tmp['minRH'] = int(value['humidity'] * 100)
                    tmp['datetime'] = datetime.utcfromtimestamp(value['time']).replace(tzinfo=tz.tzutc())\
                        .astimezone(tz.tzlocal()).isoformat()
                    final.append(tmp)
            if flag == "forecast10day":
                for value in result['daily']['data']:
                    tmp = dict()
                    tmp['maxTemp'] = value['temperatureMax']
                    tmp['avgWindSpd'] = value['windSpeed']
                    tmp['minRH'] = int(value['humidity'] * 100)
                    tmp['datetime'] = datetime.utcfromtimestamp(value['time']).replace(tzinfo=tz.tzutc())\
                        .astimezone(tz.tzlocal()).isoformat()
                    final.append(tmp)
        else:
            final.append({"error": result})

    elif source == "wunder":
        url = 'http://api.wunderground.com/api/a0288eb1235df557/{}/{}/q/{}.json'.format('forecast10day',
                                                                                        'hourly', station_name)

        result = wx_read_json(url)
        print(result)

    else:
        tmp = {'error': 'Unable to find file!'}
        final.append(tmp)

    wx_cache_write('%s_%s_%s' % (source, flag, station_name), final, cache_time)

    return final
    #  ********************************************************************************************************* #

    # seperate the single file into seperate cache files
    # if flag == "forecast10day":
    #     wx_cache_write('%s_%s_%s' % (source, 'forecast10day', station_name),
    #     json_parsed['forecast']['simpleforecast']['forecastday'], 90)
    #
    # elif flag == "hourly":
    #     wx_cache_write('%s_%s_%s' % (source, 'hourly', station_name), json_parsed['hourly_forecast'], 30)
    #
    # else:
    #     return {'ERROR': 'Unable to find file!'}

    # print(json_parsed['forecast']['simpleforecast'])
    # print(json_parsed['hourly_forecast'])

    # if flag == 'hourly':
    #     return json_parsed['hourly_forecast']
    # elif flag == 'forecast10day':
    #     return json_parsed['forecast']['simpleforecast']['forecastday']
    # else:
    #     return {'ERROR': 'Unable to find file!'}


def wx_check_cache(station_name, flag, source):
    # check to see if the required file has been downloaded in the last 5 minutes
    # if not connect to the ftp server and download, otherwise use cached version

    print("checking for file: %s_%s_%s in cache" % (source, flag, station_name))
    res = cache.get('%s_%s_%s' % (source, flag, station_name))
    if not res:
        print("File %s_%s_%s not in cache" % (source, flag, station_name))
        res = wx_connect(station_name, flag, source)
    # print(res)
    return res


def wx_cache_write(station_name, io, cache_time_minutes):
    # Write the variable to the cache based on the filename
    # this will probably work due to the low file count, otherwise might need some other method.
    # probably set cache time to 30 minutes as forecast data is only 1 hour intervals.
    # cache time for 10 day forecast is 3 hours

    cache.set(station_name, io, timeout=int(cache_time_minutes)*60)


def fetch_forecast(station_name, flag, source):
    # fetch the hourly or 10 day forecast... for given location
    return wx_check_cache(station_name, flag, source)
