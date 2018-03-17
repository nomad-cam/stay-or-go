import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import cartopy.feature as cfeature

from shapely.geometry.polygon import LinearRing

import matplotlib.pyplot as plt

from stayorgo.cfa_ftp import fetch_emv_fdr_by_date

from datetime import datetime

import os

global_scale = '10m'
proj = ccrs.Mercator()

# fig = plt.figure()
base_dir = os.path.abspath(os.path.dirname(__file__))

ax = plt.axes(projection=proj)
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linestyle='dotted')
gl.xlabels_top = False
gl.ylabels_left = False
gl.xlabels_bottom = False
gl.ylabels_right = False
ax.set_extent((140.5, 150.5, -33.5, -39.5), crs=ccrs.PlateCarree())
plt.suptitle('Victoria', fontweight='bold', fontsize=15)
param = 'FDR Forecast'
# dt = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
plt.figtext(0.13, 0.9, 'Param: %s' % param)
# plt.figtext(0.9,0.9,'Date: %s' % (dt),horizontalalignment='right')

shapename = 'admin_1_states_provinces'
state_boundary = cfeature.NaturalEarthFeature(
    category='cultural',
    name=shapename,
    scale=global_scale,
    facecolor='none'
)

ax.add_feature(state_boundary)

green = '#7ac043'
blue = '#00adef'
yellow = '#fff001'
orange = '#f89828'
red = '#ee2d24'
code_red = '#ee2d24'

# rectangle = Path([[-1.1, -0.1], [1, -0.1], [1, 0.1], [-1.1, 0.1]])
lons = [-34, -33.6, -33.6, -34]
lats = [148, 148, 148.5, 148.5]
# rect = LinearRing([[34,148],[33.6,148],[33.6,148.5],[33,148.5]])
rect = LinearRing(list(zip(lons, lats)))
ax.add_geometries([rect], ccrs.Mercator(), facecolor=red, edgecolor='black', hatch='/', zorder=100)

today = datetime.now().strftime('%d/%m/%Y')
fdr = fetch_emv_fdr_by_date('FDRTFBXML', today)
print(fdr)

tfb_shape_name = os.path.join(base_dir, 'static', 'gis', 'cfa_tfb_district.shp')
reader = shpreader.Reader(tfb_shape_name)
districts = reader.geometries()

dist = cfeature.ShapelyFeature(districts, crs=ccrs.PlateCarree())

record = reader.records()
dt_for = ''
dt_at = ''

for rec in record:
    ins_txt = rec.attributes['TFB_DIST']
    # print(rec.bounds)
    # print(ins_txt)
    dt_for = fdr['fdr'][0]['issuedFor']
    dt_at = fdr['fdr'][0]['issuedAt']

    for num in range(len(fdr['fdr'])):
        if fdr['fdr'][num]['district'].upper() == ins_txt:
            # print(fdr['fdr'][num]['district'])
            hatch = None
            edge = 'black'
            if fdr['fdr'][num]['status'] == 'LOW-MODERATE':
                face = green
            elif fdr['fdr'][num]['status'] == 'HIGH':
                face = blue
            elif fdr['fdr'][num]['status'] == 'VERY HIGH':
                face = yellow
            elif fdr['fdr'][num]['status'] == 'SEVERE':
                face = orange
            elif fdr['fdr'][num]['status'] == 'EXTREME':
                face = red
            elif fdr['fdr'][num]['status'] == 'CODE RED':
                face = red
                hatch = '/'
            else:
                face = 'grey'

    # face = 'green'
    # edge = 'black'

            ax.add_geometries(rec.geometry, crs=ccrs.PlateCarree(), facecolor=face, edgecolor=edge, hatch=hatch)

    # format west and south gippsland into 2 lines
    str_splt = rec.attributes['TFB_DIST'].split(' ')
    if len(str_splt) > 3:
        ins_txt = "%s %s\n%s %s" % (str_splt[0], str_splt[1], str_splt[2], str_splt[3])

    text_center_x = (rec.bounds[2] + rec.bounds[0])/2
    text_center_y = (rec.bounds[1] + rec.bounds[3])/2
    plt.text(text_center_x, text_center_y, ins_txt.title(),
             horizontalalignment='center', transform=ccrs.Geodetic(),
             fontsize=10,
             bbox={'facecolor': 'white', 'alpha': 0.7, 'pad': 2})


plt.figtext(0.9, 0.9, 'Date: %s' % (dt_for), horizontalalignment='right')
plt.figtext(0.9, 0.02, 'Issued At: %s' % (dt_at), horizontalalignment='right')

tfb_today = os.path.join(base_dir, 'static', 'img', 'fdr_today.png')
plt.savefig(tfb_today)
# plt.show()
