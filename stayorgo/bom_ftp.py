from ftplib import FTP
from StringIO import StringIO
from . import cache
import xml.etree.ElementTree as ET


def ftp_connect(filename):
    print("connecting to bom ftp")
    ftp = FTP('ftp.bom.gov.au')
    ftp.login()
    ftp.cwd('anon/gen/fwo')
    # ftp.retrlines('RETR IDV18560.xml', r.write) # ffdi gfdi detailed forecast
    # ftp.retrlines('RETR IDV18550.xml', r.write) # ffdi gfdi tomorrow forecast
    # ftp.retrlines('RETR IDV60920.xml', r.write) # current observations

    r = StringIO()

    f = filename + ".xml"
    print("fetching file: %s" % f)
    ftp.retrlines('RETR %s' % (f), r.write) # current observations

    print("Closing ftp connection")
    ftp.quit()

    # write a copy to the cache
    cache_write(filename,r)

    # return a copy to avoid hitting the cache already
    return r


def cache_write(filename,IO):
    # Write the variable to the cache based on the filename
    # this will probably work due to the low file count, otherwise might need some other method.

    cache.set(filename, IO)


def cache_check(filename):
    # check to see if the required file has been downloaded in the last 5 minutes
    # if not connect to the ftp server and download, otherwise use cached version

    print("checking for file: %s in cache" % filename)
    res = cache.get(filename)
    if not res:
        print("File %s not in cache" % filename)
        res = ftp_connect(filename)

    return res

def wx_obs(filename, station_id):
    # decode the xml file for the given weather station
    # First set default values as some weather stations don't report all variables
    station_name = "Unable to Verify for %s" % station_id
    time_local = "NaN"
    air_temperature = "NaN"
    rel_humidity = "NaN"
    wind_spd_kmh = "NaN"

    print("Finding the current observations for station id: %s" % station_id)
    all_obs = cache_check(filename)

    root = ET.fromstring(all_obs.getvalue())

    # find the required station by wmo-id
    for child in root.findall('.//station[@wmo-id="%s"]' % (station_id)):
        #
        station_name = child.get('description')
        time_local = child[0].get("time-local")

        for element in child[0][0].iter('element'):
            # print element.tag, element.attrib

            if element.get('type') == 'air_temperature':
                #print('Air Temperature: %s' % element.text)
                air_temperature = element.text

            if element.get('type') == 'rel-humidity':
                #print('Humidity: %s' % element.text)
                rel_humidity = element.text

            if element.get('type') == 'wind_spd_kmh':
                #print('Average Wind Speed: %s' % element.text)
                wind_spd_kmh = element.text

    return {'station_id': station_id,
            'station_name': station_name,
            'time-local': time_local,
            'air_temperature': air_temperature,
            'rel-humidity': rel_humidity,
            'wind_spd_kmh': wind_spd_kmh}


def station_list(station_id):
    all_obs = cache_check("IDV60920")

    root = ET.fromstring(all_obs.getvalue())

    bom_id = "NaN"
    wmo_id = "NaN"
    station_name = "NaN"
    lat = "NaN"
    lon = "NaN"
    forecast_district = "NaN"
    res_all = []

    if station_id == "ALL":
        for child in root.findall('.//station'):
            #
            bom_id = child.get('bom-id')
            wmo_id = child.get('wmo-id')
            station_name = child.get('description')
            lat = child.get('lat')
            lon = child.get('lon')
            forecast_district = child.get('forecast-district-id')
            fire_district = "VIC_FW%s" % forecast_district[-3:]

            res_all.append({"bom-id": bom_id,
                            "wmo-id": wmo_id,
                            "name": station_name,
                            "lat": lat,
                            "lon": lon,
                            "forecast-district": forecast_district,
                            "fire-district": fire_district    })
        return res_all

    else:
        for child in root.findall('.//station[@bom-id="%s"]' % (station_id)):
            #
            bom_id = child.get('bom-id')
            wmo_id = child.get('wmo-id')
            station_name = child.get('description')
            lat = child.get('lat')
            lon = child.get('lon')
            forecast_district = child.get('forecast-district-id')
            fire_district = "VIC_FW%s" % forecast_district[-3:]

            res = {"bom-id": bom_id,
            "wmo-id": wmo_id,
            "name": station_name,
            "lat": lat,
            "lon": lon,
            "forecast-district": forecast_district,
            "fire-district": fire_district    }

        return res

