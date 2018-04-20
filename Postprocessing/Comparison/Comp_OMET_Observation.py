#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : Compare OMET of all reanalysis datasets from observation in the Atlantic
Author          : Yang Liu
Date            : 2017.12.06
Last Update     : 2018.04.20
Description     : The code aims to plot and compare the meridional energy transport
                  in the ocean obtained from reanalysis data with direct observation
                  in the Atlantic Ocean. The oceanic meridional energy transport is
                  calculated from ORAS4, GLORYS2V3, SODA3 and ORAS5.
Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, sys, matplotlib, logging
variables       : Oceanic Meridional Energy Transport       RAPID-ARRAY
                  Oceanic Meridional Energy Transport       ORAS4, GLORYS2v3

Caveat!!        : Spatial and temporal coverage
                  Observation
                  RAPID-ARRAY    2004.04.02 00:00 - 2015.10   26.5N
                  GSR            ??
                  OSNAP          2014 - 2016
                  Reanalysis
                  GLORYS2V3      1992 - 2014         90S - 90N
                  ORAS4          1958 - 2014         90S - 90N
                  SODA3          1980 - 2015         90S - 90N
                  Hindcast
                  NEMO ORCA083   1958 - 2012

                  The full dataset of ORAS4 is from 1958. However, a quality report from
                  Magdalena from ECMWF indicates the quality of data for the first
                  two decades are very poor. Hence we use the data from 1979. which
                  is the start of satellite era.
                  The full dataset of ORAS4 is from 1958.

                  For the time series from RAPID ARRAY, the record starts from 00:00:00 02-04-2004.
                  The time step in the dataset is 12 hours (00:00:00 and 12:00:00).
                  From mocha_mht_data_2015.nc, the record ends at 00:00:00 12-10-2015

                  The hindcast is performed with NEMO-LIM ocean model on ORCA012 grid by
                  Ben Moat et. al. from NOC. The time coverage is from 1958 - 2012, 55 years
                  monthly time series at 26.5N.
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
# Reanalysis
datapath_ORAS4 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ORAS4/postprocessing'
datapath_GLORYS2V3 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/GLORYS2V3/postprocessing'
datapath_SODA3 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/SODA3/postprocessing'
# observation
datapath_RAPID = '/home/yang/NLeSC/Computation_Modeling/BlueAction/Oceanography/RAPID_ARRAY'
# hindcast
datapath_hindcast = '/home/yang/NLeSC/Computation_Modeling/BlueAction/Oceanography/ORCA083hindcast_BenMoat'
# mask path
datapath_mask_ORAS4 ='/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ORAS4'
datapath_mask_GLORYS2V3 ='/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/GLORYS2V3'
datapath_mask_SODA3 ='/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/SODA3'
# specify output path for figures
output_path = '/home/yang/NLeSC/Computation_Modeling/BlueAction/Oceanography/Comp_RAPID'
####################################################################################
print '*******************************************************************'
print '*********************** Locations on ORCA *************************'
print '********************** against Observation ************************'
print '*******************************************************************'
# ii jj pairs of locations on ORCA grid for comparison with observcation
# for RAPID ARRAY
# ORCA1 (ORAS4)
ii_ORCA1_RAPID = np.arange(207,274,1,dtype=int) # from 207 to 273
jj_ORCA1_RAPID = np.array([188,188,188,188,188,
                           188,188,188,188,188,
                           188,188,188,188,188,
                           188,188,188,188,188,
                           187,187,187,187,187,
                           187,187,187,187,187,
                           187,187,187,186,186,
                           186,186,185,185,185,
                           185,185,185,185,185,
                           185,185,185,185,185,
                           185,185,185,185,185,
                           185,185,185,186,186,
                           186,187,187,188,188,
                           189,189], dtype=int)
