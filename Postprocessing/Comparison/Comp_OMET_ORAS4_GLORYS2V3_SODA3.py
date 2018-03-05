#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : Compare oceanic meridional energy transport (ORAS4,GLORYS2V3)
Author          : Yang Liu
Date            : 2017.11.06
Last Update     : 2018.03.06
Description     : The code aims to compare the oceanic meridional energy transport
                  calculated from different oceanic reanalysis datasets. In this,
                  case, this includes GLORYS2V3 from Mercator Ocean, ORAS4 from ECMWF,
                  and SODA3 from University of Maryland & TAMU.
Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, sys, matplotlib
variables       : Meridional Energy Transport               E         [Tera-Watt]
                  Meridional Overturning Circulation        Psi       [Sv]
Caveat!!        : MOM5 Grid
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

import numpy as np
import seaborn as sns
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
# specify output path for figures
output_path = '/home/yang/NLeSC/Computation_Modeling/BlueAction/OMET/Comparison'
# the threshold ( index of latitude) of the OMET
lat_GLORYS2V3 = 788 # at 60 N
lat_ORAS4 = 233 # at 60 N
lat_SODA3 = 789 # at 60 N

####################################################################################
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

# MOM5_z50
ji_5 = 1440
jj_5 = 1070
level_5 = 50

# zonal integral
dataset_GLORYS2V3 = Dataset(datapath_GLORYS2V3 + os.sep + 'GLORYS2V3_model_monthly_orca025_E_zonal_int.nc')
dataset_ORAS4 = Dataset(datapath_ORAS4 + os.sep + 'oras4_model_monthly_orca1_E_zonal_int.nc')
dataset_SODA3 = Dataset(datapath_SODA3 + os.sep + 'OMET_SODA3_model_5daily_1980_2015_E_zonal_int.nc')
# extract Oceanic meridional energy transport
# dimension (year,month,latitude)
# full latitude
OMET_GLORYS2V3_full = dataset_GLORYS2V3.variables['E'][:]/1000
OMET_ORAS4_full = dataset_ORAS4.variables['E'][21:,:,:]/1000
OMET_SODA3_full = dataset_SODA3.variables['E'][:]/1000
# selected latitude (60N)
OMET_GLORYS2V3 = dataset_GLORYS2V3.variables['E'][:,:,lat_GLORYS2V3]/1000 # from Tera Watt to Peta Watt # start from 1993
OMET_ORAS4 = dataset_ORAS4.variables['E'][21:,:,lat_ORAS4]/1000 # from Tera Watt to Peta Watt # start from 1979
OMET_SODA3 = dataset_SODA3.variables['E'][:,:,lat_SODA3]/1000 # from Tera Watt to Peta Watt # start from 1979
# latitude
latitude_aux_GLORYS2V3 = dataset_GLORYS2V3.variables['latitude_aux'][:]
latitude_aux_ORAS4 = dataset_ORAS4.variables['latitude_aux'][:]
latitude_aux_SODA3 = dataset_SODA3.variables['latitude_aux'][:]
print '*******************************************************************'
print '*********************** prepare variables *************************'
print '*******************************************************************'
# take the time series of E
OMET_GLORYS2V3_series = OMET_GLORYS2V3.reshape(264)
OMET_ORAS4_series = OMET_ORAS4.reshape(432)
OMET_SODA3_series = OMET_SODA3.reshape(432)

print '*******************************************************************'
print '*************************** whitening *****************************'
print '*******************************************************************'
# remove the seasonal cycling of OMET at 60N
month_ind = np.arange(12)
# dimension of OMET[year,month]
# GLORYS2V3
OMET_GLORYS2V3_seansonal_cycle = np.mean(OMET_GLORYS2V3,axis=0)
OMET_GLORYS2V3_white = np.zeros(OMET_GLORYS2V3.shape,dtype=float)
for i in month_ind:
    OMET_GLORYS2V3_white[:,i] = OMET_GLORYS2V3[:,i] - OMET_GLORYS2V3_seansonal_cycle[i]
# take the time series of whitened OMET
OMET_GLORYS2V3_white_series = OMET_GLORYS2V3_white.reshape(264)
# ORAS4
OMET_ORAS4_seansonal_cycle = np.mean(OMET_ORAS4,axis=0)
OMET_ORAS4_white = np.zeros(OMET_ORAS4.shape,dtype=float)
for i in month_ind:
    OMET_ORAS4_white[:,i] = OMET_ORAS4[:,i] - OMET_ORAS4_seansonal_cycle[i]
