#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : Compare AMET and OMET of all reanalysis datasets
Author          : Yang Liu
Date            : 2017.11.12
Last Update     : 2018.01.10
Description     : The code aims to plot and compare the meridional energy transport
                  in both the atmosphere and ocean. The atmospheric meridional energy
                  transport is calculated from reanalysis data ERA-Interim, MERRA2 and
                  JRA55. The oceanic meridional energy transport is calculated from ORAS4,
                  GLORYS2V3, SODA3 and ORAS5.
Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, sys, matplotlib, logging
variables       : Atmospheric Meridional Energy Transport   ERA-Interim
                  Oceanic Meridional Energy Transport       ORAS4
Caveat!!        : Spatial and temporal coverage
                  Atmosphere
                  ERA-Interim 1979 - 2016
                  MERRA2      1980 - 2016
                  JRA55       1979 - 2015
                  Ocean
                  GLORYS2V3   1992 - 2014
                  ORAS4       1968 - 2014
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
# specify data path
datapath_ERAI = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ERAI/postprocessing'
datapath_MERRA2 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/MERRA2/postprocessing'
datapath_JRA55 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/JRA55/postprocessing'

datapath_ORAS4 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ORAS4/postprocessing'
datapath_GLORYS2V3 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/GLORYS2V3/postprocessing'
# specify output path for the netCDF4 file
output_path = '/home/yang/NLeSC/Computation_Modeling/BlueAction/Bjerknes/AMET_OMET'
# index of latitude for insteret
# 60N
lat_ERAI = 40 # at 60 N
lat_MERRA2 = 80 # at 60 N
lat_JRA55 = 53 # at 60 N

lat_GLORYS2V3 = 788 # at 60 N
lat_ORAS4 = 233 # at 60 N
# after a cut to 20-90 N
lat_ORAS4_cut = 53 # at 60 N
lat_GLORYS2V3_cut = 209 # at 60 N
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

dataset_ERAI = Dataset(datapath_ERAI + os.sep + 'model_daily_075_1979_2016_E_zonal_int.nc')
dataset_MERRA2 = Dataset(datapath_MERRA2 + os.sep + 'AMET_MERRA2_model_daily_1980_2016_E_zonal_int.nc')
dataset_JRA55 = Dataset(datapath_JRA55 + os.sep + 'AMET_JRA55_model_daily_1979_2015_E_zonal_int.nc')

dataset_GLORYS2V3 = Dataset(datapath_GLORYS2V3 + os.sep + 'GLORYS2V3_model_monthly_orca025_E_zonal_int.nc')
dataset_ORAS4 = Dataset(datapath_ORAS4 + os.sep + 'oras4_model_monthly_orca1_E_zonal_int.nc')

#dataset_AMET_point = Dataset(datapath_AMET + os.sep + 'model_daily_075_1979_2016_E_point.nc')
#dataset_OMET_point = Dataset(datapath_OMET + os.sep + 'oras4_model_monthly_orca1_1958_2014_E_point.nc')

for k in dataset_ERAI.variables:
    print dataset_ERAI.variables['%s' % (k)]

# from 1979 to 2014
# from 20N - 90N
AMET_ERAI = dataset_ERAI.variables['E'][:]/1000 # from Tera Watt to Peta Watt
AMET_MERRA2 = dataset_MERRA2.variables['E'][:]/1000 # from Tera Watt to Peta Watt
AMET_JRA55 = dataset_JRA55.variables['E'][:,:,0:124]/1000 # from Tera Watt to Peta Watt

OMET_ORAS4 = dataset_ORAS4.variables['E'][21:,:,180:]/1000 # start from 1979
OMET_GLORYS2V3 = dataset_GLORYS2V3.variables['E'][:,:,579:]/1000 # start from 1993

year_ERAI = dataset_ERAI.variables['year'][:]             # from 1979 to 2014
year_MERRA2 = dataset_MERRA2.variables['year'][:]         # from 1980 to 2014
year_JRA55 = dataset_JRA55.variables['year'][:]           # from 1979 to 2015

year_ORAS4 = dataset_ORAS4.variables['year'][21:]         # from 1979 to 2014
year_GLORYS2V3 = dataset_GLORYS2V3.variables['year'][:]   # from 1993 to 2014

latitude_ERAI = dataset_ERAI.variables['latitude'][:]
latitude_MERRA2 = dataset_MERRA2.variables['latitude'][:]
latitude_JRA55 = dataset_JRA55.variables['latitude'][0:124]

latitude_ORAS4 = dataset_ORAS4.variables['latitude_aux'][180:]
latitude_GLORYS2V3 = dataset_GLORYS2V3.variables['latitude_aux'][579:]

print '*******************************************************************'
print '*************************** whitening *****************************'
print '*******************************************************************'
month_ind = np.arange(12)
seansonal_cycle_AMET_ERAI = np.mean(AMET_ERAI,axis=0)
seansonal_cycle_AMET_MERRA2 = np.mean(AMET_MERRA2,axis=0)
seansonal_cycle_AMET_JRA55 = np.mean(AMET_JRA55,axis=0)