# ORCA025(GLORYS2V3)
ii_ORCA025_RAPID = np.arange(828,1092,1,dtype=int) # from 828 to 1091
jj_ORCA025_RAPID = np.array([606,606,606,606,606,
                           606,606,606,606,605,
                           605,605,605,605,605,
                           605,605,605,605,605,
                           605,605,605,606,606,
                           606,606,606,606,606,
                           606,606,606,606,606,
                           606,606,606,606,606,
                           606,606,606,606,606,
                           606,606,606,606,606,
                           606,606,606,606,605,
                           605,605,605,605,605,
                           605,605,605,605,605,
                           605,605,605,605,605,
                           605,605,605,605,605,
                           604,604,604,604,604,
                           604,604,604,604,604,
                           604,604,604,604,604,
                           604,604,604,604,604,
                           604,603,603,603,603,
                           603,603,603,603,603,
                           603,603,603,603,603,
                           603,603,603,603,603,
                           603,603,603,603,603,
                           603,603,602,602,602,
                           602,601,601,601,601,
                           600,600,600,600,599,
                           599,599,598,598,598,
                           597,597,597,596,596,
                           596,596,595,595,595,
                           595,594,594,594,594,
                           594,594,594,594,594,
                           594,594,594,594,594,
                           594,594,594,594,594,
                           594,594,594,594,594,
                           594,594,594,594,594,
                           594,594,594,594,594,
                           594,594,594,594,594,
                           594,594,594,594,594,
                           594,594,594,594,594,
                           594,594,594,594,594,
                           594,594,594,594,594,
                           594,594,594,594,594,
                           594,594,594,594,594,
                           594,594,594,594,595,
                           595,596,597,598,599,
                           599,600,600,600,600,
                           600,601,601,602,602,
                           602,603,603,603,604,
                           604,604,605,605,606,
                           606,607,607,607,607,
                           607,608,608,609,610,
                           611,612,612,612], dtype=int)
# MOM5(SODA3)
ii_MOM5_RAPID = np.arange(799,1063,1,dtype=int) # from 799 to 1062
jj_MOM5_RAPID = np.array([594,594,594,594,594,
                          594,594,594,594,595,
                          595,595,595,595,595,
                          595,595,595,595,595,
                          595,595,595,596,596,
                          596,596,596,596,596,
                          596,596,596,596,596,
                          596,596,596,596,596,
                          596,596,596,596,596,
                          596,596,596,596,596,
                          596,596,596,596,595,
                          595,595,595,595,595,
                          595,595,595,595,595,
                          595,595,595,595,595,
                          595,595,595,595,595,
                          594,594,594,594,594,
                          594,594,594,594,594,
                          594,594,594,594,594,
                          594,594,594,594,594,
                          594,593,593,593,593,
                          593,593,593,593,593,
                          593,592,592,592,592,
                          592,592,592,592,592,
                          592,592,592,592,592,
                          592,592,591,591,591,
                          591,591,590,590,590,
                          590,590,589,589,589,
                          588,588,588,587,587,
                          587,586,586,586,586,
                          586,585,585,585,585,
                          585,584,584,584,584,
                          584,584,584,584,584,
                          584,584,584,584,584,
                          584,584,584,584,584,
                          584,584,584,584,584,
                          584,584,584,584,584,
                          584,584,584,584,584,
                          584,584,584,584,584,
                          584,584,584,584,584,
                          584,584,584,584,584,
                          584,584,584,584,584,
                          584,584,584,584,584,
                          584,584,584,584,584,
                          584,584,584,584,584,
                          584,584,584,584,585,
                          585,586,587,588,588,
                          588,589,589,589,589,
                          589,589,590,590,591,
                          591,592,592,593,594,
                          594,595,595,596,596,
                          597,597,597,597,598,
                          598,598,599,599,599,
                          600,600,600,601], dtype=int)