# take the time series of whitened OMET
OMET_ORAS4_white_series = OMET_ORAS4_white.reshape(432)
# ORAS4
OMET_SODA3_seansonal_cycle = np.mean(OMET_SODA3,axis=0)
OMET_SODA3_white = np.zeros(OMET_SODA3.shape,dtype=float)
for i in month_ind:
    OMET_SODA3_white[:,i] = OMET_SODA3[:,i] - OMET_SODA3_seansonal_cycle[i]
# take the time series of whitened OMET
OMET_SODA3_white_series = OMET_SODA3_white.reshape(432)
print '*******************************************************************'
print '********************** Running mean/sum ***************************'
print '*******************************************************************'
# running mean is calculated on time series
# define the running window for the running mean
window = 12 # in month
#window = 60 # in month
#window = 120 # in month
# calculate the running mean and sum of OMET
# GLORYS2V3
OMET_GLORYS2V3_running_mean = np.zeros(len(OMET_GLORYS2V3_series)-window+1)
#OMET_running_sum = np.zeros(len(OMET_series)-window+1)
for i in np.arange(len(OMET_GLORYS2V3_series)-window+1):
    OMET_GLORYS2V3_running_mean[i] = np.mean(OMET_GLORYS2V3_series[i:i+window])
    #OMET_GLORYS2V3_running_sum[i] = np.sum(OMET_GLORYS2V3_series[i:i+window])

# ORAS4
OMET_ORAS4_running_mean = np.zeros(len(OMET_ORAS4_series)-window+1)
#OMET_running_sum = np.zeros(len(OMET_series)-window+1)
for i in np.arange(len(OMET_ORAS4_series)-window+1):
    OMET_ORAS4_running_mean[i] = np.mean(OMET_ORAS4_series[i:i+window])
    #OMET_running_sum[i] = np.sum(OMET_series[i:i+window])

# SODA3
OMET_SODA3_running_mean = np.zeros(len(OMET_SODA3_series)-window+1)
#OMET_running_sum = np.zeros(len(OMET_series)-window+1)
for i in np.arange(len(OMET_SODA3_series)-window+1):
    OMET_SODA3_running_mean[i] = np.mean(OMET_SODA3_series[i:i+window])
    #OMET_running_sum[i] = np.sum(OMET_series[i:i+window])

# calculate the running mean and sum of OMET after removing the seasonal cycling
# GLORYS2V3
OMET_GLORYS2V3_white_running_mean = np.zeros(len(OMET_GLORYS2V3_white_series)-window+1)
#OMET_running_sum = np.zeros(len(OMET_series)-window+1)
for i in np.arange(len(OMET_GLORYS2V3_white_series)-window+1):
    OMET_GLORYS2V3_white_running_mean[i] = np.mean(OMET_GLORYS2V3_white_series[i:i+window])
    #OMET_white_running_sum[i] = np.sum(OMET_white_series[i:i+window])

# ORAS4
OMET_ORAS4_white_running_mean = np.zeros(len(OMET_ORAS4_white_series)-window+1)
#OMET_running_sum = np.zeros(len(OMET_series)-window+1)
for i in np.arange(len(OMET_ORAS4_white_series)-window+1):
    OMET_ORAS4_white_running_mean[i] = np.mean(OMET_ORAS4_white_series[i:i+window])
    #OMET_white_running_sum[i] = np.sum(OMET_white_series[i:i+window])

# SODA3
OMET_SODA3_white_running_mean = np.zeros(len(OMET_SODA3_white_series)-window+1)
#OMET_running_sum = np.zeros(len(OMET_series)-window+1)
for i in np.arange(len(OMET_SODA3_white_series)-window+1):
    OMET_SODA3_white_running_mean[i] = np.mean(OMET_SODA3_white_series[i:i+window])
    #OMET_white_running_sum[i] = np.sum(OMET_white_series[i:i+window])
print '*******************************************************************'
print '*************************** time series ***************************'
print '*******************************************************************'
# index and namelist of years for time series and running mean time series
index_1993_begin = np.arange(1,265,1)
index_1993 = np.arange(169,433,1) # starting from index of year 1993
index_year_1993 = np.arange(1993,2015,1)

index_1979 = np.arange(1,433,1)
index_year_1979 = np.arange(1979,2015,1)

