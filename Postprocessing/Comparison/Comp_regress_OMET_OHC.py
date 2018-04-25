#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : Regress ocean heat content on oceanic meridional energy transport (ORAS4,GLORYS2V3,SODA3)
Author          : Yang Liu
Date            : 2018.04.21
Last Update     : 2018.04.21
Description     : The code aims to compare OHC computed from different reanalysis
                  products and the regress OHC on OMET to see the connection of energy
                  transport with major climate patterns. All those OHC and OMET are
                  calculated from reanalysis datasets. In this case, it includes GLORYS2V3
                  from Mercator Ocean, ORAS4 from ECMWF, and SODA3 from University
                  of Maryland & TAMU.

                  The ocean reanalysis included here are all driven by ERA-Interim.

                  The differnce, obtained from OMET at sections (20N - 80N), gives that it
                  is better to check the spatial distribution from 1995 to 2003.
Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, sys, matplotlib
variables       : Meridional Energy Transport           E         [Tera-Watt]
                  Ocean Heat Content                    OHC       [Joule]
Caveat!!        : Time range
                  GLORYS2V3   1993 - 2014
                  ORAS4       1958(1979 in use) - 2014
                  SODA3       1980 - 2015

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
datapath_OMET_ORAS4 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ORAS4/postprocessing'
datapath_OMET_GLORYS2V3 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/GLORYS2V3/postprocessing'
datapath_OMET_SODA3 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/SODA3/postprocessing'
# target fields for regression
datapath_OHC_ORAS4 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ORAS4/statistics'
datapath_OHC_GLORYS2V3 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/GLORYS2V3/statistics'
datapath_OHC_SODA3 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/SODA3/statistics'
# mask path
datapath_mask_ORAS4 ='/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ORAS4'
datapath_mask_GLORYS2V3 ='/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/GLORYS2V3'
datapath_mask_SODA3 ='/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/SODA3'
# specify output path for figures
output_path_regress = '/home/yang/NLeSC/Computation_Modeling/BlueAction/OMET/Comparison/regress/OHC'
#output_path_comp = '/home/yang/NLeSC/Computation_Modeling/BlueAction/OMET/Comparison/OHC'
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
lat_interest_list = [20,30,40,50,60,70,80]
# after cut
lat_interest['ORAS4_cut'] = [lat_ORAS4_20_cut,lat_ORAS4_30_cut,lat_ORAS4_40_cut,lat_ORAS4_50_cut,lat_ORAS4_60_cut,lat_ORAS4_70_cut,lat_ORAS4_80_cut]
lat_interest['GLORYS2V3_cut'] = [lat_GLORYS2V3_20_cut,lat_GLORYS2V3_30_cut,lat_GLORYS2V3_40_cut,lat_GLORYS2V3_50_cut,lat_GLORYS2V3_60_cut,lat_GLORYS2V3_70_cut,lat_GLORYS2V3_80_cut]
lat_interest['SODA3_cut'] = [lat_SODA3_20_cut,lat_SODA3_30_cut,lat_SODA3_40_cut,lat_SODA3_50_cut,lat_SODA3_60_cut,lat_SODA3_70_cut,lat_SODA3_80_cut]
lat_interest['ORAS4'] = [lat_ORAS4_20,lat_ORAS4_30,lat_ORAS4_40,lat_ORAS4_50,lat_ORAS4_60,lat_ORAS4_70,lat_ORAS4_80]
lat_interest['GLORYS2V3'] = [lat_GLORYS2V3_20,lat_GLORYS2V3_30,lat_GLORYS2V3_40,lat_GLORYS2V3_50,lat_GLORYS2V3_60,lat_GLORYS2V3_70,lat_GLORYS2V3_80]
lat_interest['SODA3'] = [lat_SODA3_20,lat_SODA3_30,lat_SODA3_40,lat_SODA3_50,lat_SODA3_60,lat_SODA3_70,lat_SODA3_80]
print '*******************************************************************'
print '*********************** extract variables *************************'
print '*******************************************************************'
# ORCA1_z42 grid infor (Madec and Imbard 1996)
ji_1 = 362
jj_1 = 292
level_1 = 42

# ORCA025_z75 grid infor (Madec and Imbard 1996)
ji_025 = 1440
jj_025 = 1021
level_025 = 75

