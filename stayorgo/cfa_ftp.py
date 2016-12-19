import feedparser
from datetime import datetime
from dateutil import tz
from . import cache

def cfa_connect(filename):

    feed = feedparser.parse("http://www.cfa.vic.gov.au/restrictions/%s.xml" % filename)
    #print(feed)

    utc = datetime.strptime(feed['updated'], "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=tz.tzutc())
    aest = utc.astimezone(tz.tzlocal()).strftime("%a, %d %b %Y %H:%M:%S")
    #print(aest)

    clean_feed =  feed['entries']
    clean_feed.append( {"updated": feed['updated'],
                        "updated-local": aest} )
    #print (clean_feed)
    cfa_cache_write(filename,clean_feed)

    return clean_feed

def cfa_check_cache(filename):
    # check to see if the required file has been downloaded in the last 5 minutes
    # if not connect to the ftp server and download, otherwise use cached version

    print("checking for file: %s in cache" % filename)
    res = cache.get(filename)
    if not res:
        print("File %s not in cache" % filename)
        res = cfa_connect(filename)

    return res

def cfa_cache_write(filename,IO):
    # Write the variable to the cache based on the filename
    # this will probably work due to the low file count, otherwise might need some other method.

    cache.set(filename, IO)


def fetch_cfa_tfb_rss(filename):
    #
    return cfa_check_cache(filename)
