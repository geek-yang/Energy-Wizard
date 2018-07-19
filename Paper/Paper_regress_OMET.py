#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : Regress climate patterns on oceanic meridional energy transport (ORAS4,GLORYS2V3,SODA3)
Author          : Yang Liu
Date            : 2018.06.07
Last Update     : 2018.07.19
Description     : The code aims to regress non-climatological fields on the oceanic
                  meridional energy transport calculated from different oceanic
                  reanalysis datasets. In this, case, this includes GLORYS2V3
                  from Mercator Ocean, ORAS4 from ECMWF, and SODA3 from University
                  of Maryland & TAMU.

                  The non-climatological fields include include Sea Level Pressure (SLP), Sea
                  Surface Tmperature (SST), Surface Skin Temperature (TS) and Sea
                  Ice Concentration (SIC). This helps with the understanding of the connections
                  of OMET with major climate patterns.

                  Since the ocean reanalysis included here are all driven by ERA-Interim,
                  we will take the non-climatological fields from ERA-Interim for regression.

                  The differnce, obtained from OMET at sections (20N - 80N), gives that it
                  is better to check the spatial distribution from 1995 to 2003

Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, sys, matplotlib
variables       : Meridional Energy Transport               E         [Tera-Watt]
                  Meridional Overturning Circulation        Psi       [Sv]
Caveat!!        : Time range
                  GLORYS2V3   1993 - 2014
                  ORAS4       1958(1979 in use) - 2014
                  SODA3       1980 - 2015
                  non-climatological fields  1979 - 2016

                  MOM5 Grid
                  Direction of Axis: from south to north, west to east
                  Model Level: MOM5 Arakawa-B grid
                  Dimension:
                  Latitude      1070
                  Longitude     1440
                  Depth         50

                  ORCA1 Grid
                  Direction of Axis: from south to north, west to east
                  Model Level: ORCA Arakawa-C grid
                  Dimension:
                  Latitude      362
                  Longitude     292
                  Depth         42

                  ORCA025 Grid
                  Direction of Axis: from south to north, west to east
                  Model Level: ORCA Arakawa-C grid
                  Dimension:
                  Latitude      1021
                  Longitude     1440
                  Depth         75

                  The mask might have filled value of 1E+20 (in order to maintain
                  the size of the netCDF file and make full use of the storage). When
                  take the mean of intergral, this could result in abnormal large results.
                  With an aim to avoid this problem, it is important to re-set the filled
                  value to be 0 and then take the array with filled value during calculation.
                  (use "masked_array.filled()")
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

# print the system structure and the path of the kernal
print platform.architecture()
print os.path

# calculate the time for the code execution
start_time = tttt.time()
# switch on the seaborn effect
sns.set()

################################   Input zone  ######################################
# specify data path
# OMET
datapath_ORAS4 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ORAS4/postprocessing'
datapath_GLORYS2V3 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/GLORYS2V3/postprocessing'
datapath_SODA3 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/SODA3/postprocessing'
# target fields for regression
datapath_ERAI_fields = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ERAI/regression'
# specify output path for figures
output_path = '/home/yang/NLeSC/PhD/Paperwork/Article/AMET_OMET/figures'
# index of latitude for insteret
################################   Input zone  ######################################

print '****************************************************************************'
print '********************    latitude index of insteret     *********************'
print '****************************************************************************'
# There is a cut to JRA, too
# index of latitude for insteret
# 20N
lat_ORAS4_20 = 181
lat_GLORYS2V3_20 = 579
lat_SODA3_20 = 569
# after a cut to 20-90 N
lat_ORAS4_20_cut = 1
lat_GLORYS2V3_20_cut = 0
lat_SODA3_20_cut = 0

# 30N
lat_ORAS4_30 = 192
lat_GLORYS2V3_30 = 623
lat_SODA3_30 = 613
# after a cut to 20-90 N
lat_ORAS4_30_cut = 12
lat_GLORYS2V3_30_cut = 44
lat_SODA3_30_cut = 44

# 40N
lat_ORAS4_40 = 204
lat_GLORYS2V3_40 = 672
lat_SODA3_40 = 662
# after a cut to 20-90 N
lat_ORAS4_40_cut = 24
lat_GLORYS2V3_40_cut = 93
lat_SODA3_40_cut = 93