index_1980 = np.arange(13,445,1)
index_year_1980 = np.arange(1980,2016,1)

index_full = np.arange(1,445,1)
index_year_full = np.arange(1979,2016,1)
# index_running_mean_1993 = np.arange(169,433-window+1,1)
# index_year_running_mean_1993 = np.arange(1993+window/12,2015,1)
#
# index_running_mean_1979 = np.arange(1,433-window+1,1)
# index_year_running_mean_1979 = np.arange(1979+window/12,2015,1)

# plot the OMET after removing seasonal cycle
fig1 = plt.figure()
plt.plot(index_1979,OMET_ORAS4_white_series,'c-',label='ORAS4')
plt.plot(index_1993,OMET_GLORYS2V3_white_series,'m-',label='GLORYS2V3')
plt.plot(index_1980,OMET_SODA3_white_series,'y-',label='SODA3')
plt.title('Oceanic Meridional Energy Transport Anomaly at 60N (1979-2015)')
#plt.legend()
fig1.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(0, 444, 38), index_year_full)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.legend()
plt.show()
fig1.savefig(output_path + os.sep + 'anomaly' + os.sep + 'Comp_OMET_anomaly_60N_time_series_1979_2014.jpg', dpi = 500)

# plot the running mean of OMET after removing seasonal cycle
fig0 = plt.figure()
plt.plot(index_1979[window-1:],OMET_ORAS4_white_running_mean,'c-',label='ORAS4')
plt.plot(index_1993[window-1:],OMET_GLORYS2V3_white_running_mean,'m-',label='GLORYS2V3')
plt.plot(index_1980[window-1:],OMET_SODA3_white_running_mean,'y-',label='SODA3')
plt.title('Running Mean of OMET Anomalies at 60N with a window of %d months (1979-2015)' % (window))
#plt.legend()
fig0.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(0, 444, 38), index_year_full)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.legend()
plt.show()
fig0.savefig(output_path + os.sep + 'anomaly' + os.sep + 'Comp_OMET_anomaly_60N_running_mean_window_%d_only.jpg' % (window), dpi = 500)

# plot the OMET with running mean
fig2 = plt.figure()
plt.plot(index_1979,OMET_ORAS4_series,'c--',linewidth=1.0,label='ORAS4 time series')
plt.plot(index_1993,OMET_GLORYS2V3_series,'m--',linewidth=1.0,label='GLORYS2V3 time series')
plt.plot(index_1980,OMET_SODA3_series,'y--',linewidth=1.0,label='SODA3 time series')
plt.plot(index_1979[window-1:],OMET_ORAS4_running_mean,'c-',linewidth=2.0,label='ORAS4 running mean')
plt.plot(index_1993[window-1:],OMET_GLORYS2V3_running_mean,'m-',linewidth=2.0,label='GLORYS2V3 running mean')
plt.plot(index_1980[window-1:],OMET_SODA3_running_mean,'y-',linewidth=2.0,label='SODA3 running mean')
plt.title('Running Mean of OMET at 60N with a window of %d months (1979-2015)' % (window))
#plt.legend()
fig2.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(0, 444, 38), index_year_full)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.legend()
plt.show()
fig2.savefig(output_path + os.sep +'Comp_OMET_60N_running_mean_window_%d_comp.jpg' % (window), dpi = 500)

# plot the OMET after removing the seasonal cycling with running mean
fig3 = plt.figure()
plt.plot(index_1979,OMET_ORAS4_white_series,'c--',linewidth=1.0,label='ORAS4 time series')
plt.plot(index_1993,OMET_GLORYS2V3_white_series,'m--',linewidth=1.0,label='GLORYS2V3 time series')
plt.plot(index_1980,OMET_SODA3_white_series,'y--',linewidth=1.0,label='SODA3 time series')
plt.plot(index_1979[window-1:],OMET_ORAS4_white_running_mean,'c-',linewidth=2.0,label='ORAS4 running mean')
plt.plot(index_1993[window-1:],OMET_GLORYS2V3_white_running_mean,'m-',linewidth=2.0,label='GLORYS2V3 running mean')
plt.plot(index_1980[window-1:],OMET_SODA3_white_running_mean,'y-',linewidth=2.0,label='SODA3 running mean')
plt.title('Running Mean of OMET Anomalies at 60N with a window of %d months (1979-2015)' % (window))
#plt.legend()
fig3.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(0, 444, 38), index_year_full)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.legend()
plt.show()
fig3.savefig(output_path + os.sep + 'anomaly' + os.sep + 'Comp_OMET_anomaly_60N_running_mean_window_%d_comp.jpg' % (window), dpi = 500)


