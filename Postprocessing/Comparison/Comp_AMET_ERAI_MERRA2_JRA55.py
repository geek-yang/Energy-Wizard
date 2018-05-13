#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : Compare atmospheric meridional energy transport (MERRA2,ERA-Interim,JRA55)
Author          : Yang Liu
Date            : 2017.11.06
Last Update     : 2018.05.11
Description     : The code aims to compare the atmospheric meridional energy transport
                  calculated from different atmospheric reanalysis datasets. In this,
                  case, this includes MERRA II from NASA, ERA-Interim from ECMWF and
                  JRA55 from JMA.
Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, sys, matplotlib
variables       : Meridional Total Energy Transport           E         [Tera-Watt]
                  Meridional Internal Energy Transport        E_cpT     [Tera-Watt]
                  Meridional Latent Energy Transport          E_Lvq     [Tera-Watt]
                  Meridional Geopotential Energy Transport    E_gz      [Tera-Watt]
                  Meridional Kinetic Energy Transport         E_uv2     [Tera-Watt]
Caveat!!        : Spatial and temporal coverage
                  Temporal
                  ERA-Interim 1979 - 2016
                  MERRA2      1980 - 2016
                  JRA55       1979 - 2015
                  Spatial
                  ERA-Interim 20N - 90N
                  MERRA2      20N - 90N
                  JRA55       90S - 90N
