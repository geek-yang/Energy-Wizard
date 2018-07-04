#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : Compute Turbulent Flux at surface as residuals from OMET and OHC' (ORAS4,GLORYS2V3,SODA3)
Author          : Yang Liu
Date            : 2018.05.14
Last Update     : 2018.07.02
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
                  NEMO ORCA   1979 - 2012

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
sns.set_style("ticks")
sns.despine()

################################   Input zone  ######################################
# specify data path
# OMET
datapath_OMET_ORAS4 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ORAS4/postprocessing'
datapath_OMET_GLORYS2V3 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/GLORYS2V3/postprocessing'
datapath_OMET_SODA3 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/SODA3/postprocessing'
datapath_OMET_NEMO = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ORCA012_BenMoat/postprocessing'
# OHC
datapath_OHC_ORAS4 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ORAS4/statistics'
datapath_OHC_GLORYS2V3 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/GLORYS2V3/statistics'
datapath_OHC_SODA3 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/SODA3/statistics'
datapath_OHC_NEMO = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ORCA012_BenMoat/postprocessing'
# mask
datapath_mask_ORAS4 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ORAS4'
datapath_mask_GLORYS2V3 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/GLORYS2V3'
datapath_mask_SODA3 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/SODA3'
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
dataset_OMET_GLORYS2V3 = Dataset(datapath_OMET_GLORYS2V3 + os.sep + 'GLORYS2V3_model_monthly_orca025_E_point.nc')
dataset_OMET_ORAS4 = Dataset(datapath_OMET_ORAS4 + os.sep + 'oras4_model_monthly_orca1_E_point.nc')
dataset_OMET_SODA3 = Dataset(datapath_OMET_SODA3 + os.sep + 'OMET_SODA3_model_5daily_1980_2015_E_point.nc')
# OHC point
dataset_OHC_GLORYS2V3 = Dataset(datapath_OHC_GLORYS2V3 + os.sep + 'GLORYS2V3_model_monthly_orca025_OHC_point.nc')
dataset_OHC_ORAS4 = Dataset(datapath_OHC_ORAS4 + os.sep + 'oras4_model_monthly_orca1_OHC_point.nc')
dataset_OHC_SODA3 = Dataset(datapath_OHC_SODA3 + os.sep + 'OMET_SODA3_model_5daily_1980_2015_OHC.nc')
#year
year_ORAS4 = dataset_OMET_ORAS4.variables['year'][35:-2]      # from 1979 to 2014
year_GLORYS2V3 = dataset_OMET_GLORYS2V3.variables['year'][:-2]# from 1993 to 2014
year_SODA3 = dataset_OMET_SODA3.variables['year'][13:-3]      # from 1980 to 2015
# latitude
latitude_GLORYS2V3 = dataset_OHC_GLORYS2V3.variables['latitude_aux'][579:]
latitude_ORAS4 = dataset_OHC_ORAS4.variables['latitude_aux'][180:]
latitude_SODA3 = dataset_OHC_SODA3.variables['latitude_aux'][569:]
print '*******************************************************************'
print '**********************   mask for oceans  *************************'
print '*******************************************************************'
# get OMET in the atlantic
# extract Oceanic meridional energy transport (Tera Watt)
# dimension (year,month,latitude)
OMET_ORAS4_point = dataset_OMET_ORAS4.variables['E'][21:,:,:,:]/1000 # start from 1979
OMET_GLORYS2V3_point = dataset_OMET_GLORYS2V3.variables['E'][:]/1000 # start from 1993
OMET_SODA3_point = dataset_OMET_SODA3.variables['E'][:]/1000 # start from 1980

# land-sea mask
mesh_mask_ORAS4 = Dataset(datapath_mask_ORAS4 + os.sep + 'mesh_mask.nc')
mesh_mask_GLORYS2V3 = Dataset(datapath_mask_GLORYS2V3 + os.sep + 'G2V3_mesh_mask_myocean.nc')
mesh_mask_SODA3 = Dataset(datapath_mask_SODA3 + os.sep + 'topog.nc')
# lat and lon of T grid
lat_ORAS4 =  mesh_mask_ORAS4.variables['nav_lat'][:]
lat_GLORYS2V3 =  mesh_mask_GLORYS2V3.variables['nav_lat'][:]
lat_SODA3 =  mesh_mask_SODA3.variables['y_T'][:]