# 50N
lat_ORAS4_50 = 218
lat_GLORYS2V3_50 = 726
lat_SODA3_50 = 719
# after a cut to 20-90 N
lat_ORAS4_50_cut = 38
lat_GLORYS2V3_50_cut = 147
lat_SODA3_50_cut = 150

# 60N
lat_ORAS4_60 = 233
lat_GLORYS2V3_60 = 788
lat_SODA3_60 = 789
# after a cut to 20-90 N
lat_ORAS4_60_cut = 53
lat_GLORYS2V3_60_cut = 209
lat_SODA3_60_cut = 220

# 70N
lat_ORAS4_70 = 250
lat_GLORYS2V3_70 = 857
lat_SODA3_70 = 880
# after a cut to 20-90 N
lat_ORAS4_70_cut = 70
lat_GLORYS2V3_70_cut = 278
lat_SODA3_70_cut = 311

# 80N
lat_ORAS4_80 = 269
lat_GLORYS2V3_80 = 932
lat_SODA3_80 = 974
# after a cut to 20-90 N
lat_ORAS4_80_cut = 89
lat_GLORYS2V3_80_cut = 353
lat_SODA3_80_cut = 405

# make a dictionary for instereted sections (for process automation)
lat_interest = {}
lat_interest_list = [60]
# after cut
lat_interest['ORAS4'] = [lat_ORAS4_60_cut]
lat_interest['GLORYS2V3'] = [lat_GLORYS2V3_60_cut]
lat_interest['SODA3'] = [lat_SODA3_60_cut]

print '*******************************************************************'
print '*********************** extract variables *************************'
print '*******************************************************************'
# # ORCA1_z42 grid infor (Madec and Imbard 1996)
# ji_1 = 362
# jj_1 = 292
# level_1 = 42
#
# # ORCA025_z75 grid infor (Madec and Imbard 1996)
# ji_025 = 1440
# jj_025 = 1021
# level_025 = 75

# # MOM5_z50 grid info
# ji_5 = 1440
# jj_5 = 1070
# level_5 = 50
dataset_GLORYS2V3 = Dataset(datapath_GLORYS2V3 + os.sep + 'GLORYS2V3_model_monthly_orca025_E_zonal_int.nc')
dataset_ORAS4 = Dataset(datapath_ORAS4 + os.sep + 'oras4_model_monthly_orca1_E_zonal_int.nc')
dataset_SODA3 = Dataset(datapath_SODA3 + os.sep + 'OMET_SODA3_model_5daily_1980_2015_E_zonal_int.nc')

dataset_ERAI_fields_SIC_SST_SLP = Dataset(datapath_ERAI_fields + os.sep + 'surface_ERAI_monthly_regress_1979_2016.nc')
dataset_ERAI_fields_TS_T2M = Dataset(datapath_ERAI_fields + os.sep + 'surface_ERAI_monthly_regress_1979_2016_extra.nc')

OMET_ORAS4 = dataset_ORAS4.variables['E'][21:,:,180:]/1000 # start from 1979
OMET_GLORYS2V3 = dataset_GLORYS2V3.variables['E'][:,:,579:]/1000 # start from 1993
OMET_SODA3 = dataset_SODA3.variables['E'][:,:,569:]/1000 # start from 1980

year_ORAS4 = dataset_ORAS4.variables['year'][21:]         # from 1979 to 2014
year_GLORYS2V3 = dataset_GLORYS2V3.variables['year'][:]   # from 1993 to 2014
year_SODA3 = dataset_SODA3.variables['year'][:]           # from 1980 to 2014

latitude_ORAS4 = dataset_ORAS4.variables['latitude_aux'][180:]
latitude_GLORYS2V3 = dataset_GLORYS2V3.variables['latitude_aux'][579:]
latitude_SODA3 = dataset_SODA3.variables['latitude_aux'][569:]

SLP_ERAI_series = dataset_ERAI_fields_SIC_SST_SLP.variables['msl'][:]   # dimension (time, lat, lon)

SST_ERAI_series = dataset_ERAI_fields_SIC_SST_SLP.variables['sst'][:]
SST_ERAI_mask = np.ma.getmaskarray(SST_ERAI_series[0,:,:])

