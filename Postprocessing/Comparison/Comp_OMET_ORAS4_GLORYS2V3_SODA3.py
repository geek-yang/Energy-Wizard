#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : Compare oceanic meridional energy transport (ORAS4,GLORYS2V3,SODA3)
Author          : Yang Liu
Date            : 2017.11.06
Last Update     : 2018.05.11
Description     : The code aims to compare the oceanic meridional energy transport
                  calculated from different oceanic reanalysis datasets. In this,
                  case, this includes GLORYS2V3 from Mercator Ocean, ORAS4 from ECMWF,
                  and SODA3 from University of Maryland & TAMU.
Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, sys, matplotlib
variables       : Meridional Energy Transport               E         [Tera-Watt]
                  Meridional Overturning Circulation        Psi       [Sv]
Caveat!!        : Resolution

                  GLORYS2V3   1993 - 2014
                  ORAS4       1958 - 2014
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
import pandas
from scipy import stats

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
# index of latitude for insteret

# 20 N (no cut)
lat_ORAS4_20 = 181
lat_GLORYS2V3_20 = 579
lat_SODA3_20 = 569

# 30 N (no cut)
lat_ORAS4_30 = 192
lat_GLORYS2V3_30 = 623
lat_SODA3_30 = 613

# 40 N (no cut)
lat_ORAS4_40 = 204
lat_GLORYS2V3_40 = 672
lat_SODA3_40 = 662

# 50 N (no cut)
lat_ORAS4_50 = 218
lat_GLORYS2V3_50 = 726
lat_SODA3_50 = 719

# 60 N (no cut)
lat_ORAS4_60 = 233
lat_GLORYS2V3_60 = 788
lat_SODA3_60 = 789

# 70 N (no cut)
lat_ORAS4_70 = 250
lat_GLORYS2V3_70 = 857
lat_SODA3_70 = 880

# 80 N (no cut)
lat_ORAS4_80 = 269
lat_GLORYS2V3_80 = 932
lat_SODA3_80 = 974

# make a dictionary for instereted sections (for process automation)
lat_interest = {}
lat_interest_list = [20,30,40,50,60,70,80]
lat_interest['ORAS4'] = [lat_ORAS4_20,lat_ORAS4_30,lat_ORAS4_40,lat_ORAS4_50,lat_ORAS4_60,lat_ORAS4_70,lat_ORAS4_80]
lat_interest['GLORYS2V3'] = [lat_GLORYS2V3_20,lat_GLORYS2V3_30,lat_GLORYS2V3_40,lat_GLORYS2V3_50,lat_GLORYS2V3_60,lat_GLORYS2V3_70,lat_GLORYS2V3_80]
lat_interest['SODA3'] = [lat_SODA3_20,lat_SODA3_30,lat_SODA3_40,lat_SODA3_50,lat_SODA3_60,lat_SODA3_70,lat_SODA3_80]

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
# selected latitude (60N)
OMET_GLORYS2V3 = dataset_GLORYS2V3.variables['E'][:]/1000 # from Tera Watt to Peta Watt # start from 1993
OMET_ORAS4 = dataset_ORAS4.variables['E'][21:,:,:]/1000 # from Tera Watt to Peta Watt # start from 1979
OMET_SODA3 = dataset_SODA3.variables['E'][:]/1000 # from Tera Watt to Peta Watt # start from 1979
#year
year_ORAS4 = dataset_ORAS4.variables['year'][21:]         # from 1979 to 2014
year_GLORYS2V3 = dataset_GLORYS2V3.variables['year'][:]   # from 1993 to 2014
year_SODA3 = dataset_SODA3.variables['year'][:]           # from 1980 to 2014
# latitude
latitude_GLORYS2V3 = dataset_GLORYS2V3.variables['latitude_aux'][:]
latitude_ORAS4 = dataset_ORAS4.variables['latitude_aux'][:]
latitude_SODA3 = dataset_SODA3.variables['latitude_aux'][:]
# csv file for saving statistic matrix
csv_path = '/home/yang/NLeSC/Computation_Modeling/BlueAction/OMET/Comparison'
print '*******************************************************************'
print '*************************** whitening *****************************'
print '*******************************************************************'
# remove the seasonal cycling of OMET at 60N
month_ind = np.arange(12)
# dimension of OMET[year,month]