# MOM5_z50 grid info
ji_5 = 1440
jj_5 = 1070
level_5 = 50
# OMET
dataset_OMET_GLORYS2V3 = Dataset(datapath_OMET_GLORYS2V3 + os.sep + 'GLORYS2V3_model_monthly_orca025_E_zonal_int.nc')
dataset_OMET_ORAS4 = Dataset(datapath_OMET_ORAS4 + os.sep + 'oras4_model_monthly_orca1_E_zonal_int.nc')
dataset_OMET_SODA3 = Dataset(datapath_OMET_SODA3 + os.sep + 'OMET_SODA3_model_5daily_1980_2015_E_zonal_int.nc')
# OHC
dataset_OHC_GLORYS2V3 = Dataset(datapath_OHC_GLORYS2V3 + os.sep + 'GLORYS2V3_model_monthly_orca025_OHC_point.nc')
dataset_OHC_ORAS4 = Dataset(datapath_OHC_ORAS4 + os.sep + 'oras4_model_monthly_orca1_OHC_point.nc')
dataset_OHC_SODA3 = Dataset(datapath_OHC_SODA3 + os.sep + 'OMET_SODA3_model_5daily_1980_2015_OHC.nc')
# mask
dataset_mask_ORAS4 = Dataset(datapath_mask_ORAS4 + os.sep + 'mesh_mask.nc')
dataset_mask_GLORYS2V3 = Dataset(datapath_mask_GLORYS2V3 + os.sep + 'G2V3_mesh_mask_myocean.nc')
dataset_mask_SODA3 = Dataset(datapath_mask_SODA3 + os.sep + 'topog.nc')
# OMET
OMET_ORAS4 = dataset_OMET_ORAS4.variables['E'][21:,:,180:]/1000         # start from 1979
OMET_GLORYS2V3 = dataset_OMET_GLORYS2V3.variables['E'][:,:,579:]/1000   # start from 1993
OMET_SODA3 = dataset_OMET_SODA3.variables['E'][:,:,569:]/1000           # start from 1980
# OHC
# entire column (globe) unit: Peta joule
OHC_glo_vert_ORAS4 = dataset_OHC_ORAS4.variables['OHC_glo_vert'][21:,:,:,:] / 1E+3 # start from 1979
OHC_glo_vert_GLORYS2V3 = dataset_OHC_GLORYS2V3.variables['OHC_glo_vert'][:] / 1E+3 # start from 1993
OHC_glo_vert_SODA3 = dataset_OHC_SODA3.variables['OHC_glo_vert'][:] / 1E+3        # start from 1980
# year
year_ORAS4 = dataset_OMET_ORAS4.variables['year'][21:]         # from 1979 to 2014
year_GLORYS2V3 = dataset_OMET_GLORYS2V3.variables['year'][:]   # from 1993 to 2014
year_SODA3 = dataset_OMET_SODA3.variables['year'][:]           # from 1980 to 2015
# nominal latitude
latitude_ORAS4 = dataset_OMET_ORAS4.variables['latitude_aux'][180:]
latitude_GLORYS2V3 = dataset_OMET_GLORYS2V3.variables['latitude_aux'][579:]
latitude_SODA3 = dataset_OMET_SODA3.variables['latitude_aux'][569:]
# latitude
lat_ORAS4_ORCA = dataset_OHC_ORAS4.variables['gphit'][:]
lat_GLORYS2V3_ORCA = dataset_OHC_GLORYS2V3.variables['gphit'][:]
lat_SODA3_MOM = dataset_OHC_SODA3.variables['y_T'][:]
# longitude
lon_ORAS4_ORCA = dataset_OHC_ORAS4.variables['glamt'][:]
lon_GLORYS2V3_ORCA = dataset_OHC_GLORYS2V3.variables['glamt'][:]
lon_SODA3_MOM = dataset_OHC_SODA3.variables['x_T'][:]
# mask
mask_ORAS4 = dataset_mask_ORAS4.variables['vmask'][0,0,:,:]
mask_GLORYS2V3 = dataset_mask_GLORYS2V3.variables['vmask'][0,0,:,:]
mask_SODA3 = dataset_mask_SODA3.variables['wet_c'][:]
print '*******************************************************************'
print '*************************** whitening *****************************'
print '*******************************************************************'
month_ind = np.arange(12)
# seasonal cycle of OMET
seansonal_cycle_OMET_ORAS4 = np.mean(OMET_ORAS4,axis=0)
seansonal_cycle_OMET_GLORYS2V3 = np.mean(OMET_GLORYS2V3,axis=0)
seansonal_cycle_OMET_SODA3 = np.mean(OMET_SODA3,axis=0)
# seasonal cycle of OHC for the globe
seansonal_cycle_OHC_glo_vert_ORAS4 = np.mean(OHC_glo_vert_ORAS4,axis=0)
seansonal_cycle_OHC_glo_vert_GLORYS2V3 = np.mean(OHC_glo_vert_GLORYS2V3,axis=0)
seansonal_cycle_OHC_glo_vert_SODA3 = np.mean(OHC_glo_vert_SODA3,axis=0)