SIC_ERAI_series = dataset_ERAI_fields_SIC_SST_SLP.variables['ci'][:]
SIC_ERAI_mask = np.ma.getmaskarray(SIC_ERAI_series[0,:,:])

TS_ERAI = dataset_ERAI_fields_TS_T2M.variables['ts'][:]

latitude_ERAI_fields = dataset_ERAI_fields_SIC_SST_SLP.variables['latitude'][:]
longitude_ERAI_fields = dataset_ERAI_fields_SIC_SST_SLP.variables['longitude'][:]

time_series = dataset_ERAI_fields_SIC_SST_SLP.variables['time'][:]
year_ERAI = dataset_ERAI_fields_TS_T2M.variables['year'][:]

print '*******************************************************************'
print '*************************** whitening *****************************'
print '*******************************************************************'
month_ind = np.arange(12)
# seasonal cycle of OMET
seansonal_cycle_OMET_ORAS4 = np.mean(OMET_ORAS4,axis=0)
seansonal_cycle_OMET_GLORYS2V3 = np.mean(OMET_GLORYS2V3,axis=0)
seansonal_cycle_OMET_SODA3 = np.mean(OMET_SODA3,axis=0)

seasonal_cycle_SLP_ERAI = np.zeros((12,len(latitude_ERAI_fields),len(longitude_ERAI_fields))) # from 20N - 90N
seasonal_cycle_SST_ERAI = np.zeros((12,len(latitude_ERAI_fields),len(longitude_ERAI_fields))) # from 20N - 90N
seasonal_cycle_TS_ERAI = np.mean(TS_ERAI,axis=0)

OMET_ORAS4_white = np.zeros(OMET_ORAS4.shape,dtype=float)
OMET_GLORYS2V3_white = np.zeros(OMET_GLORYS2V3.shape,dtype=float)
OMET_SODA3_white = np.zeros(OMET_SODA3.shape,dtype=float)

SLP_ERAI_white_series = np.zeros(SLP_ERAI_series.shape,dtype=float)
SST_ERAI_white_series = np.zeros(SST_ERAI_series.shape,dtype=float)
TS_ERAI_white = np.zeros(TS_ERAI.shape,dtype=float)

for i in np.arange(len(year_ORAS4)):
    for j in month_ind:
        OMET_ORAS4_white[i,j,:] = OMET_ORAS4[i,j,:] - seansonal_cycle_OMET_ORAS4[j,:]

for i in np.arange(len(year_GLORYS2V3)):
    for j in month_ind:
        OMET_GLORYS2V3_white[i,j,:] = OMET_GLORYS2V3[i,j,:] - seansonal_cycle_OMET_GLORYS2V3[j,:]

for i in np.arange(len(year_SODA3)):
    for j in month_ind:
        OMET_SODA3_white[i,j,:] = OMET_SODA3[i,j,:] - seansonal_cycle_OMET_SODA3[j,:]

for i in np.arange(len(year_ERAI)):
    for j in month_ind:
        TS_ERAI_white[i,j,:] = TS_ERAI[i,j,:] - seasonal_cycle_TS_ERAI[j,:]

# anomalies
for i in month_ind:
    # calculate the monthly mean (seasonal cycling)
    seasonal_cycle_SLP_ERAI[i,:,:] = np.mean(SLP_ERAI_series[i::12,:,:],axis=0)
    seasonal_cycle_SST_ERAI[i,:,:] = np.mean(SST_ERAI_series[i::12,:,:],axis=0)
    # remove seasonal mean
    SLP_ERAI_white_series[i::12,:,:] = SLP_ERAI_series[i::12,:,:] - seasonal_cycle_SLP_ERAI[i,:,:]
    SST_ERAI_white_series[i::12,:,:] = SST_ERAI_series[i::12,:,:] - seasonal_cycle_SST_ERAI[i,:,:]

