#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : Compare oceanic variable fields (MERRA2,ERA-Interim,JRA55)
Author          : Yang Liu
Date            : 2018.01.14
Last Update     : 2018.01.14
Description     : The code aims to compare the spatial and temporal distribution of
                  different fields from difference atmospheric reanalysis datasets. In this,
                  case, this includes ERA-Interim from ECMWF, MERRA2 from NASA and JRA55 from
                  JMA. The script works with pressure level data.
Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, sys, matplotlib
variables       : Absolute Temperature             T         [K]
                  Meridional Wind Velocity         v         [m/s]
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
datapath_ERAI = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ERAI/statistics/pressure'
datapath_MERRA2 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/MERRA2/statistics/pressure'
#datapath_JRA55 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/JRA55/statistics'
# specify output path for figures
output_path = '/home/yang/NLeSC/Computation_Modeling/BlueAction/AMET/Comparison/var'
####################################################################################
print '*******************************************************************'
print '*********************** extract variables *************************'
print '*******************************************************************'
# take the variable keys
dataset_ERAI = Dataset(datapath_ERAI + os.sep + 'ERAI_1997_monthly_pressure.nc')
dataset_MERRA2 = Dataset(datapath_MERRA2 + os.sep + 'MERRA2_200.instM_3d_asm_Np.199707.SUB.nc4')
# extract variables
T_ERAI = dataset_ERAI.variables['t'][6,:,0:95,:] - 273.15
v_ERAI = dataset_ERAI.variables['v'][6,:,0:95,:]
T_MERRA2 = dataset_MERRA2.variables['T'][0,:,:,:] - 273.15
v_MERRA2 = dataset_MERRA2.variables['V'][0,:,:,:]
T_MERRA2[T_MERRA2>1000] = 0
v_MERRA2[v_MERRA2>1000] = 0
# level
level_ERAI = dataset_ERAI.variables['level'][:]  # from TOA to surface
level_MERRA2 = dataset_MERRA2.variables['lev'][:] # from surface to TOA
# dp
dp_ERAI = np.zeros(level_ERAI.shape)
dp_MERRA2 = np.zeros(level_MERRA2.shape)
for i in np.arange(len(level_ERAI)):
    if i ==0:
        dp_ERAI[i] = level_ERAI[i]
    else:
        dp_ERAI[i] = level_ERAI[i] - level_ERAI[i-1]

for i in np.arange(len(level_MERRA2)):
    if i == len(level_MERRA2) - 1:
        dp_MERRA2[i] = level_MERRA2[i]
    else:
        dp_MERRA2[i] = level_MERRA2[i] - level_MERRA2[i+1]
# latitude
latitude_ERAI = dataset_ERAI.variables['latitude'][0:95] # lat 60N index 40
latitude_MERRA2 = dataset_MERRA2.variables['lat'][:]
# longitude
longitude_ERAI = dataset_ERAI.variables['longitude'][:]
longitude_ERAI[longitude_ERAI > 180] = longitude_ERAI[longitude_ERAI > 180] -360
longitude_MERRA2 = dataset_MERRA2.variables['lon'][:]
# zonal mean at 60N July
T_zonal_ERAI = np.mean(T_ERAI,2)
T_zonal_MERRA2 = np.mean(T_MERRA2,2)
v_zonal_ERAI = np.mean(v_ERAI,2)
v_zonal_MERRA2 = np.mean(v_MERRA2,2)
# vertical mean at 60N July
T_vert_ERAI_weight = np.zeros(T_ERAI.shape)
T_vert_MERRA2_weight = np.zeros(T_MERRA2.shape)
v_vert_ERAI_weight = np.zeros(v_ERAI.shape)
v_vert_MERRA2_weight = np.zeros(T_MERRA2.shape)

for i in np.arange(len(level_ERAI)):
    T_vert_ERAI_weight[i,:,:] = T_ERAI[i,:,:] * dp_ERAI[i]
    v_vert_ERAI_weight[i,:,:] = v_ERAI[i,:,:] * dp_ERAI[i]

for i in np.arange(len(level_MERRA2)):
    T_vert_MERRA2_weight[i,:,:] = T_MERRA2[i,:,:] * dp_MERRA2[i]
    v_vert_MERRA2_weight[i,:,:] = v_MERRA2[i,:,:] * dp_MERRA2[i]

