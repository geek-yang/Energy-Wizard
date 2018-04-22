#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : Compare Ocean Heat Content (ORAS4,GLORYS2V3,SODA3)
Author          : Yang Liu
Date            : 2018.04.21
Last Update     : 2018.04.21
Description     : The code aims to compare OHC computed from different reanalysis
                  products. The OHC are calculated from reanalysis datasets. In this case,
                  it includes GLORYS2V3 from Mercator Ocean, ORAS4 from ECMWF, and SODA3
                  from University of Maryland & TAMU.
Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, sys, matplotlib
variables       : Ocean Heat Content                    OHC       [Joule]
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
# target fields for regression
datapath_OHC_ORAS4 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ORAS4/statistics'
datapath_OHC_GLORYS2V3 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/GLORYS2V3/statistics'
datapath_OHC_SODA3 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/SODA3/statistics'
# mask path
datapath_mask_ORAS4 ='/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ORAS4'
datapath_mask_GLORYS2V3 ='/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/GLORYS2V3'
datapath_mask_SODA3 ='/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/SODA3'
# specify output path for figures
output_path_comp = '/home/yang/NLeSC/Computation_Modeling/BlueAction/OMET/Comparison/OHC'
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
# OHC
dataset_OHC_GLORYS2V3 = Dataset(datapath_OHC_GLORYS2V3 + os.sep + 'GLORYS2V3_model_monthly_orca025_OHC_point.nc')
dataset_OHC_ORAS4 = Dataset(datapath_OHC_ORAS4 + os.sep + 'oras4_model_monthly_orca1_OHC_point.nc')
dataset_OHC_SODA3 = Dataset(datapath_OHC_SODA3 + os.sep + 'OMET_SODA3_model_5daily_1980_2015_OHC.nc')
# mask
dataset_mask_ORAS4 = Dataset(datapath_mask_ORAS4 + os.sep + 'mesh_mask.nc')
dataset_mask_GLORYS2V3 = Dataset(datapath_mask_GLORYS2V3 + os.sep + 'G2V3_mesh_mask_myocean.nc')
dataset_mask_SODA3 = Dataset(datapath_mask_SODA3 + os.sep + 'topog.nc')
#***************************************************************************#
#*****************            options for data            ******************#
#***************************************************************************#
option = {}
option['globe'] = ['OHC_glo_vert','OHC_glo_vert_0_500','OHC_glo_vert_500_1000','OHC_glo_vert_1000_2000','OHC_glo_vert_2000_inf']
option['atlantic'] = ['OHC_atl_vert','OHC_atl_vert_0_500','OHC_atl_vert_500_1000','OHC_atl_vert_1000_2000','OHC_atl_vert_2000_inf']

# mask
mask_ORAS4 = dataset_mask_ORAS4.variables['vmask'][0,0,:,:]
mask_GLORYS2V3 = dataset_mask_GLORYS2V3.variables['vmask'][0,0,:,:]
mask_SODA3 = dataset_mask_SODA3.variables['wet_c'][:]

