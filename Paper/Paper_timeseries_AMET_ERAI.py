#!/usr/bin/env python
"""
Copyright Netherlands eScience Center

Function        : Postprocessing meridional energy transport from HPC cloud (ERA-Interim)
Author          : Yang Liu
Date            : 2018.06.04
Last Update     : 2018.06.04
Description     : The code aims to postprocess the output from the HPC cloud
                  regarding the computation of atmospheric meridional energy
                  transport based on atmospheric reanalysis dataset ERA-Interim
                  from ECMWF. The complete procedure includes data extraction and
                  making plots.

Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, matplotlib
variables       : Absolute Temperature              T
                  Specific Humidity                 q
                  Logarithmic Surface Pressure      lnsp
                  Zonal Divergent Wind              u
                  Meridional Divergent Wind         v
                  Surface geopotential              z
Caveat!!        : The data is from 30 deg north to 90 deg north (Northern Hemisphere).
"""
import numpy as np
import time as tttt
from netCDF4 import Dataset,num2date
import os
import seaborn as sns
import platform
import logging
#import matplotlib
# Generate images without having a window appear
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, cm

##########################################################################
###########################   Units vacabulory   #########################
# cpT:  [J / kg K] * [K]     = [J / kg]
# Lvq:  [J / kg] * [kg / kg] = [J / kg]
# gz in [m2 / s2] = [ kg m2 / kg s2 ] = [J / kg]

# multiply by v: [J / kg] * [m / s] => [J m / kg s]
# sum over longitudes [J m / kg s] * [ m ] = [J m2 / kg s]

# integrate over pressure: dp: [Pa] = [N m-2] = [kg m2 s-2 m-2] = [kg s-2]
# [J m2 / kg s] * [Pa] = [J m2 / kg s] * [kg / s2] = [J m2 / s3]
# and factor 1/g: [J m2 / s3] * [s2 /m2] = [J / s] = [Wat]
##########################################################################

# print the system structure and the path of the kernal
print platform.architecture()
print os.path

# calculate the time for the code execution
start_time = tttt.time()
# switch on the seaborn effect
sns.set()
#sns.set_style("whitegrid")
#sns.set_style("darkgrid")
sns.set_style("ticks")
sns.despine()

################################   Input zone  ######################################
# specify data path
datapath = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ERAI/postprocessing'
# specify output path for the netCDF4 file
output_path = '/home/yang/NLeSC/PhD/Paperwork/Article/AMET_OMET/figures'
Lat_num = 60
####################################################################################
print '*******************************************************************'
print '*********************** extract variables *************************'
print '*******************************************************************'
# zonal integral
dataset = Dataset(datapath + os.sep + 'model_daily_075_1979_2016_E_zonal_int.nc')
# spacial distribution
dataset_point = Dataset(datapath + os.sep + 'model_daily_075_1979_2016_E_point.nc')

for k in dataset.variables:
    print dataset.variables['%s' % (k)]

# zonal integral
E = dataset.variables['E'][:]
E_internal = dataset.variables['E_cpT'][:]
E_latent = dataset.variables['E_Lvq'][:]
E_geopotential = dataset.variables['E_gz'][:]
E_kinetic = dataset.variables['E_uv2'][:]

# spacial distribution
E_point = dataset_point.variables['E'][:]
#E_point_internal = dataset_point.variables['E_cpT'][:]
#E_point_latent = dataset_point.variables['E_Lvq'][:]
#E_point_geopotential = dataset_point.variables['E_gz'][:]
#E_point_kinetic = dataset_point.variables['E_uv2'][:]

year = dataset.variables['year'][:]
month = dataset.variables['month'][:]
latitude = dataset.variables['latitude'][:]
longitude = dataset_point.variables['longitude'][:]

print '*******************************************************************'
print '****************** prepare variables for plot *********************'
print '*******************************************************************'
# remove seasonal cycles
# zonal integral
E_seasonal_cycle = np.mean(E,0)
month_ind = np.arange(12)
E_white = np.zeros(E.shape)
for i in month_ind:
    for j in np.arange(len(year)):
        E_white[j,i,:] = E[j,i,:] - E_seasonal_cycle[i,:]
# spacial distribution
E_point_seasonal_cycle = np.mean(E_point,0)
E_point_white = np.zeros(E_point.shape)
for i in month_ind:
    for j in np.arange(len(year)):
        E_point_white[j,i,:,:] = E_point[j,i,:,:] - E_point_seasonal_cycle[i,:,:]

# reshape the array into time series
# original signals
series_E = E.reshape(len(year)*len(month),len(latitude))
series_E_internal = E_internal.reshape(len(year)*len(month),len(latitude))
series_E_latent = E_latent.reshape(len(year)*len(month),len(latitude))
series_E_geopotential = E_geopotential.reshape(len(year)*len(month),len(latitude))
series_E_kinetic = E_kinetic.reshape(len(year)*len(month),len(latitude))
# whiten signals
series_E_white = E_white.reshape(len(year)*len(month),len(latitude))
series_E_point_white = E_point_white.reshape(len(year)*len(month),len(latitude),len(longitude))

# transpose
# original signals
T_series_E = np.transpose(series_E)
T_series_E_internal = np.transpose(series_E_internal)
T_series_E_latent = np.transpose(series_E_latent)
T_series_E_geopotential = np.transpose(series_E_geopotential)
T_series_E_kinetic = np.transpose(series_E_kinetic)
# whiten signals
T_series_E_white = np.transpose(series_E_white)

index = np.arange(1,len(year)*len(month)+1,1)
index_year = np.arange(1980,year[-1]+1,5)
axis_ref = np.zeros(len(index))

# everything in one plot
fig6 = plt.figure()
plt.plot(index,T_series_E_internal[40,:]/1000,'r--',label='cpT')
plt.plot(index,T_series_E_latent[40,:]/1000,'m-.',label='Lvq')
plt.plot(index,T_series_E_geopotential[40,:]/1000,'g:',label='gz')
plt.plot(index,T_series_E_kinetic[40,:]/1000,'c:',label='u2')
plt.plot(index,T_series_E[40,:]/1000,'b-',label='total')
#plt.title('Atmospheric Meridional Energy Transport time series at %d N (1979-2016)' % (Lat_num))
plt.legend(frameon=True, loc=2, prop={'size': 16})
fig6.set_size_inches(12.5, 6)
plt.xlabel("Time",fontsize=16)
#plt.xticks(np.linspace(0, 456, 39), index_year)
plt.xticks(np.arange(13,len(year)*len(month)+1,60), index_year,fontsize=16)
#plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)",fontsize=16)
plt.yticks(fontsize=16)
plt.show()
fig6.savefig(output_path + os.sep + 'Meridional_Energy_%dN_eachComponent_time_series_1979_2016.jpg' % (Lat_num), dpi = 500)

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