OMET_ORAS4_white = np.zeros(OMET_ORAS4.shape,dtype=float)
OMET_GLORYS2V3_white = np.zeros(OMET_GLORYS2V3.shape,dtype=float)
OMET_SODA3_white = np.zeros(OMET_SODA3.shape,dtype=float)

OHC_glo_vert_ORAS4_white = np.zeros(OHC_glo_vert_ORAS4.shape,dtype=float)
OHC_glo_vert_GLORYS2V3_white = np.zeros(OHC_glo_vert_GLORYS2V3.shape,dtype=float)
OHC_glo_vert_SODA3_white = np.zeros(OHC_glo_vert_SODA3.shape,dtype=float)

for i in np.arange(len(year_ORAS4)):
    for j in month_ind:
        OMET_ORAS4_white[i,j,:] = OMET_ORAS4[i,j,:] - seansonal_cycle_OMET_ORAS4[j,:]
        OHC_glo_vert_ORAS4_white[i,j,:,:] = OHC_glo_vert_ORAS4[i,j,:,:] - seansonal_cycle_OHC_glo_vert_ORAS4[j,:,:]

for i in np.arange(len(year_GLORYS2V3)):
    for j in month_ind:
        OMET_GLORYS2V3_white[i,j,:] = OMET_GLORYS2V3[i,j,:] - seansonal_cycle_OMET_GLORYS2V3[j,:]
        OHC_glo_vert_GLORYS2V3_white[i,j,:,:] = OHC_glo_vert_GLORYS2V3[i,j,:,:] - seansonal_cycle_OHC_glo_vert_GLORYS2V3[j,:,:]

for i in np.arange(len(year_SODA3)):
    for j in month_ind:
        OMET_SODA3_white[i,j,:] = OMET_SODA3[i,j,:] - seansonal_cycle_OMET_SODA3[j,:]
        OHC_glo_vert_SODA3_white[i,j,:,:] = OHC_glo_vert_SODA3[i,j,:,:] - seansonal_cycle_OHC_glo_vert_SODA3[j,:,:]

