# import fiona
import cartopy.io.shapereader as shpreader
from shapely.geometry import shape, Point
import os
import json


def fetch_localities_list(locality):
    # base_dir = os.getcwd()
    base_dir = os.path.abspath(os.path.dirname(__file__))
    fname = os.path.join(base_dir,'static','gis','locality_list.json')
    
    with open(fname,'r') as infile:
        data = json.load(infile)

    # print(data)
    l = []
    if locality == 'ALL':       
        # print('ALL')
        for locality2 in data:
            l.append(locality2['locality'])
        # print(l)
    else:
        # l.append('None')
        # print(locality)
        for locality3 in data:
            # print(locality3)
            if locality in locality3['locality']:
                l.append(locality3['locality'])
        # print(l)

    return l

def town2location(locality):
    # base_dir = os.getcwd()
    base_dir = os.path.abspath(os.path.dirname(__file__))
    fname = os.path.join(base_dir,'static','gis','locality_list.json')

    with open(fname,'r') as infile:
        data = json.load(infile)

    loc = []
    for local in data:
        # print(local)
        if local['locality'] == locality:
            loc = [local['locality'], local['y_loc'], local['x_loc']]
            str = "%s,%s" % (loc[1], loc[2])
            loc.append(town2TFBdistrict(str))

    return loc


def town2TFBdistrict(locality):
    # print(locality)
    y_loc = float(locality.split(',')[0])
    x_loc = float(locality.split(',')[1])
    # print(x_loc,y_loc)
    # base_dir = os.getcwd()
    base_dir = os.path.abspath(os.path.dirname(__file__))
    district_poly = os.path.join(base_dir, 'static', 'gis', 'cfa_tfb_district.shp')

    reader = shpreader.Reader(district_poly)
    point = Point(x_loc,y_loc)

    district = ""
    for shape in reader.records():
        sh = shape.geometry
        if sh.contains(point):
            district = shape.attributes['TFB_DIST']
    # with fiona.open(district_poly) as infile:
    #     for locality in infile:
    #         sh = shape(locality['geometry'])
    #         if sh.contains(point):
    #             # print(shape.attributes['TFB_DIST'])
    #             district = locality['properties']['TFB_DIST']
    return district.title()


def generate_localities():
    # base_dir = os.getcwd()
    base_dir = os.path.abspath(os.path.dirname(__file__))
    print(base_dir)
    localities_poly = os.path.join(base_dir,'static','gis','locality_polygon.shp')

    reader = shpreader.Reader(localities_poly)
    record = reader.records()

    locality_list = []

    for locality in record:
        loc_center_x = round((locality.bounds[2] + locality.bounds[0]) / 2, 4)
        loc_center_y = round((locality.bounds[1] + locality.bounds[3]) / 2, 4)

        locality_list.append('%s,%s,%s' % (locality.attributes['locality'].title(), loc_center_x, loc_center_y))

    # with fiona.open(localities_poly) as infile:
    #     for locality in infile:
    #         # geometry = locality['geometry']
    #         bbox = shape( locality['geometry']).bounds
    #         loc_center_x = round((bbox[2] + bbox[0]) / 2, 4)
    #         loc_center_y = round((bbox[1] + bbox[3]) / 2, 4)
    #
    #         # print(locality)
    #         locality_list.append('%s,%s,%s' % (locality['properties']['LOCALITY'].title(), loc_center_x, loc_center_y))
    
    locality_list.sort()

    data = []
    # convert to json file and write to folder
    for locality in locality_list:
        d = {}
        tmp_list = locality.split(",")
        d['locality'] = tmp_list[0]
        d['x_loc'] = tmp_list[1]
        d['y_loc'] = tmp_list[2]
        data.append(d)

    fname = os.path.join(base_dir,'static','gis','locality_list.json')
    with open(fname,'w') as outfile:
        json.dump(data,outfile)

    # print(locality_list)
    return 'Done.'