print '*******************************************************************'
print '********************* get keys of variables ***********************'
print '*******************************************************************'
# Reanalysis
dataset_ORAS4_point = Dataset(datapath_ORAS4 + os.sep + 'oras4_model_monthly_orca1_E_point.nc')
dataset_GLORYS2V3_point = Dataset(datapath_GLORYS2V3 + os.sep + 'GLORYS2V3_model_monthly_orca025_E_point.nc')
dataset_SODA3_point = Dataset(datapath_SODA3 + os.sep + 'OMET_SODA3_model_5daily_1980_2015_E_point.nc')

dataset_ORAS4_zonal = Dataset(datapath_ORAS4 + os.sep + 'oras4_model_monthly_orca1_E_zonal_int.nc')
dataset_GLORYS2V3_zonal = Dataset(datapath_GLORYS2V3 + os.sep + 'GLORYS2V3_model_monthly_orca025_E_zonal_int.nc')
dataset_SODA3_zonal = Dataset(datapath_SODA3 + os.sep + 'OMET_SODA3_model_5daily_1980_2015_E_zonal_int.nc')
# observation
dataset_RAPID = Dataset(datapath_RAPID + os.sep + 'mocha_mht_data_2015.nc')
# hindcast
dataset_hindcast = Dataset(datapath_hindcast + os.sep + 'OMET_psi_hindcast_ORCA083_1958-2012_Atlantic_2605.nc')
# mask
dataset_mask_ORAS4 = Dataset(datapath_mask_ORAS4 + os.sep + 'mesh_mask.nc')
dataset_mask_GLORYS2V3 = Dataset(datapath_mask_GLORYS2V3 + os.sep + 'G2V3_mesh_mask_myocean.nc')
dataset_mask_SODA3 = Dataset(datapath_mask_SODA3 + os.sep + 'topog.nc')
print '*******************************************************************'
print '*********************** extract variables *************************'
print '*******************************************************************'
# extract variables
# reanalysis
# meridional energy transport
OMET_ORAS4 = dataset_ORAS4_point.variables['E'][46:,:,:,:]/1E+3     # from 2004
OMET_GLORYS2V3 = dataset_GLORYS2V3_point.variables['E'][11:,:,:,:]/1E+3  # from 2004
OMET_SODA3 = dataset_SODA3_point.variables['E'][24:,:,:,:]/1E+3  # from 2004
# stream function
Psi_ORAS4 = dataset_ORAS4_zonal.variables['Psi_atl'][46:,:,:,:]     # the unit is 1E+6 (Sv)
Psi_GLORYS2V3 = dataset_GLORYS2V3_zonal.variables['Psi_atl'][11:,:,:,:] # the unit is 1E+6 (Sv)
# year
year_ORAS4 = dataset_ORAS4_point.variables['year'][46:]             # from 2004
year_GLORYS2V3 = dataset_GLORYS2V3_point.variables['year'][11:]     # from 2004
year_SODA3 = dataset_SODA3_point.variables['year'][24:]             # from 2004
# nominal latitude
lat_ORAS4 =  dataset_ORAS4_zonal.variables['latitude_aux'][:]
lat_GLORYS2V3 = dataset_GLORYS2V3_zonal.variables['latitude_aux'][:]
lat_SODA3 = dataset_SODA3_zonal.variables['latitude_aux'][:]
# latitude
lat_ORAS4_ORCA = dataset_ORAS4_point.variables['latitude'][:]
lat_GLORYS2V3_ORCA = dataset_GLORYS2V3_point.variables['latitude'][:]
lat_SODA3_MOM = dataset_SODA3_point.variables['latitude'][:]
# longitude
lon_ORAS4_ORCA = dataset_ORAS4_point.variables['longitude'][:]
lon_GLORYS2V3_ORCA = dataset_GLORYS2V3_point.variables['longitude'][:]
lon_SODA3_MOM = dataset_SODA3_point.variables['longitude'][:]
# mask
mask_ORAS4 = dataset_mask_ORAS4.variables['vmask'][0,0,:,:]
mask_GLORYS2V3 = dataset_mask_GLORYS2V3.variables['vmask'][0,0,:,:]
mask_SODA3 = dataset_mask_SODA3.variables['wet_c'][:]
# observation
# RAPID ARRAY
# meridional energy transport
OMET_RAPID = dataset_RAPID.variables['Q_sum'][:]/1E+15
# stream function
Psi_RAPID = dataset_RAPID.variables['moc'][:]
# hindcast
# meridional energy transport
OMET_hindcast = dataset_hindcast.variables['E'][:]
# stream function
psi_hindcast = dataset_hindcast.variables['psi'][:]
print '*******************************************************************'
print '********************* Pick up OMET and AMOC ***********************'
print '******************* with specific ii jj pairs *********************'
print '*******************************************************************'
# construct the matrix
OMET_ORAS4_RAPID = np.zeros((len(year_ORAS4),12,len(ii_ORCA1_RAPID)),dtype= float)
OMET_GLORYS2V3_RAPID = np.zeros((len(year_GLORYS2V3),12,len(ii_ORCA025_RAPID)),dtype= float)
OMET_SODA3_RAPID = np.zeros((len(year_SODA3),12,len(ii_MOM5_RAPID)),dtype= float)

