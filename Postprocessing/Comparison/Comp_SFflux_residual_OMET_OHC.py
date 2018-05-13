#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : Compute Turbulent Flux at surface as residuals from OMET and OHC' (ORAS4,GLORYS2V3,SODA3)
Author          : Yang Liu
Date            : 2018.05.13
Last Update     : 2018.05.13
Description     : The code aims to compute the surface heat flux (turbulent flux)
                  as the residuals from the trend of ocean heat content and the oceanic
                  meridional energy transport. All the quantities are calculated from
                  different oceanic reanalysis datasets. In this, case, this includes
                  GLORYS2V3 from Mercator Ocean, ORAS4 from ECMWF, and SODA3 from
                  University of Maryland.

                  Regarding the computation of turbulent flux, we will calculate
                  it as the residual from OHC and OMET. However, due to the nature
                  of curvilinear grid, it is not possible to calculate them point-wise.
                  It is because the lat-lon of each point varies irregularly. As a result,
                  it is not possible to calculate the zonal submation of turbulent flux
                  as there is no 'zonal' physically. The central scheme method is not
                  applicable as well as the distance to the center point varies for each
                  point. It seems the only possible way is to calculate turbulent flux
                  point to point. Whereas, we didn't save zonal divergence of energy transport.
                  Hence, the only reazonable way is calculating SFflux for between certain
                  latitudes.
Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, sys, matplotlib
variables       : Meridional Energy Transport               OMET      [Tera-Watt]
                  Meridional Overturning Circulation        Psi       [Sv]
                  Ocean Heat Content                        OHC       [Joule]
Caveat!!        : Resolution
                  Time range
                  GLORYS2V3   1993 - 2014
                  ORAS4       1958 - 2014 (1979 in use)
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
datapath_OMET_ORAS4 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ORAS4/postprocessing'
datapath_OMET_GLORYS2V3 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/GLORYS2V3/postprocessing'
datapath_OMET_SODA3 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/SODA3/postprocessing'
# OHC
datapath_OHC_ORAS4 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ORAS4/statistics'
datapath_OHC_GLORYS2V3 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/GLORYS2V3/statistics'
datapath_OHC_SODA3 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/SODA3/statistics'
# specify output path for figures
output_path = '/home/yang/NLeSC/Computation_Modeling/BlueAction/OMET/Comparison/SFflux'
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

# OMET zonal integral
dataset_OMET_GLORYS2V3 = Dataset(datapath_OMET_GLORYS2V3 + os.sep + 'GLORYS2V3_model_monthly_orca025_E_zonal_int.nc')
dataset_OMET_ORAS4 = Dataset(datapath_OMET_ORAS4 + os.sep + 'oras4_model_monthly_orca1_E_zonal_int.nc')
dataset_OMET_SODA3 = Dataset(datapath_OMET_SODA3 + os.sep + 'OMET_SODA3_model_5daily_1980_2015_E_zonal_int.nc')
# OHC point
dataset_OHC_GLORYS2V3 = Dataset(datapath_OHC_GLORYS2V3 + os.sep + 'GLORYS2V3_model_monthly_orca025_OHC_point.nc')
dataset_OHC_ORAS4 = Dataset(datapath_OHC_ORAS4 + os.sep + 'oras4_model_monthly_orca1_OHC_point.nc')
dataset_OHC_SODA3 = Dataset(datapath_OHC_SODA3 + os.sep + 'OMET_SODA3_model_5daily_1980_2015_OHC.nc')
# extract Oceanic meridional energy transport (Tera Watt)
# dimension (year,month,latitude)
OMET_GLORYS2V3 = dataset_OMET_GLORYS2V3.variables['E'][:]/1000 # from Tera Watt to Peta Watt # start from 1993
OMET_ORAS4 = dataset_OMET_ORAS4.variables['E'][21:,:,:]/1000 # from Tera Watt to Peta Watt # start from 1979
OMET_SODA3 = dataset_OMET_SODA3.variables['E'][:]/1000 # from Tera Watt to Peta Watt # start from 1979
# OHC (Tera Joule)
OHC_ORAS4 = np.sum(dataset_OHC_ORAS4.variables['OHC_glo_vert'][21:,:,:,:],3)/1000 # start from 1979
OHC_GLORYS2V3 = np.sum(dataset_OHC_GLORYS2V3.variables['OHC_glo_vert'][:],3)/1000 # start from 1993
OHC_SODA3 = np.sum(dataset_OHC_SODA3.variables['OHC_glo_vert'][:],3)/1000
#year
year_ORAS4 = dataset_OMET_ORAS4.variables['year'][21:]         # from 1979 to 2014
year_GLORYS2V3 = dataset_OMET_GLORYS2V3.variables['year'][:]   # from 1993 to 2014
year_SODA3 = dataset_OMET_SODA3.variables['year'][:]           # from 1980 to 2014
# latitude
latitude_GLORYS2V3 = dataset_OMET_GLORYS2V3.variables['latitude_aux'][:]
latitude_ORAS4 = dataset_OMET_ORAS4.variables['latitude_aux'][:]
latitude_SODA3 = dataset_OMET_SODA3.variables['latitude_aux'][:]

