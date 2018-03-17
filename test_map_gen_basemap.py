# import cartopy.crs as ccrs
# import cartopy.io.shapereader as shpreader
# import cartopy.feature as cfeature
# from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER

from mpl_toolkits.basemap import Basemap
import numpy as np
import os
from shapely.geometry import shape
import fiona

import matplotlib.pyplot as plt
from matplotlib.offsetbox import TextArea,DrawingArea,AnnotationBbox
from matplotlib.patches import Circle
import matplotlib.ticker as mticker

#global_scale = '10m'
# proj = ccrs.Mercator()

map = Basemap(projection='merc',llcrnrlat=-39.5,urcrnrlat=-33.5,\
              llcrnrlon=140.5,urcrnrlon=150.5,lat_ts=20,resolution='h')

map.drawcoastlines()
map.fillcontinents(color='#E6F5B1',lake_color='#D3E4E0')

map.drawparallels(np.arange(-39.,-33.,1.0),dashes=[1,5],color='0.5',labels=[1,0,0,0])
map.drawmeridians(np.arange(140.,151.,1.0),dashes=[1,5],color='0.5',labels=[0,0,0,1])

map.drawmapboundary(fill_color='#D3E4E0')
ax = plt.axes()
# ax.coastlines(resolution=global_scale)
# gl = ax.gridlines(crs=ccrs.PlateCarree(),draw_labels=True)
# gl.xlabels_top = False
# gl.ylabels_left = False
# gl.xlocator = mticker.FixedLocator(list(range(140,152)))
# gl.ylocator = mticker.FixedLocator(list(range(-33,-41,-1)))
# gl.xformatter = LONGITUDE_FORMATTER
# gl.yformatter = LATITUDE_FORMATTER
# ax.set_extent((140.5,150.5,-33.5,-39.5),crs=ccrs.PlateCarree())
#ax.set_xticks(list(range(140,151)),crs=ccrs.PlateCarree())
# plt.title('Param: FDR',fontweight='light')
plt.suptitle('Victoria',fontweight='bold',fontsize=15)
param = 'FDR'
datetime = '2017/01/23 17:57:35'
plt.figtext(0.13,0.9,'Param: %s' % (param))
plt.figtext(0.9,0.9,'Date: %s' % (datetime),horizontalalignment='right')

# shapename = 'admin_1_states_provinces'
# state_boundary = cfeature.NaturalEarthFeature(
#     category='cultural',
#     name=shapename,
#     scale=global_scale,
#     facecolor='none'
# )
#
# ax.add_feature(state_boundary)

# ocean = cfeature.NaturalEarthFeature(
#     category='physical',
#     name='ocean',
#     scale=global_scale
# )
# ax.add_feature(ocean)
#ax.add_feature(cfeature.OCEAN) #poor resolution

base_dir = os.path.abspath(os.path.dirname(__file__))
district_poly = os.path.join(base_dir, 'stayorgo', 'static', 'gis', 'cfa_tfb_district')
map.readshapefile(district_poly,'districts')

tmp = map.readshapefile(district_poly,'districts')
# print(tmp)

with fiona.open(district_poly+'.shp') as infile:
    for district in infile:
        # print(district)
        ins_txt = district['properties']['TFB_DIST'].title()
        str_splt = ins_txt.split(' ')
        if len(str_splt) > 3:
            ins_txt = "%s %s\n%s %s" % (str_splt[0],str_splt[1],str_splt[2],str_splt[3])

        bbox = shape(district['geometry']).bounds
        loc_center_x = round((bbox[2] + bbox[0]) / 2, 4)
        loc_center_y = round((bbox[1] + bbox[3]) / 2, 4)
        # convert from lat/lon to plot x/y
        coords_x,coords_y = map(loc_center_x,loc_center_y)
        plt.annotate(ins_txt, xy=(coords_x,coords_y),
                          horizontalalignment='center',
                          fontsize = 10,
                          bbox={'facecolor':'white','alpha':0.8,'pad':5})

da = DrawingArea(2,20,0,0)
p = Circle((10,10),10)
da.add_artist(p)

ab = AnnotationBbox(da, [0.9,0.9],
                        xybox=(1.02, 0.78),
                        xycoords='data',
                        boxcoords=("axes fraction", "data"),
                        box_alignment=(0., 0.5))

# plot, get current figure, get current axes
plt.gcf().gca().add_artist(da)
# for info,shp in zip(map.districts_info, map.districts):
#     # print(shape)
#     # ax.
#     # format west and south gippsland into 2 lines
#     str_splt = info['TFB_DIST'].title().split(' ')
#     print(str_splt)
#     if len(str_splt) > 3:
#         ins_txt = "%s %s\n%s %s" % (str_splt[0],str_splt[1],str_splt[2],str_splt[3])

    # x = shape(shp)
    # print(shp)
# print(district_poly)
# tfb_shape_name = 'cfa_tfb_district'
# reader = shpreader.Reader(tfb_shape_name)
# districts = reader.geometries()
#
# dist = cfeature.ShapelyFeature(districts,crs=ccrs.PlateCarree())
#
# record = reader.records()
#
# for rec in record:
#     ins_txt = rec.attributes['TFB_DIST']
#     #print(rec.bounds)
#     face = 'green'
#     edge = 'black'
#
#     ax.add_geometries(rec.geometry,crs=ccrs.PlateCarree(),facecolor=face,edgecolor=edge)
#
#     #format west and south gippsland into 2 lines
#     str_splt = rec.attributes['TFB_DIST'].split(' ')
#     if len(str_splt) > 3:
#         ins_txt = "%s %s\n%s %s" % (str_splt[0],str_splt[1],str_splt[2],str_splt[3])
#
#     text_center_x = (rec.bounds[2] + rec.bounds[0])/2
#     text_center_y = (rec.bounds[1] + rec.bounds[3])/2
#     plt.text(text_center_x,text_center_y,ins_txt.title(),
#              horizontalalignment='center',transform=ccrs.Geodetic(),
#              fontsize = 10,
#              bbox={'facecolor':'white','alpha':0.5,'pad':5})
#ax.add_feature(dist)


#plt.savefig('result.png')
plt.show()