lon_ORAS4 =  mesh_mask_ORAS4.variables['nav_lon'][:]
lon_GLORYS2V3 =  mesh_mask_GLORYS2V3.variables['nav_lon'][:]
lon_SODA3 =  mesh_mask_SODA3.variables['x_T'][:]
# mask for the atlantic
# individual sea/ocean mask
ocean_mask_ORAS4 = Dataset(datapath_mask_ORAS4 + os.sep + 'basinmask_050308_UKMO.nc')
ocean_mask_GLORYS2V3 = Dataset(datapath_mask_GLORYS2V3 + os.sep + 'new_maskglo.nc')
mesh_mask_SODA3 = Dataset(datapath_mask_SODA3 + os.sep + 'topog.nc')
# Atlantic
tmaskatl_ORAS4 = ocean_mask_ORAS4.variables['tmaskatl'][:]
tmaskatl_GLORYS2V3 = ocean_mask_GLORYS2V3.variables['tmaskatl'][:,1:-1] # attention that the size is different!
tmask_SODA3 = mesh_mask_SODA3.variables['wet'][:]

# small correction to the ORAS4 atlantic mask
tmaskatl_ORAS4[lat_ORAS4>70] = 0
# calculate the atlantic land sea mask
tmaskatl_SODA3 = np.zeros(tmask_SODA3.shape,dtype=int)
tmaskatl_SODA3[:] = tmask_SODA3
tmaskatl_SODA3[0:225,:] = 0 # boundary south
tmaskatl_SODA3[:,0:727] = 0 # boundary west
tmaskatl_SODA3[:,1200:] = 0 # boundary east
tmaskatl_SODA3[lat_SODA3>70] = 0 # boundary north
# correction Mediterranean
tmaskatl_SODA3[614:680,1100:1240] = 0
tmaskatl_SODA3[660:720,1140:1280] = 0
# correction Pacific
tmaskatl_SODA3[225:522,759:839] = 0
tmaskatl_SODA3[225:545,670:780] = 0
tmaskatl_SODA3[225:560,670:759] = 0
print '*******************************************************************'
print '******************         extract OMET         *******************'
print '*******************************************************************'
OMET_glo_GLORYS2V3_point = dataset_OMET_GLORYS2V3.variables['E'][:-2,:,579:,:]/1000 # from Tera Watt to Peta Watt # start from 1993
OMET_glo_ORAS4_point = dataset_OMET_ORAS4.variables['E'][35:-2,:,180:,:]/1000 # from Tera Watt to Peta Watt # start from 1979
OMET_glo_SODA3_point = dataset_OMET_SODA3.variables['E'][13:-3,:,569:,:]/1000 # from Tera Watt to Peta Watt # start from 1979
# prepare mask for atlantic
tmaskatl_GLORYS2V3_3D = np.repeat(tmaskatl_GLORYS2V3[np.newaxis,579:,:],12,0)
tmaskatl_ORAS4_3D = np.repeat(tmaskatl_ORAS4[np.newaxis,180:,:],12,0)
tmaskatl_SODA3_3D = np.repeat(tmaskatl_SODA3[np.newaxis,569:,:],12,0)

tmaskatl_GLORYS2V3_4D = np.repeat(tmaskatl_GLORYS2V3_3D[np.newaxis,:,:],len(year_GLORYS2V3),0)
tmaskatl_ORAS4_4D = np.repeat(tmaskatl_ORAS4_3D[np.newaxis,:,:],len(year_ORAS4),0)
tmaskatl_SODA3_4D = np.repeat(tmaskatl_SODA3_3D[np.newaxis,:,:],len(year_SODA3),0)

OMET_atl_GLORYS2V3 = np.sum(OMET_glo_GLORYS2V3_point * tmaskatl_GLORYS2V3_4D,3) # from Tera Watt to Peta Watt # start from 1993
OMET_atl_ORAS4 = np.sum(OMET_glo_ORAS4_point * tmaskatl_ORAS4_4D,3) # from Tera Watt to Peta Watt # start from 1979
OMET_atl_SODA3 = np.sum(OMET_glo_SODA3_point * tmaskatl_SODA3_4D,3) # from Tera Watt to Peta Watt # start from 1979
# set the values to be 0 after 70N
OMET_atl_ORAS4[:,:,82:] = 0

