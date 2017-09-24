import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER
# cartopy/mpl/gridliner.py
# +degree_locator = mticker.MaxNLocator(nbins=9, steps=[1, 1.5, 1.8, 2, 3, 6, 10])

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

global_scale = '10m'
#proj = ccrs.PlateCarree()
#proj = ccrs.Miller()
proj = ccrs.Mercator()

# fig = plt.figure()

ax = plt.axes(projection=proj)
ax.coastlines(resolution=global_scale)
gl = ax.gridlines(crs=ccrs.PlateCarree(),draw_labels=True,linestyle='dotted')
gl.xlabels_top = False
gl.ylabels_left = False
gl.xlocator = mticker.FixedLocator(list(range(140,152)))
gl.ylocator = mticker.FixedLocator(list(range(-33,-41,-1)))
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
ax.set_extent((140.5,150.5,-33.5,-39.5),crs=ccrs.PlateCarree())
#ax.set_xticks(list(range(140,151)),crs=ccrs.PlateCarree())
# plt.title('Param: FDR',fontweight='light')
plt.suptitle('Victoria',fontweight='bold',fontsize=15)
param = 'FDR'
datetime = '2017/01/23 17:57:35'
plt.figtext(0.13,0.9,'Param: %s' % (param))
plt.figtext(0.9,0.9,'Date: %s' % (datetime),horizontalalignment='right')

shapename = 'admin_1_states_provinces'
state_boundary = cfeature.NaturalEarthFeature(
    category='cultural',
    name=shapename,
    scale=global_scale,
    facecolor='none'
)

ax.add_feature(state_boundary)

# ocean = cfeature.NaturalEarthFeature(
#     category='physical',
#     name='ocean',
#     scale=global_scale
# )
# ax.add_feature(ocean)
#ax.add_feature(cfeature.OCEAN) #poor resolution

tfb_shape_name = './stayorgo/static/gis/cfa_tfb_district'
reader = shpreader.Reader(tfb_shape_name)
districts = reader.geometries()

dist = cfeature.ShapelyFeature(districts,crs=ccrs.PlateCarree())

record = reader.records()

for rec in record:
    ins_txt = rec.attributes['TFB_DIST']
    #print(rec.bounds)
    face = 'green'
    edge = 'black'

    ax.add_geometries(rec.geometry,crs=ccrs.PlateCarree(),facecolor=face,edgecolor=edge)

    #format west and south gippsland into 2 lines
    str_splt = rec.attributes['TFB_DIST'].split(' ')
    if len(str_splt) > 3:
        ins_txt = "%s %s\n%s %s" % (str_splt[0],str_splt[1],str_splt[2],str_splt[3])

    text_center_x = (rec.bounds[2] + rec.bounds[0])/2
    text_center_y = (rec.bounds[1] + rec.bounds[3])/2
    plt.text(text_center_x,text_center_y,ins_txt.title(),
             horizontalalignment='center',transform=ccrs.Geodetic(),
             fontsize = 10,
             bbox={'facecolor':'white','alpha':0.5,'pad':5})
#ax.add_feature(dist)


#plt.savefig('result.png')
plt.show()