seansonal_cycle_OMET_ORAS4 = np.mean(OMET_ORAS4,axis=0)
seansonal_cycle_OMET_GLORYS2V3 = np.mean(OMET_GLORYS2V3,axis=0)
seansonal_cycle_OMET_SODA3 = np.mean(OMET_SODA3,axis=0)

OMET_ORAS4_white = np.zeros(OMET_ORAS4.shape,dtype=float)
OMET_GLORYS2V3_white = np.zeros(OMET_GLORYS2V3.shape,dtype=float)
OMET_SODA3_white = np.zeros(OMET_SODA3.shape,dtype=float)

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
print '*********************** prepare variables *************************'
print '*******************************************************************'
# annual mean of AMET and OMET at different latitudes
#OMET_ORAS4_mean = np.mean(np.mean(OMET_ORAS4,0),0)
#OMET_GLORYS2V3_mean = np.mean(np.mean(OMET_GLORYS2V3,0),0)
#OMET_SODA3_mean = np.mean(np.mean(OMET_SODA3,0),0)

# take the time series of E
OMET_ORAS4_series = OMET_ORAS4.reshape(len(year_ORAS4)*len(month_ind),len(latitude_ORAS4))
OMET_GLORYS2V3_series = OMET_GLORYS2V3.reshape(len(year_GLORYS2V3)*len(month_ind),len(latitude_GLORYS2V3))
OMET_SODA3_series = OMET_SODA3.reshape(len(year_SODA3)*len(month_ind),len(latitude_SODA3))
# dataset without seasonal cycle - time series
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

# calculate the running mean of OMET
# original time series
OMET_ORAS4_series_running_mean = np.zeros((len(OMET_ORAS4_series)-window+1,len(latitude_ORAS4)),dtype=float)
OMET_GLORYS2V3_series_running_mean = np.zeros((len(OMET_GLORYS2V3_series)-window+1,len(latitude_GLORYS2V3)),dtype=float)
OMET_SODA3_series_running_mean = np.zeros((len(OMET_SODA3_series)-window+1,len(latitude_SODA3)),dtype=float)
# white time series
OMET_ORAS4_white_series_running_mean = np.zeros((len(OMET_ORAS4_white_series)-window+1,len(latitude_ORAS4)),dtype=float)
OMET_GLORYS2V3_white_series_running_mean = np.zeros((len(OMET_GLORYS2V3_white_series)-window+1,len(latitude_GLORYS2V3)),dtype=float)
OMET_SODA3_white_series_running_mean = np.zeros((len(OMET_SODA3_white_series)-window+1,len(latitude_SODA3)),dtype=float)

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

# plot the OMET series before removing seasonal cycle
for i in np.arange(len(lat_interest_list)):
    fig1 = plt.figure()
    plt.plot(index_1979,OMET_ORAS4_series[:,lat_interest['ORAS4'][i]],'c-',label='ORAS4')
    plt.plot(index_1993,OMET_GLORYS2V3_series[:,lat_interest['GLORYS2V3'][i]],'m-',label='GLORYS2V3')
    plt.plot(index_1980,OMET_SODA3_series[:,lat_interest['SODA3'][i]],'y-',label='SODA3')
    plt.title('Oceanic Meridional Energy Transport at %dN (1979-2015)' % (lat_interest_list[i]))
    fig1.set_size_inches(12.5, 6)
    plt.xlabel("Time")
    plt.xticks(np.linspace(0, 444, 38), index_year_full)
    plt.xticks(rotation=60)
    plt.ylabel("Meridional Energy Transport (PW)")
    plt.legend()
    plt.show()
    fig1.savefig(output_path + os.sep + 'original_series' + os.sep + 'Comp_OMET_%dN_time_series_1979_2015.jpg' % (lat_interest_list[i]), dpi = 500)

