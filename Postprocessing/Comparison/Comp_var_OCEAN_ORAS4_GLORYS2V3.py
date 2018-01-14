#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : Compare oceanic variable fields (MERRA2,ERA-Interim,JRA55)
Author          : Yang Liu
Date            : 2018.01.11
Last Update     : 2018.01.11
Description     : The code aims to compare the spatial and temporal distribution of
                  different fields from difference oceanic reanalysis datasets. In this,
                  case, this includes ORAS4 from ECMWF, GLORYS2V3 from
Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, sys, matplotlib
variables       : Absolute Temperature              T         [K]
                  Zonal Divergent Wind              u         [m/s]
                  Meridional Divergent Wind         v         [m/s]


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
datapath_ORAS4 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ORAS4/statistics'
datapath_ORAS4_mask = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ORAS4'
datapath_GLORYS2V3 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/GLORYS2V3/statistics'
datapath_GLORYS2V3_mask = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/GLORYS2V3'
# specify output path for figures
output_path = '/home/yang/NLeSC/Computation_Modeling/BlueAction/OMET/Comparison/var'
# the threshold ( index of latitude) of the OMET

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

# take the variable keys
dataset_GLORYS2V3 = Dataset(datapath_GLORYS2V3 + os.sep + 'GLORYS2V3_model_monthly_orca025_var_point.nc')
dataset_GLORYS2V3_mask = Dataset(datapath_GLORYS2V3_mask + os.sep + 'G2V3_mesh_mask_myocean.nc')
dataset_ORAS4 = Dataset(datapath_ORAS4 + os.sep + 'oras4_model_monthly_orca1_var_point.nc')
dataset_ORAS4_mask = Dataset(datapath_ORAS4_mask + os.sep + 'mesh_mask.nc')
# extract variables
# zonal mean
theta_glo_zonal_GLORYS2V3 = dataset_GLORYS2V3.variables['theta_glo_zonal'][:]
theta_glo_zonal_ORAS4 = dataset_ORAS4.variables['theta_glo_zonal'][:]
v_glo_zonal_GLORYS2V3 = dataset_GLORYS2V3.variables['v_glo_zonal'][:]
v_glo_zonal_ORAS4 = dataset_ORAS4.variables['v_glo_zonal'][:]
# vertical mean
theta_glo_vert_GLORYS2V3 = dataset_GLORYS2V3.variables['theta_glo_vert'][:]
theta_glo_vert_ORAS4 = dataset_ORAS4.variables['theta_glo_vert'][:]
v_glo_vert_GLORYS2V3 = dataset_GLORYS2V3.variables['v_glo_vert'][:]
v_glo_vert_ORAS4 = dataset_ORAS4.variables['v_glo_vert'][:]
# latitude
theta_latitude_aux_GLORYS2V3 = dataset_GLORYS2V3_mask.variables['nav_lat'][:,1061]
theta_latitude_aux_ORAS4 = dataset_ORAS4_mask.variables['nav_lat'][:,96]
v_latitude_aux_GLORYS2V3 = dataset_GLORYS2V3_mask.variables['gphiv'][0,:,1060]
v_latitude_aux_ORAS4 = dataset_ORAS4_mask.variables['gphiv'][0,:,96]
# lontitude
theta_longitude_GLORYS2V3 = dataset_GLORYS2V3_mask.variables['nav_lon'][:]
theta_longitude_ORAS4 = dataset_ORAS4_mask.variables['nav_lon'][:]
v_longitude_GLORYS2V3 = dataset_GLORYS2V3_mask.variables['glamv'][0,:,:]
v_longitude_ORAS4 = dataset_ORAS4_mask.variables['glamv'][0,:,:]
# depth
depth_GLORYS2V3 = dataset_GLORYS2V3_mask.variables['deptht'][:]
depth_ORAS4 = dataset_ORAS4_mask.variables['nav_lev'][:]
# year
year_GLORYS2V3 = dataset_GLORYS2V3.variables['year'][:]
year_ORAS4 = dataset_ORAS4.variables['year'][:]

