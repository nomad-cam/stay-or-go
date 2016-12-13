from ftplib import FTP
from StringIO import StringIO
import xml.etree.ElementTree as ET

ftp = FTP('ftp.bom.gov.au')
ftp.login()
r = StringIO()
ftp.cwd('anon/gen/fwo')
# ftp.retrlines('RETR IDV18560.xml', r.write) # ffdi gfdi forecast
ftp.retrlines('RETR IDV60920.xml', r.write) # current observations

ftp.quit()

tree = ET.fromstring( r.getvalue() )
# print (tree)
# root = tree.getroot()

for child in tree:
    # print( child.tag, child.attrib )

    if child.tag == 'forecast':
        print('found the forecast')

        for forecast in child:
            print( forecast.tag, forecast.attrib )

    if child.tag == 'observations':
        print( 'found obeservations' )

        for obs in child:
            # print( obs.tag, obs.attrib)
            
            print( obs.get('stn-name') ) # display the station name
            for element in obs[0][0].iter('element'):
                # print element.tag, element.attrib
                
                if element.get('type') == 'air_temperature':
                    print('Air Temperature: %s' % element.text )

                if element.get('type') == 'rel-humidity':
                    print('Humidity: %s' % element.text )

                if element.get('type') == 'wind_spd_kmh':
                    print('Average Wind Speed: %s' % element.text )
                   
