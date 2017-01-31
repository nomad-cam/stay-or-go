import cartopy.io.shapereader as shpreader
import os
import json


def fetch_localities_list(locality):
    base_dir = os.getcwd()
    fname = os.path.join(base_dir,'stayorgo','static','gis','locality_list.json')
    
    with open(fname,'r') as infile:
        data = json.load(infile)

    # print(data)
    l = []
    if locality == 'ALL':       
        print('ALL') 
        for locality2 in data:
            l.append(locality2['locality'])
        print(l)
    else:
        # l.append('None')
        print(locality)
        for locality3 in data:
            print(locality3)
            if locality in locality3['locality']:
                l.append(locality3['locality'])
        print(l)

    return l

def town2location(locality):
    base_dir = os.getcwd()
    fname = os.path.join(base_dir,'stayorgo','static','gis','locality_list.json')

    with open(fname,'r') as infile:
        data = json.load(infile)

    loc = []
    for local in data:
        print(local)
        if local['locality'] == locality:
            loc = [local['locality'], local['y_loc'], local['x_loc']]

    return loc

def generate_localities():
    base_dir = os.getcwd()
    localities_poly = os.path.join(base_dir,'stayorgo','static','gis','locality_polygon.shp')
    reader = shpreader.Reader(localities_poly)
    record = reader.records()

    locality_list = []
    #i=0
    for locality in record:
        loc_center_x = round((locality.bounds[2] + locality.bounds[0])/2,4)
        loc_center_y = round((locality.bounds[1] + locality.bounds[3])/2,4)

        locality_list.append('%s,%s,%s' % (locality.attributes['LOCALITY'].title(),loc_center_x,loc_center_y))
        #print(locality.attributes['LOCALITY'].title(),loc_center_x,loc_center_y)
        #i+=1
    
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

    fname = os.path.join(base_dir,'stayorgo','static','gis','locality_list.json')
    with open(fname,'w') as outfile:
        json.dump(data,outfile)

    print(locality_list)
    return 'Done.'