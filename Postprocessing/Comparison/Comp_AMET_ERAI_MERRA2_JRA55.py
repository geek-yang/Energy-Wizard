#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : Compare atmospheric meridional energy transport (MERRA2,ERA-Interim,JRA55)
Author          : Yang Liu
Date            : 2017.11.6
Last Update     : 2018.01.09
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
# generate images without having a window appear
#matplotlib.use('Agg')
import matplotlib.pyplot as plt

# switch on the seaborn effect
sns.set()

################################   Input zone  ######################################
# specify data path
datapath_ERAI = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ERAI/postprocessing'
datapath_MERRA2 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/MERRA2/postprocessing'
datapath_JRA55 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/JRA55/postprocessing'
# specify output path for the netCDF4 file
output_path = '/home/yang/NLeSC/Computation_Modeling/BlueAction/AMET/Comparison'
# index of latitude for insteret
# 60N
lat_ERAI = 40 # at 60 N
lat_MERRA2 = 80 # at 60 N
lat_JRA55 = 53 # at 60 N
# from 90N to 20N --> 0:124
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
AMET_E_ERAI_full = dataset_ERAI.variables['E'][:]/1000 # from Tera Watt to Peta Watt
AMET_E_MERRA2_full = dataset_MERRA2.variables['E'][:]/1000 # from Tera Watt to Peta Watt
AMET_E_JRA55_full = dataset_JRA55.variables['E'][:,:,0:124]/1000 # from Tera Watt to Peta Watt
# internal energy
AMET_E_cpT_ERAI_full = dataset_ERAI.variables['E_cpT'][:]/1000
AMET_E_cpT_MERRA2_full = dataset_MERRA2.variables['E_cpT'][:]/1000
AMET_E_cpT_JRA55_full = dataset_JRA55.variables['E_cpT'][:,:,0:124]/1000
# latent heat
AMET_E_Lvq_ERAI_full = dataset_ERAI.variables['E_Lvq'][:]/1000
AMET_E_Lvq_MERRA2_full = dataset_MERRA2.variables['E_Lvq'][:]/1000
AMET_E_Lvq_JRA55_full = dataset_JRA55.variables['E_Lvq'][:,:,0:124]/1000
# geopotential
AMET_E_gz_ERAI_full = dataset_ERAI.variables['E_gz'][:]/1000
AMET_E_gz_MERRA2_full = dataset_MERRA2.variables['E_gz'][:]/1000
AMET_E_gz_JRA55_full = dataset_JRA55.variables['E_gz'][:,:,0:124]/1000
# kinetic energy
AMET_E_uv2_ERAI_full = dataset_ERAI.variables['E_uv2'][:]/1000
AMET_E_uv2_MERRA2_full = dataset_MERRA2.variables['E_uv2'][:]/1000
AMET_E_uv2_JRA55_full = dataset_JRA55.variables['E_uv2'][:,:,0:124]/1000

# selected latitude (60N)
# total energy transport
AMET_E_ERAI = dataset_ERAI.variables['E'][:,:,lat_ERAI]/1000 # from Tera Watt to Peta Watt
AMET_E_MERRA2 = dataset_MERRA2.variables['E'][:,:,lat_MERRA2]/1000 # from Tera Watt to Peta Watt
AMET_E_JRA55 = dataset_JRA55.variables['E'][:,:,lat_JRA55]/1000 # from Tera Watt to Peta Watt
# internal energy
AMET_E_cpT_ERAI = dataset_ERAI.variables['E_cpT'][:,:,lat_ERAI]/1000
AMET_E_cpT_MERRA2 = dataset_MERRA2.variables['E_cpT'][:,:,lat_MERRA2]/1000
AMET_E_cpT_JRA55 = dataset_JRA55.variables['E_cpT'][:,:,lat_JRA55]/1000
# latent heat
AMET_E_Lvq_ERAI = dataset_ERAI.variables['E_Lvq'][:,:,lat_ERAI]/1000
AMET_E_Lvq_MERRA2 = dataset_MERRA2.variables['E_Lvq'][:,:,lat_MERRA2]/1000
AMET_E_Lvq_JRA55 = dataset_JRA55.variables['E_Lvq'][:,:,lat_JRA55]/1000
# geopotential
AMET_E_gz_ERAI = dataset_ERAI.variables['E_gz'][:,:,lat_ERAI]/1000
AMET_E_gz_MERRA2 = dataset_MERRA2.variables['E_gz'][:,:,lat_MERRA2]/1000
AMET_E_gz_JRA55 = dataset_JRA55.variables['E_gz'][:,:,lat_JRA55]/1000
# kinetic energy
AMET_E_uv2_ERAI = dataset_ERAI.variables['E_uv2'][:,:,lat_ERAI]/1000
AMET_E_uv2_MERRA2 = dataset_MERRA2.variables['E_uv2'][:,:,lat_MERRA2]/1000
AMET_E_uv2_JRA55 = dataset_JRA55.variables['E_uv2'][:,:,lat_JRA55]/1000

year_ERAI = dataset_ERAI.variables['year'][:]        # from 1979 to 2016
year_MERRA2 = dataset_MERRA2.variables['year'][:]    # from 1980 to 2016
year_JRA55 = dataset_JRA55.variables['year'][:]      # from 1979 to 2015

latitude_ERAI = dataset_ERAI.variables['latitude'][:]
latitude_MERRA2 = dataset_MERRA2.variables['latitude'][:]
latitude_JRA55 = dataset_JRA55.variables['latitude'][0:124]