print '*******************************************************************'
print '***************   standard deviation at each lat   ****************'
print '*******************************************************************'
# standard deviation at each latitude
# for error bar band
# reshape of each dataset at full latitude for the calculation of standard deviation
# OMET_ORAS4_std = np.std(OMET_ORAS4_series,axis=0)
# OMET_ORAS4_error_plus = OMET_ORAS4_mean + OMET_ORAS4_std
# OMET_ORAS4_error_minus = OMET_ORAS4_mean - OMET_ORAS4_std
#
# OMET_GLORYS2V3_std = np.std(OMET_GLORYS2V3_full,axis=0)
# OMET_GLORYS2V3_error_plus = OMET_GLORYS2V3_mean + OMET_GLORYS2V3_std
# OMET_GLORYS2V3_error_minus = OMET_GLORYS2V3_mean - OMET_GLORYS2V3_std
print '*******************************************************************'
print '***************   span of annual mean at each lat   ***************'
print '*******************************************************************'
# calculate annual mean
OMET_ORAS4_full_annual_mean = np.mean(OMET_ORAS4_full[:,:,180:],1)
OMET_GLORYS2V3_full_annual_mean = np.mean(OMET_GLORYS2V3_full[:,:,579:],1)
OMET_SODA3_full_annual_mean = np.mean(OMET_SODA3_full[:,:,569:],1)
# calculate the difference between annual mean and mean of entire time series
OMET_ORAS4_full_annual_mean_max = np.amax(OMET_ORAS4_full_annual_mean,0)
OMET_GLORYS2V3_full_annual_mean_max = np.amax(OMET_GLORYS2V3_full_annual_mean,0)
OMET_SODA3_full_annual_mean_max = np.amax(OMET_SODA3_full_annual_mean,0)

OMET_ORAS4_full_annual_mean_min = np.amin(OMET_ORAS4_full_annual_mean,0)
OMET_GLORYS2V3_full_annual_mean_min = np.amin(OMET_GLORYS2V3_full_annual_mean,0)
OMET_SODA3_full_annual_mean_min = np.amin(OMET_SODA3_full_annual_mean,0)
print '*******************************************************************'
print '*************************** x-y lines  ****************************'
print '*******************************************************************'
fig44 = plt.figure()
plt.axhline(y=0, color='k',ls='-')
plt.plot(latitude_aux_ORAS4[180:],np.mean(np.mean(OMET_ORAS4_full[:,:,180:],0),0),'c-',label='ORAS4')
plt.fill_between(latitude_aux_ORAS4[180:],OMET_ORAS4_full_annual_mean_max,OMET_ORAS4_full_annual_mean_min,alpha=0.3,edgecolor='aquamarine', facecolor='aquamarine')
plt.plot(latitude_aux_GLORYS2V3[579:],np.mean(np.mean(OMET_GLORYS2V3_full[:,:,579:],0),0),'m-',label='GLORYS2V3')
plt.fill_between(latitude_aux_GLORYS2V3[579:],OMET_GLORYS2V3_full_annual_mean_max,OMET_GLORYS2V3_full_annual_mean_min,alpha=0.3,edgecolor='plum', facecolor='plum')
plt.plot(latitude_aux_SODA3[569:],np.mean(np.mean(OMET_SODA3_full[:,:,569:],0),0),'y-',label='SODA3')
plt.fill_between(latitude_aux_SODA3[569:],OMET_SODA3_full_annual_mean_max,OMET_SODA3_full_annual_mean_min,alpha=0.3,edgecolor='lightyellow', facecolor='lightyellow')
plt.title('Mean OMET of entire time series from 20N to 90N' )
#plt.legend()
plt.xlabel("Latitudes")
#plt.xticks()
plt.ylabel("Meridional Energy Transport (PW)")
plt.legend()
plt.show()
fig44.savefig(output_path + os.sep + 'Comp_OMET_annual_mean_span.jpg', dpi = 500)