seansonal_cycle_OMET_ORAS4 = np.mean(OMET_ORAS4,axis=0)
seansonal_cycle_OMET_GLORYS2V3 = np.mean(OMET_GLORYS2V3,axis=0)

AMET_ERAI_white = np.zeros(AMET_ERAI.shape,dtype=float)
AMET_MERRA2_white = np.zeros(AMET_MERRA2.shape,dtype=float)
AMET_JRA55_white = np.zeros(AMET_JRA55.shape,dtype=float)

OMET_ORAS4_white = np.zeros(OMET_ORAS4.shape,dtype=float)
OMET_GLORYS2V3_white = np.zeros(OMET_GLORYS2V3.shape,dtype=float)

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

print '*******************************************************************'
print '****************** prepare variables for plot *********************'
print '*******************************************************************'
# annual mean of AMET and OMET at different latitudes
AMET_ERAI_mean = np.mean(np.mean(AMET_ERAI,0),0)
AMET_MERRA2_mean = np.mean(np.mean(AMET_MERRA2,0),0)
AMET_JRA55_mean = np.mean(np.mean(AMET_JRA55,0),0)

OMET_ORAS4_mean = np.mean(np.mean(OMET_ORAS4,0),0)
OMET_GLORYS2V3_mean = np.mean(np.mean(OMET_GLORYS2V3,0),0)

# dataset with seasonal cycle - time series
AMET_ERAI_series = AMET_ERAI.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI))
AMET_MERRA2_series = AMET_MERRA2.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2))
AMET_JRA55_series = AMET_JRA55.reshape(len(year_JRA55)*len(month_ind),len(latitude_JRA55))

OMET_ORAS4_series = OMET_ORAS4.reshape(len(year_ORAS4)*len(month_ind),len(latitude_ORAS4))
OMET_GLORYS2V3_series = OMET_GLORYS2V3.reshape(len(year_GLORYS2V3)*len(month_ind),len(latitude_GLORYS2V3))
# dataset without seasonal cycle - time series
AMET_ERAI_white_series = AMET_ERAI_white.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI))
AMET_MERRA2_white_series = AMET_MERRA2_white.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2))
AMET_JRA55_white_series = AMET_JRA55_white.reshape(len(year_JRA55)*len(month_ind),len(latitude_JRA55))

OMET_ORAS4_white_series = OMET_ORAS4_white.reshape(len(year_ORAS4)*len(month_ind),len(latitude_ORAS4))
OMET_GLORYS2V3_white_series = OMET_GLORYS2V3_white.reshape(len(year_GLORYS2V3)*len(month_ind),len(latitude_GLORYS2V3))

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
AMET_ERAI_white_series_running_mean = np.zeros((len(AMET_ERAI_white_series)-window+1,len(latitude_ERAI)),dtype=float)
AMET_MERRA2_white_series_running_mean = np.zeros((len(AMET_MERRA2_white_series)-window+1,len(latitude_MERRA2)),dtype=float)
AMET_JRA55_white_series_running_mean = np.zeros((len(AMET_JRA55_white_series)-window+1,len(latitude_JRA55)),dtype=float)

OMET_ORAS4_white_series_running_mean = np.zeros((len(OMET_ORAS4_white_series)-window+1,len(latitude_ORAS4)),dtype=float)
OMET_GLORYS2V3_white_series_running_mean = np.zeros((len(OMET_GLORYS2V3_white_series)-window+1,len(latitude_GLORYS2V3)),dtype=float)

for i in np.arange(len(AMET_ERAI_white_series)-window+1):
    for j in np.arange(len(latitude_ERAI)):
        AMET_ERAI_white_series_running_mean[i,j] = np.mean(AMET_ERAI_white_series[i:i+window,j])

for i in np.arange(len(AMET_MERRA2_white_series)-window+1):
    for j in np.arange(len(latitude_MERRA2)):
        AMET_MERRA2_white_series_running_mean[i,j] = np.mean(AMET_MERRA2_white_series[i:i+window,j])

for i in np.arange(len(AMET_JRA55_white_series)-window+1):
    for j in np.arange(len(latitude_JRA55)):
        AMET_JRA55_white_series_running_mean[i,j] = np.mean(AMET_JRA55_white_series[i:i+window,j])

for i in np.arange(len(OMET_ORAS4_white_series)-window+1):
    for j in np.arange(len(latitude_ORAS4)):
        OMET_ORAS4_white_series_running_mean[i,j] = np.mean(OMET_ORAS4_white_series[i:i+window,j])

for i in np.arange(len(OMET_GLORYS2V3_white_series)-window+1):
    for j in np.arange(len(latitude_GLORYS2V3)):
        OMET_GLORYS2V3_white_series_running_mean[i,j] = np.mean(OMET_GLORYS2V3_white_series[i:i+window,j])