for i in np.arange(len(year_ORAS4)):
    for j in np.arange(12):
        for k in np.arange(len(ii_ORCA1_RAPID)):
            OMET_ORAS4_RAPID[i,j,k] = OMET_ORAS4[i,j,jj_ORCA1_RAPID[k],ii_ORCA1_RAPID[k]] \
                                      * mask_ORAS4[jj_ORCA1_RAPID[k],ii_ORCA1_RAPID[k]]

for i in np.arange(len(year_GLORYS2V3)):
    for j in np.arange(12):
        for k in np.arange(len(ii_ORCA025_RAPID)):
            OMET_GLORYS2V3_RAPID[i,j,k] = OMET_GLORYS2V3[i,j,jj_ORCA025_RAPID[k],ii_ORCA025_RAPID[k]] \
                                          * mask_GLORYS2V3[jj_ORCA025_RAPID[k],ii_ORCA025_RAPID[k]]

for i in np.arange(len(year_SODA3)):
    for j in np.arange(12):
        for k in np.arange(len(ii_MOM5_RAPID)):
            OMET_SODA3_RAPID[i,j,k] = OMET_SODA3[i,j,jj_MOM5_RAPID[k],ii_MOM5_RAPID[k]] \
                                          * mask_SODA3[jj_MOM5_RAPID[k],ii_MOM5_RAPID[k]]
# take the zonal integral
OMET_ORAS4_RAPID_int = np.sum(OMET_ORAS4_RAPID,2)
OMET_GLORYS2V3_RAPID_int = np.sum(OMET_GLORYS2V3_RAPID,2)
OMET_SODA3_RAPID_int = np.sum(OMET_SODA3_RAPID,2)
# reshape to get the time series
OMET_ORAS4_RAPID_series = OMET_ORAS4_RAPID_int.reshape(len(year_ORAS4)*12)
OMET_GLORYS2V3_RAPID_series = OMET_GLORYS2V3_RAPID_int.reshape(len(year_GLORYS2V3)*12)
OMET_SODA3_RAPID_series = OMET_SODA3_RAPID_int.reshape(len(year_SODA3)*12)
# reshape the hindcast dataset
OMET_hindcast_series = OMET_hindcast.reshape(55*12)
print '*******************************************************************'
print '***********************   running means   *************************'
print '*******************************************************************'
# running mean is calculated on time series
# define the running window for the running mean
window = 12 # in month
#window = 60 # in month
#window = 120 # in month
window_day = 90 # in days