del OMET_glo_GLORYS2V3_point
del OMET_glo_ORAS4_point
del OMET_glo_SODA3_point

OHC_atl_vert_ORAS4 = np.sum(dataset_OHC_ORAS4.variables['OHC_atl_vert'][35:-2,:,180:,:],3)/1E+3         # start from 1979
OHC_atl_vert_GLORYS2V3 = np.sum(dataset_OHC_GLORYS2V3.variables['OHC_atl_vert'][:-2,:,579:,:],3)/1E+3   # start from 1993
OHC_atl_vert_SODA3 = np.sum(dataset_OHC_SODA3.variables['OHC_atl_vert'][13:-3,:,569:,:],3)/1E+3         # start from 1980
# set the values to be 0 after 70N
OHC_atl_vert_ORAS4[:,:,82:] = 0
print '*******************************************************************'
print '*****************      data re-arrangement       ******************'
print '*****************   domain wise - per 5 degree   ******************'
print '*******************************************************************'
# Due to the curvillinear grid of ocean models, OHC on each grid point is
# too small to obtain meaningful convergence. Hence we need to take OHC in
# a closed region and then average them to certain latitudes. The procedure
# likes a running sum in the spatial domain. Here we take the size of the
# domain of 5 degree latitudinally.

# ORAS4 - 7 points / 5 deg
# GLORYS2V3 - 23 points / 5 deg
# SODA3 - 23 points / 5 deg

window_ORAS4 = 7
window_GLORYS2V3 = 23
window_SODA3 = 23

# the sum is placed at the center
OHC_atl_vert_ORAS4_band = np.zeros((len(year_ORAS4),12,len(latitude_ORAS4)-window_ORAS4+1),dtype=float)
OHC_atl_vert_GLORYS2V3_band = np.zeros((len(year_GLORYS2V3),12,len(latitude_GLORYS2V3)-window_GLORYS2V3+1),dtype=float)
OHC_atl_vert_SODA3_band = np.zeros((len(year_SODA3),12,len(latitude_SODA3)-window_SODA3+1),dtype=float)
# latitude after adjustment
latitude_ORAS4_center = latitude_ORAS4[(window_ORAS4-1)/2:-((window_ORAS4-1)/2)]
latitude_GLORYS2V3_center = latitude_GLORYS2V3[(window_GLORYS2V3-1)/2:-((window_GLORYS2V3-1)/2)]
latitude_SODA3_center = latitude_SODA3[(window_SODA3-1)/2:-((window_SODA3-1)/2)]
# take the running sum
for i in np.arange(len(latitude_ORAS4_center)):
    OHC_atl_vert_ORAS4_band[:,:,i] = np.sum(OHC_atl_vert_ORAS4[:,:,i:i+window_ORAS4],2)

for i in np.arange(len(latitude_GLORYS2V3_center)):
    OHC_atl_vert_GLORYS2V3_band[:,:,i] = np.sum(OHC_atl_vert_GLORYS2V3[:,:,i:i+window_GLORYS2V3],2)

for i in np.arange(len(latitude_SODA3_center)):
    OHC_atl_vert_SODA3_band[:,:,i] = np.sum(OHC_atl_vert_SODA3[:,:,i:i+window_SODA3],2)
print '*******************************************************************'
print '*************************** time series ***************************'
print '*******************************************************************'
OMET_atl_ORAS4_series = OMET_atl_ORAS4.reshape(len(year_ORAS4)*12,len(latitude_ORAS4))
OMET_atl_GLORYS2V3_series = OMET_atl_GLORYS2V3.reshape(len(year_GLORYS2V3)*12,len(latitude_GLORYS2V3))
OMET_atl_SODA3_series = OMET_atl_SODA3.reshape(len(year_SODA3)*12,len(latitude_SODA3))

OHC_atl_vert_ORAS4_band_series = OHC_atl_vert_ORAS4_band.reshape(len(year_ORAS4)*12,len(latitude_ORAS4_center))
OHC_atl_vert_GLORYS2V3_band_series = OHC_atl_vert_GLORYS2V3_band.reshape(len(year_GLORYS2V3)*12,len(latitude_GLORYS2V3_center))
OHC_atl_vert_SODA3_band_series = OHC_atl_vert_SODA3_band.reshape(len(year_SODA3)*12,len(latitude_SODA3_center))

