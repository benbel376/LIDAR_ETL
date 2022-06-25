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
from branca.element import Figure
import urllib.request, json 
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")

class Util:
    
    def create_meta(self, region_list, name, url, offset=0):
        """creates meta data
        Params:
            region_list: csv or txt file with list of regions
            name: name for the metadata to generate.
            url: the url to fetch the metadata from.
            offset: the line number in the region_list to start fetching data from
            
        return: None.
        """
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

        params:
            json_path: path to file

        return:
            a python dictionary
        """
        try:
            with open(json_path) as js:
                json_obj = json.load(js)
            return json_obj

        except FileNotFoundError:
            print('File not found.')
    
    
    
    def compare(self, meta_loc, coor):
        """ compares meta_loc with the polygon coordinate to determine where the polygon is found
        
        params:
            meta_loc: the location of the metadata
            coor: the polygon coordinates: it is a list of points.
            
        return: regions that hold the polygon and their boundaries.
        
        """
        
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




    def convert_EPSG(self, fromT, toT, lon, lat):
        """ converts EPSG formats from one type to another
        
        params: 
            fromT: the initial epsg value to convert from in integer
            toT: the fianl epsg value to convert to in integer
            lon: the longitude value in old format
            lat: the latitude value in old format
            
        return: new longitude and latitude values in the new format
        
        """
        input1 = Proj(init=f'epsg:{fromT}')
        input2 = Proj(init=f'epsg:{toT}') 
        x, y = transform(input1,input2, lon, lat)
        return [x, y]
        
    def loop_EPSG_converter(self, listin, fromT, toT):
        converted = []
        for item in listin:
            converted.append(self.convert_EPSG(fromT, toT, item[0], item[1]))
            
        return converted

    def generate_polygon(self, coor, epsg):
        polygon_g = Polygon(coor)
        crs = {'init': 'epsg:'+str(epsg)}
        polygon = geopandas.GeoDataFrame(index=[0], crs=crs, geometry=[polygon_g])       
        
        return polygon


    def show_on_map(self, polygon, zoom):
        #region selection
        poly = mapping((polygon.iloc[:,0][0]))
        tmp = poly['coordinates'][0][0]
        anchor = [tmp[1], tmp[0]]
        fig = Figure(width=600, height=400)
        m = folium.Map(anchor, zoom_start=zoom, tiles='cartodbpositron')
        folium.GeoJson(polygon).add_to(m)
        folium.LatLngPopup().add_to(m)
        fig.add_child(m)
        return fig


    def modify_pipe_json(self, json_loc, url, path, in_epsg, out_epsg, polygon_b, bounds=None):
        dicti = self.read_json(json_loc)
        if bounds is not None:
            dicti['pipeline'][0]['bounds'] = f"([{bounds[0]},{bounds[2]}],[{bounds[1]},{bounds[3]}])"
        dicti['pipeline'][0]['polygon'] = str(polygon_b.iloc[:,0][0])
        dicti['pipeline'][0]['filename'] = url
        dicti['pipeline'][2]['in_srs'] = f"EPSG:{in_epsg}"
        dicti['pipeline'][2]['out_srs'] = f"EPSG:{out_epsg}"
        dicti['pipeline'][3]['filename'] = f"{path}"
        
        return dicti