def data_extract(var_name, window):
    # extract variables with netcdf tool and take zonal mean
    OHC_glo_vert_ORAS4 = np.sum(dataset_OHC_ORAS4.variables['{}'.format(var_name)][21:,:,180:,:],3) # start from 1979
    OHC_glo_vert_GLORYS2V3 = np.sum(dataset_OHC_GLORYS2V3.variables['{}'.format(var_name)][:,:,579:,:],3) # start from 1993
    OHC_glo_vert_SODA3 = np.sum(dataset_OHC_SODA3.variables['{}'.format(var_name)][:,:,569:,:],3)       # start from 1980
    # year
    year_ORAS4 = dataset_OHC_ORAS4.variables['year'][21:]         # from 1979 to 2014
    year_GLORYS2V3 = dataset_OHC_GLORYS2V3.variables['year'][:]   # from 1993 to 2014
    year_SODA3 = dataset_OHC_SODA3.variables['year'][:]           # from 1980 to 2015
    # nominal latitude
    latitude_ORAS4 = dataset_OHC_ORAS4.variables['latitude_aux'][180:]
    latitude_GLORYS2V3 = dataset_OHC_GLORYS2V3.variables['latitude_aux'][579:]
    latitude_SODA3 = dataset_OHC_SODA3.variables['latitude_aux'][569:]
    print '*******************************************************************'
    print '*************************** whitening *****************************'
    print '*******************************************************************'
    month_ind = np.arange(12)
    # seasonal cycle of OHC for the globe
    seansonal_cycle_OHC_glo_vert_ORAS4 = np.mean(OHC_glo_vert_ORAS4,axis=0)
    seansonal_cycle_OHC_glo_vert_GLORYS2V3 = np.mean(OHC_glo_vert_GLORYS2V3,axis=0)
    seansonal_cycle_OHC_glo_vert_SODA3 = np.mean(OHC_glo_vert_SODA3,axis=0)

    OHC_glo_vert_ORAS4_white = np.zeros(OHC_glo_vert_ORAS4.shape,dtype=float)
    OHC_glo_vert_GLORYS2V3_white = np.zeros(OHC_glo_vert_GLORYS2V3.shape,dtype=float)
    OHC_glo_vert_SODA3_white = np.zeros(OHC_glo_vert_SODA3.shape,dtype=float)

    for i in np.arange(len(year_ORAS4)):
        for j in month_ind:
            OHC_glo_vert_ORAS4_white[i,j,:] = OHC_glo_vert_ORAS4[i,j,:] - seansonal_cycle_OHC_glo_vert_ORAS4[j,:]

    for i in np.arange(len(year_GLORYS2V3)):
        for j in month_ind:
            OHC_glo_vert_GLORYS2V3_white[i,j,:] = OHC_glo_vert_GLORYS2V3[i,j,:] - seansonal_cycle_OHC_glo_vert_GLORYS2V3[j,:]

    for i in np.arange(len(year_SODA3)):
        for j in month_ind:
            OHC_glo_vert_SODA3_white[i,j,:] = OHC_glo_vert_SODA3[i,j,:] - seansonal_cycle_OHC_glo_vert_SODA3[j,:]
    print '*******************************************************************'
    print '****************** prepare variables for plot *********************'
    print '*******************************************************************'
    # dataset with seasonal cycle - time series
    OHC_glo_vert_ORAS4_series = OHC_glo_vert_ORAS4.reshape(len(year_ORAS4)*len(month_ind),len(latitude_ORAS4))
    OHC_glo_vert_GLORYS2V3_series = OHC_glo_vert_GLORYS2V3.reshape(len(year_GLORYS2V3)*len(month_ind),len(latitude_GLORYS2V3))
    OHC_glo_vert_SODA3_series = OHC_glo_vert_SODA3.reshape(len(year_SODA3)*len(month_ind),len(latitude_SODA3))
    # dataset without seasonal cycle - time series
    OHC_glo_vert_ORAS4_white_series = OHC_glo_vert_ORAS4_white.reshape(len(year_ORAS4)*len(month_ind),len(latitude_ORAS4))
    OHC_glo_vert_GLORYS2V3_white_series = OHC_glo_vert_GLORYS2V3_white.reshape(len(year_GLORYS2V3)*len(month_ind),len(latitude_GLORYS2V3))
    OHC_glo_vert_SODA3_white_series = OHC_glo_vert_SODA3_white.reshape(len(year_SODA3)*len(month_ind),len(latitude_SODA3))
    print '*******************************************************************'
    print '********************** Running mean/sum ***************************'
    print '*******************************************************************'
    # calculate the running mean of OHC
    # original time series
    OHC_glo_vert_ORAS4_series_running_mean = np.zeros((len(year_ORAS4)*len(month_ind)-window+1,len(latitude_ORAS4)),dtype=float)
    OHC_glo_vert_GLORYS2V3_series_running_mean = np.zeros((len(year_GLORYS2V3)*len(month_ind)-window+1,len(latitude_GLORYS2V3)),dtype=float)
    OHC_glo_vert_SODA3_series_running_mean = np.zeros((len(year_SODA3)*len(month_ind)-window+1,len(latitude_SODA3)),dtype=float)
    # white time series
    OHC_glo_vert_ORAS4_white_series_running_mean = np.zeros((len(year_ORAS4)*len(month_ind)-window+1,len(latitude_ORAS4)),dtype=float)
    OHC_glo_vert_GLORYS2V3_white_series_running_mean = np.zeros((len(year_GLORYS2V3)*len(month_ind)-window+1,len(latitude_GLORYS2V3)),dtype=float)
    OHC_glo_vert_SODA3_white_series_running_mean = np.zeros((len(year_SODA3)*len(month_ind)-window+1,len(latitude_SODA3)),dtype=float)

    for i in np.arange(len(year_ORAS4)*len(month_ind)-window+1):
        for j in np.arange(len(latitude_ORAS4)):
            OHC_glo_vert_ORAS4_series_running_mean[i,j] = np.mean(OHC_glo_vert_ORAS4_series[i:i+window,j])
            OHC_glo_vert_ORAS4_white_series_running_mean[i,j] = np.mean(OHC_glo_vert_ORAS4_white_series[i:i+window,j])

    for i in np.arange(len(year_GLORYS2V3)*len(month_ind)-window+1):
        for j in np.arange(len(latitude_GLORYS2V3)):
            OHC_glo_vert_GLORYS2V3_series_running_mean[i,j] = np.mean(OHC_glo_vert_GLORYS2V3_series[i:i+window,j])
            OHC_glo_vert_GLORYS2V3_white_series_running_mean[i,j] = np.mean(OHC_glo_vert_GLORYS2V3_white_series[i:i+window,j])

    for i in np.arange(len(year_SODA3)*len(month_ind)-window+1):
        for j in np.arange(len(latitude_SODA3)):
            OHC_glo_vert_SODA3_series_running_mean[i,j] = np.mean(OHC_glo_vert_SODA3_series[i:i+window,j])
            OHC_glo_vert_SODA3_white_series_running_mean[i,j] = np.mean(OHC_glo_vert_SODA3_white_series[i:i+window,j])

    print '*******************************************************************'
    print '**********************   Return values  ***************************'
    print '*******************************************************************'
    return (OHC_glo_vert_ORAS4_series, OHC_glo_vert_GLORYS2V3_series, OHC_glo_vert_SODA3_series,
           OHC_glo_vert_ORAS4_white_series, OHC_glo_vert_GLORYS2V3_white_series, OHC_glo_vert_SODA3_white_series,
           OHC_glo_vert_ORAS4_series_running_mean, OHC_glo_vert_GLORYS2V3_series_running_mean, OHC_glo_vert_SODA3_series_running_mean,
           OHC_glo_vert_ORAS4_white_series_running_mean, OHC_glo_vert_GLORYS2V3_white_series_running_mean, OHC_glo_vert_SODA3_white_series_running_mean)

