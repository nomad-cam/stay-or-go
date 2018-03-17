import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER
# cartopy/mpl/gridliner.py
# +degree_locator = mticker.MaxNLocator(nbins=9, steps=[1, 1.5, 1.8, 2, 3, 6, 10])

from shapely.geometry.polygon import LinearRing

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from matplotlib.image import imread

from stayorgo.cfa_ftp import fetch_emv_fdr_by_date

import numpy as np

from datetime import datetime
import os
import re

global_scale = '10m'
#proj = ccrs.PlateCarree()
#proj = ccrs.Miller()
proj = ccrs.Mercator()

# fig = plt.figure()
base_dir = os.path.abspath(os.path.dirname(__file__))

ax = plt.axes(projection=proj)
# ax.coastlines(resolution=global_scale)
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
param = 'FDR Forecast'
# dt = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
plt.figtext(0.13,0.9,'Param: %s' % (param))
# plt.figtext(0.9,0.9,'Date: %s' % (dt),horizontalalignment='right')

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
rect = LinearRing(list(zip(lons,lats)))
ax.add_geometries([rect], ccrs.Mercator(), facecolor=red, edgecolor='black', hatch='/', zorder=100)

fdr = fetch_emv_fdr_by_date('FDRTFBXML','26/10/2017')
# print(fdr)

tfb_shape_name = os.path.join(base_dir,'stayorgo','static','gis','cfa_tfb_district.shp')
reader = shpreader.Reader(tfb_shape_name)
districts = reader.geometries()

dist = cfeature.ShapelyFeature(districts,crs=ccrs.PlateCarree())

record = reader.records()
dt = ''

for rec in record:
    ins_txt = rec.attributes['TFB_DIST']
    #print(rec.bounds)
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

    #format west and south gippsland into 2 lines
    str_splt = rec.attributes['TFB_DIST'].split(' ')
    if len(str_splt) > 3:
        ins_txt = "%s %s\n%s %s" % (str_splt[0], str_splt[1], str_splt[2], str_splt[3])

    text_center_x = (rec.bounds[2] + rec.bounds[0])/2
    text_center_y = (rec.bounds[1] + rec.bounds[3])/2
    plt.text(text_center_x, text_center_y, ins_txt.title(),
             horizontalalignment='center', transform=ccrs.Geodetic(),
             fontsize = 10,
             bbox={'facecolor':'white', 'alpha':0.7, 'pad':2})


plt.figtext(0.9,0.9,'Date: %s' % (dt_for),horizontalalignment='right')
plt.figtext(0.9,0.02,'Issued At: %s' % (dt_at),horizontalalignment='right')

# ax.add_feature(dist)