# set the filled value to be 0
np.ma.set_fill_value(theta_glo_zonal_GLORYS2V3,0)
np.ma.set_fill_value(theta_glo_zonal_ORAS4,0)
np.ma.set_fill_value(v_glo_zonal_GLORYS2V3,0)
np.ma.set_fill_value(v_glo_zonal_ORAS4,0)
np.ma.set_fill_value(theta_glo_vert_GLORYS2V3,0)
np.ma.set_fill_value(theta_glo_vert_ORAS4,0)
np.ma.set_fill_value(v_glo_vert_GLORYS2V3,0)
np.ma.set_fill_value(v_glo_vert_ORAS4,0)
print '*******************************************************************'
print '********************** horizontal profile *************************'
print '*******************************************************************'
########################      control panel      #########################
# time: 2001.01 lat lon : 60N
# year_index_ORAS4 = 43
# month_index_ORAS4 = 0
# lat_index_ORAS4 = 233
# year_index_GLORYS2V3 = 8
# month_index_GLORYS2V3 = 0
# lat_index_GLORYS2V3 = 788
# time: 2000.9 lat lon : 60N
# year_index_ORAS4 = 42
# month_index_ORAS4 = 8
# lat_index_ORAS4 = 233
# year_index_GLORYS2V3 = 7
# month_index_GLORYS2V3 = 8
# lat_index_GLORYS2V3 = 788
##########################################################################
# temperature
fig1 = plt.figure()
plt.axhline(y=0, color='k',ls='-')
plt.scatter(theta_longitude_ORAS4[233,:],theta_glo_vert_ORAS4[43,0,233,:],c='c',marker='.',label='ORAS4')
plt.scatter(theta_longitude_GLORYS2V3[788,:],theta_glo_vert_GLORYS2V3[8,0,788,:],c='m',marker='.',label='GLORYS2V3')
plt.title('Monthly Mean T Field of 2001-01 at 60N (horizontal profile)' )
fig1.set_size_inches(8, 5)
#plt.legend()
plt.xlabel("Latitudes")
#plt.xticks()
plt.ylabel("Potential Temperature (Celsius)")
plt.legend()
plt.show()
fig1.savefig(output_path + os.sep + 'Comp_var_monthly_vert_mean_T_200101_60N.jpg', dpi = 500)

# velocity
# meridional velocity time: 2001.01 lat lon : 60N
fig2 = plt.figure()
plt.axhline(y=0, color='k',ls='-')
plt.scatter(v_longitude_ORAS4[233,:],v_glo_vert_ORAS4[43,0,233,:],c='c',marker='.',label='ORAS4')
plt.scatter(v_longitude_GLORYS2V3[788,:],v_glo_vert_GLORYS2V3[8,0,788,:],c='m',marker='.',label='GLORYS2V3')
plt.title('Monthly Mean v Field of 2001-01 at 60N (horizontal profile)' )
fig2.set_size_inches(8, 5)
#plt.legend()
plt.xlabel("Latitudes")
#plt.xticks()
plt.ylabel("Meridional Current Velocity (m/s)")
plt.legend()
plt.show()
fig2.savefig(output_path + os.sep + 'Comp_var_monthly_vert_mean_v_200101_60N.jpg', dpi = 500)
print '*******************************************************************'
print '*********************** vertical profile **************************'
print '*******************************************************************'
# temperature
fig3 = plt.figure()
plt.axhline(y=0, color='k',ls='-')
#plt.scatter(depth_ORAS4,theta_glo_zonal_ORAS4[43,0,:,233],c='c',marker='o',label='ORAS4')
#plt.scatter(depth_GLORYS2V3,theta_glo_zonal_GLORYS2V3[8,0,:,788],c='m',marker='o',label='GLORYS2V3')
plt.scatter(theta_glo_zonal_ORAS4[43,0,:,233],depth_ORAS4,c='c',marker='.',label='ORAS4')
plt.scatter(theta_glo_zonal_GLORYS2V3[8,0,:,788],depth_GLORYS2V3,c='m',marker='.',label='GLORYS2V3')
plt.title('Monthly Mean T Field of 2001-01 at 60N (vertical profile)' )
fig3.set_size_inches(5, 8)
#plt.legend()
plt.xlabel("Potential Temperature (Celsius)")
#plt.xticks()
plt.ylabel("Depth")
plt.legend()
#invert the y axis
plt.gca().invert_yaxis()
plt.show()
fig3.savefig(output_path + os.sep + 'Comp_var_monthly_zonal_mean_T_200101_60N.jpg', dpi = 500)

fig4 = plt.figure()
plt.axhline(y=0, color='k',ls='-')
plt.scatter(v_glo_zonal_ORAS4[43,0,:,233],depth_ORAS4,c='c',marker='.',label='ORAS4')
plt.scatter(v_glo_zonal_GLORYS2V3[8,0,:,788],depth_GLORYS2V3,c='m',marker='.',label='GLORYS2V3')
plt.title('Monthly Mean v Field of 2001-01 at 60N (vertical profile)' )
fig4.set_size_inches(5, 8)
#plt.legend()
plt.xlabel("Meridional Current Velocity (m/s)")
#plt.xticks()
plt.ylabel("Depth")
plt.legend()
#invert the y axis
plt.gca().invert_yaxis()
plt.show()
fig4.savefig(output_path + os.sep + 'Comp_var_monthly_zonal_mean_v_200101_60N.jpg', dpi = 500)