print '*******************************************************************'
print '*********************** prepare variables *************************'
print '*******************************************************************'
# take the time series of E
# total energy transport
AMET_E_ERAI_series = AMET_E_ERAI.reshape(456)
AMET_E_MERRA2_series = AMET_E_MERRA2.reshape(444)
AMET_E_JRA55_series = AMET_E_JRA55.reshape(444)
# internal energy
AMET_E_cpT_ERAI_series = AMET_E_cpT_ERAI.reshape(456)
AMET_E_cpT_MERRA2_series = AMET_E_cpT_MERRA2.reshape(444)
AMET_E_cpT_JRA55_series = AMET_E_cpT_JRA55.reshape(444)
# latent heat
AMET_E_Lvq_ERAI_series = AMET_E_Lvq_ERAI.reshape(456)
AMET_E_Lvq_MERRA2_series = AMET_E_Lvq_MERRA2.reshape(444)
AMET_E_Lvq_JRA55_series = AMET_E_Lvq_JRA55.reshape(444)
# geopotential
AMET_E_gz_ERAI_series = AMET_E_gz_ERAI.reshape(456)
AMET_E_gz_MERRA2_series = AMET_E_gz_MERRA2.reshape(444)
AMET_E_gz_JRA55_series = AMET_E_gz_JRA55.reshape(444)
# kinetic energy
AMET_E_uv2_ERAI_series = AMET_E_uv2_ERAI.reshape(456)
AMET_E_uv2_MERRA2_series = AMET_E_uv2_MERRA2.reshape(444)
AMET_E_uv2_JRA55_series = AMET_E_uv2_JRA55.reshape(444)
print '*******************************************************************'
print '*************************** whitening *****************************'
print '*******************************************************************'
# remove the seasonal cycling of AMET at 60N
month_ind = np.arange(12)
# dimension of AMET[year,month]
# total energy transport
AMET_E_ERAI_seansonal_cycle = np.mean(AMET_E_ERAI,axis=0)
AMET_E_ERAI_white = np.zeros(AMET_E_ERAI.shape,dtype=float)
for i in month_ind:
    AMET_E_ERAI_white[:,i] = AMET_E_ERAI[:,i] - AMET_E_ERAI_seansonal_cycle[i]
# take the time series of whitened AMET
AMET_E_ERAI_white_series = AMET_E_ERAI_white.reshape(456)

AMET_E_MERRA2_seansonal_cycle = np.mean(AMET_E_MERRA2,axis=0)
AMET_E_MERRA2_white = np.zeros(AMET_E_MERRA2.shape,dtype=float)
for i in month_ind:
    AMET_E_MERRA2_white[:,i] = AMET_E_MERRA2[:,i] - AMET_E_MERRA2_seansonal_cycle[i]
# take the time series of whitened AMET
AMET_E_MERRA2_white_series = AMET_E_MERRA2_white.reshape(444)

AMET_E_JRA55_seansonal_cycle = np.mean(AMET_E_JRA55,axis=0)
AMET_E_JRA55_white = np.zeros(AMET_E_JRA55.shape,dtype=float)
for i in month_ind:
    AMET_E_JRA55_white[:,i] = AMET_E_JRA55[:,i] - AMET_E_JRA55_seansonal_cycle[i]
# take the time series of whitened AMET
AMET_E_JRA55_white_series = AMET_E_JRA55_white.reshape(444)

# internal energy
AMET_E_cpT_ERAI_seansonal_cycle = np.mean(AMET_E_cpT_ERAI,axis=0)
AMET_E_cpT_ERAI_white = np.zeros(AMET_E_cpT_ERAI.shape,dtype=float)
for i in month_ind:
    AMET_E_cpT_ERAI_white[:,i] = AMET_E_cpT_ERAI[:,i] - AMET_E_cpT_ERAI_seansonal_cycle[i]
# take the time series of whitened AMET
AMET_E_cpT_ERAI_white_series = AMET_E_cpT_ERAI_white.reshape(456)

AMET_E_cpT_MERRA2_seansonal_cycle = np.mean(AMET_E_cpT_MERRA2,axis=0)
AMET_E_cpT_MERRA2_white = np.zeros(AMET_E_cpT_MERRA2.shape,dtype=float)
for i in month_ind:
    AMET_E_cpT_MERRA2_white[:,i] = AMET_E_cpT_MERRA2[:,i] - AMET_E_cpT_MERRA2_seansonal_cycle[i]
# take the time series of whitened AMET
AMET_E_cpT_MERRA2_white_series = AMET_E_cpT_MERRA2_white.reshape(444)

AMET_E_cpT_JRA55_seansonal_cycle = np.mean(AMET_E_cpT_JRA55,axis=0)
AMET_E_cpT_JRA55_white = np.zeros(AMET_E_cpT_JRA55.shape,dtype=float)
for i in month_ind:
    AMET_E_cpT_JRA55_white[:,i] = AMET_E_cpT_JRA55[:,i] - AMET_E_cpT_JRA55_seansonal_cycle[i]
# take the time series of whitened AMET
AMET_E_cpT_JRA55_white_series = AMET_E_cpT_JRA55_white.reshape(444)

# latent heat
AMET_E_Lvq_ERAI_seansonal_cycle = np.mean(AMET_E_Lvq_ERAI,axis=0)
AMET_E_Lvq_ERAI_white = np.zeros(AMET_E_Lvq_ERAI.shape,dtype=float)
for i in month_ind:
    AMET_E_Lvq_ERAI_white[:,i] = AMET_E_Lvq_ERAI[:,i] - AMET_E_Lvq_ERAI_seansonal_cycle[i]
# take the time series of whitened AMET
AMET_E_Lvq_ERAI_white_series = AMET_E_Lvq_ERAI_white.reshape(456)

AMET_E_Lvq_MERRA2_seansonal_cycle = np.mean(AMET_E_Lvq_MERRA2,axis=0)
AMET_E_Lvq_MERRA2_white = np.zeros(AMET_E_Lvq_MERRA2.shape,dtype=float)
for i in month_ind:
    AMET_E_Lvq_MERRA2_white[:,i] = AMET_E_Lvq_MERRA2[:,i] - AMET_E_Lvq_MERRA2_seansonal_cycle[i]
# take the time series of whitened AMET
AMET_E_Lvq_MERRA2_white_series = AMET_E_Lvq_MERRA2_white.reshape(444)

AMET_E_Lvq_JRA55_seansonal_cycle = np.mean(AMET_E_Lvq_JRA55,axis=0)
AMET_E_Lvq_JRA55_white = np.zeros(AMET_E_Lvq_JRA55.shape,dtype=float)
for i in month_ind:
    AMET_E_Lvq_JRA55_white[:,i] = AMET_E_Lvq_JRA55[:,i] - AMET_E_Lvq_JRA55_seansonal_cycle[i]
