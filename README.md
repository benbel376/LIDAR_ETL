# LIDER ETL
![image](https://user-images.githubusercontent.com/44437166/182764292-56939b27-152e-4ba5-8443-0aa8aa5932b0.png)

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

### Introduction
In this project we will be developing reliable, pip installable python module that can be used to work with LIDAR point cloud data. the business context is the following:

```We can better predict maize harvest if we better understand how water flows through a field, and which parts are likely to be flooded or too dry. One important ingredient to understanding water flow in a field is by measuring the elevation of the field at many points. The USGS recently released high resolution elevation data as a lidar point cloud called USGS 3DEP in a public dataset on Amazon. This dataset is essential to build models of water flow and predict plant health and maize harvest. ```

LIDAR high definition elevation data - USGS 3DEP - The USGS recently released high resolution elevation data as a lidar point cloud in a public dataset on Amazon. This dataset is complicated to understand and use, and it would be useful to have an easy way to access and use it in order to build models of water flow and predict plant health and maize harvest. 

The project's task was to write a modular python code/package to connect to the API, query the data model to select with  a specified input and get a desired output. For example, submit a boundary (GPS coordinates polygon) and receive back a raster of the height of the terrain within the boundary.

![image](https://user-images.githubusercontent.com/44437166/182767144-49aa7fa9-992e-4b1c-b136-7658cc7aeaad.png)


This project can be used to work with Working with satellite imagery as well as geographical data files. It allows you to Load the Data from its source (s3 bucket) and Visualize it, filter 

## Data
- **The Data:**  is a [LIDAR HIgh definition elevation data](https://registry.opendata.aws/usgs-lidar/). It is a point cloud, which is basically a set of data points in space. The points may represent a 3D shape or object. Each point position has its set of Cartesian coordinates (X, Y, Z) and associated characteristics like intensity, color, and many others. In the context of this project, the data is a national baseline of consistent high-resolution topographic elevation data – both bare earth and 3D point clouds collected in the 3D Elevation Program led by USGS.

- **Source of data:** USGS uploaded publicly available amazon s3 bucket found in the following url https://s3-us-west-2.amazonaws.com/usgs-lidar-public.

- **Data Structure:** 1,801 Datasets are currently available via the USGS 3D Elevation Program that are organized based on region and year. The data is stored in Entwine Point Tile (EPT) format, which is a simple and flexible octree-based storage format for point cloud data. 
## essential folder structure
![image](https://user-images.githubusercontent.com/44437166/177312047-50415cba-d225-4036-b3fc-a206606cf2f5.png)
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


## Technology Used
- Python Library
  - PDAL
  - Geopandas
## Prerequistes

- python 3.8

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
## Usage
![image](https://user-images.githubusercontent.com/44437166/182864566-f4eaa00e-a802-4642-b0ed-a2b71d385141.png)
![image](https://user-images.githubusercontent.com/44437166/182864601-198cac62-331d-4006-b8a4-ea5a72e56d02.png)
![image](https://user-images.githubusercontent.com/44437166/182864619-58fc8630-cecc-42f5-a983-6e6f99c2083a.png)
![image](https://user-images.githubusercontent.com/44437166/182864642-5d72cb23-b8ac-4a4e-babf-185654d036fe.png)
![image](https://user-images.githubusercontent.com/44437166/182864651-7b44d432-b45a-4f07-93bd-7e5c427d479d.png)

## License
- [MIT License](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwiMqbrwqaz5AhVPiqQKHa5uCtkQFnoECAYQAQ&url=https%3A%2F%2Fopensource.org%2Flicenses%2FMIT&usg=AOvVaw1MsEPekvPKCIceu2jiRDy4)

## Author

👤 **Biniyam Belayneh**

- GitHub: [Biniyam Belayneh](https://github.com/benbel376)
- LinkedIn: [Biniyam Belayneh](https://www.linkedin.com/in/biniyam-belayneh-demisse-42909617a/)
## Acknowledgement
- Thank you [10 academy](https://www.10academy.org/) for the project idea and resource provision
- Thank you [python tutorials](https://packaging.python.org/tutorials/packaging-projects/) for awsome blog posts on data engineering
- Thank you [LIDAR HIgh definition elevation data](https://registry.opendata.aws/usgs-lidar/). for data source
## Show your support

Give a ⭐ if you like this project!

