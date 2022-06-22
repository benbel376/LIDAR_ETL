import pdal
import json
import geopandas
import pandas as pd
from shapely.geometry import Polygon, Point, mapping
import numpy as np
from pyproj import Proj, transform
import folium
import laspy as lp


class pypoint: 
    """
    class that provides data fetching, transforming, and visualization functionalities
    
    """
    def generate_geo_df(pipe, epsg):
    """
    returns a geopandas dataframe
    """
        try:
            cloud_points = []
            elevations =[]
            geometry_points=[]
            for row in pipe.arrays[0]:
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

    def render_3d(points, s: float = 0.01) -> None:
        """ Plots a 3D terrain scatter plot for the cloud data points of geopandas data frame using matplotlib
        """

        fig, ax = plt.subplots(1, 1, figsize=(12, 10))
        ax = plt.axes(projection='3d')
        ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=s)
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        plt.savefig('plot3d.png', dpi=120)
        plt.show()


    def plot_heatmap(df, title) -> None:
        """ Plots a 2D heat map for the point cloud data using matplotlib
        """

        fig, ax = plt.subplots(1, 1, figsize=(12, 10))
        df.plot(column='elevation', ax=ax, legend=True, cmap="terrain")
        plt.title(title)
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.savefig('eatmap.png', dpi=120)
        plt.show()