# plot the OMET series after removing seasonal cycle
for i in np.arange(len(lat_interest_list)):
    fig2 = plt.figure()
    plt.plot(index_1979,OMET_ORAS4_white_series[:,lat_interest['ORAS4'][i]],'c-',label='ORAS4')
    plt.plot(index_1993,OMET_GLORYS2V3_white_series[:,lat_interest['GLORYS2V3'][i]],'m-',label='GLORYS2V3')
    plt.plot(index_1980,OMET_SODA3_white_series[:,lat_interest['SODA3'][i]],'y-',label='SODA3')
    plt.title('Oceanic Meridional Energy Transport Anomaly at %dN (1979-2015)' % (lat_interest_list[i]))
    fig2.set_size_inches(12.5, 6)
    plt.xlabel("Time")
    plt.xticks(np.linspace(0, 444, 38), index_year_full)
    plt.xticks(rotation=60)
    plt.ylabel("Meridional Energy Transport (PW)")
    plt.legend()
    plt.show()
    fig2.savefig(output_path + os.sep + 'anomaly_series' + os.sep + 'Comp_OMET_anomaly_%dN_time_series_1979_2015.jpg' % (lat_interest_list[i]), dpi = 500)

# plot the running mean of OMET before removing seasonal cycle
for i in np.arange(len(lat_interest_list)):
    fig3 = plt.figure()
    plt.plot(index_1979[window-1:],OMET_ORAS4_series_running_mean[:,lat_interest['ORAS4'][i]],'c-',label='ORAS4')
    plt.plot(index_1993[window-1:],OMET_GLORYS2V3_series_running_mean[:,lat_interest['GLORYS2V3'][i]],'m-',label='GLORYS2V3')
    plt.plot(index_1980[window-1:],OMET_SODA3_series_running_mean[:,lat_interest['SODA3'][i]],'y-',label='SODA3')
    plt.title('Running Mean of OMET at %dN with a window of %d months (1979-2015)' % (lat_interest_list[i],window))
    fig3.set_size_inches(12.5, 6)
    plt.xlabel("Time")
    plt.xticks(np.linspace(0, 444, 38), index_year_full)
    plt.xticks(rotation=60)
    plt.ylabel("Meridional Energy Transport (PW)")
    plt.legend()
    plt.show()
    fig3.savefig(output_path + os.sep + 'original_lowpass' + os.sep + 'Comp_OMET_%dN_running_mean_window_%d_only.jpg' % (lat_interest_list[i],window), dpi = 500)

# plot the running mean of OMET after removing seasonal cycle
for i in np.arange(len(lat_interest_list)):
    fig4 = plt.figure()
    plt.plot(index_1979[window-1:],OMET_ORAS4_white_series_running_mean[:,lat_interest['ORAS4'][i]],'c-',label='ORAS4')
    plt.plot(index_1993[window-1:],OMET_GLORYS2V3_white_series_running_mean[:,lat_interest['GLORYS2V3'][i]],'m-',label='GLORYS2V3')
    plt.plot(index_1980[window-1:],OMET_SODA3_white_series_running_mean[:,lat_interest['SODA3'][i]],'y-',label='SODA3')
    plt.title('Running Mean of OMET Anomalies at %dN with a window of %d months (1979-2015)' % (lat_interest_list[i],window))
    fig4.set_size_inches(12.5, 6)
    plt.xlabel("Time")
    plt.xticks(np.linspace(0, 444, 38), index_year_full)
    plt.xticks(rotation=60)
    plt.ylabel("Meridional Energy Transport (PW)")
    plt.legend()
    plt.show()
    fig4.savefig(output_path + os.sep + 'anomaly_lowpass' + os.sep + 'Comp_OMET_anomaly_%dN_running_mean_window_%d_only.jpg' % (lat_interest_list[i],window), dpi = 500)