print '*******************************************************************'
print '****************** prepare variables for plot *********************'
print '*******************************************************************'
# dataset with seasonal cycle - time series
OMET_ORAS4_series = OMET_ORAS4.reshape(len(year_ORAS4)*len(month_ind),len(latitude_ORAS4))
OMET_GLORYS2V3_series = OMET_GLORYS2V3.reshape(len(year_GLORYS2V3)*len(month_ind),len(latitude_GLORYS2V3))
OMET_SODA3_series = OMET_SODA3.reshape(len(year_SODA3)*len(month_ind),len(latitude_SODA3))
# dataset without seasonal cycle - time series
OMET_ORAS4_white_series = OMET_ORAS4_white.reshape(len(year_ORAS4)*len(month_ind),len(latitude_ORAS4))
OMET_GLORYS2V3_white_series = OMET_GLORYS2V3_white.reshape(len(year_GLORYS2V3)*len(month_ind),len(latitude_GLORYS2V3))
OMET_SODA3_white_series = OMET_SODA3_white.reshape(len(year_SODA3)*len(month_ind),len(latitude_SODA3))
print '*******************************************************************'
print '***************************  Detrend  *****************************'
print '*******************************************************************'
####################################################
######      detrend - polynomial fitting      ######
####################################################
# detrend sea ice
poly_fit_SST_ERAI = np.zeros(SST_ERAI_white_series.shape,dtype=float)
for i in np.arange(len(latitude_ERAI_fields)):
    for j in np.arange(len(longitude_ERAI_fields)):
        polynomial = np.polyfit(np.arange(len(time_series)), SST_ERAI_white_series[:,i,j], 2)
        poly = np.poly1d(polynomial)
        poly_fit_SST_ERAI[:,i,j] = poly(np.arange(len(time_series)))

SST_ERAI_white_detrend_poly = np.zeros(SST_ERAI_white_series.shape,dtype=float)
SST_ERAI_white_detrend_poly = SST_ERAI_white_series - poly_fit_SST_ERAI

# detrend OMET
poly_fit_OMET_GLORYS2V3 = np.zeros(OMET_GLORYS2V3_white_series.shape,dtype=float)
for i in np.arange(len(latitude_GLORYS2V3)):
        polynomial_OMET = np.polyfit(np.arange(len(year_GLORYS2V3)*len(month_ind)), OMET_GLORYS2V3_white_series[:,i], 2)
        poly_OMET = np.poly1d(polynomial_OMET)
        poly_fit_OMET_GLORYS2V3[:,i] = poly_OMET(np.arange(len(year_GLORYS2V3)*len(month_ind)))

OMET_GLORYS2V3_white_detrend_series = np.zeros(OMET_GLORYS2V3_white_series.shape,dtype=float)
OMET_GLORYS2V3_white_detrend_series = OMET_GLORYS2V3_white_series - poly_fit_OMET_GLORYS2V3

# detrend OMET
poly_fit_OMET_ORAS4 = np.zeros(OMET_ORAS4_white_series.shape,dtype=float)
for i in np.arange(len(latitude_ORAS4)):
        polynomial_OMET = np.polyfit(np.arange(len(year_ORAS4)*len(month_ind)), OMET_ORAS4_white_series[:,i], 2)
        poly_OMET = np.poly1d(polynomial_OMET)
        poly_fit_OMET_ORAS4[:,i] = poly_OMET(np.arange(len(year_ORAS4)*len(month_ind)))

OMET_ORAS4_white_detrend_series = np.zeros(OMET_ORAS4_white_series.shape,dtype=float)
OMET_ORAS4_white_detrend_series = OMET_ORAS4_white_series - poly_fit_OMET_ORAS4

# detrend OMET
poly_fit_OMET_SODA3 = np.zeros(OMET_SODA3_white_series.shape,dtype=float)
for i in np.arange(len(latitude_SODA3)):
        polynomial_OMET = np.polyfit(np.arange(len(year_SODA3)*len(month_ind)), OMET_SODA3_white_series[:,i], 2)
        poly_OMET = np.poly1d(polynomial_OMET)
        poly_fit_OMET_SODA3[:,i] = poly_OMET(np.arange(len(year_SODA3)*len(month_ind)))

OMET_SODA3_white_detrend_series = np.zeros(OMET_SODA3_white_series.shape,dtype=float)
OMET_SODA3_white_detrend_series = OMET_SODA3_white_series - poly_fit_OMET_SODA3
print '*******************************************************************'
print '**********************     regression     *************************'
print '**********************   autocorrelation  *************************'
print '*******************************************************************'
OMET_ORAS4_norm = np.sum(OMET_ORAS4_white_detrend_series[lat_interest['ORAS4'][0]]**2)
auto_correlate = np.correlate(OMET_ORAS4_white_detrend_series[lat_interest['ORAS4'][0]],OMET_ORAS4_white_detrend_series[lat_interest['ORAS4'][0]],'full') / OMET_ORAS4_norm
# use only second half
auto_correlate = auto_correlate[len(auto_correlate)/2:]
plt.plot(auto_correlate)
plt.show()
print '*******************************************************************'
print '**********************     regression     *************************'
print '******************    original and anomalies   ********************'
print '*******************************************************************'