print '*******************************************************************'
print '********************  Compute Turbulent Flux  *********************'
print '********************        area wise         *********************'
print '*******************************************************************'
# Compute D(OHC)/dt
OHC_dt_atl_ORAS4_series = np.zeros(OHC_atl_vert_ORAS4_band_series.shape,dtype=float)
OHC_dt_atl_GLORYS2V3_series =np.zeros(OHC_atl_vert_GLORYS2V3_band_series.shape,dtype=float)
OHC_dt_atl_SODA3_series = np.zeros(OHC_atl_vert_SODA3_band_series.shape,dtype=float)

OHC_dt_atl_ORAS4_series[1:-1,:] = (OHC_atl_vert_ORAS4_band_series[2:,:] - OHC_atl_vert_ORAS4_band_series[0:-2,:]) / (30*86400) / 2
OHC_dt_atl_GLORYS2V3_series[1:-1,:] = (OHC_atl_vert_GLORYS2V3_band_series[2:,:] - OHC_atl_vert_GLORYS2V3_band_series[0:-2,:]) / (30*86400) / 2
OHC_dt_atl_SODA3_series[1:-1,:] = (OHC_atl_vert_SODA3_band_series[2:,:] - OHC_atl_vert_SODA3_band_series[0:-2,:]) / (30*86400) / 2
# compute the OMET convergence
OMET_converge_atl_ORAS4_series = np.zeros(OHC_atl_vert_ORAS4_band_series.shape,dtype=float)
OMET_converge_atl_GLORYS2V3_series = np.zeros(OHC_atl_vert_GLORYS2V3_band_series.shape,dtype=float)
OMET_converge_atl_SODA3_series = np.zeros(OHC_atl_vert_SODA3_band_series.shape,dtype=float)
# for the points at boundary (S & N) (all the datasets are from south to north)
#OMET_converge_ORAS4_series[:,0] = 0 - OMET_ORAS4_series[:,1]
#OMET_converge_GLORYS2V3_series[:,0] = 0 - OMET_GLORYS2V3_series[:,1]
#OMET_converge_SODA3_series[:,0] = 0 - OMET_SODA3_series[:,1]

#OMET_converge_ORAS4_series[:,-1] = OMET_ORAS4_series[:,-2] - 0
#OMET_converge_GLORYS2V3_series[:,-1] = OMET_GLORYS2V3_series[:,-2] - 0
#OMET_converge_SODA3_series[:,-1] = OMET_SODA3_series[:,-2] - 0

OMET_converge_atl_ORAS4_series[:] = (OMET_atl_ORAS4_series[:,0:-(window_ORAS4-1)] - OMET_atl_ORAS4_series[:,window_ORAS4-1:])
OMET_converge_atl_GLORYS2V3_series[:] = (OMET_atl_GLORYS2V3_series[:,0:-(window_GLORYS2V3-1)] - OMET_atl_GLORYS2V3_series[:,window_GLORYS2V3-1:])
OMET_converge_atl_SODA3_series[:] = (OMET_atl_SODA3_series[:,0:-(window_SODA3-1)] - OMET_atl_SODA3_series[:,window_SODA3-1:])
# calculate the turbulent flux as residuals
SFflux_atl_ORAS4_series = np.zeros(OHC_atl_vert_ORAS4_band_series.shape,dtype=float)
SFflux_atl_GLORYS2V3_series = np.zeros(OHC_atl_vert_GLORYS2V3_band_series.shape,dtype=float)
SFflux_atl_SODA3_series = np.zeros(OHC_atl_vert_SODA3_band_series.shape,dtype=float)
# positive points into the ocean
SFflux_atl_ORAS4_series[:] = OHC_dt_atl_ORAS4_series - OMET_converge_atl_ORAS4_series
SFflux_atl_GLORYS2V3_series[:] = OHC_dt_atl_GLORYS2V3_series - OMET_converge_atl_GLORYS2V3_series
SFflux_atl_SODA3_series[:] = OHC_dt_atl_SODA3_series - OMET_converge_atl_SODA3_series