print '*******************************************************************'
print '*************************** time series ***************************'
print '*******************************************************************'
OMET_ORAS4_series = OMET_ORAS4.reshape(len(year_ORAS4)*12,len(latitude_ORAS4))
OMET_GLORYS2V3_series = OMET_GLORYS2V3.reshape(len(year_GLORYS2V3)*12,len(latitude_GLORYS2V3))
OMET_SODA3_series = OMET_SODA3.reshape(len(year_SODA3)*12,len(latitude_SODA3))

OHC_ORAS4_series = OHC_ORAS4.reshape(len(year_ORAS4)*12,len(latitude_ORAS4))
OHC_GLORYS2V3_series = OHC_GLORYS2V3.reshape(len(year_GLORYS2V3)*12,len(latitude_GLORYS2V3))
OHC_SODA3_series = OHC_SODA3.reshape(len(year_SODA3)*12,len(latitude_SODA3))

print '*******************************************************************'
print '********************  Compute Turbulent Flux  *********************'
print '*******************************************************************'
# Compute D(OHC)/dt
OHC_dt_ORAS4_series = np.zeros((len(year_ORAS4)*12,len(latitude_ORAS4)),dtype=float)
OHC_dt_GLORYS2V3_series =np.zeros((len(year_GLORYS2V3)*12,len(latitude_GLORYS2V3)),dtype=float)
OHC_dt_SODA3_series = np.zeros((len(year_SODA3)*12,len(latitude_SODA3)),dtype=float)

OHC_dt_ORAS4_series[1:-1,:] = (OHC_ORAS4_series[2:,:] - OHC_ORAS4_series[0:-2,:]) / (30*86400) / 2
OHC_dt_GLORYS2V3_series[1:-1,:] = (OHC_GLORYS2V3_series[2:,:] - OHC_GLORYS2V3_series[0:-2,:]) / (30*86400) / 2
OHC_dt_SODA3_series[1:-1,:] = (OHC_SODA3_series[2:,:] - OHC_SODA3_series[0:-2,:]) / (30*86400) / 2
# compute the OMET convergence
OMET_converge_ORAS4_series = np.zeros((len(year_ORAS4)*12,len(latitude_ORAS4)),dtype=float)
OMET_converge_GLORYS2V3_series = np.zeros((len(year_GLORYS2V3)*12,len(latitude_GLORYS2V3)),dtype=float)
OMET_converge_SODA3_series = np.zeros((len(year_SODA3)*12,len(latitude_SODA3)),dtype=float)
# for the points at boundary (S & N) (all the datasets are from south to north)
#OMET_converge_ORAS4_series[:,0] = 0 - OMET_ORAS4_series[:,1]
#OMET_converge_GLORYS2V3_series[:,0] = 0 - OMET_GLORYS2V3_series[:,1]
#OMET_converge_SODA3_series[:,0] = 0 - OMET_SODA3_series[:,1]