# plot the OMET with running mean
for i in np.arange(len(lat_interest_list)):
    fig5 = plt.figure()
    plt.plot(index_1979,OMET_ORAS4_series[:,lat_interest['ORAS4'][i]],'c--',linewidth=1.0,label='ORAS4 time series')
    plt.plot(index_1993,OMET_GLORYS2V3_series[:,lat_interest['GLORYS2V3'][i]],'m--',linewidth=1.0,label='GLORYS2V3 time series')
    plt.plot(index_1980,OMET_SODA3_series[:,lat_interest['SODA3'][i]],'y--',linewidth=1.0,label='SODA3 time series')
    plt.plot(index_1979[window-1:],OMET_ORAS4_series_running_mean[:,lat_interest['ORAS4'][i]],'c-',linewidth=2.0,label='ORAS4 running mean')
    plt.plot(index_1993[window-1:],OMET_GLORYS2V3_series_running_mean[:,lat_interest['GLORYS2V3'][i]],'m-',linewidth=2.0,label='GLORYS2V3 running mean')
    plt.plot(index_1980[window-1:],OMET_SODA3_series_running_mean[:,lat_interest['SODA3'][i]],'y-',linewidth=2.0,label='SODA3 running mean')
    plt.title('Running Mean of OMET at %dN with a window of %d months (1979-2015)' % (lat_interest_list[i],window))
    fig5.set_size_inches(12.5, 6)
    plt.xlabel("Time")
    plt.xticks(np.linspace(0, 444, 38), index_year_full)
    plt.xticks(rotation=60)
    plt.ylabel("Meridional Energy Transport (PW)")
    plt.legend()
    plt.show()
    fig5.savefig(output_path + os.sep + 'original_series_lowpass' + os.sep + 'Comp_OMET_%dN_running_mean_window_%d_comp.jpg' % (lat_interest_list[i],window), dpi = 500)

# plot the OMET after removing the seasonal cycling with running mean
for i in np.arange(len(lat_interest_list)):
    fig6 = plt.figure()
    plt.plot(index_1979,OMET_ORAS4_white_series[:,lat_interest['ORAS4'][i]],'c--',linewidth=1.0,label='ORAS4 time series')
    plt.plot(index_1993,OMET_GLORYS2V3_white_series[:,lat_interest['GLORYS2V3'][i]],'m--',linewidth=1.0,label='GLORYS2V3 time series')
    plt.plot(index_1980,OMET_SODA3_white_series[:,lat_interest['SODA3'][i]],'y--',linewidth=1.0,label='SODA3 time series')
    plt.plot(index_1979[window-1:],OMET_ORAS4_white_series_running_mean[:,lat_interest['ORAS4'][i]],'c-',linewidth=2.0,label='ORAS4 running mean')
    plt.plot(index_1993[window-1:],OMET_GLORYS2V3_white_series_running_mean[:,lat_interest['GLORYS2V3'][i]],'m-',linewidth=2.0,label='GLORYS2V3 running mean')
    plt.plot(index_1980[window-1:],OMET_SODA3_white_series_running_mean[:,lat_interest['SODA3'][i]],'y-',linewidth=2.0,label='SODA3 running mean')
    plt.title('Running Mean of OMET Anomalies at %dN with a window of %d months (1979-2015)' % (lat_interest_list[i],window))
    #plt.legend()
    fig6.set_size_inches(12.5, 6)
    plt.xlabel("Time")
    plt.xticks(np.linspace(0, 444, 38), index_year_full)
    plt.xticks(rotation=60)
    plt.ylabel("Meridional Energy Transport (PW)")
    plt.legend()
    plt.show()
    fig6.savefig(output_path + os.sep + 'anomaly_series_lowpass' + os.sep + 'Comp_OMET_anomaly_%dN_running_mean_window_%d_comp.jpg' % (lat_interest_list[i],window), dpi = 500)


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
OMET_ORAS4_full_annual_mean = np.mean(OMET_ORAS4[:,:,180:],1)
OMET_GLORYS2V3_full_annual_mean = np.mean(OMET_GLORYS2V3[:,:,579:],1)
OMET_SODA3_full_annual_mean = np.mean(OMET_SODA3[:,:,569:],1)
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
# annual mean of meridional energy transport at each latitude in north hemisphere
fig7 = plt.figure()
plt.axhline(y=0, color='k',ls='-')
plt.plot(latitude_ORAS4[180:],np.mean(OMET_ORAS4_full_annual_mean,0),'c-',label='ORAS4')
plt.fill_between(latitude_ORAS4[180:],OMET_ORAS4_full_annual_mean_max,OMET_ORAS4_full_annual_mean_min,alpha=0.3,edgecolor='aquamarine', facecolor='aquamarine')
plt.plot(latitude_GLORYS2V3[579:],np.mean(OMET_GLORYS2V3_full_annual_mean,0),'m-',label='GLORYS2V3')
plt.fill_between(latitude_GLORYS2V3[579:],OMET_GLORYS2V3_full_annual_mean_max,OMET_GLORYS2V3_full_annual_mean_min,alpha=0.3,edgecolor='plum', facecolor='plum')
plt.plot(latitude_SODA3[569:],np.mean(OMET_SODA3_full_annual_mean,0),'y-',label='SODA3')
plt.fill_between(latitude_SODA3[569:],OMET_SODA3_full_annual_mean_max,OMET_SODA3_full_annual_mean_min,alpha=0.3,edgecolor='lightyellow', facecolor='lightyellow')
plt.title('Mean OMET of entire time series from 20N to 90N' )
#plt.legend()
plt.xlabel("Latitudes")
#plt.xticks()
plt.ylabel("Meridional Energy Transport (PW)")
plt.legend()
plt.show()
fig7.savefig(output_path + os.sep + 'Comp_OMET_annual_mean_span.jpg', dpi = 500)

