#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : Compare AMET and fields on pressure levels
Author          : Yang Liu
Date            : 2018.03.23
Last Update     : 2018.03.23
Description     : The code aims to plot and compare the meridional energy transport
                  computed from pressure levels of each atmospheric reanalysis datasets.
                  Regressions of AMET from model level of each product on the variable
                  fields from pressure level are performed, too. Since the variables
                  come from 3 pressure levels, which are 200hPa (tropopause, 10km),
                  500hPa (mid-troposphere, 5km) and 850hPa (low-troposphere, 1km), we
                  can have more insight on the source of difference between different
                  products.
Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, sys, matplotlib, logging
variables       : Atmospheric Meridional Energy Transport   ERA-Interim     MERRA2       JRA55
Caveat!!        : Spatial and temporal coverage
                  Atmosphere
                  ERA-Interim 1979 - 2016
                  MERRA2      1980 - 2016
                  JRA55       1979 - 2015

                  For the fields on pressure level, three levels are included:
                  200hPa
                  500hPa
                  850hPa
"""

import seaborn as sns
import numpy as np
import scipy as sp
from scipy import stats
import time as tttt
from netCDF4 import Dataset,num2date
import os
import platform
import sys
import logging
import matplotlib
# generate images without having a window appear
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.path as mpath
from mpl_toolkits.basemap import Basemap, cm
import matplotlib.cm as mpl_cm
import cartopy
import cartopy.crs as ccrs
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import iris
import iris.plot as iplt
import iris.quickplot as qplt
import pandas

# switch on the seaborn effect
sns.set()

# calculate the time for the code execution
start_time = tttt.time()

################################   Input zone  ######################################
# specify data path
datapath_ERAI = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ERAI/postprocessing'
datapath_MERRA2 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/MERRA2/postprocessing'
datapath_JRA55 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/JRA55/postprocessing'
# target fields for regression
datapath_ERAI_pressure = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ERAI/regression'
datapath_MERRA2_pressure = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/MERRA2/regression'
#datapath_JRA55_fields = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/JRA55/regression'
# specify output path for the netCDF4 file
output_path = '/home/yang/NLeSC/Computation_Modeling/BlueAction/AMET/Comparison/regress/Pressure'
####################################################################################
# index of latitude for insteret
# There is a cut to JRA, too
# index of latitude for insteret
# 20N
lat_ERAI_20 = 93
lat_MERRA2_20 = 0
lat_JRA55_20 = 124
# 30N
lat_ERAI_30 = 80
lat_MERRA2_30 = 20
lat_JRA55_30 = 106
# 40N
lat_ERAI_40 = 67
lat_MERRA2_40 = 40
lat_JRA55_40 = 88
# 50N
lat_ERAI_50 = 53
lat_MERRA2_50 = 60
lat_JRA55_50 = 70
# 60N
lat_ERAI_60 = 40
lat_MERRA2_60 = 80
lat_JRA55_60 = 53
# 70N
lat_ERAI_70 = 27
lat_MERRA2_70 = 100
lat_JRA55_70 = 35
# 80N
lat_ERAI_80 = 13
lat_MERRA2_80 = 120
lat_JRA55_80 = 17
# make a dictionary for instereted sections (for process automation)
lat_interest = {}
lat_interest_list = [20,30,40,50,60,70,80]
lat_interest['ERAI'] = [lat_ERAI_20,lat_ERAI_30,lat_ERAI_40,lat_ERAI_50,lat_ERAI_60,lat_ERAI_70,lat_ERAI_80]
lat_interest['MERRA2'] = [lat_MERRA2_20,lat_MERRA2_30,lat_MERRA2_40,lat_MERRA2_50,lat_MERRA2_60,lat_MERRA2_70,lat_MERRA2_80]
lat_interest['JRA55'] = [lat_JRA55_20,lat_JRA55_30,lat_JRA55_40,lat_JRA55_50,lat_JRA55_60,lat_JRA55_70,lat_JRA55_80]
print '*******************************************************************'
print '*********************** extract variables *************************'
print '*******************************************************************'
dataset_ERAI = Dataset(datapath_ERAI + os.sep + 'model_daily_075_1979_2016_E_zonal_int.nc')
dataset_MERRA2 = Dataset(datapath_MERRA2 + os.sep + 'AMET_MERRA2_model_daily_1980_2016_E_zonal_int.nc')
dataset_JRA55 = Dataset(datapath_JRA55 + os.sep + 'AMET_JRA55_model_daily_1979_2015_E_zonal_int.nc')

dataset_ERAI_200hPa = Dataset(datapath_ERAI_pressure + os.sep + 'pressure_200hPa_ERAI_monthly_regress_1979_2016.nc')
dataset_ERAI_500hPa = Dataset(datapath_ERAI_pressure + os.sep + 'pressure_500hPa_ERAI_monthly_regress_1979_2016.nc')
dataset_ERAI_850hPa = Dataset(datapath_ERAI_pressure + os.sep + 'pressure_850hPa_ERAI_monthly_regress_1979_2016.nc')

dataset_MERRA2_200hPa = Dataset(datapath_MERRA2_pressure + os.sep + 'pressure_200hPa_MERRA2_monthly_regress_1980_2016.nc')
dataset_MERRA2_500hPa = Dataset(datapath_MERRA2_pressure + os.sep + 'pressure_500hPa_MERRA2_monthly_regress_1980_2016.nc')
dataset_MERRA2_850hPa = Dataset(datapath_MERRA2_pressure + os.sep + 'pressure_850hPa_MERRA2_monthly_regress_1980_2016.nc')

AMET_ERAI = dataset_ERAI.variables['E'][:]/1000 # from Tera Watt to Peta Watt
AMET_MERRA2 = dataset_MERRA2.variables['E'][:]/1000 # from Tera Watt to Peta Watt
AMET_JRA55 = dataset_JRA55.variables['E'][:,:,0:125]/1000 # from Tera Watt to Peta Watt

year_ERAI = dataset_ERAI.variables['year'][:]             # from 1979 to 2016
year_MERRA2 = dataset_MERRA2.variables['year'][:]         # from 1980 to 2016
year_JRA55 = dataset_JRA55.variables['year'][:]           # from 1979 to 2015

latitude_ERAI = dataset_ERAI.variables['latitude'][:]
latitude_MERRA2 = dataset_MERRA2.variables['latitude'][:]
latitude_JRA55 = dataset_JRA55.variables['latitude'][0:125]

t_ERAI_200hPa = dataset_ERAI_200hPa.variables['t'][:]
t_ERAI_500hPa = dataset_ERAI_200hPa.variables['t'][:]
t_ERAI_850hPa = dataset_ERAI_200hPa.variables['t'][:]

t_MERRA2_200hPa = dataset_MERRA2_200hPa.variables['T'][:]
t_MERRA2_500hPa = dataset_MERRA2_200hPa.variables['T'][:]
t_MERRA2_850hPa = dataset_MERRA2_200hPa.variables['T'][:]

latitude_ERAI_pressure = dataset_ERAI_200hPa.variables['latitude'][:]
latitude_MERRA2_pressure = dataset_MERRA2_200hPa.variables['latitude'][:]

longitude_ERAI_pressure = dataset_ERAI_200hPa.variables['longitude'][:]
longitude_MERRA2_pressure = dataset_MERRA2_200hPa.variables['longitude'][:]

print '*******************************************************************'
print '*************************** whitening *****************************'
print '*******************************************************************'
month_ind = np.arange(12)
# climatology of AMET
seansonal_cycle_AMET_ERAI = np.mean(AMET_ERAI,axis=0)
seansonal_cycle_AMET_MERRA2 = np.mean(AMET_MERRA2,axis=0)
seansonal_cycle_AMET_JRA55 = np.mean(AMET_JRA55,axis=0)

seansonal_cycle_t_ERAI_200hPa = np.mean(t_ERAI_200hPa,axis=0)
seansonal_cycle_t_ERAI_500hPa = np.mean(t_ERAI_500hPa,axis=0)
seansonal_cycle_t_ERAI_850hPa = np.mean(t_ERAI_850hPa,axis=0)

seansonal_cycle_t_MERRA2_200hPa = np.mean(t_MERRA2_200hPa,axis=0)
seansonal_cycle_t_MERRA2_500hPa = np.mean(t_MERRA2_500hPa,axis=0)
seansonal_cycle_t_MERRA2_850hPa = np.mean(t_MERRA2_850hPa,axis=0)

AMET_ERAI_white = np.zeros(AMET_ERAI.shape,dtype=float)
AMET_MERRA2_white = np.zeros(AMET_MERRA2.shape,dtype=float)
AMET_JRA55_white = np.zeros(AMET_JRA55.shape,dtype=float)

t_ERAI_200hPa_white = np.zeros(t_ERAI_200hPa.shape,dtype=float)
t_ERAI_500hPa_white = np.zeros(t_ERAI_500hPa.shape,dtype=float)
t_ERAI_850hPa_white = np.zeros(t_ERAI_850hPa.shape,dtype=float)

t_MERRA2_200hPa_white = np.zeros(t_MERRA2_200hPa.shape,dtype=float)
t_MERRA2_500hPa_white = np.zeros(t_MERRA2_500hPa.shape,dtype=float)
t_MERRA2_850hPa_white = np.zeros(t_MERRA2_850hPa.shape,dtype=float)

for i in np.arange(len(year_ERAI)):
    for j in month_ind:
        AMET_ERAI_white[i,j,:] = AMET_ERAI[i,j,:] - seansonal_cycle_AMET_ERAI[j,:]

for i in np.arange(len(year_MERRA2)):
    for j in month_ind:
        AMET_MERRA2_white[i,j,:] = AMET_MERRA2[i,j,:] - seansonal_cycle_AMET_MERRA2[j,:]

for i in np.arange(len(year_JRA55)):
    for j in month_ind:
        AMET_JRA55_white[i,j,:] = AMET_JRA55[i,j,:] - seansonal_cycle_AMET_JRA55[j,:]

for i in np.arange(len(year_ERAI)):
    for j in month_ind:
        t_ERAI_200hPa_white[i,j,:,:] = t_ERAI_200hPa[i,j,:,:] - seansonal_cycle_t_ERAI_200hPa[j,:,:]
        t_ERAI_500hPa_white[i,j,:,:] = t_ERAI_500hPa[i,j,:,:] - seansonal_cycle_t_ERAI_500hPa[j,:,:]
        t_ERAI_850hPa_white[i,j,:,:] = t_ERAI_850hPa[i,j,:,:] - seansonal_cycle_t_ERAI_850hPa[j,:,:]

for i in np.arange(len(year_MERRA2)):
    for j in month_ind:
        t_MERRA2_200hPa_white[i,j,:,:] = t_MERRA2_200hPa[i,j,:,:] - seansonal_cycle_t_MERRA2_200hPa[j,:,:]
        t_MERRA2_500hPa_white[i,j,:,:] = t_MERRA2_500hPa[i,j,:,:] - seansonal_cycle_t_MERRA2_500hPa[j,:,:]
        t_MERRA2_850hPa_white[i,j,:,:] = t_MERRA2_850hPa[i,j,:,:] - seansonal_cycle_t_MERRA2_850hPa[j,:,:]
print '*******************************************************************'
print '****************** prepare variables for plot *********************'
print '*******************************************************************'
# dataset with seasonal cycle - time series
AMET_ERAI_series = AMET_ERAI.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI))
AMET_MERRA2_series = AMET_MERRA2.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2))
AMET_JRA55_series = AMET_JRA55.reshape(len(year_JRA55)*len(month_ind),len(latitude_JRA55))
# dataset without seasonal cycle - time series
AMET_ERAI_white_series = AMET_ERAI_white.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI))
AMET_MERRA2_white_series = AMET_MERRA2_white.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2))
AMET_JRA55_white_series = AMET_JRA55_white.reshape(len(year_JRA55)*len(month_ind),len(latitude_JRA55))
# fields on pressure level with seasonal cycle - time series
t_ERAI_200hPa_series = t_ERAI_200hPa.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI_pressure),len(longitude_ERAI_pressure))
t_ERAI_500hPa_series = t_ERAI_500hPa.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI_pressure),len(longitude_ERAI_pressure))
t_ERAI_850hPa_series = t_ERAI_850hPa.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI_pressure),len(longitude_ERAI_pressure))

t_MERRA2_200hPa_series = t_MERRA2_200hPa.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2_pressure),len(longitude_MERRA2_pressure))
t_MERRA2_500hPa_series = t_MERRA2_500hPa.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2_pressure),len(longitude_MERRA2_pressure))
t_MERRA2_850hPa_series = t_MERRA2_850hPa.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2_pressure),len(longitude_MERRA2_pressure))
# fields without seasonal cycle - time series
t_ERAI_200hPa_white_series = t_ERAI_200hPa_white.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI_pressure),len(longitude_ERAI_pressure))
t_ERAI_500hPa_white_series = t_ERAI_500hPa_white.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI_pressure),len(longitude_ERAI_pressure))
t_ERAI_850hPa_white_series = t_ERAI_850hPa_white.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI_pressure),len(longitude_ERAI_pressure))

t_MERRA2_200hPa_white_series = t_MERRA2_200hPa_white.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2_pressure),len(longitude_MERRA2_pressure))
t_MERRA2_500hPa_white_series = t_MERRA2_500hPa_white.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2_pressure),len(longitude_MERRA2_pressure))
t_MERRA2_850hPa_white_series = t_MERRA2_850hPa_white.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2_pressure),len(longitude_MERRA2_pressure))

print '*******************************************************************'
print '**********************     regression     *************************'
print '******************    original and anomalies   ********************'
print '*******************************************************************'
level_list = ['200hPa','500hPa','850hPa']

#***************************************************************************#
#*****************   regress of ERA Interim fields on pressure level  *******************#
#*************   on AMET from ERA-Interim   ***************#
#***************************************************************************#

# create an array to store the correlation coefficient
slope_ERAI_fields = np.zeros((len(latitude_ERAI_pressure),len(longitude_ERAI_pressure)),dtype = float)
r_value_ERAI_fields = np.zeros((len(latitude_ERAI_pressure),len(longitude_ERAI_pressure)),dtype = float)
p_value_ERAI_fields= np.zeros((len(latitude_ERAI_pressure),len(longitude_ERAI_pressure)),dtype = float)

latitude_ERAI_iris = iris.coords.DimCoord(latitude_ERAI_pressure,standard_name='latitude',long_name='latitude',
                             var_name='lat',units='degrees')
longitude_ERAI_iris = iris.coords.DimCoord(longitude_ERAI_pressure,standard_name='longitude',long_name='longitude',
                             var_name='lon',units='degrees')
# choose the coordinate system for Cube (for regrid module)
coord_sys = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)

for c in np.arange(len(lat_interest_list)):
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      ERA-Interim      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      200hPa      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
    # linear regress t on AMET (anomalies)
    # plot correlation coefficient
    for i in np.arange(len(latitude_ERAI_pressure)):
        for j in np.arange(len(longitude_ERAI_pressure)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope_ERAI_fields[i,j],_,r_value_ERAI_fields[i,j],p_value_ERAI_fields[i,j],_ = stats.linregress(AMET_ERAI_white_series[:,lat_interest['ERAI'][c]],t_ERAI_200hPa_white_series[:,i,j])
    # figsize works for the size of the map, not the entire figure
    fig1 = plt.figure()
    cube_ERAI = iris.cube.Cube(r_value_ERAI_fields,long_name='Correlation coefficient between t and AMET',
                               var_name='r',units='1',dim_coords_and_dims=[(latitude_ERAI_iris, 0), (longitude_ERAI_iris, 1)])
    cube_ERAI.coord('latitude').coord_system = coord_sys
    cube_ERAI.coord('longitude').coord_system = coord_sys
    # suptitle is the title for the figure
    fig1.suptitle('Regression of Temperature Anomaly on 200hPa on AMET Anomaly across %d N (ERA-Interim)' % (lat_interest_list[c]) ,fontsize = 7,y=0.93)
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_global()
    #ax.set_aspect('auto')
    ax.set_aspect('1.0')
    ax.coastlines()
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,linewidth=1, color='gray', alpha=0.5,linestyle='--')
    gl.xlabels_top = False
    # use of formatter (fixed), only after this the style setup will work
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    # specify label styles
    gl.xlabel_style = {'size': 6, 'color': 'gray'}
    gl.ylabel_style = {'size': 6, 'color': 'gray'}
    # Load a Cynthia Brewer palette.
    #brewer_cmap = mpl_cm.get_cmap('brewer_RdYlBu_11')
    cs = iplt.pcolormesh(cube_ERAI,cmap='coolwarm',vmin=-0.30,vmax=0.30)
    cbar = fig1.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.1,format="%.2f")
    cbar.set_ticks([-0.30, -0.25, -0.20, -0.15, -0.10, -0.05, 0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30])
    cbar.set_clim(-0.30, 0.30)
    cbar.ax.tick_params(labelsize = 6)
    cbar.set_label('Correlation coefficient',size = 6)
    # locate the indices of p_value matrix where error p<0.05 (99.5% confident)
    ii, jj = np.where(p_value_ERAI_fields<=0.05)
    # get the coordinate on the map (lon,lat) and plot scatter dots
    ax.scatter(longitude_ERAI_pressure[jj],latitude_ERAI_pressure[ii],transform=ccrs.Geodetic(),s=0.1,c='g',alpha=0.3) # alpha bleding factor with map
    # show and save plot
    plt.show()
    fig1.savefig(output_path + os.sep + 'ERAI' + os.sep + "Regression_AMET_%dN_t_200hPa_white_correlation_coef.jpeg" % (lat_interest_list[c]),dpi=300)
    plt.close(fig1)

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      500hPa      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
    for i in np.arange(len(latitude_ERAI_pressure)):
        for j in np.arange(len(longitude_ERAI_pressure)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope_ERAI_fields[i,j],_,r_value_ERAI_fields[i,j],p_value_ERAI_fields[i,j],_ = stats.linregress(AMET_ERAI_white_series[:,lat_interest['ERAI'][c]],t_ERAI_500hPa_white_series[:,i,j])
    fig2 = plt.figure()
    cube_ERAI = iris.cube.Cube(r_value_ERAI_fields,long_name='Correlation coefficient between t and AMET',
                               var_name='r',units='1',dim_coords_and_dims=[(latitude_ERAI_iris, 0), (longitude_ERAI_iris, 1)])
    cube_ERAI.coord('latitude').coord_system = coord_sys
    cube_ERAI.coord('longitude').coord_system = coord_sys
    # suptitle is the title for the figure
    fig2.suptitle('Regression of Temperature Anomaly on 500hPa on AMET Anomaly across %d N (ERA-Interim)' % (lat_interest_list[c]) ,fontsize = 7,y=0.93)
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_global()
    #ax.set_aspect('auto')
    ax.set_aspect('1.0')
    ax.coastlines()
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,linewidth=1, color='gray', alpha=0.5,linestyle='--')
    gl.xlabels_top = False
    # use of formatter (fixed), only after this the style setup will work
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    # specify label styles
    gl.xlabel_style = {'size': 6, 'color': 'gray'}
    gl.ylabel_style = {'size': 6, 'color': 'gray'}
    # Load a Cynthia Brewer palette.
    #brewer_cmap = mpl_cm.get_cmap('brewer_RdYlBu_11')
    cs = iplt.pcolormesh(cube_ERAI,cmap='coolwarm',vmin=-0.30,vmax=0.30)
    cbar = fig2.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.1,format="%.2f")
    cbar.set_ticks([-0.30, -0.25, -0.20, -0.15, -0.10, -0.05, 0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30])
    cbar.set_clim(-0.30, 0.30)
    cbar.ax.tick_params(labelsize = 6)
    cbar.set_label('Correlation coefficient',size = 6)
    # locate the indices of p_value matrix where error p<0.05 (99.5% confident)
    ii, jj = np.where(p_value_ERAI_fields<=0.05)
    # get the coordinate on the map (lon,lat) and plot scatter dots
    ax.scatter(longitude_ERAI_pressure[jj],latitude_ERAI_pressure[ii],transform=ccrs.Geodetic(),s=0.1,c='g',alpha=0.3) # alpha bleding factor with map
    # show and save plot
    plt.show()
    fig2.savefig(output_path + os.sep + 'ERAI' + os.sep + "Regression_AMET_%dN_t_500hPa_white_correlation_coef.jpeg" % (lat_interest_list[c]),dpi=300)
    plt.close(fig2)

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      850hPa      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
    for i in np.arange(len(latitude_ERAI_pressure)):
        for j in np.arange(len(longitude_ERAI_pressure)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope_ERAI_fields[i,j],_,r_value_ERAI_fields[i,j],p_value_ERAI_fields[i,j],_ = stats.linregress(AMET_ERAI_white_series[:,lat_interest['ERAI'][c]],t_ERAI_850hPa_white_series[:,i,j])
    fig3 = plt.figure()
    cube_ERAI = iris.cube.Cube(r_value_ERAI_fields,long_name='Correlation coefficient between t and AMET',
                               var_name='r',units='1',dim_coords_and_dims=[(latitude_ERAI_iris, 0), (longitude_ERAI_iris, 1)])
    cube_ERAI.coord('latitude').coord_system = coord_sys
    cube_ERAI.coord('longitude').coord_system = coord_sys
    # suptitle is the title for the figure
    fig3.suptitle('Regression of Temperature Anomaly on 850hPa on AMET Anomaly across %d N (ERA-Interim)' % (lat_interest_list[c]) ,fontsize = 7,y=0.93)
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_global()
    #ax.set_aspect('auto')
    ax.set_aspect('1.0')
    ax.coastlines()
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,linewidth=1, color='gray', alpha=0.5,linestyle='--')
    gl.xlabels_top = False
    # use of formatter (fixed), only after this the style setup will work
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    # specify label styles
    gl.xlabel_style = {'size': 6, 'color': 'gray'}
    gl.ylabel_style = {'size': 6, 'color': 'gray'}
    # Load a Cynthia Brewer palette.
    #brewer_cmap = mpl_cm.get_cmap('brewer_RdYlBu_11')
    cs = iplt.pcolormesh(cube_ERAI,cmap='coolwarm',vmin=-0.30,vmax=0.30)
    cbar = fig3.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.1,format="%.2f")
    cbar.set_ticks([-0.30, -0.25, -0.20, -0.15, -0.10, -0.05, 0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30])
    cbar.set_clim(-0.30, 0.30)
    cbar.ax.tick_params(labelsize = 6)
    cbar.set_label('Correlation coefficient',size = 6)
    # locate the indices of p_value matrix where error p<0.05 (99.5% confident)
    ii, jj = np.where(p_value_ERAI_fields<=0.05)
    # get the coordinate on the map (lon,lat) and plot scatter dots
    ax.scatter(longitude_ERAI_pressure[jj],latitude_ERAI_pressure[ii],transform=ccrs.Geodetic(),s=0.1,c='g',alpha=0.3) # alpha bleding factor with map
    # show and save plot
    plt.show()
    fig3.savefig(output_path + os.sep + 'ERAI' + os.sep + "Regression_AMET_%dN_t_850hPa_white_correlation_coef.jpeg" % (lat_interest_list[c]),dpi=300)
    plt.close(fig3)

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