#OMET_converge_ORAS4_series[:,-1] = OMET_ORAS4_series[:,-2] - 0
#OMET_converge_GLORYS2V3_series[:,-1] = OMET_GLORYS2V3_series[:,-2] - 0
#OMET_converge_SODA3_series[:,-1] = OMET_SODA3_series[:,-2] - 0

OMET_converge_ORAS4_series[:,1:-1] = (OMET_ORAS4_series[:,0:-2] - OMET_ORAS4_series[:,2:])/2
OMET_converge_GLORYS2V3_series[:,1:-1] = (OMET_GLORYS2V3_series[:,0:-2] - OMET_GLORYS2V3_series[:,2:])/2
OMET_converge_SODA3_series[:,1:-1] = (OMET_SODA3_series[:,0:-2] - OMET_SODA3_series[:,2:])/2
# calculate the turbulent flux as residuals
SFflux_ORAS4_series = np.zeros((len(year_ORAS4)*12,len(latitude_ORAS4)),dtype=float)
SFflux_GLORYS2V3_series = np.zeros((len(year_GLORYS2V3)*12,len(latitude_GLORYS2V3)),dtype=float)
SFflux_SODA3_series = np.zeros((len(year_SODA3)*12,len(latitude_SODA3)),dtype=float)
# positive points into the ocean
SFflux_ORAS4_series = OHC_dt_ORAS4_series - OMET_converge_ORAS4_series
SFflux_GLORYS2V3_series = OHC_dt_GLORYS2V3_series - OMET_converge_GLORYS2V3_series
SFflux_SODA3_series = OHC_dt_SODA3_series - OMET_converge_SODA3_series
print '*******************************************************************'
print '*************************** whitening *****************************'
print '*******************************************************************'
month_ind = np.arange(12)
# seasonal cycling
seasonal_cycle_OHC_dt_ORAS4 = np.zeros((12,len(latitude_ORAS4)),dtype=float)
seasonal_cycle_OHC_dt_GLORYS2V3 = np.zeros((12,len(latitude_GLORYS2V3)),dtype=float)
seasonal_cycle_OHC_dt_SODA3 = np.zeros((12,len(latitude_SODA3)),dtype=float)

seasonal_cycle_OMET_converge_ORAS4 = np.zeros((12,len(latitude_ORAS4)),dtype=float)
seasonal_cycle_OMET_converge_GLORYS2V3 = np.zeros((12,len(latitude_GLORYS2V3)),dtype=float)
seasonal_cycle_OMET_converge_SODA3 = np.zeros((12,len(latitude_SODA3)),dtype=float)

seasonal_cycle_SFflux_ORAS4 = np.zeros((12,len(latitude_ORAS4)),dtype=float)
seasonal_cycle_SFflux_GLORYS2V3 = np.zeros((12,len(latitude_GLORYS2V3)),dtype=float)
seasonal_cycle_SFflux_SODA3 = np.zeros((12,len(latitude_SODA3)),dtype=float)

# white signal
OHC_dt_ORAS4_white_series = np.zeros(OHC_dt_ORAS4_series.shape,dtype=float)
OHC_dt_GLORYS2V3_white_series = np.zeros(OHC_dt_GLORYS2V3_series.shape,dtype=float)
OHC_dt_SODA3_white_series = np.zeros(OHC_dt_SODA3_series.shape,dtype=float)

OMET_converge_ORAS4_white_series = np.zeros(OMET_converge_ORAS4_series.shape,dtype=float)
OMET_converge_GLORYS2V3_white_series = np.zeros(OMET_converge_GLORYS2V3_series.shape,dtype=float)
OMET_converge_SODA3_white_series = np.zeros(OMET_converge_SODA3_series.shape,dtype=float)

SFflux_ORAS4_white_series = np.zeros(SFflux_ORAS4_series.shape,dtype=float)
SFflux_GLORYS2V3_white_series = np.zeros(SFflux_GLORYS2V3_series.shape,dtype=float)
SFflux_SODA3_white_series = np.zeros(SFflux_SODA3_series.shape,dtype=float)