# annual mean of meridional energy transport at each latitude in the entire globe
fig8 = plt.figure()
plt.axhline(y=0, color='k',ls='-')
plt.plot(latitude_ORAS4,np.mean(np.mean(OMET_ORAS4,0),0),'c-',label='ORAS4')
plt.plot(latitude_GLORYS2V3,np.mean(np.mean(OMET_GLORYS2V3,0),0),'m-',label='GLORYS2V3')
plt.plot(latitude_SODA3,np.mean(np.mean(OMET_SODA3,0),0),'y-',label='SODA3')
plt.title('Mean OMET of entire time series from 90S to 90N' )
#plt.legend()
plt.xlabel("Latitudes")
#plt.xticks()
plt.ylabel("Meridional Energy Transport (PW)")
plt.legend()
plt.show()
fig8.savefig(output_path + os.sep + 'Comp_OMET_annual_mean.jpg', dpi = 500)

print '*******************************************************************'
print '******************    trend at each latitude    *******************'
print '*******************************************************************'
counter_ORAS4 = np.arange(len(year_ORAS4)*len(month_ind))
counter_GLORYS2V3 = np.arange(len(year_GLORYS2V3)*len(month_ind))
counter_SODA3 = np.arange(len(year_SODA3)*len(month_ind))
# the calculation of trend are based on target climatolory after removing seasonal cycles
# trend of OMET at each lat
# create an array to store the slope coefficient and residual
a_ORAS4 = np.zeros((len(latitude_ORAS4)),dtype = float)
b_ORAS4 = np.zeros((len(latitude_ORAS4)),dtype = float)
# the least square fit equation is y = ax + b
# np.lstsq solves the equation ax=b, a & b are the input
# thus the input file should be reformed for the function
# we can rewrite the line y = Ap, with A = [x,1] and p = [[a],[b]]
A_ORAS4 = np.vstack([counter_ORAS4,np.ones(len(counter_ORAS4))]).T
# start the least square fitting
for i in np.arange(len(latitude_ORAS4)):
        # return value: coefficient matrix a and b, where a is the slope
        a_ORAS4[i], b_ORAS4[i] = np.linalg.lstsq(A_ORAS4,OMET_ORAS4_white_series[:,i])[0]