#***************************************************************************#
#*****************   regress of ERA Interim SST fields   *******************#
#*************      on OMET from ORAS4, GLORYS2V3, SODA3     ***************#
#***************************************************************************#
# create an array to store the correlation coefficient
slope_ERAI_fields = np.zeros((len(latitude_ERAI_fields),len(longitude_ERAI_fields)),dtype = float)
r_value_ERAI_fields = np.zeros((len(latitude_ERAI_fields),len(longitude_ERAI_fields)),dtype = float)
p_value_ERAI_fields= np.ones((len(latitude_ERAI_fields),len(longitude_ERAI_fields)),dtype = float)

latitude_ERAI_iris = iris.coords.DimCoord(latitude_ERAI_fields,standard_name='latitude',long_name='latitude',
                             var_name='lat',units='degrees')
longitude_ERAI_iris = iris.coords.DimCoord(longitude_ERAI_fields,standard_name='longitude',long_name='longitude',
                             var_name='lon',units='degrees')
# choose the coordinate system for Cube (for regrid module)
coord_sys = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)

#*****************             SST anomalies             *******************#

for c in np.arange(len(lat_interest_list)):
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      ORAS4      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
    # linear regress SST on OMET (anomalies)
    # plot correlation coefficient
    for i in np.arange(len(latitude_ERAI_fields)):
        for j in np.arange(len(longitude_ERAI_fields)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope_ERAI_fields[i,j],_,r_value_ERAI_fields[i,j],p_value_ERAI_fields[i,j],_ = stats.linregress(OMET_ORAS4_white_detrend_series[:,lat_interest['ORAS4'][c]],SST_ERAI_white_detrend_poly[:-24,i,j])
    p_value_ERAI_fields[SST_ERAI_mask==True] = 1.0
    # figsize works for the size of the map, not the entire figure
    fig4 = plt.figure()
    cube_ERAI = iris.cube.Cube(np.ma.masked_where(SST_ERAI_mask,r_value_ERAI_fields),long_name='Correlation coefficient between SST and OMET',
                               var_name='r',units='1',dim_coords_and_dims=[(latitude_ERAI_iris, 0), (longitude_ERAI_iris, 1)])
    cube_ERAI.coord('latitude').coord_system = coord_sys
    cube_ERAI.coord('longitude').coord_system = coord_sys
    # suptitle is the title for the figure
    #fig4.suptitle('Regression of SST Anomaly from ERA-Interim on OMET Anomaly of ORAS4 across %d N' % (lat_interest_list[c]) ,fontsize = 7,y=0.93)
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
    gl.xlabel_style = {'size': 9, 'color': 'gray'}
    gl.ylabel_style = {'size': 9, 'color': 'gray'}
    # Load a Cynthia Brewer palette.
    #brewer_cmap = mpl_cm.get_cmap('brewer_RdYlBu_11')
    cs = iplt.pcolormesh(cube_ERAI,cmap='coolwarm',vmin=-0.50,vmax=0.50)
    cbar = fig4.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.1,format="%.2f")
    cbar.set_ticks([-0.50, -0.25, 0, 0.25, 0.50])
    cbar.set_clim(-0.50, 0.50)
    cbar.ax.tick_params(labelsize = 9)
    cbar.set_label('Correlation coefficient',size = 12)
    # locate the indices of p_value matrix where error p<0.005 (99.5% confident)
    ii, jj = np.where(p_value_ERAI_fields<=0.005)
    # get the coordinate on the map (lon,lat) and plot scatter dots
    ax.scatter(longitude_ERAI_fields[jj],latitude_ERAI_fields[ii],transform=ccrs.Geodetic(),s=0.1,c='g',alpha=0.3) # alpha bleding factor with map
    # show and save plot
    plt.show()
    fig4.savefig(output_path + os.sep + "Regression_OMET_ORAS4_%dN_SST_ERAI_white_correlation_coef.jpeg" % (lat_interest_list[c]),dpi=400)
    plt.close(fig4)

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      GLORYS2V3      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
    for i in np.arange(len(latitude_ERAI_fields)):
        for j in np.arange(len(longitude_ERAI_fields)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope_ERAI_fields[i,j],_,r_value_ERAI_fields[i,j],p_value_ERAI_fields[i,j],_ = stats.linregress(OMET_GLORYS2V3_white_detrend_series[:,lat_interest['GLORYS2V3'][c]],SST_ERAI_white_detrend_poly[168:-24,i,j])
    p_value_ERAI_fields[SST_ERAI_mask==True] = 1.0
    # figsize works for the size of the map, not the entire figure
    fig5 = plt.figure()
    cube_ERAI = iris.cube.Cube(np.ma.masked_where(SST_ERAI_mask,r_value_ERAI_fields),long_name='Correlation coefficient between SST and OMET',
                               var_name='r',units='1',dim_coords_and_dims=[(latitude_ERAI_iris, 0), (longitude_ERAI_iris, 1)])
    cube_ERAI.coord('latitude').coord_system = coord_sys
    cube_ERAI.coord('longitude').coord_system = coord_sys
    # suptitle is the title for the figure
    #fig5.suptitle('Regression of SST Anomaly from ERA-Interim on OMET Anomaly of GLORYS2V3 across %d N' % (lat_interest_list[c]) ,fontsize = 7,y=0.93)
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
    gl.xlabel_style = {'size': 9, 'color': 'gray'}
    gl.ylabel_style = {'size': 9, 'color': 'gray'}
    cs = iplt.pcolormesh(cube_ERAI,cmap='coolwarm',vmin=-0.50,vmax=0.50)
    cbar = fig5.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.1,format="%.2f")
    cbar.set_ticks([-0.50, -0.25, 0, 0.25, 0.50])
    cbar.set_clim(-0.50, 0.50)
    cbar.ax.tick_params(labelsize = 9)
    cbar.set_label('Correlation coefficient',size = 12)
    # locate the indices of p_value matrix where error p<0.005 (99.5% confident)
    ii, jj = np.where(p_value_ERAI_fields<=0.005)
    # get the coordinate on the map (lon,lat) and plot scatter dots
    ax.scatter(longitude_ERAI_fields[jj],latitude_ERAI_fields[ii],transform=ccrs.Geodetic(),s=0.1,c='g',alpha=0.3) # alpha bleding factor with map
    # show and save plot
    plt.show()
    fig5.savefig(output_path + os.sep + "Regression_OMET_GLORYS2V3_%dN_SST_ERAI_white_correlation_coef.jpeg" % (lat_interest_list[c]),dpi=400)
    plt.close(fig5)

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@       SODA3      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
    for i in np.arange(len(latitude_ERAI_fields)):
        for j in np.arange(len(longitude_ERAI_fields)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope_ERAI_fields[i,j],_,r_value_ERAI_fields[i,j],p_value_ERAI_fields[i,j],_ = stats.linregress(OMET_SODA3_white_detrend_series[:,lat_interest['SODA3'][c]],SST_ERAI_white_detrend_poly[12:-12,i,j])
    p_value_ERAI_fields[SST_ERAI_mask==True] = 1.0
    # figsize works for the size of the map, not the entire figure
    fig6 = plt.figure()
    cube_ERAI = iris.cube.Cube(np.ma.masked_where(SST_ERAI_mask,r_value_ERAI_fields),long_name='Correlation coefficient between SST and OMET',
                               var_name='r',units='1',dim_coords_and_dims=[(latitude_ERAI_iris, 0), (longitude_ERAI_iris, 1)])
    cube_ERAI.coord('latitude').coord_system = coord_sys
    cube_ERAI.coord('longitude').coord_system = coord_sys
    # suptitle is the title for the figure
    #fig6.suptitle('Regression of SST Anomaly from ERA-Interim on OMET Anomaly of SODA3 across %d N' % (lat_interest_list[c]) ,fontsize = 7,y=0.93)
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
    gl.xlabel_style = {'size': 9, 'color': 'gray'}
    gl.ylabel_style = {'size': 9, 'color': 'gray'}
    cs = iplt.pcolormesh(cube_ERAI,cmap='coolwarm',vmin=-0.50,vmax=0.50)
    cbar = fig6.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.1,format="%.2f")
    cbar.set_ticks([-0.50, -0.25, 0, 0.25, 0.50])
    cbar.set_clim(-0.50, 0.50)
    cbar.ax.tick_params(labelsize = 9)
    cbar.set_label('Correlation coefficient',size = 12)
    # locate the indices of p_value matrix where error p<0.005 (99.5% confident)
    ii, jj = np.where(p_value_ERAI_fields<=0.005)
    # get the coordinate on the map (lon,lat) and plot scatter dots
    ax.scatter(longitude_ERAI_fields[jj],latitude_ERAI_fields[ii],transform=ccrs.Geodetic(),s=0.1,c='g',alpha=0.3) # alpha bleding factor with map
    # show and save plot
    plt.show()
    fig6.savefig(output_path + os.sep + "Regression_OMET_SODA3_%dN_SST_ERAI_white_correlation_coef.jpeg" % (lat_interest_list[c]),dpi=400)
    plt.close(fig6)