for i in month_ind:
    # calculate the monthly mean (seasonal cycling)
    seasonal_cycle_OHC_dt_ORAS4[i,:] = np.mean(OHC_dt_ORAS4_series[i::12,:],axis=0)
    seasonal_cycle_OHC_dt_GLORYS2V3[i,:] = np.mean(OHC_dt_GLORYS2V3_series[i::12,:],axis=0)
    seasonal_cycle_OHC_dt_SODA3[i,:] = np.mean(OHC_dt_SODA3_series[i::12,:],axis=0)
    seasonal_cycle_OMET_converge_ORAS4[i,:] = np.mean(OMET_converge_ORAS4_series[i::12,:],axis=0)
    seasonal_cycle_OMET_converge_GLORYS2V3[i,:] = np.mean(OMET_converge_GLORYS2V3_series[i::12,:],axis=0)
    seasonal_cycle_OMET_converge_SODA3[i,:] = np.mean(OMET_converge_SODA3_series[i::12,:],axis=0)
    seasonal_cycle_SFflux_ORAS4[i,:] = np.mean(SFflux_ORAS4_series[i::12,:],axis=0)
    seasonal_cycle_SFflux_GLORYS2V3[i,:] = np.mean(SFflux_GLORYS2V3_series[i::12,:],axis=0)
    seasonal_cycle_SFflux_SODA3[i,:] = np.mean(SFflux_SODA3_series[i::12,:],axis=0)
    OHC_dt_ORAS4_white_series[i::12,:] = OHC_dt_ORAS4_series[i::12,:] - seasonal_cycle_OHC_dt_ORAS4[i,:]
    OHC_dt_GLORYS2V3_white_series[i::12,:] = OHC_dt_GLORYS2V3_series[i::12,:] - seasonal_cycle_OHC_dt_GLORYS2V3[i,:]
    OHC_dt_SODA3_white_series[i::12,:] = OHC_dt_SODA3_series[i::12,:] - seasonal_cycle_OHC_dt_SODA3[i,:]
    OMET_converge_ORAS4_white_series[i::12,:] = OMET_converge_ORAS4_series[i::12,:] - seasonal_cycle_OMET_converge_ORAS4[i,:]
    OMET_converge_GLORYS2V3_white_series[i::12,:] = OMET_converge_GLORYS2V3_series[i::12,:] - seasonal_cycle_OMET_converge_GLORYS2V3[i,:]
    OMET_converge_SODA3_white_series[i::12,:] = OMET_converge_SODA3_series[i::12,:] - seasonal_cycle_OMET_converge_SODA3[i,:]
    SFflux_ORAS4_white_series[i::12,:] = SFflux_ORAS4_series[i::12,:] - seasonal_cycle_SFflux_ORAS4[i,:]
    SFflux_GLORYS2V3_white_series[i::12,:] = SFflux_GLORYS2V3_series[i::12,:] - seasonal_cycle_SFflux_GLORYS2V3[i,:]
    SFflux_SODA3_white_series[i::12,:] = SFflux_SODA3_series[i::12,:] - seasonal_cycle_SFflux_SODA3[i,:]
print '*******************************************************************'
print '***************************   plots   *****************************'
print '*******************************************************************'
index_1993 = np.arange(169,433,1) # starting from index of year 1993
index_year_1993 = np.arange(1993,2015,1)

index_1979 = np.arange(1,433,1)
index_year_1979 = np.arange(1979,2015,1)

index_1980 = np.arange(13,445,1)
index_year_1980 = np.arange(1980,2016,1)

index_full = np.arange(1,445,1)
index_year_full = np.arange(1979,2016,1)