a_GLORYS2V3 = np.zeros((len(latitude_GLORYS2V3)),dtype = float)
b_GLORYS2V3 = np.zeros((len(latitude_GLORYS2V3)),dtype = float)
A_GLORYS2V3 = np.vstack([counter_GLORYS2V3,np.ones(len(counter_GLORYS2V3))]).T
for i in np.arange(len(latitude_GLORYS2V3)):
        a_GLORYS2V3[i], b_GLORYS2V3[i] = np.linalg.lstsq(A_GLORYS2V3,OMET_GLORYS2V3_white_series[:,i])[0]

a_SODA3 = np.zeros((len(latitude_SODA3)),dtype = float)
b_SODA3 = np.zeros((len(latitude_SODA3)),dtype = float)
A_SODA3 = np.vstack([counter_SODA3,np.ones(len(counter_SODA3))]).T
for i in np.arange(len(latitude_SODA3)):
        a_SODA3[i], b_SODA3[i] = np.linalg.lstsq(A_SODA3,OMET_SODA3_white_series[:,i])[0]

# trend of OMET anomalies at each latitude
fig9 = plt.figure()
plt.axhline(y=0, color='k',ls='-')
plt.plot(latitude_ORAS4,a_ORAS4*12,'c-',label='ORAS4')
plt.plot(latitude_GLORYS2V3,a_GLORYS2V3*12,'m-',label='GLORYS2V3')
plt.plot(latitude_SODA3,a_SODA3*12,'y-',label='SODA3')
plt.title('Trend of OMET anomalies from 90S to 90N' )
#plt.legend()
plt.xlabel("Latitudes")
#plt.xticks()
plt.ylabel("Meridional Energy Transport (PW/year)")
plt.legend()
plt.show()
fig9.savefig(output_path + os.sep + 'Comp_OMET_white_trend_globe.jpg', dpi = 400)

# trend of OMET anomalies from 20N to 90N
fig10 = plt.figure()
plt.axhline(y=0, color='k',ls='-')
plt.plot(latitude_ORAS4[180:],a_ORAS4[180:]*12,'c-',label='ORAS4')
plt.plot(latitude_GLORYS2V3[579:],a_GLORYS2V3[579:]*12,'m-',label='GLORYS2V3')
plt.plot(latitude_SODA3[569:],a_SODA3[569:]*12,'y-',label='SODA3')
plt.title('Trend of OMET anomalies from 20N to 90N' )
#plt.legend()
plt.xlabel("Latitudes")
#plt.xticks()
plt.ylabel("Meridional Energy Transport (PW/year)")
plt.legend()
plt.show()
fig10.savefig(output_path + os.sep + 'Comp_OMET_white_trend.jpg', dpi = 400)
print '*******************************************************************'
print '******************   highlight the difference   *******************'
print '*******************************************************************'
# fig9 = plt.figure()
# plt.plot(index_1993_begin,OMET_GLORYS2V3_white_series[:,lat_interest['GLORYS2V3'][i]]-OMET_ORAS4_white_series[168:,lat_interest['ORAS4'][i]],'b-',linewidth=1.0,label='GLORYS2V3-ORAS4')
# plt.title('Difference between GLORYS2V3 and ORAS4 (time series) at %dN' % ())
# #plt.legend()
# fig9.set_size_inches(12, 5)
# plt.xlabel("Time")
# plt.xticks(np.linspace(0, 264, 23), index_year_1993)
# plt.xticks(rotation=60)
# plt.ylabel("Meridional Energy Transport residual (PW)")
# plt.legend()
# plt.show()
# fig9.savefig(output_path + os.sep + 'Comp_OMET_GLORYS2V3_minus_ORAS4_%dN.jpg' % (), dpi = 500)

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