# calculate the running mean of AMET and OMET at differnt latitudes
OMET_ORAS4_RAPID_series_running_mean = np.zeros((len(OMET_ORAS4_RAPID_series)-window+1),dtype=float)
for i in np.arange(len(OMET_ORAS4_RAPID_series)-window+1):
        OMET_ORAS4_RAPID_series_running_mean[i] = np.mean(OMET_ORAS4_RAPID_series[i:i+window])

OMET_GLORYS2V3_RAPID_series_running_mean = np.zeros((len(OMET_GLORYS2V3_RAPID_series)-window+1),dtype=float)
for i in np.arange(len(OMET_GLORYS2V3_RAPID_series)-window+1):
        OMET_GLORYS2V3_RAPID_series_running_mean[i] = np.mean(OMET_GLORYS2V3_RAPID_series[i:i+window])

OMET_SODA3_RAPID_series_running_mean = np.zeros((len(OMET_SODA3_RAPID_series)-window+1),dtype=float)
for i in np.arange(len(OMET_SODA3_RAPID_series)-window+1):
        OMET_SODA3_RAPID_series_running_mean[i] = np.mean(OMET_SODA3_RAPID_series[i:i+window])

OMET_RAPID_running_mean = np.zeros((len(OMET_RAPID)-window_day+1),dtype=float)
for i in np.arange(len(OMET_RAPID)-window_day+1):
        OMET_RAPID_running_mean[i] = np.mean(OMET_RAPID[i:i+window_day])

print '*******************************************************************'
print '**********************  Pin points on ORCA ************************'
print '*******************************************************************'
lat_ORCA1 = np.zeros(len(jj_ORCA1_RAPID),dtype=float)
lon_ORCA1 = np.zeros(len(ii_ORCA1_RAPID),dtype=float)

lat_ORCA025 = np.zeros(len(jj_ORCA025_RAPID),dtype=float)
lon_ORCA025 = np.zeros(len(ii_ORCA025_RAPID),dtype=float)

lat_MOM5 = np.zeros(len(jj_MOM5_RAPID),dtype=float)
lon_MOM5 = np.zeros(len(ii_MOM5_RAPID),dtype=float)

for i in np.arange(len(jj_ORCA1_RAPID)):
    lat_ORCA1[i] = lat_ORAS4_ORCA[jj_ORCA1_RAPID[i],ii_ORCA1_RAPID[i]]
    lon_ORCA1[i] = lon_ORAS4_ORCA[jj_ORCA1_RAPID[i],ii_ORCA1_RAPID[i]]

for i in np.arange(len(jj_ORCA025_RAPID)):
    lat_ORCA025[i] = lat_GLORYS2V3_ORCA[jj_ORCA025_RAPID[i],ii_ORCA025_RAPID[i]]
    lon_ORCA025[i] = lon_GLORYS2V3_ORCA[jj_ORCA025_RAPID[i],ii_ORCA025_RAPID[i]]

for i in np.arange(len(jj_MOM5_RAPID)):
    lat_MOM5[i] = lat_SODA3_MOM[jj_MOM5_RAPID[i],ii_MOM5_RAPID[i]]
    lon_MOM5[i] = lon_SODA3_MOM[jj_MOM5_RAPID[i],ii_MOM5_RAPID[i]]