# surface flux
for i in np.arange(len(lat_interest_list)):
    fig1 = plt.figure()
    plt.plot(index_1979,SFflux_ORAS4_series[:,lat_interest['ORAS4'][i]],'c-',linewidth=1.0,label='ORAS4')
    plt.plot(index_1993,SFflux_GLORYS2V3_series[:,lat_interest['GLORYS2V3'][i]],'m-',linewidth=1.0,label='GLORYS2V3')
    plt.plot(index_1980,SFflux_SODA3_series[:,lat_interest['SODA3'][i]],'y-',linewidth=1.0,label='SODA3')
    plt.title('Turbulent flux at %dN (1979-2015)' % (lat_interest_list[i]))
    fig1.set_size_inches(12.5, 6)
    plt.xlabel("Time")
    plt.xticks(np.linspace(0, 444, 38), index_year_full)
    plt.xticks(rotation=60)
    plt.ylabel("Turbulent Flux (PW)")
    plt.legend()
    plt.show()
    fig1.savefig(output_path + os.sep + 'SFflux' + os.sep + 'Comp_SFflux_%dN.jpg' % (lat_interest_list[i]), dpi = 400)

# surface flux, OMET and OHC
for i in np.arange(len(lat_interest_list)):
    fig2 = plt.figure()
    plt.plot(index_1979,SFflux_ORAS4_series[:,lat_interest['ORAS4'][i]],'c-',linewidth=1.0,label='ORAS4 SFflux')
    plt.plot(index_1993,SFflux_GLORYS2V3_series[:,lat_interest['GLORYS2V3'][i]],'m-',linewidth=1.0,label='GLORYS2V3 SFflux')
    plt.plot(index_1980,SFflux_SODA3_series[:,lat_interest['SODA3'][i]],'y-',linewidth=1.0,label='SODA3 SFflux')
    plt.plot(index_1979,OMET_converge_ORAS4_series[:,lat_interest['ORAS4'][i]],'c--',linewidth=1.0,label='ORAS4 OMET')
    plt.plot(index_1993,OMET_converge_GLORYS2V3_series[:,lat_interest['GLORYS2V3'][i]],'m--',linewidth=1.0,label='GLORYS2V3 OMET')
    plt.plot(index_1980,OMET_converge_SODA3_series[:,lat_interest['SODA3'][i]],'y--',linewidth=1.0,label='SODA3 OMET')
    plt.plot(index_1979,OHC_dt_ORAS4_series[:,lat_interest['ORAS4'][i]],'c:',linewidth=1.0,label='ORAS4 OHC')
    plt.plot(index_1993,OHC_dt_GLORYS2V3_series[:,lat_interest['GLORYS2V3'][i]],'m:',linewidth=1.0,label='GLORYS2V3 OHC')
    plt.plot(index_1980,OHC_dt_SODA3_series[:,lat_interest['SODA3'][i]],'y:',linewidth=1.0,label='SODA3 OHC')
    plt.title('Turbulent flux, OHC tendency and OMET convergence at %dN (1979-2015)' % (lat_interest_list[i]))
    fig2.set_size_inches(12.5, 6)
    plt.xlabel("Time")
    plt.xticks(np.linspace(0, 444, 38), index_year_full)
    plt.xticks(rotation=60)
    plt.ylabel("Energy Transport (PW)")
    plt.legend()
    plt.show()
    fig2.savefig(output_path + os.sep + 'comp' + os.sep + 'Comp_SFflux_OMET_OHC_%dN.jpg' % (lat_interest_list[i]), dpi = 400)

