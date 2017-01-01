import feedparser
import json
import urllib.request
from datetime import datetime
from dateutil import tz
from . import cache

def cfa_connect(filename):

    feed = feedparser.parse("http://www.cfa.vic.gov.au/restrictions/%s.xml" % filename)
    print(feed)

    utc = datetime.strptime(feed['updated'], "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=tz.tzutc())
    aest = utc.astimezone(tz.tzlocal()).strftime("%a, %d %b %Y %H:%M:%S")
    #print(aest)

    clean_feed =  feed['entries']
    clean_feed.append( {"updated": feed['updated'],
                        "updated-local": aest} )
    #print (clean_feed)
    cache_write(filename,clean_feed)

    return clean_feed


def emv_connect(filename):

    # fdrtfb_json = 'https://data.emergency.vic.gov.au/Show?pageId=getFDRTFBJSON'
    # incident_json = 'https://data.emergency.vic.gov.au/Show?pageId=getIncidentJSON'
    # fdrtfb_xml = 'https://data.emergency.vic.gov.au/Show?pageId=getFDRTFBXML'
    feed = 'https://data.emergency.vic.gov.au/Show?pageId=get%s' % filename

    f = urllib.request.urlopen(feed)
    data = json.loads(f.read().decode('utf-8'))
    f.close()

    #print(data)
    cache_write(filename,data)

    return data


def check_cache(filename,flag):
    # check to see if the required file has been downloaded in the last 5 minutes
    # if not connect to the ftp server and download, otherwise use cached version

    print("checking for file: %s in cache" % filename)
    res = cache.get(filename)
    if not res:
        print("File %s not in cache" % filename)
        if flag == 'CFA':
            res = cfa_connect(filename)
        if flag == 'EMV':
            res = emv_connect(filename)

    #print(res)
    return res

def cache_write(filename,IO):
    # Write the variable to the cache based on the filename
    # this will probably work due to the low file count, otherwise might need some other method.

    cache.set(filename, IO)


def fetch_cfa_fdr_tfb(filename):
    #
    #emv_connect('FDRTFBJSON')
    return check_cache(filename,'CFA')


def fetch_emv_fdr_tfb(filename):
    #
    #emv_connect('FDRTFBJSON')
    return check_cache(filename,'EMV')
