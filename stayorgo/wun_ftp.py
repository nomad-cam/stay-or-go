import urllib.request
#import urllib2 #python2.7
import json

from . import cache

def wun_connect(station_name):
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
    if latlon:
        f = urllib.request.urlopen('http://api.wunderground.com/api/a0288eb1235df557/hourly/q/%s.json' % station_name)
    else:
        f = urllib.request.urlopen('http://api.wunderground.com/api/a0288eb1235df557/hourly/q/AU/%s.json' % station_name)

    # print(f,station_name,latlon)

    json_string = f.read()
    #print(json_string)

    json_parsed = json.loads(json_string.decode('utf-8'))

    # print(json_parsed['hourly_forecast'])

    f.close()

    wun_cache_write(station_name, json_parsed)

    return json_parsed



def wun_check_cache(station_name):
    # check to see if the required file has been downloaded in the last 5 minutes
    # if not connect to the ftp server and download, otherwise use cached version

    print("checking for file: %s in cache" % station_name)
    res = cache.get(station_name)
    if not res:
        print("File %s not in cache" % station_name)
        res = wun_connect(station_name)
    print(res)
    return res['hourly_forecast']

def wun_cache_write(station_name,IO):
    # Write the variable to the cache based on the filename
    # this will probably work due to the low file count, otherwise might need some other method.
    # probably set cache time to 30 minutes as forecast data is only 1 hour intervals.

    cache.set(station_name, IO, timeout=30*60)


def fetch_wun_forecast(station_name):
    #
    return wun_check_cache(station_name)