print '*******************************************************************'
print '*****************    time series plot - check    ******************'
print '*******************************************************************'
month_ind = np.arange(12)
index_1993 = np.arange(1,241,1) # starting from index of year 1993
index_year_1993 = np.arange(1993,2013,1)

fig1 = plt.figure()
plt.plot(index_1993,SFflux_atl_ORAS4_series[:,50],'b-',linewidth=1.0,label='ORAS4 SFflux')
plt.plot(index_1993,OMET_converge_atl_ORAS4_series[:,50],'r-',linewidth=1.0,label='ORAS4 OMET')
plt.plot(index_1993,OHC_dt_atl_ORAS4_series[:,50],'g-',linewidth=1.0,label='ORAS4 OHC')
plt.title('Time series of Turbulent Flux, OHC tendency and OMET convergence around 60N')
fig1.set_size_inches(12.5, 6)
plt.xlabel("Time")
plt.xticks(np.linspace(0, 240, 21), index_year_1993)
plt.ylabel("Energy convergence(PW)")
plt.legend(frameon=True, loc=4, prop={'size': 14})
plt.show()
fig1.savefig(output_path + os.sep + 'band' + os.sep + 'atlantic' + os.sep + 'Series_SFflux_OMET_OHC_ORAS4.jpg', dpi = 400)
print '*******************************************************************'
print '******************    trend at each latitude    *******************'
print '*******************************************************************'
counter_ORAS4 = np.arange(len(year_ORAS4)*12)
counter_GLORYS2V3 = np.arange(len(year_GLORYS2V3)*12)
counter_SODA3 = np.arange(len(year_SODA3)*12)

# ORAS4
# the calculation of trend are based on target climatolory after removing seasonal cycles
# trend of OMET at each lat
# create an array to store the slope coefficient and residual
a_SFflux_ORAS4 = np.zeros((len(latitude_ORAS4_center)),dtype = float)
b_SFflux_ORAS4 = np.zeros((len(latitude_ORAS4_center)),dtype = float)
# the least square fit equation is y = ax + b
# np.lstsq solves the equation ax=b, a & b are the input
# thus the input file should be reformed for the function
# we can rewrite the line y = Ap, with A = [x,1] and p = [[a],[b]]
A_SFflux_ORAS4 = np.vstack([counter_ORAS4,np.ones(len(counter_ORAS4))]).T
# start the least square fitting
for i in np.arange(len(latitude_ORAS4_center)):
        # return value: coefficient matrix a and b, where a is the slope
        a_SFflux_ORAS4[i], b_SFflux_ORAS4[i] = np.linalg.lstsq(A_SFflux_ORAS4,SFflux_atl_ORAS4_series[:,i])[0]

a_OMET_converge_ORAS4 = np.zeros((len(latitude_ORAS4_center)),dtype = float)
b_OMET_converge_ORAS4 = np.zeros((len(latitude_ORAS4_center)),dtype = float)
A_OMET_converge_ORAS4 = np.vstack([counter_ORAS4,np.ones(len(counter_ORAS4))]).T
for i in np.arange(len(latitude_ORAS4_center)):
        a_OMET_converge_ORAS4[i], b_OMET_converge_ORAS4[i] = np.linalg.lstsq(A_OMET_converge_ORAS4,OMET_converge_atl_ORAS4_series[:,i])[0]

a_OHC_dt_ORAS4 = np.zeros((len(latitude_ORAS4_center)),dtype = float)
b_OHC_dt_ORAS4 = np.zeros((len(latitude_ORAS4_center)),dtype = float)
A_OHC_dt_ORAS4 = np.vstack([counter_ORAS4,np.ones(len(counter_ORAS4))]).T
for i in np.arange(len(latitude_ORAS4_center)):
        a_OHC_dt_ORAS4[i], b_OHC_dt_ORAS4[i] = np.linalg.lstsq(A_OHC_dt_ORAS4,OHC_dt_atl_ORAS4_series[:,i])[0]

# GLORYS2V3
a_SFflux_GLORYS2V3 = np.zeros((len(latitude_GLORYS2V3_center)),dtype = float)
b_SFflux_GLORYS2V3 = np.zeros((len(latitude_GLORYS2V3_center)),dtype = float)
A_SFflux_GLORYS2V3 = np.vstack([counter_GLORYS2V3,np.ones(len(counter_GLORYS2V3))]).T
for i in np.arange(len(latitude_GLORYS2V3_center)):
        a_SFflux_GLORYS2V3[i], b_SFflux_GLORYS2V3[i] = np.linalg.lstsq(A_SFflux_GLORYS2V3,SFflux_atl_GLORYS2V3_series[:,i])[0]