print '*******************************************************************'
print '****************** prepare variables for plot *********************'
print '*******************************************************************'
# OMET with seasonal cycle - time series
OMET_ORAS4_series = OMET_ORAS4.reshape(len(year_ORAS4)*len(month_ind),len(latitude_ORAS4))
del OMET_ORAS4
OMET_GLORYS2V3_series = OMET_GLORYS2V3.reshape(len(year_GLORYS2V3)*len(month_ind),len(latitude_GLORYS2V3))
del OMET_GLORYS2V3
OMET_SODA3_series = OMET_SODA3.reshape(len(year_SODA3)*len(month_ind),len(latitude_SODA3))
del OMET_SODA3
# OMET without seasonal cycle - time series
OMET_ORAS4_white_series = OMET_ORAS4_white.reshape(len(year_ORAS4)*len(month_ind),len(latitude_ORAS4))
del OMET_ORAS4_white
OMET_GLORYS2V3_white_series = OMET_GLORYS2V3_white.reshape(len(year_GLORYS2V3)*len(month_ind),len(latitude_GLORYS2V3))
del OMET_GLORYS2V3_white
OMET_SODA3_white_series = OMET_SODA3_white.reshape(len(year_SODA3)*len(month_ind),len(latitude_SODA3))
del OMET_SODA3_white
# OHC with seasonal cycle - time series
OHC_glo_vert_ORAS4_series = OHC_glo_vert_ORAS4.reshape(len(year_ORAS4)*len(month_ind),jj_1,ji_1)
del OHC_glo_vert_ORAS4
OHC_glo_vert_GLORYS2V3_series = OHC_glo_vert_GLORYS2V3.reshape(len(year_GLORYS2V3)*len(month_ind),jj_025,ji_025)
del OHC_glo_vert_GLORYS2V3
OHC_glo_vert_SODA3_series = OHC_glo_vert_SODA3.reshape(len(year_SODA3)*len(month_ind),jj_5,ji_5)
del OHC_glo_vert_SODA3
# OHC without seasonal cycle - time series
OHC_glo_vert_ORAS4_white_series = OHC_glo_vert_ORAS4_white.reshape(len(year_ORAS4)*len(month_ind),jj_1,ji_1)
del OHC_glo_vert_ORAS4_white
OHC_glo_vert_GLORYS2V3_white_series = OHC_glo_vert_GLORYS2V3_white.reshape(len(year_GLORYS2V3)*len(month_ind),jj_025,ji_025)
del OHC_glo_vert_GLORYS2V3_white
OHC_glo_vert_SODA3_white_series = OHC_glo_vert_SODA3_white.reshape(len(year_SODA3)*len(month_ind),jj_5,ji_5)
del OHC_glo_vert_SODA3_white
print '*******************************************************************'
print '********************** Running mean/sum ***************************'
print '*******************************************************************'
# running mean is calculated on time series
# define the running window for the running mean
#window = 12 # in month
#window = 60 # in month
#window = 120 # in month
#window = 180 # in month
print '*******************************************************************'
print '**********************     regression     *************************'
print '******************    original and anomalies   ********************'
print '*******************************************************************'

#***************************************************************************#
#*****************      regress of OHC ORAS4 fields      *******************#
#*****************          on OMET from ORAS4           *******************#
#***************************************************************************#

# create an array to store the correlation coefficient
slope_fields = np.zeros((jj_1,ji_1),dtype = float)
r_value_fields = np.zeros((jj_1,ji_1),dtype = float)
p_value_fields= np.zeros((jj_1,ji_1),dtype = float)

latitude_iris = iris.coords.AuxCoord(lat_ORAS4_ORCA,standard_name='latitude',long_name='latitude',
                             var_name='lat',units='degrees')
longitude_iris = iris.coords.AuxCoord(lon_ORAS4_ORCA,standard_name='longitude',long_name='longitude',
                             var_name='lon',units='degrees')
# choose the coordinate system for Cube (for regrid module)
coord_sys = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)
for c in np.arange(len(lat_interest_list)):
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      ORAS4      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
    # linear regress OHC on OMET (anomalies)
    # plot regression coefficient
    for i in np.arange(jj_1):
        for j in np.arange(ji_1):
            # return value: slope, intercept, r_value, p_value, stderr
            slope_fields[i,j],_,r_value_fields[i,j],p_value_fields[i,j],_ = stats.linregress(OMET_ORAS4_white_series[:,lat_interest['ORAS4_cut'][c]],OHC_glo_vert_ORAS4_white_series[:,i,j])
    # figsize works for the size of the map, not the entire figure
    fig1 = plt.figure()
    cube = iris.cube.Cube(np.ma.masked_where(mask_ORAS4, r_value_fields), long_name='Regression coefficient of OHC and OMET',
                               var_name='r',units='1',aux_coords_and_dims=[(latitude_iris, (0,1)), (longitude_iris, (0,1))])
    cube.coord('latitude').coord_system = coord_sys
    cube.coord('longitude').coord_system = coord_sys
    cube_regrid, extent = iris.analysis.cartography.project(cube, ccrs.PlateCarree(), nx=720, ny=360)
    # suptitle is the title for the figure
    fig1.suptitle('Regression of OHC Anomaly on OMET Anomaly of ORAS4 across %d N' % (lat_interest_list[c]) ,fontsize = 7,y=0.93)
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
    cs = iplt.pcolormesh(cube_regrid,cmap='coolwarm',vmin=-0.10,vmax=0.10)
    cbar = fig1.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.1,format="%.2f")
    #cbar.set_ticks([-0.50, -0.40, -0.30, -0.20, -0.10, 0, 0.10, 0.20, 0.30, 0.40, 0.50])
    #cbar.set_clim(-0.50, 0.50)
    cbar.ax.tick_params(labelsize = 6)
    cbar.set_label('Correlation coefficient',size = 6)
    # locate the indices of p_value matrix where error p<0.05 (99.5% confident)
    ii, jj = np.where(p_value_fields<=0.05)
    # get the coordinate on the map (lon,lat) and plot scatter dots
    ax.scatter(lon_ORAS4_ORCA[ii,jj],lat_ORAS4_ORCA[ii,jj],transform=ccrs.Geodetic(),s=0.1,c='g',alpha=0.3) # alpha bleding factor with map
    # show and save plot
    plt.show()
    fig1.savefig(output_path_regress + os.sep + 'OMET_ORAS4_OHC_ORAS4' + os.sep + "Regression_OMET_ORAS4_%dN_OHC_white_regression_coef.jpeg" % (lat_interest_list[c]),dpi=300)
    plt.close(fig1)
