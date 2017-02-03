import urllib.request
#import urllib2 #python2.7
import json

from . import cache

def wun_connect(station_name,flag):
    # connect to the wunderground forecast api
    #
    # Done: http://api.wunderground.com/api/a0288eb1235df557/hourly/q/-37.914,145.369.json

    list_split = station_name.split(',')
    latlon = False
    if len(list_split) == 2:
        try:
            float(list_split[0])
            latlon = True
        except ValueError:
            pass
            latlon = False

    # need to modify slightly if the lat lon notation is being used
    # Can combine call to reduce access requirements
    # http://api.wunderground.com/api/<key>/forecast10day/hourly/q/AU/Selby.json
    if latlon:
        f = urllib.request.urlopen('http://api.wunderground.com/api/a0288eb1235df557/%s/%s/q/%s.json' \
                                   % ('forecast10day','hourly', station_name))
    else:
        f = urllib.request.urlopen('http://api.wunderground.com/api/a0288eb1235df557/%s/%s/q/%s.json' \
                                   % ('forecast10day','hourly', station_name))

    # print(f,station_name,latlon)

    json_string = f.read()
    #print(json_string)

    json_parsed = json.loads(json_string.decode('utf-8'))

    # print(json_parsed['hourly_forecast'])

    f.close()

    # seperate the single file into seperate cache files
    wun_cache_write('%s_%s'%('forecast10day',station_name), json_parsed['forecast']['simpleforecast'], 90)
    wun_cache_write('%s_%s' % ('hourly', station_name), json_parsed['hourly_forecast'], 30)

    # print(json_parsed['forecast']['simpleforecast'])
    # print(json_parsed['hourly_forecast'])

    if flag == 'hourly':
        return json_parsed['hourly_forecast']
    elif flag == 'forecast10day':
        return json_parsed['forecast']['simpleforecast']['forecastday']
    else:
        return {'ERROR': 'Unable to find file!'}



def wun_check_cache(station_name,flag):
    # check to see if the required file has been downloaded in the last 5 minutes
    # if not connect to the ftp server and download, otherwise use cached version

    print("checking for file: %s_%s in cache" % (flag,station_name))
    res = cache.get('%s_%s'%(flag,station_name))
    if not res:
        print("File %s_%s not in cache" % (flag,station_name))
        res = wun_connect(station_name,flag)
    # print(res)
    return res

def wun_cache_write(station_name,IO,cache_time_minutes):
    # Write the variable to the cache based on the filename
    # this will probably work due to the low file count, otherwise might need some other method.
    # probably set cache time to 30 minutes as forecast data is only 1 hour intervals.
    # cache time for 10 day forecast is 3 hours

    cache.set(station_name, IO, timeout=int(cache_time_minutes)*60)


def fetch_wun_forecast(station_name,flag):
    # fetch the hourly or 10 day forecast... for given location
    return wun_check_cache(station_name,flag)

# def fetch_wun_forecast10(station_name):
#     #
#     return wun_check_cache(station_name,'forecast10day')