# take the time series of whitened AMET
AMET_E_Lvq_JRA55_white_series = AMET_E_Lvq_JRA55_white.reshape(444)

# geopotential
AMET_E_gz_ERAI_seansonal_cycle = np.mean(AMET_E_gz_ERAI,axis=0)
AMET_E_gz_ERAI_white = np.zeros(AMET_E_gz_ERAI.shape,dtype=float)
for i in month_ind:
    AMET_E_gz_ERAI_white[:,i] = AMET_E_gz_ERAI[:,i] - AMET_E_gz_ERAI_seansonal_cycle[i]
# take the time series of whitened AMET
AMET_E_gz_ERAI_white_series = AMET_E_gz_ERAI_white.reshape(456)

AMET_E_gz_MERRA2_seansonal_cycle = np.mean(AMET_E_gz_MERRA2,axis=0)
AMET_E_gz_MERRA2_white = np.zeros(AMET_E_gz_MERRA2.shape,dtype=float)
for i in month_ind:
    AMET_E_gz_MERRA2_white[:,i] = AMET_E_gz_MERRA2[:,i] - AMET_E_gz_MERRA2_seansonal_cycle[i]
# take the time series of whitened AMET
AMET_E_gz_MERRA2_white_series = AMET_E_gz_MERRA2_white.reshape(444)

AMET_E_gz_JRA55_seansonal_cycle = np.mean(AMET_E_gz_JRA55,axis=0)
AMET_E_gz_JRA55_white = np.zeros(AMET_E_gz_JRA55.shape,dtype=float)
for i in month_ind:
    AMET_E_gz_JRA55_white[:,i] = AMET_E_gz_JRA55[:,i] - AMET_E_gz_JRA55_seansonal_cycle[i]
# take the time series of whitened AMET
AMET_E_gz_JRA55_white_series = AMET_E_gz_JRA55_white.reshape(444)

# kinetic energy
AMET_E_uv2_ERAI_seansonal_cycle = np.mean(AMET_E_uv2_ERAI,axis=0)
AMET_E_uv2_ERAI_white = np.zeros(AMET_E_uv2_ERAI.shape,dtype=float)
for i in month_ind:
    AMET_E_uv2_ERAI_white[:,i] = AMET_E_uv2_ERAI[:,i] - AMET_E_uv2_ERAI_seansonal_cycle[i]
# take the time series of whitened AMET
AMET_E_uv2_ERAI_white_series = AMET_E_uv2_ERAI_white.reshape(456)

AMET_E_uv2_MERRA2_seansonal_cycle = np.mean(AMET_E_uv2_MERRA2,axis=0)
AMET_E_uv2_MERRA2_white = np.zeros(AMET_E_uv2_MERRA2.shape,dtype=float)
for i in month_ind:
    AMET_E_uv2_MERRA2_white[:,i] = AMET_E_uv2_MERRA2[:,i] - AMET_E_uv2_MERRA2_seansonal_cycle[i]
# take the time series of whitened AMET
AMET_E_uv2_MERRA2_white_series = AMET_E_uv2_MERRA2_white.reshape(444)

AMET_E_uv2_JRA55_seansonal_cycle = np.mean(AMET_E_uv2_JRA55,axis=0)
AMET_E_uv2_JRA55_white = np.zeros(AMET_E_uv2_JRA55.shape,dtype=float)
for i in month_ind:
    AMET_E_uv2_JRA55_white[:,i] = AMET_E_uv2_JRA55[:,i] - AMET_E_uv2_JRA55_seansonal_cycle[i]
# take the time series of whitened AMET
AMET_E_uv2_JRA55_white_series = AMET_E_uv2_JRA55_white.reshape(444)
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
AMET_E_ERAI_running_mean = np.zeros(len(AMET_E_ERAI_series)-window+1)
for i in np.arange(len(AMET_E_ERAI_series)-window+1):
    AMET_E_ERAI_running_mean[i] = np.mean(AMET_E_ERAI_series[i:i+window])

AMET_E_MERRA2_running_mean = np.zeros(len(AMET_E_MERRA2_series)-window+1)
for i in np.arange(len(AMET_E_MERRA2_series)-window+1):
    AMET_E_MERRA2_running_mean[i] = np.mean(AMET_E_MERRA2_series[i:i+window])

AMET_E_JRA55_running_mean = np.zeros(len(AMET_E_JRA55_series)-window+1)
for i in np.arange(len(AMET_E_JRA55_series)-window+1):
    AMET_E_JRA55_running_mean[i] = np.mean(AMET_E_JRA55_series[i:i+window])

# internal energy
AMET_E_cpT_ERAI_running_mean = np.zeros(len(AMET_E_cpT_ERAI_series)-window+1)
for i in np.arange(len(AMET_E_cpT_ERAI_series)-window+1):
    AMET_E_cpT_ERAI_running_mean[i] = np.mean(AMET_E_cpT_ERAI_series[i:i+window])

AMET_E_cpT_MERRA2_running_mean = np.zeros(len(AMET_E_cpT_MERRA2_series)-window+1)
for i in np.arange(len(AMET_E_cpT_MERRA2_series)-window+1):
    AMET_E_cpT_MERRA2_running_mean[i] = np.mean(AMET_E_cpT_MERRA2_series[i:i+window])

AMET_E_cpT_JRA55_running_mean = np.zeros(len(AMET_E_cpT_JRA55_series)-window+1)
for i in np.arange(len(AMET_E_cpT_JRA55_series)-window+1):
    AMET_E_cpT_JRA55_running_mean[i] = np.mean(AMET_E_cpT_JRA55_series[i:i+window])

# latent heat
AMET_E_Lvq_ERAI_running_mean = np.zeros(len(AMET_E_Lvq_ERAI_series)-window+1)
for i in np.arange(len(AMET_E_Lvq_ERAI_series)-window+1):
    AMET_E_Lvq_ERAI_running_mean[i] = np.mean(AMET_E_Lvq_ERAI_series[i:i+window])

AMET_E_Lvq_MERRA2_running_mean = np.zeros(len(AMET_E_Lvq_MERRA2_series)-window+1)
for i in np.arange(len(AMET_E_Lvq_MERRA2_series)-window+1):
    AMET_E_Lvq_MERRA2_running_mean[i] = np.mean(AMET_E_Lvq_MERRA2_series[i:i+window])

