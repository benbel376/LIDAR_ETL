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
    
    def fetch_data(coordinates, 
                   polygon, 
                   pipeline, 
                   epsg=[3857, 4326], 
                   url='https://s3-us-west-2.amazonaws.com/usgs-lidar-public/'):
        
        coor = loop_EPSG_converter(coordinates, epsg[1], epsg[0])
        polygon = generate_polygon(coor, epsg[0])

        selection = compare("metadata.json", coor)

        print(f"Selected Regions: {selection[0]}")

        data = load_full_data(selection, url, polygon, pipeline, epsg)

        return data


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
    
    def calculate_TWI(df, prec = 0.000001, epsg = 4326, save_slope=None, save_accum=None):
        in_df = df.copy()
        points = list(zip(in_df.geometry.x, in_df.geometry.y))
        values = in_df.elevation.values

        rRes = prec

        xRange = np.arange(newdf.geometry.x.min(), newdf.geometry.x.max()+rRes, rRes)
        yRange = np.arange(newdf.geometry.y.min(), newdf.geometry.y.max()+rRes, rRes)

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
        for point in newdf['geometry']:
            x = point.xy[0][0]
            y = point.xy[1][0]
            row, col = dataset.index(x,y)
            slope_l.append(slope[row,col])
            accum_l.append(accum_d8[row,col])

        TWI = []

        for i in range(len(slope_l)):
            TWI.append(np.log(abs((accum_l[i]/math.tan((slope_l[i]* math.pi/180.0))))))

        df["TWI"] = TWI

        return df
    
    
    
    
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
        
        
    def grid_resample(df,size, epsg=4326):
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

        df22 = generate_geo_df(grid_barycenter, epsg)

        return df22