#***************************************************************************#
#*****************    regress of OHC GLORYS2V3 fields    *******************#
#*****************        on OMET from GLORYS2V3         *******************#
#***************************************************************************#
# create an array to store the correlation coefficient
slope_fields = np.zeros((jj_025,ji_025),dtype = float)
r_value_fields = np.zeros((jj_025,ji_025),dtype = float)
p_value_fields= np.zeros((jj_025,ji_025),dtype = float)

latitude_iris = iris.coords.AuxCoord(lat_GLORYS2V3_ORCA,standard_name='latitude',long_name='latitude',
                             var_name='lat',units='degrees')
longitude_iris = iris.coords.AuxCoord(lon_GLORYS2V3_ORCA,standard_name='longitude',long_name='longitude',
                             var_name='lon',units='degrees')
# choose the coordinate system for Cube (for regrid module)
coord_sys = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)
for c in np.arange(len(lat_interest_list)):
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      GLORYS2V3      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
    # linear regress OHC on OMET (anomalies)
    # plot regression coefficient
    for i in np.arange(jj_025):
        for j in np.arange(ji_025):
            # return value: slope, intercept, r_value, p_value, stderr
            slope_fields[i,j],_,r_value_fields[i,j],p_value_fields[i,j],_ = stats.linregress(OMET_GLORYS2V3_white_series[:,lat_interest['GLORYS2V3_cut'][c]],OHC_glo_vert_GLORYS2V3_white_series[:,i,j])
    # figsize works for the size of the map, not the entire figure
    fig2 = plt.figure()
    cube = iris.cube.Cube(np.ma.masked_where(mask_GLORYS2V3, r_value_fields), long_name='Regression coefficient of OHC and OMET',
                               var_name='r',units='1',aux_coords_and_dims=[(latitude_iris, (0,1)), (longitude_iris, (0,1))])
    cube.coord('latitude').coord_system = coord_sys
    cube.coord('longitude').coord_system = coord_sys
    cube_regrid, extent = iris.analysis.cartography.project(cube, ccrs.PlateCarree(), nx=1440, ny=1020)
    # suptitle is the title for the figure
    fig2.suptitle('Regression of OHC Anomaly on OMET Anomaly of GLORYS2V3 across %d N' % (lat_interest_list[c]) ,fontsize = 7,y=0.93)
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
    cs = iplt.pcolormesh(cube_regrid,cmap='coolwarm',vmin=-0.10,vmax=0.10)
    cbar = fig2.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.1,format="%.2f")
    #cbar.set_ticks([-0.50, -0.40, -0.30, -0.20, -0.10, 0, 0.10, 0.20, 0.30, 0.40, 0.50])
    #cbar.set_clim(-0.50, 0.50)
    cbar.ax.tick_params(labelsize = 6)
    cbar.set_label('Correlation coefficient',size = 6)
    #cbar.set_label('Regression coefficient (Peta Watt / Peta Joule)',size = 6)
    # locate the indices of p_value matrix where error p<0.05 (99.5% confident)
    ii, jj = np.where(p_value_fields<=0.05)
    # get the coordinate on the map (lon,lat) and plot scatter dots
    ax.scatter(lon_GLORYS2V3_ORCA[ii,jj],lat_GLORYS2V3_ORCA[ii,jj],transform=ccrs.Geodetic(),s=0.1,c='g',alpha=0.3) # alpha bleding factor with map
    # show and save plot
    plt.show()
    fig2.savefig(output_path_regress + os.sep + 'OMET_GLORYS2V3_OHC_GLORYS2V3' + os.sep + "Regression_OMET_GLORYS2V3_%dN_OHC_white_correlation_coef.jpeg" % (lat_interest_list[c]),dpi=300)
    plt.close(fig2)
