#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : Compare AMET and OMET of all reanalysis datasets
Author          : Yang Liu
Date            : 2017.11.12
Last Update     : 2018.03.07
Description     : The code aims to plot and compare the meridional energy transport
                  in both the atmosphere and ocean. The atmospheric meridional energy
                  transport is calculated from reanalysis data ERA-Interim, MERRA2 and
                  JRA55. The oceanic meridional energy transport is calculated from ORAS4,
                  GLORYS2V3, SODA3 and ORAS5.
Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, sys, matplotlib, logging
variables       : Atmospheric Meridional Energy Transport   ERA-Interim     MERRA2       JRA55
                  Oceanic Meridional Energy Transport       ORAS4           GLORYS2V3    SODA3
Caveat!!        : Spatial and temporal coverage
                  Atmosphere
                  ERA-Interim 1979 - 2016
                  MERRA2      1980 - 2016
                  JRA55       1979 - 2015
                  Ocean
                  GLORYS2V3   1992 - 2014
                  ORAS4       1958 - 2014
                  SODA3       1980 - 2015
                  The full dataset of ORAS4 is from 1958. However, a quality report from
                  Magdalena from ECMWF indicates the quality of data for the first
                  two decades are very poor. Hence we use the data from 1979. which
                  is the start of satellite era.
                  The full dataset of ORAS4 is from 1958.

                  Data from 20N - 90N are taken into account!