# surface flux, OMET and OHC
for i in np.arange(len(lat_interest_list)):
    fig3 = plt.figure()
    plt.plot(index_1979,SFflux_ORAS4_white_series[:,lat_interest['ORAS4'][i]],'c-',linewidth=1.0,label='ORAS4 SFflux')
    plt.plot(index_1993,SFflux_GLORYS2V3_white_series[:,lat_interest['GLORYS2V3'][i]],'m-',linewidth=1.0,label='GLORYS2V3 SFflux')
    plt.plot(index_1980,SFflux_SODA3_white_series[:,lat_interest['SODA3'][i]],'y-',linewidth=1.0,label='SODA3 SFflux')
    plt.plot(index_1979,OMET_converge_ORAS4_white_series[:,lat_interest['ORAS4'][i]],'c--',linewidth=1.0,label='ORAS4 OMET')
    plt.plot(index_1993,OMET_converge_GLORYS2V3_white_series[:,lat_interest['GLORYS2V3'][i]],'m--',linewidth=1.0,label='GLORYS2V3 OMET')
    plt.plot(index_1980,OMET_converge_SODA3_white_series[:,lat_interest['SODA3'][i]],'y--',linewidth=1.0,label='SODA3 OMET')
    plt.plot(index_1979,OHC_dt_ORAS4_white_series[:,lat_interest['ORAS4'][i]],'c:',linewidth=1.0,label='ORAS4 OHC')
    plt.plot(index_1993,OHC_dt_GLORYS2V3_white_series[:,lat_interest['GLORYS2V3'][i]],'m:',linewidth=1.0,label='GLORYS2V3 OHC')
    plt.plot(index_1980,OHC_dt_SODA3_white_series[:,lat_interest['SODA3'][i]],'y:',linewidth=1.0,label='SODA3 OHC')
    plt.title('Anomalies of Turbulent Flux, OHC tendency and OMET convergence at %dN (1979-2015)' % (lat_interest_list[i]))
    fig3.set_size_inches(12.5, 6)
    plt.xlabel("Time")
    plt.xticks(np.linspace(0, 444, 38), index_year_full)
    plt.xticks(rotation=60)
    plt.ylabel("Energy Transport (PW)")
    plt.legend()
    plt.show()
    fig3.savefig(output_path + os.sep + 'comp' + os.sep + 'Comp_SFflux_OMET_OHC_%dN_lowpass.jpg' % (lat_interest_list[i]), dpi = 400)

print '*******************************************************************'
print '******************    trend at each latitude    *******************'
print '*******************************************************************'
counter_ORAS4 = np.arange(len(year_ORAS4)*len(month_ind))
counter_GLORYS2V3 = np.arange(len(year_GLORYS2V3)*len(month_ind))
counter_SODA3 = np.arange(len(year_SODA3)*len(month_ind))

# ORAS4
# the calculation of trend are based on target climatolory after removing seasonal cycles
# trend of OMET at each lat
# create an array to store the slope coefficient and residual
a_SFflux_ORAS4 = np.zeros((len(latitude_ORAS4)),dtype = float)
b_SFflux_ORAS4 = np.zeros((len(latitude_ORAS4)),dtype = float)
# the least square fit equation is y = ax + b
# np.lstsq solves the equation ax=b, a & b are the input
# thus the input file should be reformed for the function
# we can rewrite the line y = Ap, with A = [x,1] and p = [[a],[b]]
A_SFflux_ORAS4 = np.vstack([counter_ORAS4,np.ones(len(counter_ORAS4))]).T
# start the least square fitting
for i in np.arange(len(latitude_ORAS4)):
        # return value: coefficient matrix a and b, where a is the slope
        a_SFflux_ORAS4[i], b_SFflux_ORAS4[i] = np.linalg.lstsq(A_SFflux_ORAS4,SFflux_ORAS4_white_series[:,i])[0]

a_OMET_converge_ORAS4 = np.zeros((len(latitude_ORAS4)),dtype = float)
b_OMET_converge_ORAS4 = np.zeros((len(latitude_ORAS4)),dtype = float)
A_OMET_converge_ORAS4 = np.vstack([counter_ORAS4,np.ones(len(counter_ORAS4))]).T
for i in np.arange(len(latitude_ORAS4)):
        a_OMET_converge_ORAS4[i], b_OMET_converge_ORAS4[i] = np.linalg.lstsq(A_OMET_converge_ORAS4,OMET_converge_ORAS4_white_series[:,i])[0]

a_OHC_dt_ORAS4 = np.zeros((len(latitude_ORAS4)),dtype = float)
b_OHC_dt_ORAS4 = np.zeros((len(latitude_ORAS4)),dtype = float)
A_OHC_dt_ORAS4 = np.vstack([counter_ORAS4,np.ones(len(counter_ORAS4))]).T
for i in np.arange(len(latitude_ORAS4)):
        a_OHC_dt_ORAS4[i], b_OHC_dt_ORAS4[i] = np.linalg.lstsq(A_OHC_dt_ORAS4,OHC_dt_ORAS4_white_series[:,i])[0]