AMET_E_Lvq_JRA55_running_mean = np.zeros(len(AMET_E_Lvq_JRA55_series)-window+1)
for i in np.arange(len(AMET_E_Lvq_JRA55_series)-window+1):
    AMET_E_Lvq_JRA55_running_mean[i] = np.mean(AMET_E_Lvq_JRA55_series[i:i+window])

# geopotential
AMET_E_gz_ERAI_running_mean = np.zeros(len(AMET_E_gz_ERAI_series)-window+1)
for i in np.arange(len(AMET_E_gz_ERAI_series)-window+1):
    AMET_E_gz_ERAI_running_mean[i] = np.mean(AMET_E_gz_ERAI_series[i:i+window])

AMET_E_gz_MERRA2_running_mean = np.zeros(len(AMET_E_gz_MERRA2_series)-window+1)
for i in np.arange(len(AMET_E_gz_MERRA2_series)-window+1):
    AMET_E_gz_MERRA2_running_mean[i] = np.mean(AMET_E_gz_MERRA2_series[i:i+window])

AMET_E_gz_JRA55_running_mean = np.zeros(len(AMET_E_gz_JRA55_series)-window+1)
for i in np.arange(len(AMET_E_gz_JRA55_series)-window+1):
    AMET_E_gz_JRA55_running_mean[i] = np.mean(AMET_E_gz_JRA55_series[i:i+window])

# kinetic energy
AMET_E_uv2_ERAI_running_mean = np.zeros(len(AMET_E_uv2_ERAI_series)-window+1)
for i in np.arange(len(AMET_E_uv2_ERAI_series)-window+1):
    AMET_E_uv2_ERAI_running_mean[i] = np.mean(AMET_E_uv2_ERAI_series[i:i+window])

AMET_E_uv2_MERRA2_running_mean = np.zeros(len(AMET_E_uv2_MERRA2_series)-window+1)
for i in np.arange(len(AMET_E_uv2_MERRA2_series)-window+1):
    AMET_E_uv2_MERRA2_running_mean[i] = np.mean(AMET_E_uv2_MERRA2_series[i:i+window])

AMET_E_uv2_JRA55_running_mean = np.zeros(len(AMET_E_uv2_JRA55_series)-window+1)
for i in np.arange(len(AMET_E_uv2_JRA55_series)-window+1):
    AMET_E_uv2_JRA55_running_mean[i] = np.mean(AMET_E_uv2_JRA55_series[i:i+window])

# calculate the running mean of AMET after removing the seasonal cycling
# total energy transport
AMET_E_ERAI_white_running_mean = np.zeros(len(AMET_E_ERAI_white_series)-window+1)
for i in np.arange(len(AMET_E_ERAI_white_series)-window+1):
    AMET_E_ERAI_white_running_mean[i] = np.mean(AMET_E_ERAI_white_series[i:i+window])

AMET_E_MERRA2_white_running_mean = np.zeros(len(AMET_E_MERRA2_white_series)-window+1)
for i in np.arange(len(AMET_E_MERRA2_white_series)-window+1):
    AMET_E_MERRA2_white_running_mean[i] = np.mean(AMET_E_MERRA2_white_series[i:i+window])

AMET_E_JRA55_white_running_mean = np.zeros(len(AMET_E_JRA55_white_series)-window+1)
for i in np.arange(len(AMET_E_JRA55_white_series)-window+1):
    AMET_E_JRA55_white_running_mean[i] = np.mean(AMET_E_JRA55_white_series[i:i+window])

# internal energy
AMET_E_cpT_ERAI_white_running_mean = np.zeros(len(AMET_E_cpT_ERAI_white_series)-window+1)
for i in np.arange(len(AMET_E_cpT_ERAI_white_series)-window+1):
    AMET_E_cpT_ERAI_white_running_mean[i] = np.mean(AMET_E_cpT_ERAI_white_series[i:i+window])

AMET_E_cpT_MERRA2_white_running_mean = np.zeros(len(AMET_E_cpT_MERRA2_white_series)-window+1)
for i in np.arange(len(AMET_E_cpT_MERRA2_white_series)-window+1):
    AMET_E_cpT_MERRA2_white_running_mean[i] = np.mean(AMET_E_cpT_MERRA2_white_series[i:i+window])

AMET_E_cpT_JRA55_white_running_mean = np.zeros(len(AMET_E_cpT_JRA55_white_series)-window+1)
for i in np.arange(len(AMET_E_cpT_JRA55_white_series)-window+1):
    AMET_E_cpT_JRA55_white_running_mean[i] = np.mean(AMET_E_cpT_JRA55_white_series[i:i+window])

# latent heat
AMET_E_Lvq_ERAI_white_running_mean = np.zeros(len(AMET_E_Lvq_ERAI_white_series)-window+1)
for i in np.arange(len(AMET_E_Lvq_ERAI_white_series)-window+1):
    AMET_E_Lvq_ERAI_white_running_mean[i] = np.mean(AMET_E_Lvq_ERAI_white_series[i:i+window])

AMET_E_Lvq_MERRA2_white_running_mean = np.zeros(len(AMET_E_Lvq_MERRA2_white_series)-window+1)
for i in np.arange(len(AMET_E_Lvq_MERRA2_white_series)-window+1):
    AMET_E_Lvq_MERRA2_white_running_mean[i] = np.mean(AMET_E_Lvq_MERRA2_white_series[i:i+window])

AMET_E_Lvq_JRA55_white_running_mean = np.zeros(len(AMET_E_Lvq_JRA55_white_series)-window+1)
for i in np.arange(len(AMET_E_Lvq_JRA55_white_series)-window+1):
    AMET_E_Lvq_JRA55_white_running_mean[i] = np.mean(AMET_E_Lvq_JRA55_white_series[i:i+window])

# geopotential
AMET_E_gz_ERAI_white_running_mean = np.zeros(len(AMET_E_gz_ERAI_white_series)-window+1)
for i in np.arange(len(AMET_E_gz_ERAI_white_series)-window+1):
    AMET_E_gz_ERAI_white_running_mean[i] = np.mean(AMET_E_gz_ERAI_white_series[i:i+window])