print '*******************************************************************'
print '*************************** x-y plots *****************************'
print '*******************************************************************'
fig0 = plt.figure()
plt.plot(latitude_ERAI,AMET_ERAI_mean,'b-',label='ERA-Interim')
plt.plot(latitude_MERRA2,AMET_MERRA2_mean,'r-',label='MERRA2')
plt.plot(latitude_JRA55,AMET_JRA55_mean,'g-',label='JRA55')
plt.plot(latitude_ORAS4,OMET_ORAS4_mean,'c-',label='ORAS4')
plt.plot(latitude_GLORYS2V3,OMET_GLORYS2V3_mean,'m-',label='GLORYS2V3')
#plt.plot(latitude_AMET,AMET_mean + OMET_mean_interpolate,'g--',label='Total')
plt.title('Meridional Energy Transport')
plt.legend()
#fig1.set_size_inches(5, 5)
plt.xlabel("Latitude")
labels =['20','30','40','50','60','70','80','90']
plt.xticks(np.linspace(20, 90, 8),labels)
#plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig0.savefig(output_path + os.sep + 'AMET_OMET_annual_mean.jpg', dpi = 500)

print '*******************************************************************'
print '*********************** time series plots *************************'
print '*******************************************************************'
# index and namelist of years for time series and running mean time series
index_1993_2014 = np.arange(169,433,1) # starting from index of year 1993
index_1979_2014 = np.arange(1,433,1)
index_1980_2016 = np.arange(13,457,1)
index_1979_2016 = np.arange(1,457,1)
index_1979_2015 = np.arange(1,445,1)

# time series plot of meridional energy transport at 60N
fig1 = plt.figure()
plt.plot(index_1979_2016,AMET_ERAI_series[:,lat_ERAI],'b-',label='ERA-Interim')
plt.plot(index_1980_2016,AMET_MERRA2_series[:,lat_MERRA2],'r-',label='MERRA2')
plt.plot(index_1979_2015,AMET_JRA55_series[:,lat_JRA55],'g-',label='JRA55')
plt.plot(index_1979_2014,OMET_ORAS4_series[:,lat_ORAS4_cut],'c-',label='ORAS4')
plt.plot(index_1993_2014,OMET_GLORYS2V3_series[:,lat_GLORYS2V3_cut],'m-',label='GLORYS2V3')
plt.title('Meridional Energy Transport at 60 N')
plt.legend()
fig1.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(0, 456, 39), year_ERAI)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig1.savefig(output_path + os.sep + 'AMET_OMET_60N_total_time_series.jpg', dpi = 500)

# time series plot of meridional energy transport anomalies at 60N
fig2 = plt.figure()
plt.plot(index_1979_2016,AMET_ERAI_white_series[:,lat_ERAI],'b-',label='ERA-Interim')
plt.plot(index_1980_2016,AMET_MERRA2_white_series[:,lat_MERRA2],'r-',label='MERRA2')
plt.plot(index_1979_2015,AMET_JRA55_white_series[:,lat_JRA55],'g-',label='JRA55')
plt.plot(index_1979_2014,OMET_ORAS4_white_series[:,lat_ORAS4_cut],'c-',label='ORAS4')
plt.plot(index_1993_2014,OMET_GLORYS2V3_white_series[:,lat_GLORYS2V3_cut],'m-',label='GLORYS2V3')
plt.title('Meridional Energy Transport Anomalies at 60 N')
plt.legend()
fig2.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(0, 456, 39), year_ERAI)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig2.savefig(output_path + os.sep + 'AMET_OMET_60N_anomaly_time_series.jpg', dpi = 500)

# time series plot of meridional energy transport anomalies at 60N with x years running mean
fig3 = plt.figure()
plt.plot(index_1979_2016[window-1:],AMET_ERAI_white_series_running_mean[:,lat_ERAI],'b-',label='ERA-Interim')
plt.plot(index_1980_2016[window-1:],AMET_MERRA2_white_series_running_mean[:,lat_MERRA2],'r-',label='MERRA2')
plt.plot(index_1979_2015[window-1:],AMET_JRA55_white_series_running_mean[:,lat_JRA55],'g-',label='JRA55')
plt.plot(index_1979_2014[window-1:],OMET_ORAS4_white_series_running_mean[:,lat_ORAS4_cut],'c-',label='ORAS4')
plt.plot(index_1993_2014[window-1:],OMET_GLORYS2V3_white_series_running_mean[:,lat_GLORYS2V3_cut],'m-',label='GLORYS2V3')
plt.title('Meridional Energy Transport Anomalies with running mean of %d months at 60 N' % (window))
plt.legend()
fig3.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(0, 456, 39), year_ERAI)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig3.savefig(output_path + os.sep + 'AMET_OMET_60N_anomaly_running_mean_%dm_time_series.jpg' % (window), dpi = 500)

print '*******************************************************************'
print '****************** maps (average of point data) *******************'
print '*******************************************************************'