print '*******************************************************************'
print '************************** correlation  ***************************'
print '*******************************************************************'
# create correlation matrix
row_name_correlation = ['ORAS - GLORYS','ORAS - SODA','SODA - GLORYS',
                        'ORAS - GLORYS (anomaly)','ORAS - SODA (anomaly)','SODA - GLORYS (anomaly)']
column_name_correlation = lat_interest_list

# original & white time series
slope = np.zeros((len(column_name_correlation),len(row_name_correlation)),dtype=float)
r_value = np.zeros((len(column_name_correlation),len(row_name_correlation)),dtype=float)
p_value = np.zeros((len(column_name_correlation),len(row_name_correlation)),dtype=float)
# return value: slope, intercept, r_value, p_value, stderr
for i in np.arange(len(lat_interest_list)):
    slope[i,0],_,r_value[i,0],p_value[i,0],_ = stats.linregress(OMET_ORAS4_series[168:,lat_interest['ORAS4'][i]],OMET_GLORYS2V3_series[:,lat_interest['GLORYS2V3'][i]])
    slope[i,1],_,r_value[i,1],p_value[i,1],_ = stats.linregress(OMET_ORAS4_series[12:,lat_interest['ORAS4'][i]],OMET_SODA3_series[:-12,lat_interest['SODA3'][i]])
    slope[i,2],_,r_value[i,2],p_value[i,2],_ = stats.linregress(OMET_SODA3_series[156:-12,lat_interest['SODA3'][i]],OMET_GLORYS2V3_series[:,lat_interest['GLORYS2V3'][i]])
    slope[i,3],_,r_value[i,3],p_value[i,3],_ = stats.linregress(OMET_ORAS4_white_series[168:,lat_interest['ORAS4'][i]],OMET_GLORYS2V3_white_series[:,lat_interest['GLORYS2V3'][i]])
    slope[i,4],_,r_value[i,4],p_value[i,4],_ = stats.linregress(OMET_ORAS4_white_series[12:,lat_interest['ORAS4'][i]],OMET_SODA3_white_series[:-12,lat_interest['SODA3'][i]])
    slope[i,5],_,r_value[i,5],p_value[i,5],_ = stats.linregress(OMET_SODA3_white_series[156:-12,lat_interest['SODA3'][i]],OMET_GLORYS2V3_white_series[:,lat_interest['GLORYS2V3'][i]])

# low pass original & white time series
slope_lowpass = np.zeros((len(column_name_correlation),len(row_name_correlation)),dtype=float)
r_value_lowpass = np.zeros((len(column_name_correlation),len(row_name_correlation)),dtype=float)
p_value_lowpass = np.zeros((len(column_name_correlation),len(row_name_correlation)),dtype=float)
# return value: slope, intercept, r_value, p_value, stderr
for i in np.arange(len(lat_interest_list)):
    slope_lowpass[i,0],_,r_value_lowpass[i,0],p_value_lowpass[i,0],_ = stats.linregress(OMET_ORAS4_series_running_mean[168:,lat_interest['ORAS4'][i]],OMET_GLORYS2V3_series_running_mean[:,lat_interest['GLORYS2V3'][i]])
    slope_lowpass[i,1],_,r_value_lowpass[i,1],p_value_lowpass[i,1],_ = stats.linregress(OMET_ORAS4_series_running_mean[12:,lat_interest['ORAS4'][i]],OMET_SODA3_series_running_mean[:-12,lat_interest['SODA3'][i]])
    slope_lowpass[i,2],_,r_value_lowpass[i,2],p_value_lowpass[i,2],_ = stats.linregress(OMET_SODA3_series_running_mean[156:-12,lat_interest['SODA3'][i]],OMET_GLORYS2V3_series_running_mean[:,lat_interest['GLORYS2V3'][i]])
    slope_lowpass[i,3],_,r_value_lowpass[i,3],p_value_lowpass[i,3],_ = stats.linregress(OMET_ORAS4_white_series_running_mean[168:,lat_interest['ORAS4'][i]],OMET_GLORYS2V3_white_series_running_mean[:,lat_interest['GLORYS2V3'][i]])
    slope_lowpass[i,4],_,r_value_lowpass[i,4],p_value_lowpass[i,4],_ = stats.linregress(OMET_ORAS4_white_series_running_mean[12:,lat_interest['ORAS4'][i]],OMET_SODA3_white_series_running_mean[:-12,lat_interest['SODA3'][i]])
    slope_lowpass[i,5],_,r_value_lowpass[i,5],p_value_lowpass[i,5],_ = stats.linregress(OMET_SODA3_white_series_running_mean[156:-12,lat_interest['SODA3'][i]],OMET_GLORYS2V3_white_series_running_mean[:,lat_interest['GLORYS2V3'][i]])

