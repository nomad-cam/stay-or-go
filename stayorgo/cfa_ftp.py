import xml.etree.ElementTree as ET
import json
import urllib.request
import re
from datetime import datetime
from dateutil import tz
from . import cache

def cfa_connect(filename):

    # feed = feedparser.parse("http://www.cfa.vic.gov.au/restrictions/%s.xml" % filename)
    # # print(feed)

    # utc = datetime.strptime(feed['updated'], "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=tz.tzutc())
    # aest = utc.astimezone(tz.tzlocal()).strftime("%a, %d %b %Y %H:%M:%S")
    # #print(aest)

    # clean_feed =  feed['entries']
    # clean_feed.append( {"updated": feed['updated'],
    #                     "updated-local": aest} )
    # #print (clean_feed)
    # cache_write(filename,clean_feed)

    return filename


def emv_connect(filename):

    # fdrtfb_json = 'https://data.emergency.vic.gov.au/Show?pageId=getFDRTFBJSON'
    # incident_json = 'https://data.emergency.vic.gov.au/Show?pageId=getIncidentJSON'
    # fdrtfb_xml = 'https://data.emergency.vic.gov.au/Show?pageId=getFDRTFBXML'
    feed = 'https://data.emergency.vic.gov.au/Show?pageId=get%s' % filename

    f = urllib.request.urlopen(feed)
    # data = json.loads(f.read().decode('utf-8'))
    data = f.read().decode('utf-8')
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


def fetch_emv_fdr(filename,district):
    #
    #emv_connect('FDRTFBXML')
    fdrtfb = check_cache(filename,'EMV')
    #print(fdrtfb)
    
    emv_fdr = {}
    emv_fdr['fdr'] = []

    root = ET.fromstring(fdrtfb)
    # print(root.find('tfbfdr-forecast').get('file-generated-at'))
    # for chile in root.findall('.//tfbfdr-forecast'):
    #     print(chile.get('file-generated-at'))

    for child in root.findall('.//fdr'):
        #print(child.tag,child.get('issue-for'))
        tmp = {}
        tmp['date'] = child.get('issue-for')
        tmp['issuedAt'] = child.get('issue-at')
        # emv_fdr['fdr']['forecast-date'] = child.get('issue-for')

        if district == "ALL":
            # not in use atm
            for child2 in child.findall('.//district'):
                #print(child2.tag,child2.get('name'),child2.text)
                #emv_fdr[child.get('issue-for')][child2.get('name')] = child2.text
                tmp['district'] = child2.get('name')
                tmp['status'] = child2.text


        else:
            for child2 in child.findall('.//district[@name="%s"]' % (district)):
                #print(child2.tag,child2.get('name'),child2.text)
                #emv_fdr[child.get('issue-for')][child2.get('name')] = child2.text
                tmp['district'] = child2.get('name')
                tmp['status'] = child2.text
                
        emv_fdr['fdr'].append(tmp)

    # print(emv_fdr)
    return emv_fdr


def fetch_emv_tfb(filename,district):
    #
    #emv_connect('FDRTFBXML')
    fdrtfb = check_cache(filename,'EMV')
    #print(fdrtfb)
    
    emv_tfb = {}
    emv_tfb['tfb'] = []

    root = ET.fromstring(fdrtfb)
    # print(root.get('file-generated-at'))
    # for chile in root.findall('.//tfbfdr-forecast'):
    #     print(chile.get('file-generated-at'))

    for child in root.findall('.//tfb'):
        #print(child.tag,child.get('issue-for'))
        tmp = {}
        tmp['date'] = child.get('issue-for')
        tmp['fileDate'] = root.get('file-generated-at')
        # tmp['statusShort'] = child.get('status')
        # emv_fdr['fdr']['forecast-date'] = child.get('issue-for')

        tmp['statusLong'] = child.find('declaration').text

        # print(re.search(r'[2]\d{3}',tmp['statusLong']))
        m = re.search(r'[2]\d{3}',tmp['statusLong'])
        tmp['dateLong'] = tmp['statusLong'][:m.end()]

        if district == "ALL":
            # not in use atm
            for child2 in child.findall('.//district'):
                #print(child2.tag,child2.get('name'),child2.text)
                #emv_fdr[child.get('issue-for')][child2.get('name')] = child2.text
                tmp['district'] = child2.get('name')
                tmp['status'] = child2.text
                tmp['statusShort'] = 'N'
                if 'YES' in tmp['status']:
                    tmp['statusShort'] = 'Y'


        else:
            for child2 in child.findall('.//district[@name="%s"]' % (district)):
                #print(child2.tag,child2.get('name'),child2.text)
                #emv_fdr[child.get('issue-for')][child2.get('name')] = child2.text
                tmp['district'] = child2.get('name')
                tmp['status'] = child2.text
                tmp['statusShort'] = 'N'
                if 'YES' in tmp['status']:
                    tmp['statusShort'] = 'Y'
                
        emv_tfb['tfb'].append(tmp)

    # print(emv_fdr)
    return emv_tfb