"""
import numpy as np
import seaborn as sns
#import scipy as sp
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
#from scipy.interpolate import InterpolatedUnivariateSpline
import scipy
from mpl_toolkits.basemap import Basemap, cm
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import iris
import iris.plot as iplt
import iris.quickplot as qplt

# print the system structure and the path of the kernal
print platform.architecture()
print os.path

# switch on the seaborn effect
sns.set()

# calculate the time for the code execution
start_time = tttt.time()

################################   Input zone  ######################################
print '****************************************************************************'
print '*****************************   path   *************************************'
print '****************************************************************************'

# specify data path
datapath_ERAI = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ERAI/postprocessing'
datapath_MERRA2 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/MERRA2/postprocessing'
datapath_JRA55 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/JRA55/postprocessing'

datapath_ORAS4 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ORAS4/postprocessing'
datapath_GLORYS2V3 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/GLORYS2V3/postprocessing'
datapath_SODA3 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/SODA3/postprocessing'
# specify output path for the netCDF4 file
output_path = '/home/yang/NLeSC/Computation_Modeling/BlueAction/Bjerknes/AMET_OMET'

print '****************************************************************************'
print '********************    latitude index of insteret     *********************'
print '****************************************************************************'
# There is a cut to JRA, too
# index of latitude for insteret
# 20N
lat_ERAI_20 = 93
lat_MERRA2_20 = 0
lat_JRA55_20 = 124

lat_ORAS4_20 = 181
lat_GLORYS2V3_20 = 579
lat_SODA3_20 = 569
# after a cut to 20-90 N
lat_ORAS4_20_cut = 1
lat_GLORYS2V3_20_cut = 0
lat_SODA3_20_cut = 0

# 30N
lat_ERAI_30 = 80
lat_MERRA2_30 = 20
lat_JRA55_30 = 106

lat_ORAS4_30 = 192
lat_GLORYS2V3_30 = 623
lat_SODA3_30 = 613
# after a cut to 20-90 N
lat_ORAS4_30_cut = 12
lat_GLORYS2V3_30_cut = 44
lat_SODA3_30_cut = 44

# 40N
lat_ERAI_40 = 67
lat_MERRA2_40 = 40
lat_JRA55_40 = 88

lat_ORAS4_40 = 204
lat_GLORYS2V3_40 = 672
lat_SODA3_40 = 662
# after a cut to 20-90 N
lat_ORAS4_40_cut = 24
lat_GLORYS2V3_40_cut = 93
lat_SODA3_40_cut = 93

# 50N
lat_ERAI_50 = 53
lat_MERRA2_50 = 60
lat_JRA55_50 = 70

lat_ORAS4_50 = 218
lat_GLORYS2V3_50 = 726
lat_SODA3_50 = 719
# after a cut to 20-90 N
lat_ORAS4_50_cut = 38
lat_GLORYS2V3_50_cut = 147
lat_SODA3_50_cut = 150

# 60N
lat_ERAI_60 = 40
lat_MERRA2_60 = 80
lat_JRA55_60 = 53

lat_ORAS4_60 = 233
lat_GLORYS2V3_60 = 788
lat_SODA3_60 = 789
# after a cut to 20-90 N
lat_ORAS4_60_cut = 53
lat_GLORYS2V3_60_cut = 209
lat_SODA3_60_cut = 220

# 70N
lat_ERAI_70 = 27
lat_MERRA2_70 = 100
lat_JRA55_70 = 35

lat_ORAS4_70 = 250
lat_GLORYS2V3_70 = 857
lat_SODA3_70 = 880
# after a cut to 20-90 N
lat_ORAS4_70_cut = 70
lat_GLORYS2V3_70_cut = 278
lat_SODA3_70_cut = 311

# 80N
lat_ERAI_80 = 13
lat_MERRA2_80 = 120
lat_JRA55_80 = 17

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
lat_interest['ERAI'] = [lat_ERAI_20,lat_ERAI_30,lat_ERAI_40,lat_ERAI_50,lat_ERAI_60,lat_ERAI_70,lat_ERAI_80]
lat_interest['MERRA2'] = [lat_MERRA2_20,lat_MERRA2_30,lat_MERRA2_40,lat_MERRA2_50,lat_MERRA2_60,lat_MERRA2_70,lat_MERRA2_80]
lat_interest['JRA55'] = [lat_JRA55_20,lat_JRA55_30,lat_JRA55_40,lat_JRA55_50,lat_JRA55_60,lat_JRA55_70,lat_JRA55_80]
# after cut
lat_interest['ORAS4'] = [lat_ORAS4_20_cut,lat_ORAS4_30_cut,lat_ORAS4_40_cut,lat_ORAS4_50_cut,lat_ORAS4_60_cut,lat_ORAS4_70_cut,lat_ORAS4_80_cut]
lat_interest['GLORYS2V3'] = [lat_GLORYS2V3_20_cut,lat_GLORYS2V3_30_cut,lat_GLORYS2V3_40_cut,lat_GLORYS2V3_50_cut,lat_GLORYS2V3_60_cut,lat_GLORYS2V3_70_cut,lat_GLORYS2V3_80_cut]
lat_interest['SODA3'] = [lat_SODA3_20_cut,lat_SODA3_30_cut,lat_SODA3_40_cut,lat_SODA3_50_cut,lat_SODA3_60_cut,lat_SODA3_70_cut,lat_SODA3_80_cut]
# mask path
#mask_path = 'F:\DataBase\ORAS\ORAS4\Monthly\Model'
####################################################################################
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

dataset_ERAI = Dataset(datapath_ERAI + os.sep + 'model_daily_075_1979_2016_E_zonal_int.nc')
dataset_MERRA2 = Dataset(datapath_MERRA2 + os.sep + 'AMET_MERRA2_model_daily_1980_2016_E_zonal_int.nc')
dataset_JRA55 = Dataset(datapath_JRA55 + os.sep + 'AMET_JRA55_model_daily_1979_2015_E_zonal_int.nc')

dataset_GLORYS2V3 = Dataset(datapath_GLORYS2V3 + os.sep + 'GLORYS2V3_model_monthly_orca025_E_zonal_int.nc')
dataset_ORAS4 = Dataset(datapath_ORAS4 + os.sep + 'oras4_model_monthly_orca1_E_zonal_int.nc')
dataset_SODA3 = Dataset(datapath_SODA3 + os.sep + 'OMET_SODA3_model_5daily_1980_2015_E_zonal_int.nc')

#dataset_AMET_point = Dataset(datapath_AMET + os.sep + 'model_daily_075_1979_2016_E_point.nc')
#dataset_OMET_point = Dataset(datapath_OMET + os.sep + 'oras4_model_monthly_orca1_1958_2014_E_point.nc')

for k in dataset_ERAI.variables:
    print dataset_ERAI.variables['%s' % (k)]

# from 1979 to 2014
# from 20N - 90N
AMET_ERAI = dataset_ERAI.variables['E'][:]/1000 # from Tera Watt to Peta Watt
AMET_MERRA2 = dataset_MERRA2.variables['E'][:]/1000 # from Tera Watt to Peta Watt
AMET_JRA55 = dataset_JRA55.variables['E'][:,:,0:125]/1000 # from Tera Watt to Peta Watt

OMET_ORAS4 = dataset_ORAS4.variables['E'][21:,:,180:]/1000 # start from 1979
OMET_GLORYS2V3 = dataset_GLORYS2V3.variables['E'][:,:,579:]/1000 # start from 1993
OMET_SODA3 = dataset_SODA3.variables['E'][:,:,569:]/1000 # start from 1980

year_ERAI = dataset_ERAI.variables['year'][:]             # from 1979 to 2014
year_MERRA2 = dataset_MERRA2.variables['year'][:]         # from 1980 to 2014
year_JRA55 = dataset_JRA55.variables['year'][:]           # from 1979 to 2015

year_ORAS4 = dataset_ORAS4.variables['year'][21:]         # from 1979 to 2014
year_GLORYS2V3 = dataset_GLORYS2V3.variables['year'][:]   # from 1993 to 2014
year_SODA3 = dataset_SODA3.variables['year'][:]           # from 1980 to 2014

latitude_ERAI = dataset_ERAI.variables['latitude'][:]
latitude_MERRA2 = dataset_MERRA2.variables['latitude'][:]
latitude_JRA55 = dataset_JRA55.variables['latitude'][0:125]

latitude_ORAS4 = dataset_ORAS4.variables['latitude_aux'][180:]
latitude_GLORYS2V3 = dataset_GLORYS2V3.variables['latitude_aux'][579:]
latitude_SODA3 = dataset_SODA3.variables['latitude_aux'][569:]

print '*******************************************************************'
print '*************************** whitening *****************************'
print '*******************************************************************'
month_ind = np.arange(12)
seansonal_cycle_AMET_ERAI = np.mean(AMET_ERAI,axis=0)
seansonal_cycle_AMET_MERRA2 = np.mean(AMET_MERRA2,axis=0)
seansonal_cycle_AMET_JRA55 = np.mean(AMET_JRA55,axis=0)

seansonal_cycle_OMET_ORAS4 = np.mean(OMET_ORAS4,axis=0)
seansonal_cycle_OMET_GLORYS2V3 = np.mean(OMET_GLORYS2V3,axis=0)
seansonal_cycle_OMET_SODA3 = np.mean(OMET_SODA3,axis=0)

AMET_ERAI_white = np.zeros(AMET_ERAI.shape,dtype=float)
AMET_MERRA2_white = np.zeros(AMET_MERRA2.shape,dtype=float)
AMET_JRA55_white = np.zeros(AMET_JRA55.shape,dtype=float)

OMET_ORAS4_white = np.zeros(OMET_ORAS4.shape,dtype=float)
OMET_GLORYS2V3_white = np.zeros(OMET_GLORYS2V3.shape,dtype=float)
OMET_SODA3_white = np.zeros(OMET_SODA3.shape,dtype=float)

for i in np.arange(len(year_ERAI)):
    for j in month_ind:
        AMET_ERAI_white[i,j,:] = AMET_ERAI[i,j,:] - seansonal_cycle_AMET_ERAI[j,:]

for i in np.arange(len(year_MERRA2)):
    for j in month_ind:
        AMET_MERRA2_white[i,j,:] = AMET_MERRA2[i,j,:] - seansonal_cycle_AMET_MERRA2[j,:]

for i in np.arange(len(year_JRA55)):
    for j in month_ind:
        AMET_JRA55_white[i,j,:] = AMET_JRA55[i,j,:] - seansonal_cycle_AMET_JRA55[j,:]

for i in np.arange(len(year_ORAS4)):
    for j in month_ind:
        OMET_ORAS4_white[i,j,:] = OMET_ORAS4[i,j,:] - seansonal_cycle_OMET_ORAS4[j,:]

for i in np.arange(len(year_GLORYS2V3)):
    for j in month_ind:
        OMET_GLORYS2V3_white[i,j,:] = OMET_GLORYS2V3[i,j,:] - seansonal_cycle_OMET_GLORYS2V3[j,:]

for i in np.arange(len(year_SODA3)):
    for j in month_ind:
        OMET_SODA3_white[i,j,:] = OMET_SODA3[i,j,:] - seansonal_cycle_OMET_SODA3[j,:]

print '*******************************************************************'
print '****************** prepare variables for plot *********************'
print '*******************************************************************'
# annual mean of AMET and OMET at different latitudes
AMET_ERAI_mean = np.mean(np.mean(AMET_ERAI,0),0)
AMET_MERRA2_mean = np.mean(np.mean(AMET_MERRA2,0),0)
AMET_JRA55_mean = np.mean(np.mean(AMET_JRA55,0),0)

OMET_ORAS4_mean = np.mean(np.mean(OMET_ORAS4,0),0)
OMET_GLORYS2V3_mean = np.mean(np.mean(OMET_GLORYS2V3,0),0)
OMET_SODA3_mean = np.mean(np.mean(OMET_SODA3,0),0)

# dataset with seasonal cycle - time series
AMET_ERAI_series = AMET_ERAI.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI))
AMET_MERRA2_series = AMET_MERRA2.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2))
AMET_JRA55_series = AMET_JRA55.reshape(len(year_JRA55)*len(month_ind),len(latitude_JRA55))

OMET_ORAS4_series = OMET_ORAS4.reshape(len(year_ORAS4)*len(month_ind),len(latitude_ORAS4))
OMET_GLORYS2V3_series = OMET_GLORYS2V3.reshape(len(year_GLORYS2V3)*len(month_ind),len(latitude_GLORYS2V3))
OMET_SODA3_series = OMET_SODA3.reshape(len(year_SODA3)*len(month_ind),len(latitude_SODA3))

# dataset without seasonal cycle - time series
AMET_ERAI_white_series = AMET_ERAI_white.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI))
AMET_MERRA2_white_series = AMET_MERRA2_white.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2))
AMET_JRA55_white_series = AMET_JRA55_white.reshape(len(year_JRA55)*len(month_ind),len(latitude_JRA55))

OMET_ORAS4_white_series = OMET_ORAS4_white.reshape(len(year_ORAS4)*len(month_ind),len(latitude_ORAS4))
OMET_GLORYS2V3_white_series = OMET_GLORYS2V3_white.reshape(len(year_GLORYS2V3)*len(month_ind),len(latitude_GLORYS2V3))
OMET_SODA3_white_series = OMET_SODA3_white.reshape(len(year_SODA3)*len(month_ind),len(latitude_SODA3))

print '*******************************************************************'
print '********************** Running mean/sum ***************************'
print '*******************************************************************'
# running mean is calculated on time series
# define the running window for the running mean
window = 12 # in month
#window = 60 # in month
#window = 120 # in month
#window = 180 # in month
# calculate the running mean of AMET and OMET at differnt latitudes
# original time series
AMET_ERAI_series_running_mean = np.zeros((len(AMET_ERAI_series)-window+1,len(latitude_ERAI)),dtype=float)
AMET_MERRA2_series_running_mean = np.zeros((len(AMET_MERRA2_series)-window+1,len(latitude_MERRA2)),dtype=float)
AMET_JRA55_series_running_mean = np.zeros((len(AMET_JRA55_series)-window+1,len(latitude_JRA55)),dtype=float)

OMET_ORAS4_series_running_mean = np.zeros((len(OMET_ORAS4_series)-window+1,len(latitude_ORAS4)),dtype=float)
OMET_GLORYS2V3_series_running_mean = np.zeros((len(OMET_GLORYS2V3_series)-window+1,len(latitude_GLORYS2V3)),dtype=float)
OMET_SODA3_series_running_mean = np.zeros((len(OMET_SODA3_series)-window+1,len(latitude_SODA3)),dtype=float)

# white time series
AMET_ERAI_white_series_running_mean = np.zeros((len(AMET_ERAI_white_series)-window+1,len(latitude_ERAI)),dtype=float)
AMET_MERRA2_white_series_running_mean = np.zeros((len(AMET_MERRA2_white_series)-window+1,len(latitude_MERRA2)),dtype=float)
AMET_JRA55_white_series_running_mean = np.zeros((len(AMET_JRA55_white_series)-window+1,len(latitude_JRA55)),dtype=float)

OMET_ORAS4_white_series_running_mean = np.zeros((len(OMET_ORAS4_white_series)-window+1,len(latitude_ORAS4)),dtype=float)
OMET_GLORYS2V3_white_series_running_mean = np.zeros((len(OMET_GLORYS2V3_white_series)-window+1,len(latitude_GLORYS2V3)),dtype=float)
OMET_SODA3_white_series_running_mean = np.zeros((len(OMET_SODA3_white_series)-window+1,len(latitude_SODA3)),dtype=float)

for i in np.arange(len(AMET_ERAI_white_series)-window+1):
    for j in np.arange(len(latitude_ERAI)):
        AMET_ERAI_series_running_mean[i,j] = np.mean(AMET_ERAI_series[i:i+window,j])
        AMET_ERAI_white_series_running_mean[i,j] = np.mean(AMET_ERAI_white_series[i:i+window,j])

for i in np.arange(len(AMET_MERRA2_white_series)-window+1):
    for j in np.arange(len(latitude_MERRA2)):
        AMET_MERRA2_series_running_mean[i,j] = np.mean(AMET_MERRA2_series[i:i+window,j])
        AMET_MERRA2_white_series_running_mean[i,j] = np.mean(AMET_MERRA2_white_series[i:i+window,j])

for i in np.arange(len(AMET_JRA55_white_series)-window+1):
    for j in np.arange(len(latitude_JRA55)):
        AMET_JRA55_series_running_mean[i,j] = np.mean(AMET_JRA55_series[i:i+window,j])
        AMET_JRA55_white_series_running_mean[i,j] = np.mean(AMET_JRA55_white_series[i:i+window,j])

for i in np.arange(len(OMET_ORAS4_white_series)-window+1):
    for j in np.arange(len(latitude_ORAS4)):
        OMET_ORAS4_series_running_mean[i,j] = np.mean(OMET_ORAS4_series[i:i+window,j])
        OMET_ORAS4_white_series_running_mean[i,j] = np.mean(OMET_ORAS4_white_series[i:i+window,j])

for i in np.arange(len(OMET_GLORYS2V3_white_series)-window+1):
    for j in np.arange(len(latitude_GLORYS2V3)):
        OMET_GLORYS2V3_series_running_mean[i,j] = np.mean(OMET_GLORYS2V3_series[i:i+window,j])
        OMET_GLORYS2V3_white_series_running_mean[i,j] = np.mean(OMET_GLORYS2V3_white_series[i:i+window,j])

for i in np.arange(len(OMET_SODA3_white_series)-window+1):
    for j in np.arange(len(latitude_SODA3)):
        OMET_SODA3_series_running_mean[i,j] = np.mean(OMET_SODA3_series[i:i+window,j])
        OMET_SODA3_white_series_running_mean[i,j] = np.mean(OMET_SODA3_white_series[i:i+window,j])

print '*******************************************************************'
print '***************   standard deviation at each lat   ****************'
print '*******************************************************************'
# standard deviation at each latitude
# for error bar band
# reshape of each dataset at full latitude for the calculation of standard deviation
AMET_ERAI_std = np.std(AMET_ERAI_series,axis=0)
AMET_ERAI_error_plus = AMET_ERAI_mean + AMET_ERAI_std
AMET_ERAI_error_minus = AMET_ERAI_mean - AMET_ERAI_std

AMET_MERRA2_std = np.std(AMET_MERRA2_series,axis=0)
AMET_MERRA2_error_plus = AMET_MERRA2_mean + AMET_MERRA2_std
AMET_MERRA2_error_minus = AMET_MERRA2_mean - AMET_MERRA2_std

AMET_JRA55_std = np.std(AMET_JRA55_series,axis=0)
AMET_JRA55_error_plus = AMET_JRA55_mean + AMET_JRA55_std
AMET_JRA55_error_minus = AMET_JRA55_mean - AMET_JRA55_std

OMET_ORAS4_std = np.std(OMET_ORAS4_series,axis=0)
OMET_ORAS4_error_plus = OMET_ORAS4_mean + OMET_ORAS4_std
OMET_ORAS4_error_minus = OMET_ORAS4_mean - OMET_ORAS4_std

OMET_GLORYS2V3_std = np.std(OMET_GLORYS2V3_series,axis=0)
OMET_GLORYS2V3_error_plus = OMET_GLORYS2V3_mean + OMET_GLORYS2V3_std
OMET_GLORYS2V3_error_minus = OMET_GLORYS2V3_mean - OMET_GLORYS2V3_std

OMET_SODA3_std = np.std(OMET_SODA3_series,axis=0)
OMET_SODA3_error_plus = OMET_SODA3_mean + OMET_SODA3_std
OMET_SODA3_error_minus = OMET_SODA3_mean - OMET_SODA3_std
print '*******************************************************************'
print '***************   span of annual mean at each lat   ***************'
print '*******************************************************************'
# calculate annual mean
AMET_ERAI_full_annual_mean = np.mean(AMET_ERAI,1)
AMET_MERRA2_full_annual_mean = np.mean(AMET_MERRA2,1)
AMET_JRA55_full_annual_mean = np.mean(AMET_JRA55,1)
OMET_ORAS4_full_annual_mean = np.mean(OMET_ORAS4,1)
OMET_GLORYS2V3_full_annual_mean = np.mean(OMET_GLORYS2V3,1)
OMET_SODA3_full_annual_mean = np.mean(OMET_SODA3,1)
# calculate the difference between annual mean and mean of entire time series
AMET_ERAI_full_annual_mean_max = np.amax(AMET_ERAI_full_annual_mean,0)
AMET_MERRA2_full_annual_mean_max = np.amax(AMET_MERRA2_full_annual_mean,0)
AMET_JRA55_full_annual_mean_max = np.amax(AMET_JRA55_full_annual_mean,0)
OMET_ORAS4_full_annual_mean_max = np.amax(OMET_ORAS4_full_annual_mean,0)
OMET_GLORYS2V3_full_annual_mean_max = np.amax(OMET_GLORYS2V3_full_annual_mean,0)
OMET_SODA3_full_annual_mean_max = np.amax(OMET_SODA3_full_annual_mean,0)

AMET_ERAI_full_annual_mean_min = np.amin(AMET_ERAI_full_annual_mean,0)
AMET_MERRA2_full_annual_mean_min = np.amin(AMET_MERRA2_full_annual_mean,0)
AMET_JRA55_full_annual_mean_min = np.amin(AMET_JRA55_full_annual_mean,0)
OMET_ORAS4_full_annual_mean_min = np.amin(OMET_ORAS4_full_annual_mean,0)
OMET_GLORYS2V3_full_annual_mean_min = np.amin(OMET_GLORYS2V3_full_annual_mean,0)
OMET_SODA3_full_annual_mean_min = np.amin(OMET_SODA3_full_annual_mean,0)
print '*******************************************************************'
print '*************************** x-y plots *****************************'
print '*******************************************************************'
fig00 = plt.figure()
plt.plot(latitude_ERAI,AMET_ERAI_mean,'b-',label='ERA-Interim')
plt.fill_between(latitude_ERAI,AMET_ERAI_full_annual_mean_max,AMET_ERAI_full_annual_mean_min,alpha=0.3,edgecolor='lightskyblue', facecolor='lightskyblue')
plt.plot(latitude_MERRA2,AMET_MERRA2_mean,'r-',label='MERRA2')
plt.fill_between(latitude_MERRA2,AMET_MERRA2_full_annual_mean_max,AMET_MERRA2_full_annual_mean_min,alpha=0.3,edgecolor='tomato', facecolor='tomato')
plt.plot(latitude_JRA55,AMET_JRA55_mean,'g-',label='JRA55')
plt.fill_between(latitude_JRA55,AMET_JRA55_full_annual_mean_max,AMET_JRA55_full_annual_mean_min,alpha=0.3,edgecolor='lightgreen', facecolor='lightgreen')
plt.plot(latitude_ORAS4,OMET_ORAS4_mean,'c-',label='ORAS4')
plt.fill_between(latitude_ORAS4,OMET_ORAS4_full_annual_mean_max,OMET_ORAS4_full_annual_mean_min,alpha=0.3,edgecolor='aquamarine', facecolor='aquamarine')
plt.plot(latitude_GLORYS2V3,OMET_GLORYS2V3_mean,'m-',label='GLORYS2V3')
plt.fill_between(latitude_GLORYS2V3,OMET_GLORYS2V3_full_annual_mean_max,OMET_GLORYS2V3_full_annual_mean_min,alpha=0.3,edgecolor='plum', facecolor='plum')
plt.plot(latitude_SODA3,OMET_SODA3_mean,'y-',label='SODA3')
plt.fill_between(latitude_SODA3,OMET_SODA3_full_annual_mean_max,OMET_SODA3_full_annual_mean_min,alpha=0.3,edgecolor='lightyellow', facecolor='lightyellow')
#plt.plot(latitude_AMET,AMET_mean + OMET_mean_interpolate,'g--',label='Total')
plt.title('Mean AMET & OMET of entire time series from 20N to 90N')
plt.legend()
#fig1.set_size_inches(5, 5)
plt.xlabel("Latitude")
labels =['20','30','40','50','60','70','80','90']
plt.xticks(np.linspace(20, 90, 8),labels)
#plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig00.savefig(output_path + os.sep + 'AMET_OMET_annual_mean_span.jpg', dpi = 500)

fig0 = plt.figure()
plt.plot(latitude_ERAI,AMET_ERAI_mean,'b-',label='ERA-Interim')
plt.fill_between(latitude_ERAI,AMET_ERAI_error_plus,AMET_ERAI_error_minus,alpha=0.3,edgecolor='lightskyblue', facecolor='lightskyblue')
plt.plot(latitude_MERRA2,AMET_MERRA2_mean,'r-',label='MERRA2')
plt.fill_between(latitude_MERRA2,AMET_MERRA2_error_plus,AMET_MERRA2_error_minus,alpha=0.3,edgecolor='tomato', facecolor='tomato')
plt.plot(latitude_JRA55,AMET_JRA55_mean,'g-',label='JRA55')
plt.fill_between(latitude_JRA55,AMET_JRA55_error_plus,AMET_JRA55_error_minus,alpha=0.3,edgecolor='lightgreen', facecolor='lightgreen')
plt.plot(latitude_ORAS4,OMET_ORAS4_mean,'c-',label='ORAS4')
plt.fill_between(latitude_ORAS4,OMET_ORAS4_error_plus,OMET_ORAS4_error_minus,alpha=0.3,edgecolor='aquamarine', facecolor='aquamarine')
plt.plot(latitude_GLORYS2V3,OMET_GLORYS2V3_mean,'m-',label='GLORYS2V3')
plt.fill_between(latitude_GLORYS2V3,OMET_GLORYS2V3_error_plus,OMET_GLORYS2V3_error_minus,alpha=0.3,edgecolor='plum', facecolor='plum')
plt.plot(latitude_SODA3,OMET_SODA3_mean,'y-',label='SODA3')
plt.fill_between(latitude_SODA3,OMET_SODA3_error_plus,OMET_SODA3_error_minus,alpha=0.3,edgecolor='lightyellow', facecolor='lightyellow')
#plt.plot(latitude_AMET,AMET_mean + OMET_mean_interpolate,'g--',label='Total')
plt.title('Mean AMET & OMET of entire time series from 20N to 90N')
plt.legend()
#fig1.set_size_inches(5, 5)
plt.xlabel("Latitude")
labels =['20','30','40','50','60','70','80','90']
plt.xticks(np.linspace(20, 90, 8),labels)
#plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig0.savefig(output_path + os.sep + 'AMET_OMET_annual_mean_stdBar.jpg', dpi = 500)

print '*******************************************************************'
print '*********************** time series plots *************************'
print '*******************************************************************'
# index and namelist of years for time series and running mean time series
index_1993_2014 = np.arange(169,433,1) # starting from index of year 1993
index_1979_2014 = np.arange(1,433,1)
index_1980_2016 = np.arange(13,457,1)
index_1979_2016 = np.arange(1,457,1)
index_1979_2015 = np.arange(1,445,1)
index_1980_2015 = np.arange(13,445,1)

# time series plot of meridional energy transport at xN
for i in np.arange(len(lat_interest_list)):
    fig1 = plt.figure()
    plt.plot(index_1979_2016,AMET_ERAI_series[:,lat_interest['ERAI'][i]],'b-',label='ERA-Interim')
    plt.plot(index_1980_2016,AMET_MERRA2_series[:,lat_interest['MERRA2'][i]],'r-',label='MERRA2')
    plt.plot(index_1979_2015,AMET_JRA55_series[:,lat_interest['JRA55'][i]],'g-',label='JRA55')
    plt.plot(index_1979_2014,OMET_ORAS4_series[:,lat_interest['ORAS4'][i]],'c-',label='ORAS4')
    plt.plot(index_1993_2014,OMET_GLORYS2V3_series[:,lat_interest['GLORYS2V3'][i]],'m-',label='GLORYS2V3')
    plt.plot(index_1980_2015,OMET_SODA3_series[:,lat_interest['SODA3'][i]],'y-',label='SODA3')
    plt.title('Meridional Energy Transport at %d N' % (lat_interest_list[i]))
    plt.legend()
    fig1.set_size_inches(13, 6)
    plt.xlabel("Time")
    plt.xticks(np.linspace(0, 456, 39), year_ERAI)
    plt.xticks(rotation=60)
    plt.ylabel("Meridional Energy Transport (PW)")
    plt.show()
    fig1.savefig(output_path + os.sep + 'original_series' + os.sep + 'AMET_OMET_%dN_time_series.jpg' % (lat_interest_list[i]), dpi = 500)

# time series plot of meridional energy transport anomalies at xN
for i in np.arange(len(lat_interest_list)):
    fig2 = plt.figure()
    plt.plot(index_1979_2016,AMET_ERAI_white_series[:,lat_interest['ERAI'][i]],'b-',label='ERA-Interim')
    plt.plot(index_1980_2016,AMET_MERRA2_white_series[:,lat_interest['MERRA2'][i]],'r-',label='MERRA2')
    plt.plot(index_1979_2015,AMET_JRA55_white_series[:,lat_interest['JRA55'][i]],'g-',label='JRA55')
    plt.plot(index_1979_2014,OMET_ORAS4_white_series[:,lat_interest['ORAS4'][i]],'c-',label='ORAS4')
    plt.plot(index_1993_2014,OMET_GLORYS2V3_white_series[:,lat_interest['GLORYS2V3'][i]],'m-',label='GLORYS2V3')
    plt.plot(index_1980_2015,OMET_SODA3_white_series[:,lat_interest['SODA3'][i]],'y-',label='SODA3')
    plt.title('Meridional Energy Transport Anomalies at %d N' % (lat_interest_list[i]))
    plt.legend()
    fig2.set_size_inches(13, 6)
    plt.xlabel("Time")
    plt.xticks(np.linspace(0, 456, 39), year_ERAI)
    plt.xticks(rotation=60)
    plt.ylabel("Meridional Energy Transport (PW)")
    plt.show()
    fig2.savefig(output_path + os.sep + 'anomaly_series' + os.sep + 'AMET_OMET_%dN_anomaly_time_series.jpg' % (lat_interest_list[i]), dpi = 500)

# time series plot of meridional energy transport at xN with x years running mean
for i in np.arange(len(lat_interest_list)):
    fig3 = plt.figure()
    plt.plot(index_1979_2016[window-1:],AMET_ERAI_series_running_mean[:,lat_interest['ERAI'][i]],'b-',label='ERA-Interim')
    plt.plot(index_1980_2016[window-1:],AMET_MERRA2_series_running_mean[:,lat_interest['MERRA2'][i]],'r-',label='MERRA2')
    plt.plot(index_1979_2015[window-1:],AMET_JRA55_series_running_mean[:,lat_interest['JRA55'][i]],'g-',label='JRA55')
    plt.plot(index_1979_2014[window-1:],OMET_ORAS4_series_running_mean[:,lat_interest['ORAS4'][i]],'c-',label='ORAS4')
    plt.plot(index_1993_2014[window-1:],OMET_GLORYS2V3_series_running_mean[:,lat_interest['GLORYS2V3'][i]],'m-',label='GLORYS2V3')
    plt.plot(index_1980_2015[window-1:],OMET_SODA3_series_running_mean[:,lat_interest['SODA3'][i]],'y-',label='SODA3')
    plt.title('Meridional Energy Transport Anomalies with running mean of %d months at %d N' % (window,lat_interest_list[i]))
    plt.legend()
    fig3.set_size_inches(13, 6)
    plt.xlabel("Time")
    plt.xticks(np.linspace(0, 456, 39), year_ERAI)
    plt.xticks(rotation=60)
    plt.ylabel("Meridional Energy Transport (PW)")
    plt.show()
    fig3.savefig(output_path + os.sep + 'original_lowpass' + os.sep + 'AMET_OMET_%dN_running_mean_%dm_time_series.jpg' % (lat_interest_list[i],window), dpi = 500)

# time series plot of meridional energy transport anomalies at xN with x years running mean
for i in np.arange(len(lat_interest_list)):
    fig4 = plt.figure()
    plt.plot(index_1979_2016[window-1:],AMET_ERAI_white_series_running_mean[:,lat_interest['ERAI'][i]],'b-',label='ERA-Interim')
    plt.plot(index_1980_2016[window-1:],AMET_MERRA2_white_series_running_mean[:,lat_interest['MERRA2'][i]],'r-',label='MERRA2')
    plt.plot(index_1979_2015[window-1:],AMET_JRA55_white_series_running_mean[:,lat_interest['JRA55'][i]],'g-',label='JRA55')
    plt.plot(index_1979_2014[window-1:],OMET_ORAS4_white_series_running_mean[:,lat_interest['ORAS4'][i]],'c-',label='ORAS4')
    plt.plot(index_1993_2014[window-1:],OMET_GLORYS2V3_white_series_running_mean[:,lat_interest['GLORYS2V3'][i]],'m-',label='GLORYS2V3')
    plt.plot(index_1980_2015[window-1:],OMET_SODA3_white_series_running_mean[:,lat_interest['SODA3'][i]],'y-',label='SODA3')
    plt.title('Meridional Energy Transport Anomalies with running mean of %d months at %d N' % (window,lat_interest_list[i]))
    plt.legend()
    fig4.set_size_inches(13, 6)
    plt.xlabel("Time")
    plt.xticks(np.linspace(0, 456, 39), year_ERAI)
    plt.xticks(rotation=60)
    plt.ylabel("Meridional Energy Transport (PW)")
    plt.show()
    fig4.savefig(output_path + os.sep + 'anomaly_lowpass' + os.sep + 'AMET_OMET_%dN_anomaly_running_mean_%dm_time_series.jpg' % (lat_interest_list[i],window), dpi = 500)

print '*******************************************************************'
print '****************** maps (average of point data) *******************'
print '*******************************************************************'

#3D
# fig1=plt.figure()
# ax=fig1.gca(projection='3d') # change figure into 3D
# plt.hold(True)
# for i in Index_i:
#     ax.plot(aux['Ur_%d_B_0' % (i)][:300],freq_y['Ur_%d_B_0' % (i)][:300],mag_y['Ur_%d_B_0' % (i)][:300],label='Ur=%d' % (i))
#
# ax.plot(refer_x_sway,refer_y_sway,refer_z_sway,c='r',linewidth=3,label='Natural freq sway')
# ax.plot(refer_x_yaw,refer_y_yaw,refer_z_yaw,c='m',linewidth=3,label='Natural freq yaw')
# #ax.grid()
# ax.set_xlabel("Reduced velocity Ur")
# ax.set_ylabel("Frequency (Hz)")
# ax.set_zlabel("Power spectrum density (m^2/s)")
# ax.view_init(30,220)
# plt.title("B=0%")
# plt.legend()
# plt.show()