a_OMET_converge_GLORYS2V3 = np.zeros((len(latitude_GLORYS2V3_center)),dtype = float)
b_OMET_converge_GLORYS2V3 = np.zeros((len(latitude_GLORYS2V3_center)),dtype = float)
A_OMET_converge_GLORYS2V3 = np.vstack([counter_GLORYS2V3,np.ones(len(counter_GLORYS2V3))]).T
for i in np.arange(len(latitude_GLORYS2V3_center)):
        a_OMET_converge_GLORYS2V3[i], b_OMET_converge_GLORYS2V3[i] = np.linalg.lstsq(A_OMET_converge_GLORYS2V3,OMET_converge_atl_GLORYS2V3_series[:,i])[0]

a_OHC_dt_GLORYS2V3 = np.zeros((len(latitude_GLORYS2V3_center)),dtype = float)
b_OHC_dt_GLORYS2V3 = np.zeros((len(latitude_GLORYS2V3_center)),dtype = float)
A_OHC_dt_GLORYS2V3 = np.vstack([counter_GLORYS2V3,np.ones(len(counter_GLORYS2V3))]).T
for i in np.arange(len(latitude_GLORYS2V3_center)):
        a_OHC_dt_GLORYS2V3[i], b_OHC_dt_GLORYS2V3[i] = np.linalg.lstsq(A_OHC_dt_GLORYS2V3,OHC_dt_atl_GLORYS2V3_series[:,i])[0]

a_SFflux_SODA3 = np.zeros((len(latitude_SODA3_center)),dtype = float)
b_SFflux_SODA3 = np.zeros((len(latitude_SODA3_center)),dtype = float)
A_SFflux_SODA3 = np.vstack([counter_SODA3,np.ones(len(counter_SODA3))]).T
for i in np.arange(len(latitude_SODA3_center)):
        a_SFflux_SODA3[i], b_SFflux_SODA3[i] = np.linalg.lstsq(A_SFflux_SODA3,SFflux_atl_SODA3_series[:,i])[0]

a_OMET_converge_SODA3 = np.zeros((len(latitude_SODA3_center)),dtype = float)
b_OMET_converge_SODA3 = np.zeros((len(latitude_SODA3_center)),dtype = float)
A_OMET_converge_SODA3 = np.vstack([counter_SODA3,np.ones(len(counter_SODA3))]).T
for i in np.arange(len(latitude_SODA3_center)):
        a_OMET_converge_SODA3[i], b_OMET_converge_SODA3[i] = np.linalg.lstsq(A_OMET_converge_SODA3,OMET_converge_atl_SODA3_series[:,i])[0]

a_OHC_dt_SODA3 = np.zeros((len(latitude_SODA3_center)),dtype = float)
b_OHC_dt_SODA3 = np.zeros((len(latitude_SODA3_center)),dtype = float)
A_OHC_dt_SODA3 = np.vstack([counter_SODA3,np.ones(len(counter_SODA3))]).T
for i in np.arange(len(latitude_SODA3_center)):
        a_OHC_dt_SODA3[i], b_OHC_dt_SODA3[i] = np.linalg.lstsq(A_OHC_dt_SODA3,OHC_dt_atl_SODA3_series[:,i])[0]

