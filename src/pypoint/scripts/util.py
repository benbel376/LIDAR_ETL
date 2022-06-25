import pdal
import json
import geopandas
import pandas as pd
from shapely.geometry import Polygon, Point, mapping
import numpy as np
from pyproj import Proj, transform
import folium
import laspy as lp
import richdem as rd
import rasterio
import math
import urllib.request, json 
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")

class Util:
    
    def create_meta(self, region_list, name, url, offset=0):
        metadata = {}
        urlf = ""+str(url)
        counter = 0 + offset
        for i in range(len(region_list)):
            newurl = urlf+str(region_list[i+offset])+"ept.json"
            counter = counter+1
            try:
                with open(name, 'r') as openfile:
                    # Reading from json file
                    metadata = json.load(openfile)
            except:
                pass
            print((newurl), counter)
            with urllib.request.urlopen(newurl, timeout=1000000) as url:
                data = json.loads(url.read().decode())
                metadata[f'{region_list[i+offset]}'] = data
            with open(name, "w") as outfile:
                outfile.write(json.dumps(metadata))
                
                
    # loading json file
    def read_json(self, json_path):
        """ reads a json file and returns a pthon dictionary

        json_path:
            path to file

        return:
            a python dictionary
        """
        try:
            with open(json_path) as js:
                json_obj = json.load(js)
            return json_obj

        except FileNotFoundError:
            print('File not found.')
    
    
    
    def compare(meta_loc, coor):
        
        try:
            with open(meta_loc, 'r') as openfile:
                # Reading from json file
                metadata = json.load(openfile)
                metakeys = list(metadata.keys())
        except:
            pass
        selection_list = {}
        for i in range(len(metakeys)):
            bounds = metadata[metakeys[i]]['boundsConforming']
            xMin, yMin = float(bounds[0]), float(bounds[1])
            xMax, yMax = float(bounds[3]), float(bounds[4])
            for points in coor:
                px = float(points[0])
                py = float(points[1])
                if((px >= xMin) and (px <= xMax)):
                    if((py >= yMin) and (py <= yMax)):
                        save_bounds = bounds[:]
                        save_bounds.pop(2)
                        save_bounds.pop(4)
                        selection_list[metakeys[i]] = save_bounds

        return [list(selection_list.keys()), list(selection_list.values())]

    def convert_EPSG(self, fromT, lon, lat):
        """ a function that converts one EPSG format to another

        parameters:
            fromT: the original EPSG format
            lon: the longitude value
            lat: the latitude value

        Return: 
            [x, y]: a list with new EPSG formatted values

        """
        P3857 = Proj(init='epsg:3857')
        P4326 = Proj(init='epsg:4326')
        if(fromT == 4326):
            input1 = P4326
            input2 = P3857
        else:
            input1=p3857
            input2=p4326

        x, y = transform(input1,input2, lon, lat)
        return [x, y]

    def loop_EPSG_converter(self, listin):
        """ runs the EPSG converter for specified amount of iterations

        Parameter:
            listin: a list that contains a pair of latitude and longitude values

        Return: 
            converted: a new list with converted set of pairs of the values

        """
        converted = []
        for item in listin:
            converted.append(convert_EPSG(4326, item[0], item[1]))

        return converted


    def generate_polygon(self, coor, epsg):
        polygon_g = Polygon(coor)
        crs = {'init': 'epsg:'+str(epsg)}
        polygon = gpd.GeoDataFrame(index=[0], crs=crs, geometry=[polygon_g])       
        return polygon


    def show_on_map(self, polygon, zoom):
        #region selection
        poly = mapping((polygon2.iloc[:,0][0]))
        tmp = poly['coordinates'][0][0]
        anchor = [tmp[1], tmp[0]]
        m = folium.Map(anchor,zoom_start=zoom, tiles='cartodbpositron')
        folium.GeoJson(polygon).add_to(m)
        folium.LatLngPopup().add_to(m)
        return m


    def modify_pipe_json(self, json_loc, url, region, in_epsg, out_epsg):
        dicti = read_json(json_loc)
        dicti['pipeline'][0]['polygon'] = str(polygon.iloc[:,0][0])
        dicti['pipeline'][0]['filename'] = f"{url}/{region}/ept.json"
        dicti['pipeline'][2]['in_srs'] = f"EPSG:{in_epsg}"
        dicti['pipeline'][2]['out_srs'] = f"EPSG:{out_epsg}"
        print(dicti)
        return dicti