def time_series(OHC_ORAS4_series, OHC_GLORYS2V3_series, OHC_SODA3_series,
                OHC_ORAS4_series_running_mean, OHC_GLORYS2V3_series_running_mean,
                OHC_SODA3_series_running_mean, part_title, title_depth, output_path, window):
    print '*******************************************************************'
    print '*************************** time series ***************************'
    print '*******************************************************************'
    index_full = np.arange(1,445,1)
    index_year_full = np.arange(1979,2016,1)

    for i in np.arange(len(lat_interest_list)-1):
        # take the summation over a section
        OHC_ORAS4_series_sum = np.sum(OHC_ORAS4_series[:,lat_interest['ORAS4_cut'][i]:lat_interest['ORAS4_cut'][i+1]+1],1)
        OHC_GLORYS2V3_series_sum = np.sum(OHC_GLORYS2V3_series[:,lat_interest['GLORYS2V3_cut'][i]:lat_interest['GLORYS2V3_cut'][i+1]+1],1)
        OHC_SODA3_series_sum = np.sum(OHC_SODA3_series[:,lat_interest['SODA3_cut'][i]:lat_interest['SODA3_cut'][i+1]+1],1)
        OHC_ORAS4_series_running_mean_sum = np.sum(OHC_ORAS4_series_running_mean[:,lat_interest['ORAS4_cut'][i]:lat_interest['ORAS4_cut'][i+1]+1],1)
        OHC_GLORYS2V3_series_running_mean_sum = np.sum(OHC_GLORYS2V3_series_running_mean[:,lat_interest['GLORYS2V3_cut'][i]:lat_interest['GLORYS2V3_cut'][i+1]+1],1)
        OHC_SODA3_series_running_mean_sum = np.sum(OHC_SODA3_series_running_mean[:,lat_interest['SODA3_cut'][i]:lat_interest['SODA3_cut'][i+1]+1],1)
        # make plots
        fig6 = plt.figure()
        plt.plot(index_full[:-12],OHC_ORAS4_series_sum/1E+10,'c--',linewidth=1.0,label='ORAS4 time series')
        plt.plot(index_full[168:-12],OHC_GLORYS2V3_series_sum/1E+10,'m--',linewidth=1.0,label='GLORYS2V3 time series')
        plt.plot(index_full[12:],OHC_SODA3_series_sum/1E+10,'y--',linewidth=1.0,label='SODA3 time series')
        plt.plot(index_full[window-1:-12],OHC_ORAS4_series_running_mean_sum/1E+10,'c-',linewidth=2.0,label='ORAS4 running mean')
        plt.plot(index_full[168+window-1:-12],OHC_GLORYS2V3_series_running_mean_sum/1E+10,'m-',linewidth=2.0,label='GLORYS2V3 running mean')
        plt.plot(index_full[12+window-1:],OHC_SODA3_series_running_mean_sum/1E+10,'y-',linewidth=2.0,label='SODA3 running mean')
        plt.title('{} ({}) from {}N to {}N with a running mean of {} months'.format(part_title,title_depth,lat_interest_list[i],lat_interest_list[i+1],window))
        fig6.set_size_inches(12.5, 6)
        plt.xlabel("Time")
        plt.xticks(np.linspace(0, 444, 38), index_year_full)
        plt.xticks(rotation=60)
        plt.ylabel("Ocean Heat Content (1E+22 Joule)")
        plt.legend()
        plt.show()
        fig6.savefig(os.path.join(output_path,'Comp_OHC_lowpss_window_{}_{}N_{}N'.format(window,lat_interest_list[i],lat_interest_list[i+1])), dpi = 400)