# annual mean of meridional energy transport at each latitude in north hemisphere
fig4 = plt.figure()
plt.axhline(y=0, color='k',ls='-')
plt.plot(latitude_aux_ORAS4,np.mean(np.mean(OMET_ORAS4_full,0),0),'c-',label='ORAS4')
plt.plot(latitude_aux_GLORYS2V3,np.mean(np.mean(OMET_GLORYS2V3_full,0),0),'m-',label='GLORYS2V3')
plt.plot(latitude_aux_SODA3,np.mean(np.mean(OMET_SODA3_full,0),0),'y-',label='SODA3')
plt.title('Mean OMET of entire time series from 90S to 90N' )
#plt.legend()
plt.xlabel("Latitudes")
#plt.xticks()
plt.ylabel("Meridional Energy Transport (PW)")
plt.legend()
plt.show()
fig4.savefig(output_path + os.sep + 'Comp_OMET_annual_mean.jpg', dpi = 500)

print '*******************************************************************'
print '******************   highlight the difference   *******************'
print '*******************************************************************'
fig5 = plt.figure()
plt.plot(index_1993_begin,OMET_GLORYS2V3_white_series-OMET_ORAS4_white_series[168:],'b-',linewidth=1.0,label='GLORYS2V3-ORAS4')
plt.title('Difference between GLORYS2V3 and ORAS4 (time series) at 60N')
#plt.legend()
fig5.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(0, 264, 23), index_year_1993)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport residual (PW)")
plt.legend()
plt.show()
fig5.savefig(output_path + os.sep + 'Comp_OMET_GLORYS2V3_minus_ORAS4_60N.jpg', dpi = 500)

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
# calculate the standard deviation of OMET anomaly
# GLORYS2V3
OMET_GLORYS2V3_std = np.std(OMET_GLORYS2V3_series)
print 'The standard deviation of OMET from GLORYS2V3 is (in peta Watt):'
print OMET_GLORYS2V3_std
# ORAS4
OMET_ORAS4_std = np.std(OMET_ORAS4_series)
print 'The standard deviation of OMET from ORAS4 is (in peta Watt):'
print OMET_ORAS4_std
# SODA3
OMET_SODA3_std = np.std(OMET_SODA3_series)
print 'The standard deviation of OMET from SODA3 is (in peta Watt):'
print OMET_SODA3_std

# calculate the standard deviation of OMET anomaly
# GLORYS2V3
OMET_GLORYS2V3_white_std = np.std(OMET_GLORYS2V3_white_series)
print 'The standard deviation of OMET anomaly from GLORYS2V3 is (in peta Watt):'
print OMET_GLORYS2V3_white_std
# ORAS4
OMET_ORAS4_white_std = np.std(OMET_ORAS4_white_series)
print 'The standard deviation of OMET anomaly from ORAS4 is (in peta Watt):'
print OMET_ORAS4_white_std
# SODA3
OMET_SODA3_white_std = np.std(OMET_SODA3_white_series)
print 'The standard deviation of OMET anomaly from SODA3 is (in peta Watt):'
print OMET_SODA3_white_std

print '*******************************************************************'
print '*************************** mean value  ***************************'
print '*******************************************************************'
# calculate the mean of OMET anomaly
# GLORYS2V3
OMET_GLORYS2V3_mean = np.mean(OMET_GLORYS2V3_series)
print 'The mean of OMET from GLORYS2V3 is (in peta Watt):'
print OMET_GLORYS2V3_mean
# ORAS4
OMET_ORAS4_mean = np.mean(OMET_ORAS4_series)
print 'The mean of OMET from ORAS4 is (in peta Watt):'
print OMET_ORAS4_mean
# ORAS4
OMET_SODA3_mean = np.mean(OMET_SODA3_series)
print 'The mean of OMET from SODA3 is (in peta Watt):'
print OMET_SODA3_mean

# calculate the standard deviation of OMET anomaly
# GLORYS2V3
OMET_GLORYS2V3_white_mean = np.mean(OMET_GLORYS2V3_white_series)
print 'The mean of OMET anomaly from GLORYS2V3 is (in peta Watt):'
print OMET_GLORYS2V3_white_mean
# ORAS4
OMET_ORAS4_white_mean = np.mean(OMET_ORAS4_white_series)
print 'The mean of OMET anomaly from ORAS4 is (in peta Watt):'
print OMET_ORAS4_white_mean
# ORAS4
OMET_SODA3_white_mean = np.mean(OMET_SODA3_white_series)
print 'The mean of OMET anomaly from SODA3 is (in peta Watt):'
print OMET_SODA3_white_mean