# GLORYS2V3
a_SFflux_GLORYS2V3 = np.zeros((len(latitude_GLORYS2V3)),dtype = float)
b_SFflux_GLORYS2V3 = np.zeros((len(latitude_GLORYS2V3)),dtype = float)
A_SFflux_GLORYS2V3 = np.vstack([counter_GLORYS2V3,np.ones(len(counter_GLORYS2V3))]).T
for i in np.arange(len(latitude_GLORYS2V3)):
        a_SFflux_GLORYS2V3[i], b_SFflux_GLORYS2V3[i] = np.linalg.lstsq(A_SFflux_GLORYS2V3,SFflux_GLORYS2V3_white_series[:,i])[0]

a_OMET_converge_GLORYS2V3 = np.zeros((len(latitude_GLORYS2V3)),dtype = float)
b_OMET_converge_GLORYS2V3 = np.zeros((len(latitude_GLORYS2V3)),dtype = float)
A_OMET_converge_GLORYS2V3 = np.vstack([counter_GLORYS2V3,np.ones(len(counter_GLORYS2V3))]).T
for i in np.arange(len(latitude_GLORYS2V3)):
        a_OMET_converge_GLORYS2V3[i], b_OMET_converge_GLORYS2V3[i] = np.linalg.lstsq(A_OMET_converge_GLORYS2V3,OMET_converge_GLORYS2V3_white_series[:,i])[0]

a_OHC_dt_GLORYS2V3 = np.zeros((len(latitude_GLORYS2V3)),dtype = float)
b_OHC_dt_GLORYS2V3 = np.zeros((len(latitude_GLORYS2V3)),dtype = float)
A_OHC_dt_GLORYS2V3 = np.vstack([counter_GLORYS2V3,np.ones(len(counter_GLORYS2V3))]).T
for i in np.arange(len(latitude_GLORYS2V3)):
        a_OHC_dt_GLORYS2V3[i], b_OHC_dt_GLORYS2V3[i] = np.linalg.lstsq(A_OHC_dt_GLORYS2V3,OHC_dt_GLORYS2V3_white_series[:,i])[0]

a_SFflux_SODA3 = np.zeros((len(latitude_SODA3)),dtype = float)
b_SFflux_SODA3 = np.zeros((len(latitude_SODA3)),dtype = float)
A_SFflux_SODA3 = np.vstack([counter_SODA3,np.ones(len(counter_SODA3))]).T
for i in np.arange(len(latitude_SODA3)):
        a_SFflux_SODA3[i], b_SFflux_SODA3[i] = np.linalg.lstsq(A_SFflux_SODA3,SFflux_SODA3_white_series[:,i])[0]

a_OMET_converge_SODA3 = np.zeros((len(latitude_SODA3)),dtype = float)
b_OMET_converge_SODA3 = np.zeros((len(latitude_SODA3)),dtype = float)
A_OMET_converge_SODA3 = np.vstack([counter_SODA3,np.ones(len(counter_SODA3))]).T
for i in np.arange(len(latitude_SODA3)):
        a_OMET_converge_SODA3[i], b_OMET_converge_SODA3[i] = np.linalg.lstsq(A_OMET_converge_SODA3,OMET_converge_SODA3_white_series[:,i])[0]

a_OHC_dt_SODA3 = np.zeros((len(latitude_SODA3)),dtype = float)
b_OHC_dt_SODA3 = np.zeros((len(latitude_SODA3)),dtype = float)
A_OHC_dt_SODA3 = np.vstack([counter_SODA3,np.ones(len(counter_SODA3))]).T
for i in np.arange(len(latitude_SODA3)):
        a_OHC_dt_SODA3[i], b_OHC_dt_SODA3[i] = np.linalg.lstsq(A_OHC_dt_SODA3,OHC_dt_SODA3_white_series[:,i])[0]