AMET_E_gz_MERRA2_white_running_mean = np.zeros(len(AMET_E_gz_MERRA2_white_series)-window+1)
for i in np.arange(len(AMET_E_gz_MERRA2_white_series)-window+1):
    AMET_E_gz_MERRA2_white_running_mean[i] = np.mean(AMET_E_gz_MERRA2_white_series[i:i+window])

AMET_E_gz_JRA55_white_running_mean = np.zeros(len(AMET_E_gz_JRA55_white_series)-window+1)
for i in np.arange(len(AMET_E_gz_JRA55_white_series)-window+1):
    AMET_E_gz_JRA55_white_running_mean[i] = np.mean(AMET_E_gz_JRA55_white_series[i:i+window])

# kinetic energy
AMET_E_uv2_ERAI_white_running_mean = np.zeros(len(AMET_E_uv2_ERAI_white_series)-window+1)
for i in np.arange(len(AMET_E_uv2_ERAI_white_series)-window+1):
    AMET_E_uv2_ERAI_white_running_mean[i] = np.mean(AMET_E_uv2_ERAI_white_series[i:i+window])

AMET_E_uv2_MERRA2_white_running_mean = np.zeros(len(AMET_E_uv2_MERRA2_white_series)-window+1)
for i in np.arange(len(AMET_E_uv2_MERRA2_white_series)-window+1):
    AMET_E_uv2_MERRA2_white_running_mean[i] = np.mean(AMET_E_uv2_MERRA2_white_series[i:i+window])

AMET_E_uv2_JRA55_white_running_mean = np.zeros(len(AMET_E_uv2_JRA55_white_series)-window+1)
for i in np.arange(len(AMET_E_uv2_JRA55_white_series)-window+1):
    AMET_E_uv2_JRA55_white_running_mean[i] = np.mean(AMET_E_uv2_JRA55_white_series[i:i+window])

print '*******************************************************************'
print '***************   standard deviation at each lat   ****************'
print '*******************************************************************'
# standard deviation at each latitude
# for error bar band
# reshape of each dataset at full latitude for the calculation of standard deviation
AMET_E_ERAI_series_full = AMET_E_ERAI_full.reshape(len(year_ERAI)*12,len(latitude_ERAI))
AMET_E_ERAI_std_full = np.std(AMET_E_ERAI_series_full,axis=0)
AMET_E_ERAI_error_plus = np.mean(np.mean(AMET_E_ERAI_full,0),0) + AMET_E_ERAI_std_full
AMET_E_ERAI_error_minus = np.mean(np.mean(AMET_E_ERAI_full,0),0) - AMET_E_ERAI_std_full

AMET_E_MERRA2_series_full = AMET_E_MERRA2_full.reshape((len(year_MERRA2)*12,len(latitude_MERRA2)))
AMET_E_MERRA2_std_full = np.std(AMET_E_MERRA2_series_full,axis=0)
AMET_E_MERRA2_error_plus = np.mean(np.mean(AMET_E_MERRA2_full,0),0) + AMET_E_MERRA2_std_full
AMET_E_MERRA2_error_minus = np.mean(np.mean(AMET_E_MERRA2_full,0),0) - AMET_E_MERRA2_std_full

AMET_E_JRA55_series_full = AMET_E_JRA55_full.reshape((len(year_JRA55)*12,len(latitude_JRA55)))
AMET_E_JRA55_std_full = np.std(AMET_E_JRA55_series_full,axis=0)
AMET_E_JRA55_error_plus = np.mean(np.mean(AMET_E_JRA55_full,0),0) + AMET_E_JRA55_std_full
AMET_E_JRA55_error_minus = np.mean(np.mean(AMET_E_JRA55_full,0),0) - AMET_E_JRA55_std_full

print '*******************************************************************'
print '**************************** X-Y Plot *****************************'
print '*******************************************************************'

# annual mean of meridional energy transport at each latitude in north hemisphere
fig1 = plt.figure()
plt.axhline(y=0, color='k',ls='-')
plt.plot(latitude_ERAI,np.mean(np.mean(AMET_E_ERAI_full,0),0),'b-',label='ERA-Interim')
plt.fill_between(latitude_ERAI,AMET_E_ERAI_error_plus,AMET_E_ERAI_error_minus,alpha=0.2,edgecolor='lightskyblue', facecolor='lightskyblue')
plt.plot(latitude_MERRA2,np.mean(np.mean(AMET_E_MERRA2_full,0),0),'r-',label='MERRA2')
plt.fill_between(latitude_MERRA2,AMET_E_MERRA2_error_plus,AMET_E_MERRA2_error_minus,alpha=0.2,edgecolor='tomato', facecolor='tomato')
plt.plot(latitude_JRA55,np.mean(np.mean(AMET_E_JRA55_full,0),0),'g-',label='JRA55')
plt.fill_between(latitude_JRA55,AMET_E_JRA55_error_plus,AMET_E_JRA55_error_minus,alpha=0.2,edgecolor='lightgreen', facecolor='lightgreen')
plt.title('Annual Mean of Atmospheric Meridional Energy Transport' )
plt.legend()
plt.xlabel("Latitudes")
labels =['20','30','40','50','60','70','80','90']
plt.xticks(np.linspace(20, 90, 8),labels)
plt.ylabel("Meridional Energy Transport (PW)")
plt.legend()
plt.show()
fig1.savefig(output_path + os.sep + 'Comp_AMET_annual_mean_E.jpg', dpi = 500)