"""

import seaborn as sns
import numpy as np
import time as tttt
from netCDF4 import Dataset,num2date
import os
import platform
import sys
import logging
import matplotlib
from mpl_toolkits.mplot3d import Axes3D
# generate images without having a window appear
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas
from scipy import stats

# switch on the seaborn effect
sns.set()

################################   Input zone  ######################################
# specify data path
datapath_ERAI = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ERAI/postprocessing'
datapath_MERRA2 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/MERRA2/postprocessing'
datapath_JRA55 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/JRA55/postprocessing'
# specify output path for the netCDF4 file
output_path = '/home/yang/NLeSC/Computation_Modeling/BlueAction/AMET/Comparison'
# csv file for saving statistic matrix
csv_path = '/home/yang/NLeSC/Computation_Modeling/BlueAction/AMET/Comparison'
print '****************************************************************************'
print '********************    latitude index of insteret     *********************'
print '****************************************************************************'
# index of latitude for insteret
# There is a cut to JRA, too
# from 90N to 20N --> 0:125
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
####################################################################################
####################################################################################
print '*******************************************************************'
print '*********************** extract variables *************************'
print '*******************************************************************'
dataset_ERAI = Dataset(datapath_ERAI + os.sep + 'model_daily_075_1979_2016_E_zonal_int.nc')
dataset_MERRA2 = Dataset(datapath_MERRA2 + os.sep + 'AMET_MERRA2_model_daily_1980_2016_E_zonal_int.nc')
dataset_JRA55 = Dataset(datapath_JRA55 + os.sep + 'AMET_JRA55_model_daily_1979_2015_E_zonal_int.nc')

for k in dataset_MERRA2.variables:
    print dataset_MERRA2.variables['%s' % (k)]

# from 1979 to 2016
# from 20N - 90N
# total energy transport
AMET_E_ERAI = dataset_ERAI.variables['E'][:]/1000 # from Tera Watt to Peta Watt
AMET_E_MERRA2 = dataset_MERRA2.variables['E'][:]/1000 # from Tera Watt to Peta Watt
AMET_E_JRA55 = dataset_JRA55.variables['E'][:,:,0:125]/1000 # from Tera Watt to Peta Watt
# internal energy
AMET_E_cpT_ERAI = dataset_ERAI.variables['E_cpT'][:]/1000
AMET_E_cpT_MERRA2 = dataset_MERRA2.variables['E_cpT'][:]/1000
AMET_E_cpT_JRA55 = dataset_JRA55.variables['E_cpT'][:,:,0:125]/1000
# latent heat
AMET_E_Lvq_ERAI = dataset_ERAI.variables['E_Lvq'][:]/1000
AMET_E_Lvq_MERRA2 = dataset_MERRA2.variables['E_Lvq'][:]/1000
AMET_E_Lvq_JRA55 = dataset_JRA55.variables['E_Lvq'][:,:,0:125]/1000
# geopotential
AMET_E_gz_ERAI = dataset_ERAI.variables['E_gz'][:]/1000
AMET_E_gz_MERRA2 = dataset_MERRA2.variables['E_gz'][:]/1000
AMET_E_gz_JRA55 = dataset_JRA55.variables['E_gz'][:,:,0:125]/1000
# kinetic energy
AMET_E_uv2_ERAI = dataset_ERAI.variables['E_uv2'][:]/1000
AMET_E_uv2_MERRA2 = dataset_MERRA2.variables['E_uv2'][:]/1000
AMET_E_uv2_JRA55 = dataset_JRA55.variables['E_uv2'][:,:,0:125]/1000

year_ERAI = dataset_ERAI.variables['year'][:]        # from 1979 to 2016
year_MERRA2 = dataset_MERRA2.variables['year'][:]    # from 1980 to 2016
year_JRA55 = dataset_JRA55.variables['year'][:]      # from 1979 to 2015

latitude_ERAI = dataset_ERAI.variables['latitude'][:]
latitude_MERRA2 = dataset_MERRA2.variables['latitude'][:]
latitude_JRA55 = dataset_JRA55.variables['latitude'][0:125]

print '*******************************************************************'
print '*************************** whitening *****************************'
print '*******************************************************************'
# remove the seasonal cycling of AMET
month_ind = np.arange(12)
# dimension of AMET[year,month]
# total energy transport
AMET_E_ERAI_seansonal_cycle = np.mean(AMET_E_ERAI,axis=0)
AMET_E_ERAI_white = np.zeros(AMET_E_ERAI.shape,dtype=float)
for i in np.arange(len(year_ERAI)):
    for j in month_ind:
        AMET_E_ERAI_white[i,j,:] = AMET_E_ERAI[i,j,:] - AMET_E_ERAI_seansonal_cycle[j,:]

AMET_E_MERRA2_seansonal_cycle = np.mean(AMET_E_MERRA2,axis=0)
AMET_E_MERRA2_white = np.zeros(AMET_E_MERRA2.shape,dtype=float)
for i in np.arange(len(year_MERRA2)):
    for j in month_ind:
        AMET_E_MERRA2_white[i,j,:] = AMET_E_MERRA2[i,j,:] - AMET_E_MERRA2_seansonal_cycle[j,:]

AMET_E_JRA55_seansonal_cycle = np.mean(AMET_E_JRA55,axis=0)
AMET_E_JRA55_white = np.zeros(AMET_E_JRA55.shape,dtype=float)
for i in np.arange(len(year_JRA55)):
    for j in month_ind:
        AMET_E_JRA55_white[i,j,:] = AMET_E_JRA55[i,j,:] - AMET_E_JRA55_seansonal_cycle[j,:]

# internal energy
AMET_E_cpT_ERAI_seansonal_cycle = np.mean(AMET_E_cpT_ERAI,axis=0)
AMET_E_cpT_ERAI_white = np.zeros(AMET_E_cpT_ERAI.shape,dtype=float)
for i in np.arange(len(year_ERAI)):
    for j in month_ind:
        AMET_E_cpT_ERAI_white[i,j,:] = AMET_E_cpT_ERAI[i,j,:] - AMET_E_cpT_ERAI_seansonal_cycle[j,:]

AMET_E_cpT_MERRA2_seansonal_cycle = np.mean(AMET_E_cpT_MERRA2,axis=0)
AMET_E_cpT_MERRA2_white = np.zeros(AMET_E_cpT_MERRA2.shape,dtype=float)
for i in np.arange(len(year_MERRA2)):
    for j in month_ind:
        AMET_E_cpT_MERRA2_white[i,j,:] = AMET_E_cpT_MERRA2[i,j,:] - AMET_E_cpT_MERRA2_seansonal_cycle[j,:]

AMET_E_cpT_JRA55_seansonal_cycle = np.mean(AMET_E_cpT_JRA55,axis=0)
AMET_E_cpT_JRA55_white = np.zeros(AMET_E_cpT_JRA55.shape,dtype=float)
for i in np.arange(len(year_JRA55)):
    for j in month_ind:
        AMET_E_cpT_JRA55_white[i,j,:] = AMET_E_cpT_JRA55[i,j,:] - AMET_E_cpT_JRA55_seansonal_cycle[j,:]

# latent heat
AMET_E_Lvq_ERAI_seansonal_cycle = np.mean(AMET_E_Lvq_ERAI,axis=0)
AMET_E_Lvq_ERAI_white = np.zeros(AMET_E_Lvq_ERAI.shape,dtype=float)
for i in np.arange(len(year_ERAI)):
    for j in month_ind:
        AMET_E_Lvq_ERAI_white[i,j,:] = AMET_E_Lvq_ERAI[i,j,:] - AMET_E_Lvq_ERAI_seansonal_cycle[j,:]

AMET_E_Lvq_MERRA2_seansonal_cycle = np.mean(AMET_E_Lvq_MERRA2,axis=0)
AMET_E_Lvq_MERRA2_white = np.zeros(AMET_E_Lvq_MERRA2.shape,dtype=float)
for i in np.arange(len(year_MERRA2)):
    for j in month_ind:
        AMET_E_Lvq_MERRA2_white[i,j,:] = AMET_E_Lvq_MERRA2[i,j,:] - AMET_E_Lvq_MERRA2_seansonal_cycle[j,:]

AMET_E_Lvq_JRA55_seansonal_cycle = np.mean(AMET_E_Lvq_JRA55,axis=0)
AMET_E_Lvq_JRA55_white = np.zeros(AMET_E_Lvq_JRA55.shape,dtype=float)
for i in np.arange(len(year_JRA55)):
    for j in month_ind:
        AMET_E_Lvq_JRA55_white[i,j,:] = AMET_E_Lvq_JRA55[i,j,:] - AMET_E_Lvq_JRA55_seansonal_cycle[j,:]

# geopotential
AMET_E_gz_ERAI_seansonal_cycle = np.mean(AMET_E_gz_ERAI,axis=0)
AMET_E_gz_ERAI_white = np.zeros(AMET_E_gz_ERAI.shape,dtype=float)
for i in np.arange(len(year_ERAI)):
    for j in month_ind:
        AMET_E_gz_ERAI_white[i,j,:] = AMET_E_gz_ERAI[i,j,:] - AMET_E_gz_ERAI_seansonal_cycle[j,:]

AMET_E_gz_MERRA2_seansonal_cycle = np.mean(AMET_E_gz_MERRA2,axis=0)
AMET_E_gz_MERRA2_white = np.zeros(AMET_E_gz_MERRA2.shape,dtype=float)
for i in np.arange(len(year_MERRA2)):
    for j in month_ind:
        AMET_E_gz_MERRA2_white[i,j,:] = AMET_E_gz_MERRA2[i,j,:] - AMET_E_gz_MERRA2_seansonal_cycle[j,:]

AMET_E_gz_JRA55_seansonal_cycle = np.mean(AMET_E_gz_JRA55,axis=0)
AMET_E_gz_JRA55_white = np.zeros(AMET_E_gz_JRA55.shape,dtype=float)
for i in np.arange(len(year_JRA55)):
    for j in month_ind:
        AMET_E_gz_JRA55_white[i,j,:] = AMET_E_gz_JRA55[i,j,:] - AMET_E_gz_JRA55_seansonal_cycle[j,:]

# kinetic energy
AMET_E_uv2_ERAI_seansonal_cycle = np.mean(AMET_E_uv2_ERAI,axis=0)
AMET_E_uv2_ERAI_white = np.zeros(AMET_E_uv2_ERAI.shape,dtype=float)
for i in np.arange(len(year_ERAI)):
    for j in month_ind:
        AMET_E_uv2_ERAI_white[i,j,:] = AMET_E_uv2_ERAI[i,j,:] - AMET_E_uv2_ERAI_seansonal_cycle[j,:]

AMET_E_uv2_MERRA2_seansonal_cycle = np.mean(AMET_E_uv2_MERRA2,axis=0)
AMET_E_uv2_MERRA2_white = np.zeros(AMET_E_uv2_MERRA2.shape,dtype=float)
for i in np.arange(len(year_MERRA2)):
    for j in month_ind:
        AMET_E_uv2_MERRA2_white[i,j,:] = AMET_E_uv2_MERRA2[i,j,:] - AMET_E_uv2_MERRA2_seansonal_cycle[j,:]

AMET_E_uv2_JRA55_seansonal_cycle = np.mean(AMET_E_uv2_JRA55,axis=0)
AMET_E_uv2_JRA55_white = np.zeros(AMET_E_uv2_JRA55.shape,dtype=float)
for i in np.arange(len(year_JRA55)):
    for j in month_ind:
        AMET_E_uv2_JRA55_white[i,j,:] = AMET_E_uv2_JRA55[i,j,:] - AMET_E_uv2_JRA55_seansonal_cycle[j,:]

print '*******************************************************************'
print '*********************** prepare variables *************************'
print '*******************************************************************'
# take the time series of original signal
# total energy transport
AMET_E_ERAI_series = AMET_E_ERAI.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI))
AMET_E_MERRA2_series = AMET_E_MERRA2.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2))
AMET_E_JRA55_series = AMET_E_JRA55.reshape(len(year_JRA55)*len(month_ind),len(latitude_JRA55))
# internal energy
AMET_E_cpT_ERAI_series = AMET_E_cpT_ERAI.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI))
AMET_E_cpT_MERRA2_series = AMET_E_cpT_MERRA2.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2))
AMET_E_cpT_JRA55_series = AMET_E_cpT_JRA55.reshape(len(year_JRA55)*len(month_ind),len(latitude_JRA55))
# latent heat
AMET_E_Lvq_ERAI_series = AMET_E_Lvq_ERAI.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI))
AMET_E_Lvq_MERRA2_series = AMET_E_Lvq_MERRA2.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2))
AMET_E_Lvq_JRA55_series = AMET_E_Lvq_JRA55.reshape(len(year_JRA55)*len(month_ind),len(latitude_JRA55))
# geopotential
AMET_E_gz_ERAI_series = AMET_E_gz_ERAI.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI))
AMET_E_gz_MERRA2_series = AMET_E_gz_MERRA2.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2))
AMET_E_gz_JRA55_series = AMET_E_gz_JRA55.reshape(len(year_JRA55)*len(month_ind),len(latitude_JRA55))
# kinetic energy
AMET_E_uv2_ERAI_series = AMET_E_uv2_ERAI.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI))
AMET_E_uv2_MERRA2_series = AMET_E_uv2_MERRA2.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2))
AMET_E_uv2_JRA55_series = AMET_E_uv2_JRA55.reshape(len(year_JRA55)*len(month_ind),len(latitude_JRA55))

# take the time series of anomalies
AMET_E_ERAI_white_series = AMET_E_ERAI_white.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI))
AMET_E_MERRA2_white_series = AMET_E_MERRA2_white.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2))
AMET_E_JRA55_white_series = AMET_E_JRA55_white.reshape(len(year_JRA55)*len(month_ind),len(latitude_JRA55))
# internal energy
AMET_E_cpT_ERAI_white_series = AMET_E_cpT_ERAI_white.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI))
AMET_E_cpT_MERRA2_white_series = AMET_E_cpT_MERRA2_white.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2))
AMET_E_cpT_JRA55_white_series = AMET_E_cpT_JRA55_white.reshape(len(year_JRA55)*len(month_ind),len(latitude_JRA55))
# latent heat
AMET_E_Lvq_ERAI_white_series = AMET_E_Lvq_ERAI_white.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI))
AMET_E_Lvq_MERRA2_white_series = AMET_E_Lvq_MERRA2_white.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2))
AMET_E_Lvq_JRA55_white_series = AMET_E_Lvq_JRA55_white.reshape(len(year_JRA55)*len(month_ind),len(latitude_JRA55))
# geopotential
AMET_E_gz_ERAI_white_series = AMET_E_gz_ERAI_white.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI))
AMET_E_gz_MERRA2_white_series = AMET_E_gz_MERRA2_white.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2))
AMET_E_gz_JRA55_white_series = AMET_E_gz_JRA55_white.reshape(len(year_JRA55)*len(month_ind),len(latitude_JRA55))
# kinetic energy
AMET_E_uv2_ERAI_white_series = AMET_E_uv2_ERAI_white.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI))
AMET_E_uv2_MERRA2_white_series = AMET_E_uv2_MERRA2_white.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2))
AMET_E_uv2_JRA55_white_series = AMET_E_uv2_JRA55_white.reshape(len(year_JRA55)*len(month_ind),len(latitude_JRA55))
print '*******************************************************************'
print '********************** Running mean/sum ***************************'
print '*******************************************************************'
# running mean is calculated on time series
# define the running window for the running mean
window = 12 # in month
#window = 60 # in month
#window = 120 # in month
# calculate the running mean
# total energy transport
AMET_E_ERAI_running_mean = np.zeros((len(AMET_E_ERAI_series)-window+1,len(latitude_ERAI)),dtype=float)
for i in np.arange(len(AMET_E_ERAI_series)-window+1):
    AMET_E_ERAI_running_mean[i,:] = np.mean(AMET_E_ERAI_series[i:i+window,:],0)

AMET_E_MERRA2_running_mean = np.zeros((len(AMET_E_MERRA2_series)-window+1,len(latitude_MERRA2)),dtype=float)
for i in np.arange(len(AMET_E_MERRA2_series)-window+1):
    AMET_E_MERRA2_running_mean[i,:] = np.mean(AMET_E_MERRA2_series[i:i+window,:],0)

AMET_E_JRA55_running_mean = np.zeros((len(AMET_E_JRA55_series)-window+1,len(latitude_JRA55)),dtype=float)
for i in np.arange(len(AMET_E_JRA55_series)-window+1):
    AMET_E_JRA55_running_mean[i,:] = np.mean(AMET_E_JRA55_series[i:i+window,:],0)

# internal energy
AMET_E_cpT_ERAI_running_mean = np.zeros((len(AMET_E_cpT_ERAI_series)-window+1,len(latitude_ERAI)),dtype=float)
for i in np.arange(len(AMET_E_cpT_ERAI_series)-window+1):
    AMET_E_cpT_ERAI_running_mean[i,:] = np.mean(AMET_E_cpT_ERAI_series[i:i+window,:],0)

AMET_E_cpT_MERRA2_running_mean = np.zeros((len(AMET_E_cpT_MERRA2_series)-window+1,len(latitude_MERRA2)),dtype=float)
for i in np.arange(len(AMET_E_cpT_MERRA2_series)-window+1):
    AMET_E_cpT_MERRA2_running_mean[i,:] = np.mean(AMET_E_cpT_MERRA2_series[i:i+window,:],0)

AMET_E_cpT_JRA55_running_mean = np.zeros((len(AMET_E_cpT_JRA55_series)-window+1,len(latitude_JRA55)),dtype=float)
for i in np.arange(len(AMET_E_cpT_JRA55_series)-window+1):
    AMET_E_cpT_JRA55_running_mean[i,:] = np.mean(AMET_E_cpT_JRA55_series[i:i+window,:],0)

# latent heat
AMET_E_Lvq_ERAI_running_mean = np.zeros((len(AMET_E_Lvq_ERAI_series)-window+1,len(latitude_ERAI)),dtype=float)
for i in np.arange(len(AMET_E_Lvq_ERAI_series)-window+1):
    AMET_E_Lvq_ERAI_running_mean[i,:] = np.mean(AMET_E_Lvq_ERAI_series[i:i+window,:],0)

AMET_E_Lvq_MERRA2_running_mean = np.zeros((len(AMET_E_Lvq_MERRA2_series)-window+1,len(latitude_MERRA2)),dtype=float)
for i in np.arange(len(AMET_E_Lvq_MERRA2_series)-window+1):
    AMET_E_Lvq_MERRA2_running_mean[i,:] = np.mean(AMET_E_Lvq_MERRA2_series[i:i+window,:],0)

AMET_E_Lvq_JRA55_running_mean = np.zeros((len(AMET_E_Lvq_JRA55_series)-window+1,len(latitude_JRA55)),dtype=float)
for i in np.arange(len(AMET_E_Lvq_JRA55_series)-window+1):
    AMET_E_Lvq_JRA55_running_mean[i,:] = np.mean(AMET_E_Lvq_JRA55_series[i:i+window,:],0)

# geopotential
AMET_E_gz_ERAI_running_mean = np.zeros((len(AMET_E_gz_ERAI_series)-window+1,len(latitude_ERAI)),dtype=float)
for i in np.arange(len(AMET_E_gz_ERAI_series)-window+1):
    AMET_E_gz_ERAI_running_mean[i,:] = np.mean(AMET_E_gz_ERAI_series[i:i+window,:],0)

AMET_E_gz_MERRA2_running_mean = np.zeros((len(AMET_E_gz_MERRA2_series)-window+1,len(latitude_MERRA2)),dtype=float)
for i in np.arange(len(AMET_E_gz_MERRA2_series)-window+1):
    AMET_E_gz_MERRA2_running_mean[i,:] = np.mean(AMET_E_gz_MERRA2_series[i:i+window,:],0)

AMET_E_gz_JRA55_running_mean = np.zeros((len(AMET_E_gz_JRA55_series)-window+1,len(latitude_JRA55)),dtype=float)
for i in np.arange(len(AMET_E_gz_JRA55_series)-window+1):
    AMET_E_gz_JRA55_running_mean[i,:] = np.mean(AMET_E_gz_JRA55_series[i:i+window,:],0)

# kinetic energy
AMET_E_uv2_ERAI_running_mean = np.zeros((len(AMET_E_uv2_ERAI_series)-window+1,len(latitude_ERAI)),dtype=float)
for i in np.arange(len(AMET_E_uv2_ERAI_series)-window+1):
    AMET_E_uv2_ERAI_running_mean[i,:] = np.mean(AMET_E_uv2_ERAI_series[i:i+window,:],0)

AMET_E_uv2_MERRA2_running_mean = np.zeros((len(AMET_E_uv2_MERRA2_series)-window+1,len(latitude_MERRA2)),dtype=float)
for i in np.arange(len(AMET_E_uv2_MERRA2_series)-window+1):
    AMET_E_uv2_MERRA2_running_mean[i,:] = np.mean(AMET_E_uv2_MERRA2_series[i:i+window,:],0)

AMET_E_uv2_JRA55_running_mean = np.zeros((len(AMET_E_uv2_JRA55_series)-window+1,len(latitude_JRA55)),dtype=float)
for i in np.arange(len(AMET_E_uv2_JRA55_series)-window+1):
    AMET_E_uv2_JRA55_running_mean[i,:] = np.mean(AMET_E_uv2_JRA55_series[i:i+window,:],0)

# calculate the running mean of AMET after removing the seasonal cycling
# total energy transport
AMET_E_ERAI_white_running_mean = np.zeros((len(AMET_E_ERAI_white_series)-window+1,len(latitude_ERAI)),dtype=float)
for i in np.arange(len(AMET_E_ERAI_white_series)-window+1):
    AMET_E_ERAI_white_running_mean[i,:] = np.mean(AMET_E_ERAI_white_series[i:i+window,:],0)

AMET_E_MERRA2_white_running_mean = np.zeros((len(AMET_E_MERRA2_white_series)-window+1,len(latitude_MERRA2)),dtype=float)
for i in np.arange(len(AMET_E_MERRA2_white_series)-window+1):
    AMET_E_MERRA2_white_running_mean[i,:] = np.mean(AMET_E_MERRA2_white_series[i:i+window,:],0)

AMET_E_JRA55_white_running_mean = np.zeros((len(AMET_E_JRA55_white_series)-window+1,len(latitude_JRA55)),dtype=float)
for i in np.arange(len(AMET_E_JRA55_white_series)-window+1):
    AMET_E_JRA55_white_running_mean[i,:] = np.mean(AMET_E_JRA55_white_series[i:i+window,:],0)

# internal energy
AMET_E_cpT_ERAI_white_running_mean = np.zeros((len(AMET_E_cpT_ERAI_white_series)-window+1,len(latitude_ERAI)),dtype=float)
for i in np.arange(len(AMET_E_cpT_ERAI_white_series)-window+1):
    AMET_E_cpT_ERAI_white_running_mean[i,:] = np.mean(AMET_E_cpT_ERAI_white_series[i:i+window,:],0)

AMET_E_cpT_MERRA2_white_running_mean = np.zeros((len(AMET_E_cpT_MERRA2_white_series)-window+1,len(latitude_MERRA2)),dtype=float)
for i in np.arange(len(AMET_E_cpT_MERRA2_white_series)-window+1):
    AMET_E_cpT_MERRA2_white_running_mean[i,:] = np.mean(AMET_E_cpT_MERRA2_white_series[i:i+window,:],0)

AMET_E_cpT_JRA55_white_running_mean = np.zeros((len(AMET_E_cpT_JRA55_white_series)-window+1,len(latitude_JRA55)),dtype=float)
for i in np.arange(len(AMET_E_cpT_JRA55_white_series)-window+1):
    AMET_E_cpT_JRA55_white_running_mean[i,:] = np.mean(AMET_E_cpT_JRA55_white_series[i:i+window,:],0)

# latent heat
AMET_E_Lvq_ERAI_white_running_mean = np.zeros((len(AMET_E_Lvq_ERAI_white_series)-window+1,len(latitude_ERAI)),dtype=float)
for i in np.arange(len(AMET_E_Lvq_ERAI_white_series)-window+1):
    AMET_E_Lvq_ERAI_white_running_mean[i,:] = np.mean(AMET_E_Lvq_ERAI_white_series[i:i+window,:],0)

AMET_E_Lvq_MERRA2_white_running_mean = np.zeros((len(AMET_E_Lvq_MERRA2_white_series)-window+1,len(latitude_MERRA2)),dtype=float)
for i in np.arange(len(AMET_E_Lvq_MERRA2_white_series)-window+1):
    AMET_E_Lvq_MERRA2_white_running_mean[i,:] = np.mean(AMET_E_Lvq_MERRA2_white_series[i:i+window,:],0)

AMET_E_Lvq_JRA55_white_running_mean = np.zeros((len(AMET_E_Lvq_JRA55_white_series)-window+1,len(latitude_JRA55)),dtype=float)
for i in np.arange(len(AMET_E_Lvq_JRA55_white_series)-window+1):
    AMET_E_Lvq_JRA55_white_running_mean[i,:] = np.mean(AMET_E_Lvq_JRA55_white_series[i:i+window,:],0)

# geopotential
AMET_E_gz_ERAI_white_running_mean = np.zeros((len(AMET_E_gz_ERAI_white_series)-window+1,len(latitude_ERAI)),dtype=float)
for i in np.arange(len(AMET_E_gz_ERAI_white_series)-window+1):
    AMET_E_gz_ERAI_white_running_mean[i,:] = np.mean(AMET_E_gz_ERAI_white_series[i:i+window,:],0)

AMET_E_gz_MERRA2_white_running_mean = np.zeros((len(AMET_E_gz_MERRA2_white_series)-window+1,len(latitude_MERRA2)),dtype=float)
for i in np.arange(len(AMET_E_gz_MERRA2_white_series)-window+1):
    AMET_E_gz_MERRA2_white_running_mean[i,:] = np.mean(AMET_E_gz_MERRA2_white_series[i:i+window,:],0)

AMET_E_gz_JRA55_white_running_mean = np.zeros((len(AMET_E_gz_JRA55_white_series)-window+1,len(latitude_JRA55)),dtype=float)
for i in np.arange(len(AMET_E_gz_JRA55_white_series)-window+1):
    AMET_E_gz_JRA55_white_running_mean[i,:] = np.mean(AMET_E_gz_JRA55_white_series[i:i+window,:],0)

# kinetic energy
AMET_E_uv2_ERAI_white_running_mean = np.zeros((len(AMET_E_uv2_ERAI_white_series)-window+1,len(latitude_ERAI)),dtype=float)
for i in np.arange(len(AMET_E_uv2_ERAI_white_series)-window+1):
    AMET_E_uv2_ERAI_white_running_mean[i,:] = np.mean(AMET_E_uv2_ERAI_white_series[i:i+window,:],0)

AMET_E_uv2_MERRA2_white_running_mean = np.zeros((len(AMET_E_uv2_MERRA2_white_series)-window+1,len(latitude_MERRA2)),dtype=float)
for i in np.arange(len(AMET_E_uv2_MERRA2_white_series)-window+1):
    AMET_E_uv2_MERRA2_white_running_mean[i,:] = np.mean(AMET_E_uv2_MERRA2_white_series[i:i+window,:],0)

AMET_E_uv2_JRA55_white_running_mean = np.zeros((len(AMET_E_uv2_JRA55_white_series)-window+1,len(latitude_JRA55)),dtype=float)
for i in np.arange(len(AMET_E_uv2_JRA55_white_series)-window+1):
    AMET_E_uv2_JRA55_white_running_mean[i,:] = np.mean(AMET_E_uv2_JRA55_white_series[i:i+window,:],0)

print '*******************************************************************'
print '********  standard deviation of monthly mean at each lat   ********'
print '*******************************************************************'
# standard deviation at each latitude
# for error bar band
# reshape of each dataset at full latitude for the calculation of standard deviation
AMET_E_ERAI_std_full = np.std(AMET_E_ERAI_series,axis=0)
AMET_E_ERAI_error_plus = np.mean(np.mean(AMET_E_ERAI,0),0) + AMET_E_ERAI_std_full
AMET_E_ERAI_error_minus = np.mean(np.mean(AMET_E_ERAI,0),0) - AMET_E_ERAI_std_full

AMET_E_MERRA2_std_full = np.std(AMET_E_MERRA2_series,axis=0)
AMET_E_MERRA2_error_plus = np.mean(np.mean(AMET_E_MERRA2,0),0) + AMET_E_MERRA2_std_full
AMET_E_MERRA2_error_minus = np.mean(np.mean(AMET_E_MERRA2,0),0) - AMET_E_MERRA2_std_full

AMET_E_JRA55_std_full = np.std(AMET_E_JRA55_series,axis=0)
AMET_E_JRA55_error_plus = np.mean(np.mean(AMET_E_JRA55,0),0) + AMET_E_JRA55_std_full
AMET_E_JRA55_error_minus = np.mean(np.mean(AMET_E_JRA55,0),0) - AMET_E_JRA55_std_full
print '*******************************************************************'
print '***************   span of annual mean at each lat   ***************'
print '*******************************************************************'
# calculate annual mean
AMET_E_ERAI_annual_mean = np.mean(AMET_E_ERAI,1)
AMET_E_MERRA2_annual_mean = np.mean(AMET_E_MERRA2,1)
AMET_E_JRA55_annual_mean = np.mean(AMET_E_JRA55,1)
# calculate the difference between annual mean and mean of entire time series
AMET_E_ERAI_annual_mean_max = np.amax(AMET_E_ERAI_annual_mean,0)
AMET_E_MERRA2_annual_mean_max = np.amax(AMET_E_MERRA2_annual_mean,0)
AMET_E_JRA55_annual_mean_max = np.amax(AMET_E_JRA55_annual_mean,0)

AMET_E_ERAI_annual_mean_min = np.amin(AMET_E_ERAI_annual_mean,0)
AMET_E_MERRA2_annual_mean_min = np.amin(AMET_E_MERRA2_annual_mean,0)
AMET_E_JRA55_annual_mean_min = np.amin(AMET_E_JRA55_annual_mean,0)
print '*******************************************************************'
print '**************************** X-Y Plot *****************************'
print '*******************************************************************'
# annual mean of meridional energy transport at each latitude in north hemisphere
fig0 = plt.figure()
plt.axhline(y=0, color='k',ls='-')
plt.plot(latitude_ERAI,np.mean(np.mean(AMET_E_ERAI,0),0),'b-',label='ERA-Interim')
plt.fill_between(latitude_ERAI,AMET_E_ERAI_annual_mean_max,AMET_E_ERAI_annual_mean_min,alpha=0.2,edgecolor='lightskyblue', facecolor='lightskyblue')
plt.plot(latitude_MERRA2,np.mean(np.mean(AMET_E_MERRA2,0),0),'r-',label='MERRA2')
plt.fill_between(latitude_MERRA2,AMET_E_MERRA2_annual_mean_max,AMET_E_MERRA2_annual_mean_min,alpha=0.2,edgecolor='tomato', facecolor='tomato')
plt.plot(latitude_JRA55,np.mean(np.mean(AMET_E_JRA55,0),0),'g-',label='JRA55')
plt.fill_between(latitude_JRA55,AMET_E_JRA55_annual_mean_max,AMET_E_JRA55_annual_mean_min,alpha=0.2,edgecolor='lightgreen', facecolor='lightgreen')
plt.title('Mean AMET of entire time series from 20N to 90N' )
plt.legend()
plt.xlabel("Latitudes")
labels =['20','30','40','50','60','70','80','90']
plt.xticks(np.linspace(20, 90, 8),labels)
plt.ylabel("Meridional Energy Transport (PW)")
plt.legend()
plt.show()
fig0.savefig(output_path + os.sep + 'Comp_AMET_annual_mean_E_span.jpg', dpi = 300)


# annual mean of meridional energy transport at each latitude in north hemisphere
fig1 = plt.figure()
plt.axhline(y=0, color='k',ls='-')
plt.plot(latitude_ERAI,np.mean(np.mean(AMET_E_ERAI,0),0),'b-',label='ERA-Interim')
plt.fill_between(latitude_ERAI,AMET_E_ERAI_error_plus,AMET_E_ERAI_error_minus,alpha=0.2,edgecolor='lightskyblue', facecolor='lightskyblue')
plt.plot(latitude_MERRA2,np.mean(np.mean(AMET_E_MERRA2,0),0),'r-',label='MERRA2')
plt.fill_between(latitude_MERRA2,AMET_E_MERRA2_error_plus,AMET_E_MERRA2_error_minus,alpha=0.2,edgecolor='tomato', facecolor='tomato')
plt.plot(latitude_JRA55,np.mean(np.mean(AMET_E_JRA55,0),0),'g-',label='JRA55')
plt.fill_between(latitude_JRA55,AMET_E_JRA55_error_plus,AMET_E_JRA55_error_minus,alpha=0.2,edgecolor='lightgreen', facecolor='lightgreen')
plt.title('Mean AMET of entire time series from 20N to 90N' )
plt.legend()
plt.xlabel("Latitudes")
labels =['20','30','40','50','60','70','80','90']
plt.xticks(np.linspace(20, 90, 8),labels)
plt.ylabel("Meridional Energy Transport (PW)")
plt.legend()
plt.show()
fig1.savefig(output_path + os.sep + 'Comp_AMET_annual_mean_E_stdBar.jpg', dpi = 300)
plt.close(fig1)

# annual mean of meridional energy transport and each component at each latitude in north hemisphere
fig2 = plt.figure()
plt.axhline(y=0, color='k',ls='-')
plt.plot(latitude_ERAI,np.mean(np.mean(AMET_E_ERAI,0),0),'b-',label='ERA total')
plt.plot(latitude_MERRA2,np.mean(np.mean(AMET_E_MERRA2,0),0),'b--',label='MERRA total')
plt.plot(latitude_JRA55,np.mean(np.mean(AMET_E_JRA55,0),0),'b-.',label='JRA total')
plt.plot(latitude_ERAI,np.mean(np.mean(AMET_E_cpT_ERAI,0),0),'r-',label='ERA cpT')
plt.plot(latitude_MERRA2,np.mean(np.mean(AMET_E_cpT_MERRA2,0),0),'r--',label='MERRA cpT')
plt.plot(latitude_JRA55,np.mean(np.mean(AMET_E_cpT_JRA55,0),0),'r-.',label='JRA cpT')
plt.plot(latitude_ERAI,np.mean(np.mean(AMET_E_Lvq_ERAI,0),0),'m-',label='ERA Lvq')
plt.plot(latitude_MERRA2,np.mean(np.mean(AMET_E_Lvq_MERRA2,0),0),'m--',label='MERRA Lvq')
plt.plot(latitude_JRA55,np.mean(np.mean(AMET_E_Lvq_JRA55,0),0),'m-.',label='JRA Lvq')
plt.plot(latitude_ERAI,np.mean(np.mean(AMET_E_gz_ERAI,0),0),'g-',label='ERA gz')
plt.plot(latitude_MERRA2,np.mean(np.mean(AMET_E_gz_MERRA2,0),0),'g--',label='MERRA gz')
plt.plot(latitude_JRA55,np.mean(np.mean(AMET_E_gz_JRA55,0),0),'g-.',label='JRA gz')
plt.plot(latitude_ERAI,np.mean(np.mean(AMET_E_uv2_ERAI,0),0),'c-',label='ERA uv2')
plt.plot(latitude_MERRA2,np.mean(np.mean(AMET_E_uv2_MERRA2,0),0),'c--',label='MERRA uv2')
plt.plot(latitude_JRA55,np.mean(np.mean(AMET_E_uv2_JRA55,0),0),'c-.',label='JRA uv2')
plt.title('Annual Mean of Atmospheric Meridional Energy Transport and Each Component' )
plt.legend()
fig2.set_size_inches(10, 8)
plt.xlabel("Latitudes")
labels =['20','30','40','50','60','70','80','90']
plt.xticks(np.linspace(20, 90, 8),labels)
plt.ylabel("Meridional Energy Transport (PW)")
plt.legend()
plt.show()
fig2.savefig(output_path + os.sep + 'Comp_AMET_annual_mean_full_components.jpg',dpi = 300)
plt.close(fig2)
print '*******************************************************************'
print '******************    trend at each latitude    *******************'
print '*******************************************************************'
counter_ERAI = np.arange(len(year_ERAI)*len(month_ind))
counter_MERRA2 = np.arange(len(year_MERRA2)*len(month_ind))
counter_JRA55 = np.arange(len(year_JRA55)*len(month_ind))
# the calculation of trend are based on target climatolory after removing seasonal cycles
# trend of OMET at each lat
# create an array to store the slope coefficient and residual
a_ERAI = np.zeros((len(latitude_ERAI)),dtype = float)
b_ERAI = np.zeros((len(latitude_ERAI)),dtype = float)
# the least square fit equation is y = ax + b
# np.lstsq solves the equation ax=b, a & b are the input
# thus the input file should be reformed for the function
# we can rewrite the line y = Ap, with A = [x,1] and p = [[a],[b]]
A_ERAI = np.vstack([counter_ERAI,np.ones(len(counter_ERAI))]).T
# start the least square fitting
for i in np.arange(len(latitude_ERAI)):
        # return value: coefficient matrix a and b, where a is the slope
        a_ERAI[i], b_ERAI[i] = np.linalg.lstsq(A_ERAI,AMET_E_ERAI_white_series[:,i])[0]

a_MERRA2 = np.zeros((len(latitude_MERRA2)),dtype = float)
b_MERRA2 = np.zeros((len(latitude_MERRA2)),dtype = float)
A_MERRA2 = np.vstack([counter_MERRA2,np.ones(len(counter_MERRA2))]).T
for i in np.arange(len(latitude_MERRA2)):
        a_MERRA2[i], b_MERRA2[i] = np.linalg.lstsq(A_MERRA2,AMET_E_MERRA2_white_series[:,i])[0]

a_JRA55 = np.zeros((len(latitude_JRA55)),dtype = float)
b_JRA55 = np.zeros((len(latitude_JRA55)),dtype = float)
A_JRA55 = np.vstack([counter_JRA55,np.ones(len(counter_JRA55))]).T
for i in np.arange(len(latitude_JRA55)):
        a_JRA55[i], b_JRA55[i] = np.linalg.lstsq(A_JRA55,AMET_E_JRA55_white_series[:,i])[0]

# trend of AMET anomalies at each latitude
fig19 = plt.figure()
plt.axhline(y=0, color='k',ls='-')
plt.plot(latitude_ERAI,a_ERAI*12,'b-',label='ERAI')
plt.plot(latitude_MERRA2,a_MERRA2*12,'r-',label='MERRA2')
plt.plot(latitude_JRA55,a_JRA55*12,'g-',label='JRA55')
plt.title('Trend of AMET anomalies from 20N to 90N' )
#plt.legend()
plt.xlabel("Latitudes")
#plt.xticks()
plt.ylabel("Meridional Energy Transport (PW/year)")
plt.legend()
plt.show()
fig19.savefig(output_path + os.sep + 'Comp_AMET_white_trend.jpg', dpi = 400)
print '*******************************************************************'
print '*************************** time series ***************************'
print '*******************************************************************'
index_1980_2016 = np.arange(13,457,1)
index_1979_2016 = np.arange(1,457,1)
index_1979_2015 = np.arange(1,445,1)
index_1980_2015 = np.arange(1,433,1)

# plot the AMET with running mean
# total energy transport
for i in np.arange(len(lat_interest_list)):
    fig3 = plt.figure()
    plt.plot(index_1979_2016,AMET_E_ERAI_series[:,lat_interest['ERAI'][i]],'b--',linewidth=1.0,label='ERAI time series')
    plt.plot(index_1980_2016,AMET_E_MERRA2_series[:,lat_interest['MERRA2'][i]],'r--',linewidth=1.0,label='MERRA2 time series')
    plt.plot(index_1979_2015,AMET_E_JRA55_series[:,lat_interest['JRA55'][i]],'g--',linewidth=1.0,label='JRA55 time series')
    plt.plot(index_1979_2016[window-1:],AMET_E_ERAI_running_mean[:,lat_interest['ERAI'][i]],'b-',linewidth=2.0,label='ERAI low pass')
    plt.plot(index_1980_2016[window-1:],AMET_E_MERRA2_running_mean[:,lat_interest['MERRA2'][i]],'r-',linewidth=2.0,label='MERRA2 low pass')
    plt.plot(index_1979_2015[window-1:],AMET_E_JRA55_running_mean[:,lat_interest['JRA55'][i]],'g-',linewidth=2.0,label='JRA55 low pass')
    plt.title('Running Mean of AMET at %dN with a window of %d months' % (lat_interest_list[i],window))
    plt.legend()
    fig3.set_size_inches(12.5, 6)
    plt.xlabel("Time")
    plt.xticks(np.linspace(0, 456, 39), year_ERAI)
    plt.xticks(rotation=60)
    plt.ylabel("Meridional Energy Transport (PW)")
    plt.legend()
    plt.show()
    fig3.savefig(output_path + os.sep + 'original_series_lowpass' + os.sep + 'Comp_AMET_E_%dN_running_mean_window_%d_comp.jpg' % (lat_interest_list[i],window), dpi = 300)
    plt.close(fig3)

# internal energy
for i in np.arange(len(lat_interest_list)):
    fig4 = plt.figure()
    plt.plot(index_1979_2016,AMET_E_cpT_ERAI_series[:,lat_interest['ERAI'][i]],'b--',linewidth=1.0,label='ERAI time series')
    plt.plot(index_1980_2016,AMET_E_cpT_MERRA2_series[:,lat_interest['MERRA2'][i]],'r--',linewidth=1.0,label='MERRA2 time series')
    plt.plot(index_1979_2015,AMET_E_cpT_JRA55_series[:,lat_interest['JRA55'][i]],'g--',linewidth=1.0,label='JRA55 time series')
    plt.plot(index_1979_2016[window-1:],AMET_E_cpT_ERAI_running_mean[:,lat_interest['ERAI'][i]],'b-',linewidth=2.0,label='ERAI low pass')
    plt.plot(index_1980_2016[window-1:],AMET_E_cpT_MERRA2_running_mean[:,lat_interest['MERRA2'][i]],'r-',linewidth=2.0,label='MERRA2 low pass')
    plt.plot(index_1979_2015[window-1:],AMET_E_cpT_JRA55_running_mean[:,lat_interest['JRA55'][i]],'g-',linewidth=2.0,label='JRA55 low pass')
    plt.title('Running Mean of AMET (cpT) at %dN with a window of %d months' % (lat_interest_list[i],window))
    plt.legend()
    fig4.set_size_inches(12.5, 6)
    plt.xlabel("Time")
    plt.xticks(np.linspace(0, 456, 39), year_ERAI)
    plt.xticks(rotation=60)
    plt.ylabel("Meridional Energy Transport (PW)")
    plt.legend()
    plt.show()
    fig4.savefig(output_path + os.sep + 'original_series_lowpass' + os.sep + 'Comp_AMET_cpT_%dN_running_mean_window_%d_comp.jpg' % (lat_interest_list[i],window), dpi = 300)
    plt.close(fig4)

# latent heat
for i in np.arange(len(lat_interest_list)):
    fig5 = plt.figure()
    plt.plot(index_1979_2016,AMET_E_Lvq_ERAI_series[:,lat_interest['ERAI'][i]],'b--',linewidth=1.0,label='ERAI time series')
    plt.plot(index_1980_2016,AMET_E_Lvq_MERRA2_series[:,lat_interest['MERRA2'][i]],'r--',linewidth=1.0,label='MERRA2 time series')
    plt.plot(index_1979_2015,AMET_E_Lvq_JRA55_series[:,lat_interest['JRA55'][i]],'g--',linewidth=1.0,label='JRA55 time series')
    plt.plot(index_1979_2016[window-1:],AMET_E_Lvq_ERAI_running_mean[:,lat_interest['ERAI'][i]],'b-',linewidth=2.0,label='ERAI low pass')
    plt.plot(index_1980_2016[window-1:],AMET_E_Lvq_MERRA2_running_mean[:,lat_interest['MERRA2'][i]],'r-',linewidth=2.0,label='MERRA2 low pass')
    plt.plot(index_1979_2015[window-1:],AMET_E_Lvq_JRA55_running_mean[:,lat_interest['JRA55'][i]],'g-',linewidth=2.0,label='JRA55 low pass')
    plt.title('Running Mean of AMET (Lvq) at %dN with a window of %d months' % (lat_interest_list[i],window))
    plt.legend()
    fig5.set_size_inches(12.5, 6)
    plt.xlabel("Time")
    plt.xticks(np.linspace(0, 456, 39), year_ERAI)
    plt.xticks(rotation=60)
    plt.ylabel("Meridional Energy Transport (PW)")
    plt.legend()
    plt.show()
    fig5.savefig(output_path + os.sep + 'original_series_lowpass' + os.sep + 'Comp_AMET_E_Lvq_%dN_running_mean_window_%d_comp.jpg' % (lat_interest_list[i],window), dpi = 300)
    plt.close(fig5)

# geopotential
for i in np.arange(len(lat_interest_list)):
    fig6 = plt.figure()
    plt.plot(index_1979_2016,AMET_E_gz_ERAI_series[:,lat_interest['ERAI'][i]],'b--',linewidth=1.0,label='ERAI time series')
    plt.plot(index_1980_2016,AMET_E_gz_MERRA2_series[:,lat_interest['MERRA2'][i]],'r--',linewidth=1.0,label='MERRA2 time series')
    plt.plot(index_1979_2015,AMET_E_gz_JRA55_series[:,lat_interest['JRA55'][i]],'g--',linewidth=1.0,label='JRA55 time series')
    plt.plot(index_1979_2016[window-1:],AMET_E_gz_ERAI_running_mean[:,lat_interest['ERAI'][i]],'b-',linewidth=2.0,label='ERAI low pass')
    plt.plot(index_1980_2016[window-1:],AMET_E_gz_MERRA2_running_mean[:,lat_interest['MERRA2'][i]],'r-',linewidth=2.0,label='MERRA2 low pass')
    plt.plot(index_1979_2015[window-1:],AMET_E_gz_JRA55_running_mean[:,lat_interest['JRA55'][i]],'g-',linewidth=2.0,label='JRA55 low pass')
    plt.title('Running Mean of AMET (gz) at %dN with a window of %d months' % (lat_interest_list[i],window))
    plt.legend()
    fig6.set_size_inches(12.5, 6)
    plt.xlabel("Time")
    plt.xticks(np.linspace(0, 456, 39), year_ERAI)
    plt.xticks(rotation=60)
    plt.ylabel("Meridional Energy Transport (PW)")
    plt.legend()
    plt.show()
    fig6.savefig(output_path + os.sep + 'original_series_lowpass' + os.sep + 'Comp_AMET_E_gz_%dN_running_mean_window_%d_comp.jpg' % (lat_interest_list[i],window), dpi = 300)
    plt.close(fig6)

# kinetic energy
for i in np.arange(len(lat_interest_list)):
    fig7 = plt.figure()
    plt.plot(index_1979_2016,AMET_E_uv2_ERAI_series[:,lat_interest['ERAI'][i]],'b--',linewidth=1.0,label='ERAI time series')
    plt.plot(index_1980_2016,AMET_E_uv2_MERRA2_series[:,lat_interest['MERRA2'][i]],'r--',linewidth=1.0,label='MERRA2 time series')
    plt.plot(index_1979_2015,AMET_E_uv2_JRA55_series[:,lat_interest['JRA55'][i]],'g--',linewidth=1.0,label='JRA55 time series')
    plt.plot(index_1979_2016[window-1:],AMET_E_uv2_ERAI_running_mean[:,lat_interest['ERAI'][i]],'b-',linewidth=2.0,label='ERAI low pass')
    plt.plot(index_1980_2016[window-1:],AMET_E_uv2_MERRA2_running_mean[:,lat_interest['MERRA2'][i]],'r-',linewidth=2.0,label='MERRA2 low pass')
    plt.plot(index_1979_2015[window-1:],AMET_E_uv2_JRA55_running_mean[:,lat_interest['JRA55'][i]],'g-',linewidth=2.0,label='JRA55 low pass')
    plt.title('Running Mean of AMET (uv2) at %dN with a window of %d months' % (lat_interest_list[i],window))
    plt.legend()
    fig7.set_size_inches(12.5, 6)
    plt.xlabel("Time")
    plt.xticks(np.linspace(0, 456, 39), year_ERAI)
    plt.xticks(rotation=60)
    plt.ylabel("Meridional Energy Transport (PW)")
    plt.legend()
    plt.show()
    fig7.savefig(output_path + os.sep + 'original_series_lowpass' + os.sep + 'Comp_AMET_E_uv2_%dN_running_mean_window_%d_comp.jpg' % (lat_interest_list[i],window), dpi = 300)
    plt.close(fig7)

# plot the AMET after removing the seasonal cycling with running mean
for i in np.arange(len(lat_interest_list)):
    fig8 = plt.figure()
    plt.plot(index_1979_2016,AMET_E_ERAI_white_series[:,lat_interest['ERAI'][i]],'b--',linewidth=1.0,label='ERAI time series')
    plt.plot(index_1980_2016,AMET_E_MERRA2_white_series[:,lat_interest['MERRA2'][i]],'r--',linewidth=1.0,label='MERRA2 time series')
    plt.plot(index_1979_2015,AMET_E_JRA55_white_series[:,lat_interest['JRA55'][i]],'g--',linewidth=1.0,label='JRA55 time series')
    plt.plot(index_1979_2016[window-1:],AMET_E_ERAI_white_running_mean[:,lat_interest['ERAI'][i]],'b-',linewidth=2.0,label='ERAI low pass')
    plt.plot(index_1980_2016[window-1:],AMET_E_MERRA2_white_running_mean[:,lat_interest['MERRA2'][i]],'r-',linewidth=2.0,label='MERRA2 low pass')
    plt.plot(index_1979_2015[window-1:],AMET_E_JRA55_white_running_mean[:,lat_interest['JRA55'][i]],'g-',linewidth=2.0,label='JRA55 low pass')
    plt.title('Running Mean of AMET Anomalies at %dN with a window of %d months' % (lat_interest_list[i],window))
    plt.legend()
    fig8.set_size_inches(12.5, 6)
    plt.xlabel("Time")
    plt.xticks(np.linspace(0, 456, 39), year_ERAI)
    plt.xticks(rotation=60)
    plt.ylabel("Meridional Energy Transport (PW)")
    plt.legend()
    plt.show()
    fig8.savefig(output_path + os.sep + 'anomaly_series_lowpass' + os.sep + 'Comp_AMET_E_anomaly_%dN_running_mean_window_%d_comp.jpg' % (lat_interest_list[i],window), dpi = 300)
    plt.close(fig8)

#internal energy
for i in np.arange(len(lat_interest_list)):
    fig9 = plt.figure()
    plt.plot(index_1979_2016,AMET_E_cpT_ERAI_white_series[:,lat_interest['ERAI'][i]],'b--',linewidth=1.0,label='ERAI time series')
    plt.plot(index_1980_2016,AMET_E_cpT_MERRA2_white_series[:,lat_interest['MERRA2'][i]],'r--',linewidth=1.0,label='MERRA2 time series')
    plt.plot(index_1979_2015,AMET_E_cpT_JRA55_white_series[:,lat_interest['JRA55'][i]],'g--',linewidth=1.0,label='JRA55 time series')
    plt.plot(index_1979_2016[window-1:],AMET_E_cpT_ERAI_white_running_mean[:,lat_interest['ERAI'][i]],'b-',linewidth=2.0,label='ERAI low pass')
    plt.plot(index_1980_2016[window-1:],AMET_E_cpT_MERRA2_white_running_mean[:,lat_interest['MERRA2'][i]],'r-',linewidth=2.0,label='MERRA2 low pass')
    plt.plot(index_1979_2015[window-1:],AMET_E_cpT_JRA55_white_running_mean[:,lat_interest['JRA55'][i]],'g-',linewidth=2.0,label='JRA55 low pass')
    plt.title('Running Mean of AMET (cpT) Anomalies at %dN with a window of %d months' % (lat_interest_list[i],window))
    plt.legend()
    fig9.set_size_inches(12.5, 6)
    plt.xlabel("Time")
    plt.xticks(np.linspace(0, 456, 39), year_ERAI)
    plt.xticks(rotation=60)
    plt.ylabel("Meridional Energy Transport (PW)")
    plt.legend()
    plt.show()
    fig9.savefig(output_path + os.sep + 'anomaly_series_lowpass' + os.sep +'Comp_AMET_E_cpT_anomaly_%dN_running_mean_window_%d_comp.jpg' % (lat_interest_list[i],window), dpi = 300)
    plt.close(fig9)

# latent heat
for i in np.arange(len(lat_interest_list)):
    fig10 = plt.figure()
    plt.plot(index_1979_2016,AMET_E_Lvq_ERAI_white_series[:,lat_interest['ERAI'][i]],'b--',linewidth=1.0,label='ERAI time series')
    plt.plot(index_1980_2016,AMET_E_Lvq_MERRA2_white_series[:,lat_interest['MERRA2'][i]],'r--',linewidth=1.0,label='MERRA2 time series')
    plt.plot(index_1979_2015,AMET_E_Lvq_JRA55_white_series[:,lat_interest['JRA55'][i]],'g--',linewidth=1.0,label='JRA55 time series')
    plt.plot(index_1979_2016[window-1:],AMET_E_Lvq_ERAI_white_running_mean[:,lat_interest['ERAI'][i]],'b-',linewidth=2.0,label='ERAI low pass')
    plt.plot(index_1980_2016[window-1:],AMET_E_Lvq_MERRA2_white_running_mean[:,lat_interest['MERRA2'][i]],'r-',linewidth=2.0,label='MERRA2 low pass')
    plt.plot(index_1979_2015[window-1:],AMET_E_Lvq_JRA55_white_running_mean[:,lat_interest['JRA55'][i]],'g-',linewidth=2.0,label='JRA55 low pass')
    plt.title('Running Mean of AMET (Lvq) Anomalies at %dN with a window of %d months' % (lat_interest_list[i],window))
    plt.legend()
    fig10.set_size_inches(12.5, 6)
    plt.xlabel("Time")
    plt.xticks(np.linspace(0, 456, 39), year_ERAI)
    plt.xticks(rotation=60)
    plt.ylabel("Meridional Energy Transport (PW)")
    plt.legend()
    plt.show()
    fig10.savefig(output_path + os.sep + 'anomaly_series_lowpass' + os.sep +'Comp_AMET_E_Lvq_anomaly_%dN_running_mean_window_%d_comp.jpg' % (lat_interest_list[i],window), dpi = 300)
    plt.close(fig10)

# geopotential
for i in np.arange(len(lat_interest_list)):
    fig11 = plt.figure()
    plt.plot(index_1979_2016,AMET_E_gz_ERAI_white_series[:,lat_interest['ERAI'][i]],'b--',linewidth=1.0,label='ERAI time series')
    plt.plot(index_1980_2016,AMET_E_gz_MERRA2_white_series[:,lat_interest['MERRA2'][i]],'r--',linewidth=1.0,label='MERRA2 time series')
    plt.plot(index_1979_2015,AMET_E_gz_JRA55_white_series[:,lat_interest['JRA55'][i]],'g--',linewidth=1.0,label='JRA55 time series')
    plt.plot(index_1979_2016[window-1:],AMET_E_gz_ERAI_white_running_mean[:,lat_interest['ERAI'][i]],'b-',linewidth=2.0,label='ERAI low pass')
    plt.plot(index_1980_2016[window-1:],AMET_E_gz_MERRA2_white_running_mean[:,lat_interest['MERRA2'][i]],'r-',linewidth=2.0,label='MERRA2 low pass')
    plt.plot(index_1979_2015[window-1:],AMET_E_gz_JRA55_white_running_mean[:,lat_interest['JRA55'][i]],'g-',linewidth=2.0,label='JRA55 low pass')
    plt.title('Running Mean of AMET (gz) Anomalies at %dN with a window of %d months' % (lat_interest_list[i],window))
    plt.legend()
    fig11.set_size_inches(12.5, 6)
    plt.xlabel("Time")
    plt.xticks(np.linspace(0, 456, 39), year_ERAI)
    plt.xticks(rotation=60)
    plt.ylabel("Meridional Energy Transport (PW)")
    plt.legend()
    plt.show()
    fig11.savefig(output_path + os.sep + 'anomaly_series_lowpass' + os.sep + 'Comp_AMET_E_gz_anomaly_%dN_running_mean_window_%d_comp.jpg' % (lat_interest_list[i],window), dpi = 300)
    plt.close(fig11)

# kinetic energy
for i in np.arange(len(lat_interest_list)):
    fig12 = plt.figure()
    plt.plot(index_1979_2016,AMET_E_uv2_ERAI_white_series[:,lat_interest['ERAI'][i]],'b--',linewidth=1.0,label='ERAI time series')
    plt.plot(index_1980_2016,AMET_E_uv2_MERRA2_white_series[:,lat_interest['MERRA2'][i]],'r--',linewidth=1.0,label='MERRA2 time series')
    plt.plot(index_1979_2015,AMET_E_uv2_JRA55_white_series[:,lat_interest['JRA55'][i]],'g--',linewidth=1.0,label='JRA55 time series')
    plt.plot(index_1979_2016[window-1:],AMET_E_uv2_ERAI_white_running_mean[:,lat_interest['ERAI'][i]],'b-',linewidth=2.0,label='ERAI low pass')
    plt.plot(index_1980_2016[window-1:],AMET_E_uv2_MERRA2_white_running_mean[:,lat_interest['MERRA2'][i]],'r-',linewidth=2.0,label='MERRA2 low pass')
    plt.plot(index_1979_2015[window-1:],AMET_E_uv2_JRA55_white_running_mean[:,lat_interest['JRA55'][i]],'g-',linewidth=2.0,label='JRA55 low pass')
    plt.title('Running Mean of AMET (uv2) Anomalies at %dN with a window of %d months' % (lat_interest_list[i],window))
    plt.legend()
    fig12.set_size_inches(12.5, 6)
    plt.xlabel("Time")
    plt.xticks(np.linspace(0, 456, 39), year_ERAI)
    plt.xticks(rotation=60)
    plt.ylabel("Meridional Energy Transport (PW)")
    plt.legend()
    plt.show()
    fig12.savefig(output_path + os.sep + 'anomaly_series_lowpass' + os.sep +'Comp_AMET_E_uv2_anomaly_%dN_running_mean_window_%d_comp.jpg' % (lat_interest_list[i],window), dpi = 300)
    plt.close(fig12)

print '*******************************************************************'
print '*************   3D time series of AMET at key lats   **************'
print '*******************************************************************'

fig33=plt.figure()
#fig33.set_size_inches(12.5, 6)
ax=fig33.gca(projection='3d') # change figure into 3D
plt.hold(True)
for i in np.arange(len(lat_interest_list)):
    #ax.plot(index_1979_2016,np.ones(index_1979_2016.shape,dtype=int)*i,AMET_E_ERAI_series[:,lat_interest['ERAI'][i]],'b--',linewidth=1.0,label='ERAI time series at %d N' % (i))
    #ax.plot(index_1980_2016,np.ones(index_1980_2016.shape,dtype=int)*i,AMET_E_MERRA2_series[:,lat_interest['MERRA2'][i]],'r--',linewidth=1.0,label='MERRA2 time series')
    #ax.plot(index_1979_2015,np.ones(index_1979_2015.shape,dtype=int)*i,AMET_E_JRA55_series[:,lat_interest['JRA55'][i]],'g--',linewidth=1.0,label='JRA55 time series')
    ax.plot(index_1979_2016[window-1:],np.ones(index_1979_2016[window-1:].shape,dtype=int)*i,AMET_E_ERAI_running_mean[:,lat_interest['ERAI'][i]],'b-',linewidth=2.0,label='ERAI low pass')
    ax.plot(index_1980_2016[window-1:],np.ones(index_1980_2016[window-1:].shape,dtype=int)*i,AMET_E_MERRA2_running_mean[:,lat_interest['MERRA2'][i]],'r-',linewidth=2.0,label='MERRA2 low pass')
    ax.plot(index_1979_2015[window-1:],np.ones(index_1979_2015[window-1:].shape,dtype=int)*i,AMET_E_JRA55_running_mean[:,lat_interest['JRA55'][i]],'g-',linewidth=2.0,label='JRA55 low pass')
#ax.grid()
ax.set_xlabel("Time")
ax.set_xticks(np.linspace(0, 456, 39), year_ERAI.all)
ax.set_ylabel("Latitude (N)")
ax.set_zlabel("Meridional Energy Transport (PW)")
ax.view_init(30,220)
plt.title("AMET at key latitudes")
plt.legend()
plt.show()
fig33.savefig(output_path + os.sep + 'Comp_AMET_E_3D.jpg', dpi = 300)
#plt.close(fig33)
print '*******************************************************************'
print '******************   highlight the difference   *******************'
print '*******************************************************************'
#calculate the differnce between datasets for each component
#ERA-Interim minus MERRA2
for i in np.arange(len(lat_interest_list)):
    fig13 = plt.figure()
    plt.plot(index_1980_2016,AMET_E_ERAI_series[12:,lat_interest['ERAI'][i]] - AMET_E_MERRA2_series[:,lat_interest['MERRA2'][i]],'b-',linewidth=1.0,label='Total')
    plt.plot(index_1980_2016,AMET_E_cpT_ERAI_series[12:,lat_interest['ERAI'][i]] - AMET_E_cpT_MERRA2_series[:,lat_interest['MERRA2'][i]],'r-',linewidth=1.0,label='cpT')
    plt.plot(index_1980_2016,AMET_E_Lvq_ERAI_series[12:,lat_interest['ERAI'][i]] - AMET_E_Lvq_MERRA2_series[:,lat_interest['MERRA2'][i]],'m-',linewidth=1.0,label='Lvq')
    plt.plot(index_1980_2016,AMET_E_gz_ERAI_series[12:,lat_interest['ERAI'][i]] - AMET_E_gz_MERRA2_series[:,lat_interest['MERRA2'][i]],'g-',linewidth=1.0,label='gz')
    plt.plot(index_1980_2016,AMET_E_uv2_ERAI_series[12:,lat_interest['ERAI'][i]] - AMET_E_uv2_MERRA2_series[:,lat_interest['MERRA2'][i]],'c-',linewidth=1.0,label='uv2')
    plt.title('Difference between ERA-Interim and MERRA2 (time series) at %dN' % (lat_interest_list[i]))
    plt.legend()
    fig13.set_size_inches(12.5, 6)
    plt.xlabel("Time")
    plt.xticks(np.linspace(0, 444, 38), year_MERRA2)
    plt.xticks(rotation=60)
    plt.ylabel("Meridional Energy Transport residual (PW)")
    plt.legend()
    plt.show()
    fig13.savefig(output_path + os.sep + 'original_minus' + os.sep + 'Comp_AMET_ERAI_minus_MERRA2_%dN.jpg' % (lat_interest_list[i]), dpi = 300)


for i in np.arange(len(lat_interest_list)):
    fig14 = plt.figure()
    plt.plot(index_1980_2016,AMET_E_ERAI_white_series[12:,lat_interest['ERAI'][i]] - AMET_E_MERRA2_white_series[:,lat_interest['MERRA2'][i]],'b-',linewidth=1.0,label='Total')
    plt.plot(index_1980_2016,AMET_E_cpT_ERAI_white_series[12:,lat_interest['ERAI'][i]] - AMET_E_cpT_MERRA2_white_series[:,lat_interest['MERRA2'][i]],'r-',linewidth=1.0,label='cpT')
    plt.plot(index_1980_2016,AMET_E_Lvq_ERAI_white_series[12:,lat_interest['ERAI'][i]] - AMET_E_Lvq_MERRA2_white_series[:,lat_interest['MERRA2'][i]],'m-',linewidth=1.0,label='Lvq')
    plt.plot(index_1980_2016,AMET_E_gz_ERAI_white_series[12:,lat_interest['ERAI'][i]] - AMET_E_gz_MERRA2_white_series[:,lat_interest['MERRA2'][i]],'g-',linewidth=1.0,label='gz')
    plt.plot(index_1980_2016,AMET_E_uv2_ERAI_white_series[12:,lat_interest['ERAI'][i]] - AMET_E_uv2_MERRA2_white_series[:,lat_interest['MERRA2'][i]],'c-',linewidth=1.0,label='uv2')
    plt.title('Difference between ERA-Interim and MERRA2 anomalies (time series) at %dN' % (lat_interest_list[i]))
    plt.legend()
    fig14.set_size_inches(12.5, 6)
    plt.xlabel("Time")
    plt.xticks(np.linspace(0, 444, 38), year_MERRA2)
    plt.xticks(rotation=60)
    plt.ylabel("Meridional Energy Transport residual (PW)")
    plt.legend()
    plt.show()
    fig14.savefig(output_path + os.sep + 'anomaly_minus' + os.sep + 'Comp_AMET_ERAI_minus_MERRA2_anomaly_%dN.jpg' % (lat_interest_list[i]), dpi = 300)
    plt.close(fig14)

#ERA-Interim minus JRA55
for i in np.arange(len(lat_interest_list)):
    fig15 = plt.figure()
    plt.plot(index_1979_2015,AMET_E_ERAI_series[:-12,lat_interest['ERAI'][i]] - AMET_E_JRA55_series[:,lat_interest['JRA55'][i]],'b-',linewidth=1.0,label='Total')
    plt.plot(index_1979_2015,AMET_E_cpT_ERAI_series[:-12,lat_interest['ERAI'][i]] - AMET_E_cpT_JRA55_series[:,lat_interest['JRA55'][i]],'r-',linewidth=1.0,label='cpT')
    plt.plot(index_1979_2015,AMET_E_Lvq_ERAI_series[:-12,lat_interest['ERAI'][i]] - AMET_E_Lvq_JRA55_series[:,lat_interest['JRA55'][i]],'m-',linewidth=1.0,label='Lvq')
    plt.plot(index_1979_2015,AMET_E_gz_ERAI_series[:-12,lat_interest['ERAI'][i]] - AMET_E_gz_JRA55_series[:,lat_interest['JRA55'][i]],'g-',linewidth=1.0,label='gz')
    plt.plot(index_1979_2015,AMET_E_uv2_ERAI_series[:-12,lat_interest['ERAI'][i]] - AMET_E_uv2_JRA55_series[:,lat_interest['JRA55'][i]],'c-',linewidth=1.0,label='uv2')
    plt.title('Difference between ERA-Interim and JRA55 (time series) at %dN' % (lat_interest_list[i]))
    plt.legend()
    fig15.set_size_inches(12.5, 6)
    plt.xlabel("Time")
    plt.xticks(np.linspace(0, 444, 38), year_JRA55)
    plt.xticks(rotation=60)
    plt.ylabel("Meridional Energy Transport residual (PW)")
    plt.legend()
    plt.show()
    fig15.savefig(output_path + os.sep + 'original_minus' + os.sep + 'Comp_AMET_ERAI_minus_JRA55_%dN.jpg' % (lat_interest_list[i]), dpi = 300)
    plt.close(fig15)

for i in np.arange(len(lat_interest_list)):
    fig16 = plt.figure()
    plt.plot(index_1979_2015,AMET_E_ERAI_white_series[:-12,lat_interest['ERAI'][i]] - AMET_E_JRA55_white_series[:,lat_interest['JRA55'][i]],'b-',linewidth=1.0,label='Total')
    plt.plot(index_1979_2015,AMET_E_cpT_ERAI_white_series[:-12,lat_interest['ERAI'][i]] - AMET_E_cpT_JRA55_white_series[:,lat_interest['JRA55'][i]],'r-',linewidth=1.0,label='cpT')
    plt.plot(index_1979_2015,AMET_E_Lvq_ERAI_white_series[:-12,lat_interest['ERAI'][i]] - AMET_E_Lvq_JRA55_white_series[:,lat_interest['JRA55'][i]],'m-',linewidth=1.0,label='Lvq')
    plt.plot(index_1979_2015,AMET_E_gz_ERAI_white_series[:-12,lat_interest['ERAI'][i]] - AMET_E_gz_JRA55_white_series[:,lat_interest['JRA55'][i]],'g-',linewidth=1.0,label='gz')
    plt.plot(index_1979_2015,AMET_E_uv2_ERAI_white_series[:-12,lat_interest['ERAI'][i]] - AMET_E_uv2_JRA55_white_series[:,lat_interest['JRA55'][i]],'c-',linewidth=1.0,label='uv2')
    plt.title('Difference between ERA-Interim and JRA55 anomalies (time series) at %dN' % (lat_interest_list[i]))
    plt.legend()
    fig16.set_size_inches(12.5, 6)
    plt.xlabel("Time")
    plt.xticks(np.linspace(0, 444, 38), year_JRA55)
    plt.xticks(rotation=60)
    plt.ylabel("Meridional Energy Transport residual (PW)")
    plt.legend()
    plt.show()
    fig16.savefig(output_path + os.sep + 'anomaly_minus' + os.sep + 'Comp_AMET_ERAI_minus_JRA55_anomaly_%dN.jpg' % (lat_interest_list[i]), dpi = 300)
    plt.close(fig16)

# MERRA2 minus JRA55
for i in np.arange(len(lat_interest_list)):
    fig17 = plt.figure()
    plt.plot(index_1980_2015,AMET_E_MERRA2_series[:-12,lat_interest['MERRA2'][i]] - AMET_E_JRA55_series[12:,lat_interest['JRA55'][i]],'b-',linewidth=1.0,label='Total')
    plt.plot(index_1980_2015,AMET_E_cpT_MERRA2_series[:-12,lat_interest['MERRA2'][i]] - AMET_E_cpT_JRA55_series[12:,lat_interest['JRA55'][i]],'r-',linewidth=1.0,label='cpT')
    plt.plot(index_1980_2015,AMET_E_Lvq_MERRA2_series[:-12,lat_interest['MERRA2'][i]] - AMET_E_Lvq_JRA55_series[12:,lat_interest['JRA55'][i]],'m-',linewidth=1.0,label='Lvq')
    plt.plot(index_1980_2015,AMET_E_gz_MERRA2_series[:-12,lat_interest['MERRA2'][i]] - AMET_E_gz_JRA55_series[12:,lat_interest['JRA55'][i]],'g-',linewidth=1.0,label='gz')
    plt.plot(index_1980_2015,AMET_E_uv2_MERRA2_series[:-12,lat_interest['MERRA2'][i]] - AMET_E_uv2_JRA55_series[12:,lat_interest['JRA55'][i]],'c-',linewidth=1.0,label='uv2')
    plt.title('Difference between MERRA2 and JRA55 (time series) at %dN' % (lat_interest_list[i]))
    plt.legend()
    fig17.set_size_inches(12.5, 6)
    plt.xlabel("Time")
    plt.xticks(np.linspace(0, 432, 37), year_JRA55[1:])
    plt.xticks(rotation=60)
    plt.ylabel("Meridional Energy Transport residual (PW)")
    plt.legend()
    plt.show()
    fig17.savefig(output_path + os.sep + 'original_minus' + os.sep + 'Comp_AMET_MERRA2_minus_JRA55_%dN.jpg' % (lat_interest_list[i]), dpi = 300)
    plt.close(fig17)

for i in np.arange(len(lat_interest_list)):
    fig16 = plt.figure()
    plt.plot(index_1980_2015,AMET_E_MERRA2_white_series[:-12,lat_interest['MERRA2'][i]] - AMET_E_JRA55_white_series[12:,lat_interest['JRA55'][i]],'b-',linewidth=1.0,label='Total')
    plt.plot(index_1980_2015,AMET_E_cpT_MERRA2_white_series[:-12,lat_interest['MERRA2'][i]] - AMET_E_cpT_JRA55_white_series[12:,lat_interest['JRA55'][i]],'r-',linewidth=1.0,label='cpT')
    plt.plot(index_1980_2015,AMET_E_Lvq_MERRA2_white_series[:-12,lat_interest['MERRA2'][i]] - AMET_E_Lvq_JRA55_white_series[12:,lat_interest['JRA55'][i]],'m-',linewidth=1.0,label='Lvq')
    plt.plot(index_1980_2015,AMET_E_gz_MERRA2_white_series[:-12,lat_interest['MERRA2'][i]] - AMET_E_gz_JRA55_white_series[12:,lat_interest['JRA55'][i]],'g-',linewidth=1.0,label='gz')
    plt.plot(index_1980_2015,AMET_E_uv2_MERRA2_white_series[:-12,lat_interest['MERRA2'][i]] - AMET_E_uv2_JRA55_white_series[12:,lat_interest['JRA55'][i]],'c-',linewidth=1.0,label='uv2')
    plt.title('Difference between MERRA2 and JRA55 anomalies (time series) at %dN' % (lat_interest_list[i]))
    plt.legend()
    fig16.set_size_inches(12.5, 6)
    plt.xlabel("Time")
    plt.xticks(np.linspace(0, 432, 37), year_JRA55[1:])
    plt.xticks(rotation=60)
    plt.ylabel("Meridional Energy Transport residual (PW)")
    plt.legend()
    plt.show()
    fig16.savefig(output_path + os.sep + 'anomaly_minus' + os.sep + 'Comp_AMET_MERRA2_minus_JRA55_anomaly_%dN.jpg' % (lat_interest_list[i]), dpi = 300)
    plt.close(fig16)
print '*******************************************************************'
print '******************   highlight the difference   *******************'
print '****************   contour of time series (lat)   *****************'
print '*******************************************************************'

#=========================================================================#
#-----------------------   Statistical Matrix   ---------------------------
#=========================================================================#

print '*******************************************************************'
print '********************** standard deviation  ************************'
print '*******************************************************************'
# calculate the standard deviation of AMET
# ERA-Interim
AMET_E_ERAI_std = np.std(AMET_E_ERAI_series)
print 'The standard deviation of AMET from ERA-Interim is (in peta Watt):'
print AMET_E_ERAI_std
# MERRA2
AMET_E_MERRA2_std = np.std(AMET_E_MERRA2_series)
print 'The standard deviation of AMET from MERRA2 is (in peta Watt):'
print AMET_E_MERRA2_std
# JRA55
AMET_E_JRA55_std = np.std(AMET_E_JRA55_series)
print 'The standard deviation of AMET from JRA55 is (in peta Watt):'
print AMET_E_JRA55_std

# calculate the standard deviation of AMET anomaly
# ERA-Interim
AMET_E_ERAI_white_std = np.std(AMET_E_ERAI_white_series)
print 'The standard deviation of AMET anomaly from ERA-Interim is (in peta Watt):'
print AMET_E_ERAI_white_std
# MERRA2
AMET_E_MERRA2_white_std = np.std(AMET_E_MERRA2_white_series)
print 'The standard deviation of AMET anomaly from MERRA2 is (in peta Watt):'
print AMET_E_MERRA2_white_std
# JRA55
AMET_E_JRA55_white_std = np.std(AMET_E_JRA55_white_series)
print 'The standard deviation of AMET anomaly from JRA55 is (in peta Watt):'
print AMET_E_JRA55_white_std

print '*******************************************************************'
print '*************************** mean value  ***************************'
print '*******************************************************************'
# calculate the mean of AMET
# ERA-Interim
AMET_E_ERAI_mean = np.mean(AMET_E_ERAI_series)
print 'The mean of AMET from ERA-Interim is (in peta Watt):'
print AMET_E_ERAI_mean
# MERRA2
AMET_E_MERRA2_mean = np.mean(AMET_E_MERRA2_series)
print 'The mean of AMET from MERRA2 is (in peta Watt):'
print AMET_E_MERRA2_mean
# JRA55
AMET_E_JRA55_mean = np.mean(AMET_E_JRA55_series)
print 'The mean of AMET from JRA55 is (in peta Watt):'
print AMET_E_JRA55_mean

# calculate the standard deviation of AMET anomaly
# ERA-Interim
AMET_E_ERAI_white_mean = np.mean(AMET_E_ERAI_white_series)
print 'The mean of AMET anomaly from ERA-Interim is (in peta Watt):'
print AMET_E_ERAI_white_mean
# MERRA2
AMET_E_MERRA2_white_mean = np.mean(AMET_E_MERRA2_white_series)
print 'The mean of AMET anomaly from MERRA2 is (in peta Watt):'
print AMET_E_MERRA2_white_mean
# JRA55
AMET_E_JRA55_white_mean = np.mean(AMET_E_JRA55_white_series)
print 'The mean of AMET anomaly from JRA55 is (in peta Watt):'
print AMET_E_JRA55_white_mean

print '*******************************************************************'
print '************************** correlation  ***************************'
print '*******************************************************************'
# create correlation matrix
row_name_correlation = ['ERA - MERRA','ERA - JRA','MERRA - JRA',
                        'ERA - MERRA (anomaly)','ERA - JRA (anomaly)','MERRA - JRA (anomaly)']
column_name_correlation = lat_interest_list

# original & white time series
slope = np.zeros((len(column_name_correlation),len(row_name_correlation)),dtype=float)
r_value = np.zeros((len(column_name_correlation),len(row_name_correlation)),dtype=float)
p_value = np.zeros((len(column_name_correlation),len(row_name_correlation)),dtype=float)
# return value: slope, intercept, r_value, p_value, stderr
for i in np.arange(len(lat_interest_list)):
    slope[i,0],_,r_value[i,0],p_value[i,0],_ = stats.linregress(AMET_E_ERAI_series[12:,lat_interest['ERAI'][i]],AMET_E_MERRA2_series[:,lat_interest['MERRA2'][i]])
    slope[i,1],_,r_value[i,1],p_value[i,1],_ = stats.linregress(AMET_E_ERAI_series[:-12,lat_interest['ERAI'][i]],AMET_E_JRA55_series[:,lat_interest['JRA55'][i]])
    slope[i,2],_,r_value[i,2],p_value[i,2],_ = stats.linregress(AMET_E_MERRA2_series[:-12,lat_interest['MERRA2'][i]],AMET_E_JRA55_series[12:,lat_interest['JRA55'][i]])
    slope[i,3],_,r_value[i,3],p_value[i,3],_ = stats.linregress(AMET_E_ERAI_white_series[12:,lat_interest['ERAI'][i]],AMET_E_MERRA2_white_series[:,lat_interest['MERRA2'][i]])
    slope[i,4],_,r_value[i,4],p_value[i,4],_ = stats.linregress(AMET_E_ERAI_white_series[:-12,lat_interest['ERAI'][i]],AMET_E_JRA55_white_series[:,lat_interest['JRA55'][i]])
    slope[i,5],_,r_value[i,5],p_value[i,5],_ = stats.linregress(AMET_E_MERRA2_white_series[:-12,lat_interest['MERRA2'][i]],AMET_E_JRA55_white_series[12:,lat_interest['JRA55'][i]])

# low pass original & white time series
slope_lowpass = np.zeros((len(column_name_correlation),len(row_name_correlation)),dtype=float)
r_value_lowpass = np.zeros((len(column_name_correlation),len(row_name_correlation)),dtype=float)
p_value_lowpass = np.zeros((len(column_name_correlation),len(row_name_correlation)),dtype=float)
# return value: slope, intercept, r_value, p_value, stderr
for i in np.arange(len(lat_interest_list)):
    slope_lowpass[i,0],_,r_value_lowpass[i,0],p_value_lowpass[i,0],_ = stats.linregress(AMET_E_ERAI_running_mean[12:,lat_interest['ERAI'][i]],AMET_E_MERRA2_running_mean[:,lat_interest['MERRA2'][i]])
    slope_lowpass[i,1],_,r_value_lowpass[i,1],p_value_lowpass[i,1],_ = stats.linregress(AMET_E_ERAI_running_mean[:-12,lat_interest['ERAI'][i]],AMET_E_JRA55_running_mean[:,lat_interest['JRA55'][i]])
    slope_lowpass[i,2],_,r_value_lowpass[i,2],p_value_lowpass[i,2],_ = stats.linregress(AMET_E_MERRA2_running_mean[:-12,lat_interest['MERRA2'][i]],AMET_E_JRA55_running_mean[12:,lat_interest['JRA55'][i]])
    slope_lowpass[i,3],_,r_value_lowpass[i,3],p_value_lowpass[i,3],_ = stats.linregress(AMET_E_ERAI_white_running_mean[12:,lat_interest['ERAI'][i]],AMET_E_MERRA2_white_running_mean[:,lat_interest['MERRA2'][i]])
    slope_lowpass[i,4],_,r_value_lowpass[i,4],p_value_lowpass[i,4],_ = stats.linregress(AMET_E_ERAI_white_running_mean[:-12,lat_interest['ERAI'][i]],AMET_E_JRA55_white_running_mean[:,lat_interest['JRA55'][i]])
    slope_lowpass[i,5],_,r_value_lowpass[i,5],p_value_lowpass[i,5],_ = stats.linregress(AMET_E_MERRA2_white_running_mean[:-12,lat_interest['MERRA2'][i]],AMET_E_JRA55_white_running_mean[12:,lat_interest['JRA55'][i]])

print '*******************************************************************'
print '************************** save tp csv  ***************************'
print '*******************************************************************'
# statistical matrix
row_name_statistic = ['ERA-Interim','MERRA2','JRA55']
column_name_statistic = ['mean','mean(anomaly)','std','std(anomaly)']
data_for_save_statistic = np.array(([AMET_E_ERAI_mean,AMET_E_MERRA2_mean,AMET_E_JRA55_mean],
                          [AMET_E_ERAI_white_mean,AMET_E_MERRA2_white_mean,AMET_E_JRA55_white_mean],
                          [AMET_E_ERAI_std,AMET_E_MERRA2_std,AMET_E_JRA55_std],
                          [AMET_E_ERAI_white_std,AMET_E_MERRA2_white_std,AMET_E_JRA55_white_std]
                          ),dtype=float)
df_statistic = pandas.DataFrame(data_for_save_statistic,column_name_statistic,row_name_statistic)
#f_csv = open('csv_path' + 'AMET_statistic_matrix.csv','wb') # b indicates binary
df_statistic.to_csv(csv_path + os.sep + 'matrix' + os.sep + 'AMET_statistic_matrix.csv',
                    index=True, header=True, decimal='.', float_format='%.3f')

# correlation matrix - original & anomaly time series
df_correlation = pandas.DataFrame(slope,column_name_correlation,row_name_correlation)
df_correlation.to_csv(csv_path + os.sep + 'matrix' + os.sep + 'AMET_correlation_slope_matrix.csv',
                      index=True, header=True, decimal='.',float_format='%.3f')

df_correlation = pandas.DataFrame(r_value,column_name_correlation,row_name_correlation)
df_correlation.to_csv(csv_path + os.sep + 'matrix' + os.sep + 'AMET_correlation_r_matrix.csv',
                      index=True, header=True, decimal='.', float_format='%.3f')

df_correlation = pandas.DataFrame(p_value,column_name_correlation,row_name_correlation)
df_correlation.to_csv(csv_path + os.sep + 'matrix' + os.sep + 'AMET_correlation_p_matrix.csv',
                      index=True, header=True, decimal='.', float_format='%.3f')

# correlation matrix - low pass original & anomaly time series
df_correlation = pandas.DataFrame(slope_lowpass,column_name_correlation,row_name_correlation)
df_correlation.to_csv(csv_path + os.sep + 'matrix' + os.sep + 'AMET_correlation_slope_lowpass_%dm_matrix.csv' % (window),
                      index=True, header=True, decimal='.',float_format='%.3f')

df_correlation = pandas.DataFrame(r_value_lowpass,column_name_correlation,row_name_correlation)
df_correlation.to_csv(csv_path + os.sep + 'matrix' + os.sep + 'AMET_correlation_r_lowpass_%dm_matrix.csv' % (window),
                      index=True, header=True, decimal='.', float_format='%.3f')

df_correlation = pandas.DataFrame(p_value_lowpass,column_name_correlation,row_name_correlation)
df_correlation.to_csv(csv_path + os.sep + 'matrix' + os.sep + 'AMET_correlation_p_lowpass_%dm_matrix.csv' % (window),
                      index=True, header=True, decimal='.', float_format='%.3f')