fig1 = plt.figure()
m = Basemap(projection='cyl',llcrnrlat=0,urcrnrlat=90,llcrnrlon=-180,urcrnrlon=180,lon_0=0,lat_0=0,resolution='l')
m.drawcoastlines(linewidth=0.25)
m.drawparallels(np.arange(0,91,30),labels=[1,1,0,0],fontsize = 7)
m.drawmeridians(np.arange(-180,181,60),labels=[0,0,0,1],fontsize = 7)
XX1, YY1 = m(lon_ORCA1, lat_ORCA1)
XX2, YY2 = m(lon_ORCA025, lat_ORCA025)
XX3, YY3 = m(lon_MOM5, lat_MOM5)
# alpha bleding factor with map
m.scatter(XX3,YY3,1.5,marker='*',color='y',alpha=0.6, edgecolor='none',label='MOM5')
m.scatter(XX2,YY2,1.5,marker='o',color='m',alpha=0.6, edgecolor='none',label='ORCA025')
m.scatter(XX1,YY1,3.5,marker='*',color='c',alpha=0.6, edgecolor='none',label='ORCA1')
plt.title('The location of RAPID ARRAY on ORCA1 and ORCA025 grid',fontsize = 9, y=1.05)
plt.show()
fig1.savefig(output_path + os.sep + "location_ORCA_RAPID.jpeg",dpi=500)
print '*******************************************************************'
print '**********************  time series plots  ************************'
print '*******************************************************************'
# index for axis
index = np.arange(1,12*12+1,1) # 2004 - 2015
index_RAPID = np.linspace(4,12*12-3,8398) # ignore the missing April 1st 2004 and the rest of the days in Oct 2015
index_hindcast = np.arange(1,12*9+1,1) # 2004 - 2012
# meridional energy transport
fig2 = plt.figure()
plt.plot(index_RAPID[:],OMET_RAPID[:-23],'g--',label='RAPID ARRAY')
plt.plot(index[:-12],OMET_ORAS4_RAPID_series[:],'c-',label='ORAS4')
plt.plot(index[:-12],OMET_GLORYS2V3_RAPID_series[:],'m-',label='GLORYS2V3')
plt.plot(index,OMET_SODA3_RAPID_series[:],'y-',label='SODA3')
plt.title('Meridional Energy Transport in the ocean at 26.5 N (02/04/2004 - 12/10/2015)')
plt.legend()
fig2.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(1, 12*12, 12), np.arange(2004,2016,1))
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig2.savefig(output_path + os.sep + 'Comp_OMET_26.5N_RAPID_time_series.jpg', dpi = 500)

# meridional energy transport with running mean
fig3 = plt.figure()
plt.plot(index[window-1:-12],OMET_ORAS4_RAPID_series_running_mean[:],'c-',label='ORAS4')
plt.plot(index[window-1:-12],OMET_GLORYS2V3_RAPID_series_running_mean[:],'m-',label='GLORYS2V3')
plt.plot(index[window-1:],OMET_SODA3_RAPID_series_running_mean[:],'y-',label='SODA3')
plt.plot(index_RAPID[window_day-1:],OMET_RAPID_running_mean[:-23],'g-',label='RAPID ARRAY')
plt.title('Meridional Energy Transport in the ocean at 26.5 N with a running mean of %d months (02/04/2004 - 12/10/2015)' % (window))
plt.legend()
fig3.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(1, 12*12, 12), np.arange(2004,2016,1))
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig3.savefig(output_path + os.sep + 'Comp_OMET_26.5N_RAPID_running_mean_%dm_90d_time_series.jpg' % (window), dpi = 500)

# meridional energy transport with hindcast on ORCA083

fig4 = plt.figure()
plt.plot(index_RAPID[:],OMET_RAPID[:-23],'g--',label='RAPID ARRAY')
plt.plot(index[:-12],OMET_ORAS4_RAPID_series[:],'c-',label='ORAS4')
plt.plot(index[:-12],OMET_GLORYS2V3_RAPID_series[:],'m-',label='GLORYS2V3')
plt.plot(index,OMET_SODA3_RAPID_series[:],'y-',label='SODA3')
plt.plot(index_hindcast[:],OMET_hindcast_series[46*12:],'b-',label='NEMO ORCA083 hindcast')
plt.title('Meridional Energy Transport in the ocean at 26.5 N (02/04/2004 - 12/10/2015)')
plt.legend()
fig4.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(1, 12*12, 12), np.arange(2004,2016,1))
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig4.savefig(output_path + os.sep + 'Comp_OMET_26.5N_RAPID_hindcast_time_series.jpg', dpi = 500)