# annual mean of meridional energy transport and each component at each latitude in north hemisphere
fig2 = plt.figure()
plt.axhline(y=0, color='k',ls='-')
plt.plot(latitude_ERAI,np.mean(np.mean(AMET_E_ERAI_full,0),0),'b-',label='ERA total')
plt.plot(latitude_MERRA2,np.mean(np.mean(AMET_E_MERRA2_full,0),0),'b--',label='MERRA total')
plt.plot(latitude_JRA55,np.mean(np.mean(AMET_E_JRA55_full,0),0),'b-.',label='JRA total')
plt.plot(latitude_ERAI,np.mean(np.mean(AMET_E_cpT_ERAI_full,0),0),'r-',label='ERA cpT')
plt.plot(latitude_MERRA2,np.mean(np.mean(AMET_E_cpT_MERRA2_full,0),0),'r--',label='MERRA cpT')
plt.plot(latitude_JRA55,np.mean(np.mean(AMET_E_cpT_JRA55_full,0),0),'r-.',label='JRA cpT')
plt.plot(latitude_ERAI,np.mean(np.mean(AMET_E_Lvq_ERAI_full,0),0),'m-',label='ERA Lvq')
plt.plot(latitude_MERRA2,np.mean(np.mean(AMET_E_Lvq_MERRA2_full,0),0),'m--',label='MERRA Lvq')
plt.plot(latitude_JRA55,np.mean(np.mean(AMET_E_Lvq_JRA55_full,0),0),'m-.',label='JRA Lvq')
plt.plot(latitude_ERAI,np.mean(np.mean(AMET_E_gz_ERAI_full,0),0),'g-',label='ERA gz')
plt.plot(latitude_MERRA2,np.mean(np.mean(AMET_E_gz_MERRA2_full,0),0),'g--',label='MERRA gz')
plt.plot(latitude_JRA55,np.mean(np.mean(AMET_E_gz_JRA55_full,0),0),'g-.',label='JRA gz')
plt.plot(latitude_ERAI,np.mean(np.mean(AMET_E_uv2_ERAI_full,0),0),'c-',label='ERA uv2')
plt.plot(latitude_MERRA2,np.mean(np.mean(AMET_E_uv2_MERRA2_full,0),0),'c--',label='MERRA uv2')
plt.plot(latitude_JRA55,np.mean(np.mean(AMET_E_uv2_JRA55_full,0),0),'c-.',label='JRA uv2')
plt.title('Annual Mean of Atmospheric Meridional Energy Transport and Each Component' )
plt.legend()
fig2.set_size_inches(10, 8)
plt.xlabel("Latitudes")
labels =['20','30','40','50','60','70','80','90']
plt.xticks(np.linspace(20, 90, 8),labels)
plt.ylabel("Meridional Energy Transport (PW)")
plt.legend()
plt.show()
fig2.savefig(output_path + os.sep + 'Comp_AMET_annual_mean_full_components.jpg',dpi = 500)
print '*******************************************************************'
print '*************************** time series ***************************'
print '*******************************************************************'
index_1980_2016 = np.arange(13,457,1)
index_1979_2016 = np.arange(1,457,1)
index_1979_2015 = np.arange(1,445,1)

# plot the AMET with running mean
# total energy transport
fig3 = plt.figure()
plt.plot(index_1979_2016,AMET_E_ERAI_series,'b--',linewidth=1.0,label='ERAI time series')
plt.plot(index_1979_2016[window-1:],AMET_E_ERAI_running_mean,'b-',linewidth=2.0,label='ERAI running mean')
plt.plot(index_1980_2016,AMET_E_MERRA2_series,'r--',linewidth=1.0,label='MERRA2 time series')
plt.plot(index_1980_2016[window-1:],AMET_E_MERRA2_running_mean,'r-',linewidth=2.0,label='MERRA2 running mean')
plt.plot(index_1979_2015,AMET_E_JRA55_series,'g--',linewidth=1.0,label='JRA55 time series')
plt.plot(index_1979_2015[window-1:],AMET_E_JRA55_running_mean,'g-',linewidth=2.0,label='JRA55 running mean')
plt.title('Running Mean of AMET at 60N with a window of %d months' % (window))
plt.legend()
fig3.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(0, 456, 39), year_ERAI)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.legend()
plt.show()
fig3.savefig(output_path + os.sep +'Comp_AMET_E_60N_running_mean_window_%d_comp.jpg' % (window), dpi = 500)

# internal energy
fig4 = plt.figure()
plt.plot(index_1979_2016,AMET_E_cpT_ERAI_series,'b--',linewidth=1.0,label='ERAI time series')
plt.plot(index_1979_2016[window-1:],AMET_E_cpT_ERAI_running_mean,'b-',linewidth=2.0,label='ERAI running mean')
plt.plot(index_1980_2016,AMET_E_cpT_MERRA2_series,'r--',linewidth=1.0,label='MERRA2 time series')
plt.plot(index_1980_2016[window-1:],AMET_E_cpT_MERRA2_running_mean,'r-',linewidth=2.0,label='MERRA2 running mean')
plt.plot(index_1979_2015,AMET_E_cpT_JRA55_series,'g--',linewidth=1.0,label='JRA55 time series')
plt.plot(index_1979_2015[window-1:],AMET_E_cpT_JRA55_running_mean,'g-',linewidth=2.0,label='JRA55 running mean')
plt.title('Running Mean of AMET (cpT) at 60N with a window of %d months' % (window))
plt.legend()
fig4.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(0, 456, 39), year_ERAI)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.legend()
plt.show()
fig4.savefig(output_path + os.sep +'Comp_AMET_cpT_60N_running_mean_window_%d_comp.jpg' % (window), dpi = 500)

# latent heat
fig5 = plt.figure()
plt.plot(index_1979_2016,AMET_E_Lvq_ERAI_series,'b--',linewidth=1.0,label='ERAI time series')
plt.plot(index_1979_2016[window-1:],AMET_E_Lvq_ERAI_running_mean,'b-',linewidth=2.0,label='ERAI running mean')
plt.plot(index_1980_2016,AMET_E_Lvq_MERRA2_series,'r--',linewidth=1.0,label='MERRA2 time series')
plt.plot(index_1980_2016[window-1:],AMET_E_Lvq_MERRA2_running_mean,'r-',linewidth=2.0,label='MERRA2 running mean')
plt.plot(index_1979_2015,AMET_E_Lvq_JRA55_series,'g--',linewidth=1.0,label='JRA55 time series')
plt.plot(index_1979_2015[window-1:],AMET_E_Lvq_JRA55_running_mean,'g-',linewidth=2.0,label='JRA55 running mean')
plt.title('Running Mean of AMET (Lvq) at 60N with a window of %d months' % (window))
plt.legend()
fig5.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(0, 456, 39), year_ERAI)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.legend()
plt.show()
fig5.savefig(output_path + os.sep +'Comp_AMET_E_Lvq_60N_running_mean_window_%d_comp.jpg' % (window), dpi = 500)

