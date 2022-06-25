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
from scipy.interpolate import griddata
from rasterio.transform import Affine
from rasterio.crs import CRS
import urllib.request, json 
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
import sys

sys.path.append(".")
sys.path.append("..")
from scripts import util
utility = util.Util()

class Pypoint: 
    """
    class that provides data fetching, transforming, and visualization functionalities
    
    """
    
    def fetch_data(self, coordinates, 
                   meta_path,
                   save_path,
                   pipeline, 
                   epsg=[3857, 4326], 
                   url='https://s3-us-west-2.amazonaws.com/usgs-lidar-public/'):
        """
        loads data by taking path and epsg informations
        param:
            meta_path: the location of the metadata
            save_path: the location to save fetched data
            pipeline: the loction of the pdal pipeline json file
            epsg: a list of epsg files that hold original and new epsg values
            url: url to fetch the data from
            
        return: geopandas dataframe with elevation and location varibles
        """
        
        coor = utility.loop_EPSG_converter(coordinates, epsg[1], epsg[0])
        polygon = utility.generate_polygon(coor, epsg[0])

        selection = utility.compare(meta_path, coor)

        print(f"Selected Regions: {selection[0]}")

        data = self.load_full_data(selection, url, save_path, polygon, pipeline, epsg)

        return data

    

    def load_full_data(self, selection_list, url, path, polygon, json_location, epsg):
        """ loads data by taking selection information.
        
        params:
            selection_list: a list that contains region names and their boundaries
            url: url to fetch the data from
            path: the path to save the data to.
            polygon: the selection boundary in polygon form
            json_location: the location of pdal pipeline json
            epsg: a list: [from, to]
        
        return: geopandas dataframe.
        
        """
        
        
        regions = selection_list[0]
        bounds = selection_list[1]

        data = {}
        url = url
        for i in range(len(regions)):
            try:
                year = int(regions[i][-4:])
            except ValueError:
                year = None
            region = regions[i]
            furl = url+region+"ept.json"
            request = utility.modify_pipe_json(json_location, furl, path, epsg[0], epsg[1], polygon, bounds[i])
            pipe = pdal.Pipeline(json.dumps(request))
            num = pipe.execute()
            print(f"Number of loadded points: {num}")
            df = self.generate_geo_df(pipe.arrays[0], epsg[1])
            data["year"] = f"{year}"
            data["data"] = df

        return pd.DataFrame([data])

    def generate_geo_df(self, pipe, epsg):
        """ Turns an array into a geopandas dataframe.
        
        params: 
            pipe: pdal pipeline object
            epsg: from and to epsg formats
            
        return: a geopandas dataframe.
        """
        try:
            cloud_points = []
            elevations =[]
            geometry_points=[]
            for row in pipe:
                lst = row.tolist()[-3:]
                cloud_points.append(lst)
                elevations.append(lst[2])
                point = Point(lst[0], lst[1])
                geometry_points.append(point)
            geodf = geopandas.GeoDataFrame(columns=["elevation", "geometry"])
            geodf['elevation'] = elevations
            geodf['geometry'] = geometry_points
            geodf = geodf.set_geometry("geometry")
            geodf.set_crs(epsg = epsg, inplace=True)
            return geodf
        except RuntimeError as e:
            self.logger.exception('fails to extract geo data frame')
            print(e)


    
    def calculate_TWI(self, df, prec = 0.000001, epsg = 4326, save_slope=None, save_accum=None):
        """ calculates topographic wetness index based on slope and accmulation results.
        
        params: 
            df: the dataframe that holds the point cloud.
            prec: the precision for interpolation
            epsg: the final epsg format
            save_slope: a location to save the generated slope image
            save_accum: a location to save the accummulation image
            
        return: a new dataframe with TWI column added
        
        """
        
        in_df = df.copy()
        points = list(zip(in_df.geometry.x, in_df.geometry.y))
        values = in_df.elevation.values

        rRes = prec

        xRange = np.arange(in_df.geometry.x.min(), in_df.geometry.x.max()+rRes, rRes)
        yRange = np.arange(in_df.geometry.y.min(), in_df.geometry.y.max()+rRes, rRes)

        gridX, gridY = np.meshgrid(xRange, yRange)

        gridph = griddata(points, values, (gridX,gridY), method='cubic')

        transform = Affine.translation(gridX[0][0]-rRes/2, gridY[0][0]-rRes/2)*Affine.scale(rRes, rRes)
        transform

        rasterCrs = CRS.from_epsg(epsg)
        rasterCrs.data

        interpRaster = rasterio.open('raster.tif',
                                 'w',
                                 driver='GTiff',
                                 height=gridph.shape[0],
                                 width=gridph.shape[1],
                                 count=1,
                                 dtype=gridph.dtype,
                                 crs=rasterCrs,
                                 transform=transform,
                                )
        interpRaster.write(gridph,1)
        interpRaster.close()

        dataset = rasterio.open('raster.tif')

        data = dataset.read()

        data = np.squeeze(data)
        #data = np.nan_to_num(data, nan=-9999)
        sp_dem = rd.rdarray(data, no_data=-9999)

        slope = rd.TerrainAttribute(sp_dem, attrib='slope_riserun')
        if save_slope is not None:
            slope_pic = rd.rdShow(slope, axes=True, cmap='magma', figsize=(10, 5))
            plt.savefig(save_slope)

        accum_d8 = rd.FlowAccumulation(sp_dem, method='D8')
        if save_accum is not None:
            d8_fig = rd.rdShow(accum_d8,figsize=(10,5), axes=False, cmap='jet')
            plt.savefig(save_accum)

        slope_l = []
        accum_l = []
        for point in in_df['geometry']:
            x = point.xy[0][0]
            y = point.xy[1][0]
            row, col = dataset.index(x,y)
            slope_l.append(slope[row,col])
            accum_l.append(accum_d8[row,col])

        TWI = []

        for i in range(len(slope_l)):
            TWI.append(np.log(abs((accum_l[i]/math.tan((slope_l[i]* math.pi/180.0))))))

        in_df["TWI"] = TWI

        return in_df
    
    
    
    
    def render_3d(self, df, title, path, s: float = 0.01) -> None:
        """ Plots a 3D terrain scatter plot for the cloud data points of geopandas data frame using matplotlib
        
        params:
            df: the data
            title: the title for generated image
            path: path to save the generated image
            s: precision.
            
        return: none.
        """

        fig, ax = plt.subplots(1, 1, figsize=(12, 10))
        ax = plt.axes(projection='3d')
        ax.scatter(df.geometry.x, df.geometry.y, df.elevation.values, s=s)
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        plt.title(title)
        plt.savefig(f"{path}", dpi=120)
        plt.show()


    def plot_heatmap(self, df, title, path) -> None:
        """ Plots a 2D heat map for the point cloud data using matplotlib
        
        params: 
            df: the data.
            title: the title for the image to be generated.
            path: the path to save the image to be generated.
            
        returns: None.
        """

        fig, ax = plt.subplots(1, 1, figsize=(12, 10))
        df.plot(column='elevation', ax=ax, legend=True, cmap="terrain")
        plt.title(title)
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.savefig(f"{path}", dpi=120)
        plt.show()
        
        
    def grid_resample(self, df,size, epsg=4326):
        """ resamples points using grid method
        
        params: 
            df: the data
            size: the size of voxels
            epsg: the final epsg
            
        return: resampled dataframe.
        
        
        """
        newdf = df.copy()
        points1 = list(zip(newdf.geometry.x, newdf.geometry.y, newdf.elevation.values))

        voxel_size=size
        nb_vox=np.ceil((np.max(points1, axis=0) - np.min(points1, axis=0))/voxel_size)
        nb_vox

        non_empty_voxel_keys, inverse, nb_pts_per_voxel = np.unique(((points1 - np.min(points1, axis=0)) 
                                                                     // voxel_size).astype(int), axis=0, 
                                                                    return_inverse=True, return_counts=True)
        idx_pts_vox_sorted=np.argsort(inverse)

        voxel_grid={}
        grid_barycenter,grid_candidate_center=[],[]
        last_seen=0
        points_new = []
        for item in points1:
            tmp = []
            for it in item:
                tmp.append(it)
            points_new.append(tmp)

        points_new = np.array(points_new)

        for idx,vox in enumerate(non_empty_voxel_keys):
            voxel_grid[tuple(vox)]= points_new[idx_pts_vox_sorted[last_seen:last_seen+nb_pts_per_voxel[idx]]]
            nval = np.mean(voxel_grid[tuple(vox)],axis=0)
            grid_barycenter.append(nval)
            grid_candidate_center.append(
                voxel_grid[tuple(vox)][np.linalg.norm(voxel_grid[tuple(vox)] 
                                                      - np.mean(voxel_grid[tuple(vox)],axis=0),axis=1).argmin()])
            last_seen+=nb_pts_per_voxel[idx]

        df22 = self.generate_geo_df(grid_barycenter, epsg)

        return df22