#*****************             SLP anomalies             *******************#

#***************************************************************************#
#*****************   regress of ERA Interim SLP fields   *******************#
#*************     on OMET from ORAS4, GLORYS2V3, SODA3      ***************#
#***************************************************************************#

#*****************             SLP anomalies             *******************#
for c in np.arange(len(lat_interest_list)):
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      ORAS4      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
    # linear regress SLP on OMET (anomalies)
    # plot correlation coefficient
    for i in np.arange(len(latitude_ERAI_fields)):
        for j in np.arange(len(longitude_ERAI_fields)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope_ERAI_fields[i,j],_,r_value_ERAI_fields[i,j],p_value_ERAI_fields[i,j],_ = stats.linregress(OMET_ORAS4_white_detrend_series[:,lat_interest['ORAS4'][c]],SLP_ERAI_white_series[:-24,i,j])
    # figsize works for the size of the map, not the entire figure
    fig7 = plt.figure()
    cube_ERAI = iris.cube.Cube(r_value_ERAI_fields,long_name='Correlation coefficient between SLP and OMET',
                               var_name='r',units='1',dim_coords_and_dims=[(latitude_ERAI_iris, 0), (longitude_ERAI_iris, 1)])
    cube_ERAI.coord('latitude').coord_system = coord_sys
    cube_ERAI.coord('longitude').coord_system = coord_sys
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_global()
    #ax.set_aspect('auto')
    ax.set_aspect('1.0')
    ax.coastlines()
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,linewidth=1, color='gray', alpha=0.5,linestyle='--')
    gl.xlabels_top = False
    # use of formatter (fixed), only after this the style setup will work
    gl.xlabel_style = {'size': 9, 'color': 'gray'}
    gl.ylabel_style = {'size': 9, 'color': 'gray'}
    # Load a Cynthia Brewer palette.
    #brewer_cmap = mpl_cm.get_cmap('brewer_RdYlBu_11')
    cs = iplt.pcolormesh(cube_ERAI,cmap='coolwarm',vmin=-0.50,vmax=0.50)
    cbar = fig7.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.1,format="%.2f")
    cbar.set_ticks([-0.50, -0.25, 0, 0.25, 0.50])
    cbar.set_clim(-0.50, 0.50)
    cbar.ax.tick_params(labelsize = 9)
    cbar.set_label('Correlation coefficient',size = 12)
    # locate the indices of p_value matrix where error p<0.005 (99.5% confident)
    ii, jj = np.where(p_value_ERAI_fields<=0.005)
    # get the coordinate on the map (lon,lat) and plot scatter dots
    ax.scatter(longitude_ERAI_fields[jj],latitude_ERAI_fields[ii],transform=ccrs.Geodetic(),s=0.1,c='g',alpha=0.3) # alpha bleding factor with map
    # show and save plot
    plt.show()
    fig7.savefig(output_path + os.sep + "Regression_OMET_ORAS4_%dN_SLP_ERAI_white_correlation_coef.jpeg" % (lat_interest_list[c]),dpi=400)
    plt.close(fig7)
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      GLORYS2V3      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
    for i in np.arange(len(latitude_ERAI_fields)):
        for j in np.arange(len(longitude_ERAI_fields)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope_ERAI_fields[i,j],_,r_value_ERAI_fields[i,j],p_value_ERAI_fields[i,j],_ = stats.linregress(OMET_GLORYS2V3_white_detrend_series[:,lat_interest['GLORYS2V3'][c]],SLP_ERAI_white_series[168:-24,i,j])
    # figsize works for the size of the map, not the entire figure
    fig8 = plt.figure()
    cube_ERAI = iris.cube.Cube(r_value_ERAI_fields,long_name='Correlation coefficient between SLP and OMET',
                               var_name='r',units='1',dim_coords_and_dims=[(latitude_ERAI_iris, 0), (longitude_ERAI_iris, 1)])
    cube_ERAI.coord('latitude').coord_system = coord_sys
    cube_ERAI.coord('longitude').coord_system = coord_sys
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
    gl.xlabel_style = {'size': 9, 'color': 'gray'}
    gl.ylabel_style = {'size': 9, 'color': 'gray'}
    cs = iplt.pcolormesh(cube_ERAI,cmap='coolwarm',vmin=-0.50,vmax=0.50)
    cbar = fig8.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.1,format="%.2f")
    cbar.set_ticks([-0.50, -0.25, 0, 0.25, 0.50])
    cbar.set_clim(-0.50, 0.50)
    cbar.ax.tick_params(labelsize = 9)
    cbar.set_label('Correlation coefficient',size = 12)
    # locate the indices of p_value matrix where error p<0.005 (99.5% confident)
    ii, jj = np.where(p_value_ERAI_fields<=0.005)
    # get the coordinate on the map (lon,lat) and plot scatter dots
    ax.scatter(longitude_ERAI_fields[jj],latitude_ERAI_fields[ii],transform=ccrs.Geodetic(),s=0.1,c='g',alpha=0.3) # alpha bleding factor with map
    # show and save plot
    plt.show()
    fig8.savefig(output_path + os.sep + "Regression_OMET_GLORYS2V3_%dN_SLP_ERAI_white_correlation_coef.jpeg" % (lat_interest_list[c]),dpi=400)
    plt.close(fig8)

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@       SODA3      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
    for i in np.arange(len(latitude_ERAI_fields)):
        for j in np.arange(len(longitude_ERAI_fields)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope_ERAI_fields[i,j],_,r_value_ERAI_fields[i,j],p_value_ERAI_fields[i,j],_ = stats.linregress(OMET_SODA3_white_detrend_series[:,lat_interest['SODA3'][c]],SLP_ERAI_white_series[12:-12,i,j])
    # figsize works for the size of the map, not the entire figure
    fig9 = plt.figure()
    cube_ERAI = iris.cube.Cube(r_value_ERAI_fields,long_name='Correlation coefficient between SLP and OMET',
                               var_name='r',units='1',dim_coords_and_dims=[(latitude_ERAI_iris, 0), (longitude_ERAI_iris, 1)])
    cube_ERAI.coord('latitude').coord_system = coord_sys
    cube_ERAI.coord('longitude').coord_system = coord_sys
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
    gl.xlabel_style = {'size': 9, 'color': 'gray'}
    gl.ylabel_style = {'size': 9, 'color': 'gray'}
    cs = iplt.pcolormesh(cube_ERAI,cmap='coolwarm',vmin=-0.50,vmax=0.50)
    cbar = fig9.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.1,format="%.2f")
    cbar.set_ticks([-0.50, -0.25, 0, 0.25, 0.50])
    cbar.set_clim(-0.50, 0.50)
    cbar.ax.tick_params(labelsize = 9)
    cbar.set_label('Correlation coefficient',size = 12)
    # locate the indices of p_value matrix where error p<0.005 (99.5% confident)
    ii, jj = np.where(p_value_ERAI_fields<=0.005)
    # get the coordinate on the map (lon,lat) and plot scatter dots
    ax.scatter(longitude_ERAI_fields[jj],latitude_ERAI_fields[ii],transform=ccrs.Geodetic(),s=0.1,c='g',alpha=0.3) # alpha bleding factor with map
    # show and save plot
    plt.show()
    fig9.savefig(output_path + os.sep + "Regression_OMET_SODA3_%dN_SLP_ERAI_white_correlation_coef.jpeg" % (lat_interest_list[c]),dpi=400)
    plt.close(fig9)

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