# # Parse the svg string...
# # from https://matplotlib.org/devdocs/gallery/showcase/firefox.html#sphx-glr-gallery-showcase-firefox-py
# def parse_svg(path):
#     commands = {'M': (Path.MOVETO,),
#                 'L': (Path.LINETO,),
#                 'Q': (Path.CURVE3,)*2,
#                 'C': (Path.CURVE4,)*3,
#                 'Z': (Path.CLOSEPOLY,)}
#     path_re = re.compile(r'([MLHVCSQTAZ])([^MLHVCSQTAZ]+)', re.IGNORECASE)
#     float_re = re.compile(r'(?:[\s,]*)([+-]?\d+(?:\.\d+)?)')
#     vertices = []
#     codes = []
#     last = (0, 0)
#     for cmd, values in path_re.findall(path):
#         points = [float(v) for v in float_re.findall(values)]
#         points = np.array(points).reshape((len(points)//2, 2))
#         if cmd.islower():
#             points += last
#         cmd = cmd.capitalize()
#         last = points[-1]
#         codes.extend(commands[cmd])
#         vertices.extend(points.tolist())
#     return codes, vertices
#
#
# # TFB icon generation
# ban_icon = 'M256 8C119.034 8 8 119.033 8 256s111.034 248 248 248 248-111.034 248-248S392.967 8 256 8zm130.108 117.892c65.448 65.448 70 165.481 20.677 235.637L150.47 105.216c70.204-49.356 170.226-44.735 235.638 20.676zM125.892 386.108c-65.448-65.448-70-165.481-20.677-235.637L361.53 406.784c-70.203 49.356-170.226 44.736-235.638-20.676z'
# ban_icon_2 = 'M 39.309524,79.663689 C 83.154763,120.98909 127,162.31448 170.84524,203.63988 M 39.309524,79.663689 c 5.394839,-4.676557 10.048222,-10.391655 15.909182,-14.415325 7.660129,-3.834876 14.909105,-8.719694 23.503673,-10.168335 7.254683,-1.910091 14.396875,-4.571964 22.018911,-4.027041 7.59743,-0.04764 15.33283,-1.439192 22.64618,1.280377 7.46145,1.90099 15.25963,2.90823 21.78092,7.304598 6.65535,3.993061 14.62618,6.199182 19.61672,12.453697 5.4678,5.055316 10.42312,10.539326 14.30558,16.920775 4.49897,5.75303 7.98855,12.077185 10.6432,18.873765 2.41641,4.88088 4.61694,9.82089 4.5749,15.3752 1.10265,7.82803 1.85963,15.66442 0.80895,23.54446 -0.61086,6.41418 0.0805,13.11831 -3.17336,18.94401 -3.78709,9.43136 -7.10547,19.30771 -12.9062,27.69851 -5.46237,7.45135 -11.6813,14.44203 -18.8562,20.24132 -6.02566,4.20577 -12.25906,8.01213 -19.29547,10.27465 -7.14082,2.9259 -14.91542,4.20374 -22.4411,5.67181 -15.26265,0.20939 -31.05985,1.68199 -45.772256,-3.09771 -6.544383,-3.74534 -13.807126,-6.47177 -19.899917,-10.85765 -7.268441,-7.01136 -15.421252,-13.22215 -20.957432,-21.80161 -3.627132,-5.38752 -9.102195,-9.85946 -9.933251,-16.63234 -2.578205,-9.70316 -6.067651,-19.23738 -6.259871,-29.3829 -0.517818,-6.64681 -2.135831,-13.35515 0.182863,-19.84334 1.708433,-6.96738 2.542976,-14.25963 4.788486,-21.02735 4.76429,-7.800782 7.852356,-16.809713 14.771746,-23.057181 1.314582,-1.42413 2.629164,-2.84826 3.943746,-4.27239 z'
# fire_icon = 'M216 24.008c0-23.796-31.162-33.11-44.149-13.038C76.548 158.255 200 238.729 200 288c0 22.056-17.944 40-40 40s-40-17.944-40-40V182.126c0-19.388-21.854-30.757-37.731-19.684C30.754 198.379 0 257.279 0 320c0 105.869 86.131 192 192 192s192-86.131 192-192c0-170.29-168-192.853-168-295.992zM192 480c-88.224 0-160-71.776-160-160 0-46.944 20.68-97.745 56-128v96c0 39.701 32.299 72 72 72s72-32.299 72-72c0-65.106-112-128-45.411-248C208 160 352 175.3 352 320c0 88.224-71.776 160-160 160z'
# # fire_icon_2 =
#
# # SVG to matplotlib
# codes, verts = parse_svg(ban_icon_2)
# verts = np.array(verts)
# ban_path = Path(verts, codes)
#
# ban = PathPatch(ban_path, facecolor='red', edgecolor='none')
# ax.add_patch(ban)

####################################################################
# theta = np.linspace(0, 2 * np.pi, 100)
# circle_verts = np.vstack([np.sin(theta), np.cos(theta)]).T
# concentric_circle = Path.make_compound_path(Path(circle_verts[::-1]), Path(circle_verts * 0.8))
#
# # rectangle = Path([[-1.1, -0.1], [1, -0.1], [1, 0.1], [-1.1, 0.1]])
# # rectangle = Path([[-0.8, 0.8], [0.5, -1.1], [0.8, -0.8], [-0.5, 1.1]])
# rectangle = Path([[-0.8, 0.8], [0.8, -0.8]],[Path.MOVETO, Path.LINETO])
#
# xs = 143.5
# ys = -37.0
# plt.plot(xs, ys, transform=ccrs.PlateCarree(),
#              marker=concentric_circle, color='red', markersize=18,
#              linestyle='')
#
#
# plt.plot(xs, ys, transform=ccrs.PlateCarree(),
#              marker=rectangle, color='red', markersize=18,
#              linestyle='', linewidth=5)

################################################################################
# attempted image loading
# tfb_icon = os.path.join(base_dir,'stayorgo','static','img','tfb_icon_large.png')
# img = imread(tfb_icon)
#
# # ax.imshow(img, origin='upper', transform=ccrs.PlateCarree(), extent=[143.5,144.0,-37.0,-36.7], zorder=1)
# ax.imshow(img, origin='upper', transform=ccrs.PlateCarree(), extent=[143.5,144.0,-37.0,-36.7], zorder=1)

plt.savefig('today.png')
# plt.show()