#***************************************************************************#
#*****************      regress of OHC SODA3 fields      *******************#
#*****************          on OMET from SODA3           *******************#
#***************************************************************************#
# create an array to store the correlation coefficient
slope_fields = np.zeros((jj_5,ji_5),dtype = float)
r_value_fields = np.zeros((jj_5,ji_5),dtype = float)
p_value_fields= np.zeros((jj_5,ji_5),dtype = float)

latitude_iris = iris.coords.AuxCoord(lat_SODA3_MOM,standard_name='latitude',long_name='latitude',
                             var_name='lat',units='degrees')
longitude_iris = iris.coords.AuxCoord(lon_SODA3_MOM,standard_name='longitude',long_name='longitude',
                             var_name='lon',units='degrees')
# choose the coordinate system for Cube (for regrid module)
coord_sys = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)
for c in np.arange(len(lat_interest_list)):
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      SODA3      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
    # linear regress OHC on OMET (anomalies)
    # plot regression coefficient
    for i in np.arange(jj_5):
        for j in np.arange(ji_5):
            # return value: slope, intercept, r_value, p_value, stderr
            slope_fields[i,j],_,r_value_fields[i,j],p_value_fields[i,j],_ = stats.linregress(OMET_SODA3_white_series[:,lat_interest['SODA3_cut'][c]],OHC_glo_vert_SODA3_white_series[:,i,j])
    # figsize works for the size of the map, not the entire figure
    fig3 = plt.figure()
    cube = iris.cube.Cube(np.ma.masked_where(mask_SODA3, r_value_fields), long_name='Regression coefficient of OHC and OMET',
                               var_name='r',units='1',aux_coords_and_dims=[(latitude_iris, (0,1)), (longitude_iris, (0,1))])
    cube.coord('latitude').coord_system = coord_sys
    cube.coord('longitude').coord_system = coord_sys
    cube_regrid, extent = iris.analysis.cartography.project(cube, ccrs.PlateCarree(), nx=1440, ny=1020)
    # suptitle is the title for the figure
    fig3.suptitle('Regression of OHC Anomaly on OMET Anomaly of SODA3 across %d N' % (lat_interest_list[c]) ,fontsize = 7,y=0.93)
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
    cs = iplt.pcolormesh(cube_regrid,cmap='coolwarm',vmin=-0.10,vmax=0.10)
    cbar = fig3.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.1,format="%.2f")
    #cbar.set_ticks([-0.50, -0.40, -0.30, -0.20, -0.10, 0, 0.10, 0.20, 0.30, 0.40, 0.50])
    #cbar.set_clim(-0.50, 0.50)
    cbar.ax.tick_params(labelsize = 6)
    cbar.set_label('Correlation coefficient',size = 6)
    #cbar.set_label('Regression coefficient (Peta Watt / Peta Joule)',size = 6)
    # locate the indices of p_value matrix where error p<0.05 (99.5% confident)
    ii, jj = np.where(p_value_fields<=0.05)
    # get the coordinate on the map (lon,lat) and plot scatter dots
    ax.scatter(lon_SODA3_MOM[ii,jj],lat_SODA3_MOM[ii,jj],transform=ccrs.Geodetic(),s=0.1,c='g',alpha=0.3) # alpha bleding factor with map
    # show and save plot
    plt.show()
    fig3.savefig(output_path_regress + os.sep + 'OMET_SODA3_OHC_SODA3' + os.sep + "Regression_OMET_SODA3_%dN_OHC_white_correlation_coef.jpeg" % (lat_interest_list[c]),dpi=300)
    plt.close(fig3)

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