fig4 = plt.figure()
plt.axhline(y=0, color='k',ls='-')
plt.plot(latitude_ORAS4_center,a_SFflux_ORAS4*12,'b-',linewidth=1.0,label='ORAS4 SFflux')
plt.plot(latitude_GLORYS2V3_center,a_SFflux_GLORYS2V3*12,'r-',linewidth=1.0,label='GLORYS2V3 SFflux')
plt.plot(latitude_SODA3_center,a_SFflux_SODA3*12,'g-',linewidth=1.0,label='SODA3 SFflux')
plt.plot(latitude_ORAS4_center,a_OMET_converge_ORAS4*12,'b--',linewidth=1.0,label='ORAS4 OMET')
plt.plot(latitude_GLORYS2V3_center,a_OMET_converge_GLORYS2V3*12,'r--',linewidth=1.0,label='GLORYS2V3 OMET')
plt.plot(latitude_SODA3_center,a_OMET_converge_SODA3*12,'g--',linewidth=1.0,label='SODA3 OMET')
plt.plot(latitude_ORAS4_center,a_OHC_dt_ORAS4*12,'b:',linewidth=2.0,label='ORAS4 OHC')
plt.plot(latitude_GLORYS2V3_center,a_OHC_dt_GLORYS2V3*12,'r:',linewidth=2.0,label='GLORYS2V3 OHC')
plt.plot(latitude_SODA3_center,a_OHC_dt_SODA3*12,'g:',linewidth=2.0,label='SODA3 OHC')
plt.title('Trend of Turbulent Flux, OHC tendency and OMET convergence')
fig4.set_size_inches(10.5, 6)
plt.xlabel("Latitude",fontsize = 16)
plt.xticks(fontsize = 16)
plt.ylabel("Trend (PW/year)",fontsize = 16)
plt.yticks(fontsize=16)
plt.legend(frameon=True, loc=4, prop={'size': 14})
plt.show()
fig4.savefig(output_path + os.sep + 'band' + os.sep + 'atlantic' + os.sep + 'Trend_SFflux_OMET_OHC.jpg', dpi = 400)

fig8 = plt.figure()
plt.axhline(y=0, color='k',ls='-')
plt.plot(latitude_ORAS4_center,a_SFflux_ORAS4*12,'b-',linewidth=1.0,label='ORAS4 SFflux')
plt.plot(latitude_ORAS4_center,a_OMET_converge_ORAS4*12,'r--',linewidth=1.0,label='ORAS4 OMET')
plt.plot(latitude_ORAS4_center,a_OHC_dt_ORAS4*12,'g:',linewidth=2.0,label='ORAS4 OHC')
plt.title('Trend of Turbulent Flux, OHC tendency and OMET convergence')
fig8.set_size_inches(10.5, 6)
plt.xlabel("Latitude",fontsize = 16)
plt.xticks(fontsize = 16)
plt.ylabel("Trend (PW/year)",fontsize = 16)
plt.yticks(fontsize=16)
plt.legend(frameon=True, loc=4, prop={'size': 14})
plt.show()
fig8.savefig(output_path + os.sep + 'band' + os.sep + 'atlantic' + os.sep + 'Trend_SFflux_OMET_OHC_ORAS4_25N_90N.jpg', dpi = 400)

fig9 = plt.figure()
plt.axhline(y=0, color='k',ls='-')
plt.plot(latitude_GLORYS2V3_center,a_SFflux_GLORYS2V3*12,'b-',linewidth=1.0,label='GLORYS2V3 SFflux')
plt.plot(latitude_GLORYS2V3_center,a_OMET_converge_GLORYS2V3*12,'r--',linewidth=1.0,label='GLORYS2V3 OMET')
plt.plot(latitude_GLORYS2V3_center,a_OHC_dt_GLORYS2V3*12,'g:',linewidth=2.0,label='GLORYS2V3 OHC')
plt.title('Trend of Turbulent Flux, OHC tendency and OMET convergence')
fig9.set_size_inches(10.5, 6)
plt.xlabel("Latitude",fontsize = 16)
plt.xticks(fontsize = 16)
plt.ylabel("Trend (PW/year)",fontsize = 16)
plt.yticks(fontsize=16)
plt.legend(frameon=True, loc=4, prop={'size': 14})
plt.show()
fig9.savefig(output_path + os.sep + 'band' + os.sep + 'atlantic' + os.sep + 'Trend_SFflux_OMET_OHC_GLORYS2V3_25N_90N.jpg', dpi = 400)