# geopotential
fig6 = plt.figure()
plt.plot(index_1979_2016,AMET_E_gz_ERAI_series,'b--',linewidth=1.0,label='ERAI time series')
plt.plot(index_1979_2016[window-1:],AMET_E_gz_ERAI_running_mean,'b-',linewidth=2.0,label='ERAI running mean')
plt.plot(index_1980_2016,AMET_E_gz_MERRA2_series,'r--',linewidth=1.0,label='MERRA2 time series')
plt.plot(index_1980_2016[window-1:],AMET_E_gz_MERRA2_running_mean,'r-',linewidth=2.0,label='MERRA2 running mean')
plt.plot(index_1979_2015,AMET_E_gz_JRA55_series,'g--',linewidth=1.0,label='JRA55 time series')
plt.plot(index_1979_2015[window-1:],AMET_E_gz_JRA55_running_mean,'g-',linewidth=2.0,label='JRA55 running mean')
plt.title('Running Mean of AMET (gz) at 60N with a window of %d months' % (window))
plt.legend()
fig6.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(0, 456, 39), year_ERAI)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.legend()
plt.show()
fig6.savefig(output_path + os.sep +'Comp_AMET_E_gz_60N_running_mean_window_%d_comp.jpg' % (window), dpi = 500)

# kinetic energy
fig7 = plt.figure()
plt.plot(index_1979_2016,AMET_E_uv2_ERAI_series,'b--',linewidth=1.0,label='ERAI time series')
plt.plot(index_1979_2016[window-1:],AMET_E_uv2_ERAI_running_mean,'b-',linewidth=2.0,label='ERAI running mean')
plt.plot(index_1980_2016,AMET_E_uv2_MERRA2_series,'r--',linewidth=1.0,label='MERRA2 time series')
plt.plot(index_1980_2016[window-1:],AMET_E_uv2_MERRA2_running_mean,'r-',linewidth=2.0,label='MERRA2 running mean')
plt.plot(index_1979_2015,AMET_E_uv2_JRA55_series,'g--',linewidth=1.0,label='JRA55 time series')
plt.plot(index_1979_2015[window-1:],AMET_E_uv2_JRA55_running_mean,'g-',linewidth=2.0,label='JRA55 running mean')
plt.title('Running Mean of AMET (uv2) at 60N with a window of %d months' % (window))
plt.legend()
fig7.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(0, 456, 39), year_ERAI)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.legend()
plt.show()
fig7.savefig(output_path + os.sep +'Comp_AMET_E_uv2_60N_running_mean_window_%d_comp.jpg' % (window), dpi = 500)

# plot the AMET after removing the seasonal cycling with running mean
fig8 = plt.figure()
plt.plot(index_1979_2016,AMET_E_ERAI_white_series,'b--',linewidth=1.0,label='ERAI time series')
plt.plot(index_1979_2016[window-1:],AMET_E_ERAI_white_running_mean,'b-',linewidth=2.0,label='ERAI running mean')
plt.plot(index_1980_2016,AMET_E_MERRA2_white_series,'r--',linewidth=1.0,label='MERRA2 time series')
plt.plot(index_1980_2016[window-1:],AMET_E_MERRA2_white_running_mean,'r-',linewidth=2.0,label='MERRA2 running mean')
plt.plot(index_1979_2015,AMET_E_JRA55_white_series,'g--',linewidth=1.0,label='JRA55 time series')
plt.plot(index_1979_2015[window-1:],AMET_E_JRA55_white_running_mean,'g-',linewidth=2.0,label='JRA55 running mean')
plt.title('Running Mean of AMET Anomalies at 60N with a window of %d months' % (window))
plt.legend()
fig8.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(0, 456, 39), year_ERAI)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.legend()
plt.show()
fig8.savefig(output_path + os.sep + 'anomaly' + os.sep +'Comp_AMET_E_anomaly_60N_running_mean_window_%d_comp.jpg' % (window), dpi = 500)

#internal energy
fig9 = plt.figure()
plt.plot(index_1979_2016,AMET_E_cpT_ERAI_white_series,'b--',linewidth=1.0,label='ERAI time series')
plt.plot(index_1979_2016[window-1:],AMET_E_cpT_ERAI_white_running_mean,'b-',linewidth=2.0,label='ERAI running mean')
plt.plot(index_1980_2016,AMET_E_cpT_MERRA2_white_series,'r--',linewidth=1.0,label='MERRA2 time series')
plt.plot(index_1980_2016[window-1:],AMET_E_cpT_MERRA2_white_running_mean,'r-',linewidth=2.0,label='MERRA2 running mean')
plt.plot(index_1979_2015,AMET_E_cpT_JRA55_white_series,'g--',linewidth=1.0,label='JRA55 time series')
plt.plot(index_1979_2015[window-1:],AMET_E_cpT_JRA55_white_running_mean,'g-',linewidth=2.0,label='JRA55 running mean')
plt.title('Running Mean of AMET (cpT) Anomalies at 60N with a window of %d months' % (window))
plt.legend()
fig9.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(0, 456, 39), year_ERAI)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.legend()
plt.show()
fig9.savefig(output_path + os.sep + 'anomaly' + os.sep +'Comp_AMET_E_cpT_anomaly_60N_running_mean_window_%d_comp.jpg' % (window), dpi = 500)

# latent heat
fig10 = plt.figure()
plt.plot(index_1979_2016,AMET_E_Lvq_ERAI_white_series,'b--',linewidth=1.0,label='ERAI time series')
plt.plot(index_1979_2016[window-1:],AMET_E_Lvq_ERAI_white_running_mean,'b-',linewidth=2.0,label='ERAI running mean')
plt.plot(index_1980_2016,AMET_E_Lvq_MERRA2_white_series,'r--',linewidth=1.0,label='MERRA2 time series')
plt.plot(index_1980_2016[window-1:],AMET_E_Lvq_MERRA2_white_running_mean,'r-',linewidth=2.0,label='MERRA2 running mean')
plt.plot(index_1979_2015,AMET_E_Lvq_JRA55_white_series,'g--',linewidth=1.0,label='JRA55 time series')
plt.plot(index_1979_2015[window-1:],AMET_E_Lvq_JRA55_white_running_mean,'g-',linewidth=2.0,label='JRA55 running mean')
plt.title('Running Mean of AMET (Lvq) Anomalies at 60N with a window of %d months' % (window))
plt.legend()
fig10.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(0, 456, 39), year_ERAI)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.legend()
plt.show()
fig10.savefig(output_path + os.sep + 'anomaly' + os.sep +'Comp_AMET_E_Lvq_anomaly_60N_running_mean_window_%d_comp.jpg' % (window), dpi = 500)

