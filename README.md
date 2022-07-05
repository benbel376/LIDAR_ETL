# LIDER ETL

**Table of contents**

- [Overview](#overview)
- [Requirements](#requirements)
- [Install](#install)
- [Data](#Data)
- [Docs](#docs)
- [Src](#src)
- [Experiments](#experiments)
- [Tests](#tests)

## Overview

> In this project I took data using API provided by USGS_3DEP ( United States Geological Survey 3D Elevation Program). AgriTech is a company working on maize farms and this project is done for the study of maize farms for water flow across different geographical areas. Extraction, Visualization and transformation of data were achieved in this project.

## Requirements

- PDAL
- Geopandas

## Install

```
git clone hhttps://github.com/benbel376/LIDAR_ETL.git
cd LIDAR_ETL
pip install -r docs/requirements.txt
```
or 
```
use this command: pip install -i https://test.pypi.org/simple/ pypointd==0.0.1
```

## Data
- **The Data:**  is a LIDAR HIgh definition elevation data. It is a point cloud, which is basically a set of data points in space. The points may represent a 3D shape or object. Each point position has its set of Cartesian coordinates (X, Y, Z) and associated characteristics like intensity, color, and many others. In the context of this project, the data is a national baseline of consistent high-resolution topographic elevation data – both bare earth and 3D point clouds collected in the 3D Elevation Program led by USGS.

- **Source of data:** USGS uploaded publicly available amazon s3 bucket found in the following url https://s3-us-west-2.amazonaws.com/usgs-lidar-public.

- **Data Structure:** 1,801 Datasets are currently available via the USGS 3D Elevation Program that are organized based on region and year. The data is stored in Entwine Point Tile (EPT) format, which is a simple and flexible octree-based storage format for point cloud data. 
## folder structure
![image](https://user-images.githubusercontent.com/44437166/177311319-478516eb-7720-4f66-abd7-f649c64a96c4.png)
## Docs
> contains the documentation of the package
> requirements.txt
> example.ipynb

## Src

> the main package modules directory that contains modules, supporting or util scripts and essential data

## Experiments

> experimental functions are developed and tested here.

## Test

> All the unit and integration tests are found here