fig4 = plt.figure()
plt.plot(latitude_ORAS4,a_SFflux_ORAS4*12,'c-',linewidth=1.0,label='ORAS4 SFflux')
plt.plot(latitude_GLORYS2V3,a_SFflux_GLORYS2V3*12,'m-',linewidth=1.0,label='GLORYS2V3 SFflux')
plt.plot(latitude_SODA3,a_SFflux_SODA3*12,'y-',linewidth=1.0,label='SODA3 SFflux')
plt.plot(latitude_ORAS4,a_OMET_converge_ORAS4*12,'c--',linewidth=1.0,label='ORAS4 OMET')
plt.plot(latitude_GLORYS2V3,a_OMET_converge_GLORYS2V3*12,'m--',linewidth=1.0,label='GLORYS2V3 OMET')
plt.plot(latitude_SODA3,a_OMET_converge_SODA3*12,'y--',linewidth=1.0,label='SODA3 OMET')
plt.plot(latitude_ORAS4,a_OHC_dt_ORAS4*12,'c:',linewidth=1.0,label='ORAS4 OHC')
plt.plot(latitude_GLORYS2V3,a_OHC_dt_GLORYS2V3*12,'m:',linewidth=1.0,label='GLORYS2V3 OHC')
plt.plot(latitude_SODA3,a_OHC_dt_SODA3*12,'y:',linewidth=1.0,label='SODA3 OHC')
plt.title('Trend of Turbulent Flux, OHC tendency and OMET convergence')
#fig4.set_size_inches(12.5, 6)
plt.xlabel("Latitude")
plt.ylabel("Trend (PW/year)")
plt.legend()
plt.show()
fig4.savefig(output_path + os.sep + 'Trend_SFflux_OMET_OHC.jpg', dpi = 400)

fig5 = plt.figure()
plt.plot(latitude_ORAS4,a_SFflux_ORAS4*12,'c-',linewidth=1.0,label='ORAS4 SFflux')
plt.plot(latitude_ORAS4,a_OMET_converge_ORAS4*12,'c--',linewidth=1.0,label='ORAS4 OMET')
plt.plot(latitude_ORAS4,a_OHC_dt_ORAS4*12,'c:',linewidth=1.0,label='ORAS4 OHC')
plt.title('Trend of Turbulent Flux, OHC tendency and OMET convergence')
#fig4.set_size_inches(12.5, 6)
plt.xlabel("Latitude")
plt.ylabel("Trend (PW/year)")
plt.legend()
plt.show()
fig5.savefig(output_path + os.sep + 'Trend_SFflux_OMET_OHC_ORAS4.jpg', dpi = 400)

fig6 = plt.figure()
plt.plot(latitude_GLORYS2V3,a_SFflux_GLORYS2V3*12,'m-',linewidth=1.0,label='GLORYS2V3 SFflux')
plt.plot(latitude_GLORYS2V3,a_OMET_converge_GLORYS2V3*12,'m--',linewidth=1.0,label='GLORYS2V3 OMET')
plt.plot(latitude_GLORYS2V3,a_OHC_dt_GLORYS2V3*12,'m:',linewidth=1.0,label='GLORYS2V3 OHC')
plt.title('Trend of Turbulent Flux, OHC tendency and OMET convergence')
#fig4.set_size_inches(12.5, 6)
plt.xlabel("Latitude")
plt.ylabel("Trend (PW/year)")
plt.legend()
plt.show()
fig6.savefig(output_path + os.sep + 'Trend_SFflux_OMET_OHC_GLORYS2V3.jpg', dpi = 400)

fig7 = plt.figure()
plt.plot(latitude_SODA3,a_SFflux_SODA3*12,'y-',linewidth=1.0,label='SODA3 SFflux')
plt.plot(latitude_SODA3,a_OMET_converge_SODA3*12,'y--',linewidth=1.0,label='SODA3 OMET')
plt.plot(latitude_SODA3,a_OHC_dt_SODA3*12,'y:',linewidth=1.0,label='SODA3 OHC')
plt.title('Trend of Turbulent Flux, OHC tendency and OMET convergence')
#fig4.set_size_inches(12.5, 6)
plt.xlabel("Latitude")
plt.ylabel("Trend (PW/year)")
plt.legend()
plt.show()
fig7.savefig(output_path + os.sep + 'Trend_SFflux_OMET_OHC_SODA3.jpg', dpi = 400)

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