T_vert_ERAI = np.sum(T_vert_ERAI_weight,0)/level_ERAI[-1]
T_vert_MERRA2 = np.sum(T_vert_MERRA2_weight,0)/level_MERRA2[0]
v_vert_ERAI = np.sum(v_vert_ERAI_weight,0)/level_ERAI[-1]
v_vert_MERRA2 = np.sum(v_vert_MERRA2_weight,0)/level_MERRA2[0]

print '*******************************************************************'
print '********************** horizontal profile *************************'
print '*******************************************************************'
########################      control panel      #########################
# time: 1997.07 lat lon : 60N

##########################################################################
# temperature
fig1 = plt.figure()
#plt.axhline(y=0, color='k',ls='-')
plt.scatter(longitude_ERAI,T_vert_ERAI[40,:],c='c',marker='.',label='ERA-Interim')
plt.scatter(longitude_MERRA2,T_vert_MERRA2[80,:],c='m',marker='.',label='MERRA2')
plt.title('Monthly Mean T Field of 1997-07 at 60N (horizontal profile)' )
fig1.set_size_inches(8, 5)
#plt.legend()
plt.xlabel("Longitude")
#plt.xticks()
plt.ylabel("Temperature (Celsius)")
plt.legend()
plt.show()
fig1.savefig(output_path + os.sep + 'Comp_var_monthly_vert_mean_T_199707_60N.jpg', dpi = 500)

# velocity
# meridional velocity time: 2001.01 lat lon : 60N
fig2 = plt.figure()
plt.axhline(y=0, color='k',ls='-')
plt.scatter(longitude_ERAI,v_vert_ERAI[40,:],c='c',marker='.',label='ERA-Interim')
plt.scatter(longitude_MERRA2,v_vert_MERRA2[80,:],c='m',marker='.',label='MERRA2')
plt.title('Monthly Mean v Field of 1997-07 at 60N (horizontal profile)' )
fig2.set_size_inches(8, 5)
#plt.legend()
plt.xlabel("Longitude")
#plt.xticks()
plt.ylabel("Meridional Wind Velocity (m/s)")
plt.legend()
plt.show()
fig2.savefig(output_path + os.sep + 'Comp_var_monthly_vert_mean_v_199707_60N.jpg', dpi = 500)
print '*******************************************************************'
print '*********************** vertical profile **************************'
print '*******************************************************************'
# temperature
fig3 = plt.figure()
#plt.axhline(y=0, color='k',ls='-')
#plt.scatter(depth_ORAS4,theta_glo_zonal_ORAS4[43,0,:,233],c='c',marker='o',label='ORAS4')
#plt.scatter(depth_GLORYS2V3,theta_glo_zonal_GLORYS2V3[8,0,:,788],c='m',marker='o',label='GLORYS2V3')
plt.scatter(T_zonal_ERAI[:,40],level_ERAI,c='c',marker='.',label='ERA-Interim')
plt.scatter(T_zonal_MERRA2[:,80],level_MERRA2,c='m',marker='.',label='MERRA2')
plt.title('Monthly Mean T Field of 1997-07 at 60N (vertical profile)' )
fig3.set_size_inches(5, 8)
#plt.legend()
plt.xlabel("Temperature (Celsius)")
#plt.xticks()
plt.ylabel("Height (hPa)")
plt.legend()
#invert the y axis
plt.gca().invert_yaxis()
plt.show()
fig3.savefig(output_path + os.sep + 'Comp_var_monthly_zonal_mean_T_199707_60N.jpg', dpi = 500)

fig4 = plt.figure()
#plt.axhline(y=0, color='k',ls='-')
plt.scatter(v_zonal_ERAI[:,40],level_ERAI,c='c',marker='.',label='ORAS4')
plt.scatter(v_zonal_MERRA2[:,80],level_MERRA2,c='m',marker='.',label='GLORYS2V3')
plt.title('Monthly Mean v Field of 1997-07 at 60N (vertical profile)' )
fig4.set_size_inches(5, 8)
#plt.legend()
plt.xlabel("Meridional Wind Velocity (m/s)")
#plt.xticks()
plt.ylabel("Height (hPa)")
plt.legend()
#invert the y axis
plt.gca().invert_yaxis()
plt.show()
fig4.savefig(output_path + os.sep + 'Comp_var_monthly_zonal_mean_v_199707_60N.jpg', dpi = 500)