fig10 = plt.figure()
plt.axhline(y=0, color='k',ls='-')
plt.plot(latitude_SODA3_center,a_SFflux_SODA3*12,'b-',linewidth=1.0,label='SODA3 SFflux')
plt.plot(latitude_SODA3_center,a_OMET_converge_SODA3*12,'r--',linewidth=1.0,label='SODA3 OMET')
plt.plot(latitude_SODA3_center,a_OHC_dt_SODA3*12,'g:',linewidth=2.0,label='SODA3 OHC')
plt.title('Trend of Turbulent Flux, OHC tendency and OMET convergence')
fig10.set_size_inches(10.5, 6)
plt.xlabel("Latitude",fontsize = 16)
plt.xticks(fontsize = 16)
plt.ylabel("Trend (PW/year)",fontsize = 16)
plt.yticks(fontsize=16)
plt.legend(frameon=True, loc=4, prop={'size': 14})
plt.show()
fig10.savefig(output_path + os.sep + 'band' + os.sep + 'atlantic' + os.sep + 'Trend_SFflux_OMET_OHC_SODA3_25N_90N.jpg', dpi = 400)

fig11 = plt.figure()
plt.axhline(y=0, color='k',ls='-')
plt.plot(latitude_ORAS4_center,a_SFflux_ORAS4*12,'b-',linewidth=1.0,label='ORAS4 SFflux')
plt.plot(latitude_GLORYS2V3_center,a_SFflux_GLORYS2V3*12,'r-',linewidth=1.0,label='GLORYS2V3 SFflux')
plt.plot(latitude_SODA3_center,a_SFflux_SODA3*12,'g-',linewidth=2.0,label='SODA3 SFflux')
plt.title('Trend of Turbulent Flux in ORAS4, GLORYS2V3 and SODA3')
fig11.set_size_inches(10.5, 6)
plt.xlabel("Latitude",fontsize = 16)
plt.xticks(fontsize = 16)
plt.ylabel("Trend (PW/year)",fontsize = 16)
plt.yticks(fontsize=16)
plt.legend(frameon=True, loc=4, prop={'size': 14})
plt.show()
fig11.savefig(output_path + os.sep + 'band' + os.sep + 'atlantic' + os.sep + 'Trend_SFflux_ORAS4_GLORYS2V3_SODA3_25N_90N.jpg', dpi = 400)

fig12 = plt.figure()
plt.axhline(y=0, color='k',ls='-')
plt.plot(latitude_ORAS4_center,a_OMET_converge_ORAS4*12,'b-',linewidth=1.0,label='ORAS4 OMET')
plt.plot(latitude_GLORYS2V3_center,a_OMET_converge_GLORYS2V3*12,'r-',linewidth=1.0,label='GLORYS2V3 OMET')
plt.plot(latitude_SODA3_center,a_OMET_converge_SODA3*12,'g-',linewidth=2.0,label='SODA3 OMET')
plt.title('Trend of OMET convergence in ORAS4, GLORYS2V3 and SODA3')
fig12.set_size_inches(10.5, 6)
plt.xlabel("Latitude",fontsize = 16)
plt.xticks(fontsize = 16)
plt.ylabel("Trend (PW/year)",fontsize = 16)
plt.yticks(fontsize=16)
plt.legend(frameon=True, loc=4, prop={'size': 14})
plt.show()
fig12.savefig(output_path + os.sep + 'band' + os.sep + 'atlantic' + os.sep + 'Trend_OMET_ORAS4_GLORYS2V3_SODA3_25N_90N.jpg', dpi = 400)

fig13 = plt.figure()
plt.axhline(y=0, color='k',ls='-')
plt.plot(latitude_ORAS4_center,a_OHC_dt_ORAS4*12,'b-',linewidth=1.0,label='ORAS4 OHC')
plt.plot(latitude_GLORYS2V3_center,a_OHC_dt_GLORYS2V3*12,'r-',linewidth=1.0,label='GLORYS2V3 OHC')
plt.plot(latitude_SODA3_center,a_OHC_dt_SODA3*12,'g-',linewidth=2.0,label='SODA3 OHC')
plt.title('Trend of OHC tendency in ORAS4, GLORYS2V3 and SODA3')
fig13.set_size_inches(10.5, 6)
plt.xlabel("Latitude",fontsize = 16)
plt.xticks(fontsize = 16)
plt.ylabel("Trend (PW/year)",fontsize = 16)
plt.yticks(fontsize=16)
plt.legend(frameon=True, loc=4, prop={'size': 14})
plt.show()
fig13.savefig(output_path + os.sep + 'band' + os.sep + 'atlantic' + os.sep + 'Trend_OHC_ORAS4_GLORYS2V3_SODA3_25N_90N.jpg', dpi = 400)

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
