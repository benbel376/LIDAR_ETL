import pdal
import json
import geopandas
import pandas as pd
from shapely.geometry import Polygon, Point, mapping
import numpy as np
from pyproj import Proj, transform
import folium
import laspy as lp

# loading json file
def read_json(json_path):
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
        
def convert_EPSG(fromT, lon, lat):
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
    
def loop_EPSG_converter(listin):
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


def generate_polygon(coor, epsg):
    polygon_g = Polygon(coor)
    crs = {'init': 'epsg:'+str(epsg)}
    polygon = gpd.GeoDataFrame(index=[0], crs=crs, geometry=[polygon_g])       
    return polygon