print '*******************************************************************'
print '************************** save tp csv  ***************************'
print '*******************************************************************'
# statistical matrix
row_name_statistic = ['ORAS4','GLORYS2V3','SODA3']
column_name_statistic = ['mean','mean(anomaly)','std','std(anomaly)']
data_for_save_statistic = np.array(([OMET_ORAS4_mean,OMET_GLORYS2V3_mean,OMET_SODA3_mean],
                          [OMET_ORAS4_white_mean,OMET_GLORYS2V3_white_mean,OMET_SODA3_white_mean],
                          [OMET_ORAS4_std,OMET_GLORYS2V3_std,OMET_SODA3_std],
                          [OMET_ORAS4_white_std,OMET_GLORYS2V3_white_std,OMET_SODA3_white_std]
                          ),dtype=float)
df_statistic = pandas.DataFrame(data_for_save_statistic,column_name_statistic,row_name_statistic)
#f_csv = open('csv_path' + 'AMET_statistic_matrix.csv','wb') # b indicates binary
df_statistic.to_csv(csv_path + os.sep + 'matrix' + os.sep + 'OMET_statistic_matrix.csv',
                    index=True, header=True, decimal='.', float_format='%.3f')

# correlation matrix - original & anomaly time series
df_correlation = pandas.DataFrame(slope,column_name_correlation,row_name_correlation)
df_correlation.to_csv(csv_path + os.sep + 'matrix' + os.sep + 'OMET_correlation_slope_matrix.csv',
                      index=True, header=True, decimal='.',float_format='%.3f')

df_correlation = pandas.DataFrame(r_value,column_name_correlation,row_name_correlation)
df_correlation.to_csv(csv_path + os.sep + 'matrix' + os.sep + 'OMET_correlation_r_matrix.csv',
                      index=True, header=True, decimal='.', float_format='%.3f')

df_correlation = pandas.DataFrame(p_value,column_name_correlation,row_name_correlation)
df_correlation.to_csv(csv_path + os.sep + 'matrix' + os.sep + 'OMET_correlation_p_matrix.csv',
                      index=True, header=True, decimal='.', float_format='%.3f')

# correlation matrix - low pass original & anomaly time series
df_correlation = pandas.DataFrame(slope_lowpass,column_name_correlation,row_name_correlation)
df_correlation.to_csv(csv_path + os.sep + 'matrix' + os.sep + 'OMET_correlation_slope_lowpass_%dm_matrix.csv' % (window),
                      index=True, header=True, decimal='.',float_format='%.3f')

df_correlation = pandas.DataFrame(r_value_lowpass,column_name_correlation,row_name_correlation)
df_correlation.to_csv(csv_path + os.sep + 'matrix' + os.sep + 'OMET_correlation_r_lowpass_%dm_matrix.csv' % (window),
                      index=True, header=True, decimal='.', float_format='%.3f')

df_correlation = pandas.DataFrame(p_value_lowpass,column_name_correlation,row_name_correlation)
df_correlation.to_csv(csv_path + os.sep + 'matrix' + os.sep + 'OMET_correlation_p_lowpass_%dm_matrix.csv' % (window),
                      index=True, header=True, decimal='.', float_format='%.3f')