if __name__ == '__main__':
    # define the running window for the running mean
    #window = 12 # in month
    window = 60 # in month
    #window = 120 # in month
    #window = 180 # in month
    #*****************     OHC over entire column     ******************#
    # get all the variables and prepare those variables for plot
    OHC_glo_vert_ORAS4_series, OHC_glo_vert_GLORYS2V3_series, OHC_glo_vert_SODA3_series,\
    OHC_glo_vert_ORAS4_white_series, OHC_glo_vert_GLORYS2V3_white_series,\
    OHC_glo_vert_SODA3_white_series, OHC_glo_vert_ORAS4_series_running_mean,\
    OHC_glo_vert_GLORYS2V3_series_running_mean, OHC_glo_vert_SODA3_series_running_mean,\
    OHC_glo_vert_ORAS4_white_series_running_mean, OHC_glo_vert_GLORYS2V3_white_series_running_mean,\
    OHC_glo_vert_SODA3_white_series_running_mean = data_extract(option['globe'][0], window)
    # make plots
    #*****************         original  globe        ******************#
    part_name = 'OHC'
    title_depth = '0-bottom'
    output_path = os.path.join(output_path_comp,'original_series_lowpass','glo_vert')
    time_series(OHC_glo_vert_ORAS4_series, OHC_glo_vert_GLORYS2V3_series, OHC_glo_vert_SODA3_series,\
                OHC_glo_vert_ORAS4_series_running_mean,OHC_glo_vert_GLORYS2V3_series_running_mean,\
                OHC_glo_vert_SODA3_series_running_mean, part_name, title_depth, output_path, window)
    #*****************        anomalies  globe        ******************#
    part_name = 'OHC anomalies'
    title_depth = '0-bottom'
    output_path = os.path.join(output_path_comp,'anomaly_series_lowpass','glo_vert')
    time_series(OHC_glo_vert_ORAS4_white_series, OHC_glo_vert_GLORYS2V3_white_series, OHC_glo_vert_SODA3_white_series,\
                OHC_glo_vert_ORAS4_white_series_running_mean,OHC_glo_vert_GLORYS2V3_white_series_running_mean,\
                OHC_glo_vert_SODA3_white_series_running_mean, part_name, title_depth, output_path, window)
    #*****************     OHC from 0 m to 500 m     ******************#
    # get all the variables and prepare those variables for plot
    OHC_glo_vert_0_500_ORAS4_series, OHC_glo_vert_0_500_GLORYS2V3_series, OHC_glo_vert_0_500_SODA3_series,\
    OHC_glo_vert_0_500_ORAS4_white_series, OHC_glo_vert_0_500_GLORYS2V3_white_series,\
    OHC_glo_vert_0_500_SODA3_white_series, OHC_glo_vert_0_500_ORAS4_series_running_mean,\
    OHC_glo_vert_0_500_GLORYS2V3_series_running_mean, OHC_glo_vert_0_500_SODA3_series_running_mean,\
    OHC_glo_vert_0_500_ORAS4_white_series_running_mean, OHC_glo_vert_0_500_GLORYS2V3_white_series_running_mean,\
    OHC_glo_vert_0_500_SODA3_white_series_running_mean = data_extract(option['globe'][1], window)
    #*****************         original  globe        ******************#
    part_name = 'OHC'
    title_depth = '0-500m'
    output_path = os.path.join(output_path_comp,'original_series_lowpass','glo_vert_0_500')
    time_series(OHC_glo_vert_0_500_ORAS4_series, OHC_glo_vert_0_500_GLORYS2V3_series, OHC_glo_vert_0_500_SODA3_series,\
                OHC_glo_vert_0_500_ORAS4_series_running_mean,OHC_glo_vert_0_500_GLORYS2V3_series_running_mean,\
                OHC_glo_vert_0_500_SODA3_series_running_mean, part_name, title_depth, output_path, window)
    #*****************        anomalies  globe        ******************#
    part_name = 'OHC anomalies'
    title_depth = '0-500m'
    output_path = os.path.join(output_path_comp,'anomaly_series_lowpass','glo_vert_0_500')
    time_series(OHC_glo_vert_0_500_ORAS4_white_series, OHC_glo_vert_0_500_GLORYS2V3_white_series, OHC_glo_vert_0_500_SODA3_white_series,\
                OHC_glo_vert_0_500_ORAS4_white_series_running_mean,OHC_glo_vert_0_500_GLORYS2V3_white_series_running_mean,\
                OHC_glo_vert_0_500_SODA3_white_series_running_mean, part_name, title_depth, output_path, window)