# geopotential
fig11 = plt.figure()
plt.plot(index_1979_2016,AMET_E_gz_ERAI_white_series,'b--',linewidth=1.0,label='ERAI time series')
plt.plot(index_1979_2016[window-1:],AMET_E_gz_ERAI_white_running_mean,'b-',linewidth=2.0,label='ERAI running mean')
plt.plot(index_1980_2016,AMET_E_gz_MERRA2_white_series,'r--',linewidth=1.0,label='MERRA2 time series')
plt.plot(index_1980_2016[window-1:],AMET_E_gz_MERRA2_white_running_mean,'r-',linewidth=2.0,label='MERRA2 running mean')
plt.plot(index_1979_2015,AMET_E_gz_JRA55_white_series,'g--',linewidth=1.0,label='JRA55 time series')
plt.plot(index_1979_2015[window-1:],AMET_E_gz_JRA55_white_running_mean,'g-',linewidth=2.0,label='JRA55 running mean')
plt.title('Running Mean of AMET (gz) Anomalies at 60N with a window of %d months' % (window))
plt.legend()
fig11.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(0, 456, 39), year_ERAI)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.legend()
plt.show()
fig11.savefig(output_path + os.sep + 'anomaly' + os.sep + 'Comp_AMET_E_gz_anomaly_60N_running_mean_window_%d_comp.jpg' % (window), dpi = 500)

# kinetic energy
fig12 = plt.figure()
plt.plot(index_1979_2016,AMET_E_uv2_ERAI_white_series,'b--',linewidth=1.0,label='ERAI time series')
plt.plot(index_1979_2016[window-1:],AMET_E_uv2_ERAI_white_running_mean,'b-',linewidth=2.0,label='ERAI running mean')
plt.plot(index_1980_2016,AMET_E_uv2_MERRA2_white_series,'r--',linewidth=1.0,label='MERRA2 time series')
plt.plot(index_1980_2016[window-1:],AMET_E_uv2_MERRA2_white_running_mean,'r-',linewidth=2.0,label='MERRA2 running mean')
plt.plot(index_1979_2015,AMET_E_uv2_JRA55_white_series,'g--',linewidth=1.0,label='JRA55 time series')
plt.plot(index_1979_2015[window-1:],AMET_E_uv2_JRA55_white_running_mean,'g-',linewidth=2.0,label='JRA55 running mean')
plt.title('Running Mean of AMET (uv2) Anomalies at 60N with a window of %d months' % (window))
plt.legend()
fig12.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(0, 456, 39), year_ERAI)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.legend()
plt.show()
fig12.savefig(output_path + os.sep + 'anomaly' + os.sep +'Comp_AMET_E_uv2_anomaly_60N_running_mean_window_%d_comp.jpg' % (window), dpi = 500)

print '*******************************************************************'
print '******************   highlight the difference   *******************'
print '*******************************************************************'
# caculate the differnce between datasets for each component
# ERA-Interim minus MERRA2
# time series at 60N
fig13 = plt.figure()
plt.plot(index_1980_2016,AMET_E_ERAI_series[12:] - AMET_E_MERRA2_series,'b-',linewidth=1.0,label='Total')
plt.plot(index_1980_2016,AMET_E_cpT_ERAI_series[12:] - AMET_E_cpT_MERRA2_series,'r-',linewidth=1.0,label='cpT')
plt.plot(index_1980_2016,AMET_E_Lvq_ERAI_series[12:] - AMET_E_Lvq_MERRA2_series,'m-',linewidth=1.0,label='Lvq')
plt.plot(index_1980_2016,AMET_E_gz_ERAI_series[12:] - AMET_E_gz_MERRA2_series,'g-',linewidth=1.0,label='gz')
plt.plot(index_1980_2016,AMET_E_uv2_ERAI_series[12:] - AMET_E_uv2_MERRA2_series,'c-',linewidth=1.0,label='uv2')
plt.title('Difference between ERA-Interim and MERRA2 (time series) at 60N')
plt.legend()
fig13.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(0, 444, 38), year_MERRA2)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport residual (PW)")
plt.legend()
plt.show()
fig13.savefig(output_path + os.sep + 'Comp_AMET_ERAI_minus_MERRA2_60N.jpg', dpi = 500)

# anomaly of time series at 60N
fig14 = plt.figure()
plt.plot(index_1980_2016,AMET_E_ERAI_white_series[12:] - AMET_E_MERRA2_white_series,'b-',linewidth=1.0,label='Total')
plt.plot(index_1980_2016,AMET_E_cpT_ERAI_white_series[12:] - AMET_E_cpT_MERRA2_white_series,'r-',linewidth=1.0,label='cpT')
plt.plot(index_1980_2016,AMET_E_Lvq_ERAI_white_series[12:] - AMET_E_Lvq_MERRA2_white_series,'m-',linewidth=1.0,label='Lvq')
plt.plot(index_1980_2016,AMET_E_gz_ERAI_white_series[12:] - AMET_E_gz_MERRA2_white_series,'g-',linewidth=1.0,label='gz')
plt.plot(index_1980_2016,AMET_E_uv2_ERAI_white_series[12:] - AMET_E_uv2_MERRA2_white_series,'c-',linewidth=1.0,label='uv2')
plt.title('Difference between ERA-Interim and MERRA2 anomalies (time series) at 60N')
plt.legend()
fig14.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(0, 444, 38), year_MERRA2)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport residual (PW)")
plt.legend()
plt.show()
fig14.savefig(output_path + os.sep + 'Comp_AMET_ERAI_minus_MERRA2_anomaly_60N.jpg', dpi = 500)

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