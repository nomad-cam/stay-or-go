import cartopy.io.shapereader as shpreader
import os
import json


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