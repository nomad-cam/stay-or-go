import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

import numpy as np

from stayorgo.bom_ftp import wx_obs
from stayorgo.mcarthur_mk5 import fire_danger_rating
import json
import os

base_dir = os.path.abspath(os.path.dirname(__file__))
proj = ccrs.Mercator()
# proj = ccrs.PlateCarree()
scale = '10m'

ax = plt.axes(projection=proj)
ax.set_extent([140.5, 150.5, -33.5, -39.5])
# ax.add_feature(cfeature.OCEAN)
# add some ocean...
# ax.imshow(np.tile(np.array([[[211, 228, 224]]],
#                 dtype=np.uint8), [2, 2, 1]),
#             origin='upper',
#             transform=proj,
#             extent=[140.5, 150.5, -33.5, -39.5])

states_boundary = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_1_states_provinces_lines',
        scale=scale,
        facecolor='none')
ax.add_feature(states_boundary)

gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linestyle='dotted')
gl.xlabels_top = False
gl.ylabels_left = False
gl.xlocator = mticker.FixedLocator(list(range(140, 152)))
gl.ylocator = mticker.FixedLocator(list(range(-33, -41, -1)))
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER

plt.suptitle('Victoria', fontweight='bold', fontsize=15)
param = 'FDI Current'
plt.figtext(0.13, 0.9, 'Param: %s' % param)



stations_json = os.path.join(base_dir, 'stayorgo', 'static', 'gis', 'bom_stations_vic.json')

stations = []
with open(stations_json) as json_data:
    d = json.load(json_data)
    stations.append(d)
# print(stations[0]['stations'])
results = []
for station in stations[0]['stations']:
    weather = wx_obs('IDV60920', station['bom-id'])
    # print(weather)
    if weather['wind_spd_kmh'] != 'NaN' and weather['air_temperature'] != 'NaN' and weather['rel-humidity'] != 'NaN':
        fdi, fdr = fire_danger_rating(float(weather['air_temperature']),
                                      float(weather['rel-humidity']),
                                      float(weather['wind_spd_kmh']))
        # print(station['name'], station['lat'], station['lon'], station['bom-id'], fdi, fdr)
        results.append({
            'dt': weather['time-local'],
            'name': station['name'],
            'lat': station['lat'],
            'lon': station['lon'],
            'fdi': fdi,
            'fdr': fdr
        })

print(results)
plt.show()
