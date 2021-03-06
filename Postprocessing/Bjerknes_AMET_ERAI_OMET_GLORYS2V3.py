#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : Bjerknes Compensation between AMET and OMET (ERA-Interim & GLROSY2V3)
Author          : Yang Liu
Date            : 2017.11.12
Last Update     : 2017.12.14
Description     : The code aims to study the Bjerknes compensation between atmosphere
                  and ocean. The atmospheric meridional energy transport is calculated
                  from reanalysis data ERA-Interim. The oceanic meridional energy
                  transport is calculated from GLORYS2V3.
Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, sys, matplotlib, logging
variables       : Atmospheric Meridional Energy Transport   ERA-Interim
                  Oceanic Meridional Energy Transport       GLORYS2V3
Caveat!!        : The full dataset of GLORYS2V3 is from 1993 to 2014.
                  Data from 30N - 90N are taken into account!
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
datapath_AMET = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ERAI/postprocessing'
datapath_OMET = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/GLORYS2V3/postprocessing'
# specify output path for the netCDF4 file
output_path = '/home/yang/NLeSC/Computation_Modeling/BlueAction/Bjerknes/ERAInterim_GLORYS2V3'
# index of latitude for insteret
# 60N
lat_OMET = 788
lat_AMET_reverse = 40
# after a cut to 20-90 N
lat_OMET_cut = 212
lat_AMET = 54
# mask path
#mask_path = 'F:\DataBase\GLORYS\S2V3\Monthly\Model'
####################################################################################
print '*******************************************************************'
print '*********************** extract variables *************************'
print '*******************************************************************'
dataset_AMET = Dataset(datapath_AMET + os.sep + 'model_daily_075_1979_2016_E_zonal_int.nc')
dataset_OMET = Dataset(datapath_OMET + os.sep + 'GLORYS2V3_model_monthly_orca025_E_zonal_int.nc')

#dataset_AMET_point = Dataset(datapath_AMET + os.sep + 'model_daily_075_1979_2016_E_point.nc')
#dataset_OMET_point = Dataset(datapath_OMET + os.sep + 'GLORYS2V3_model_monthly_orca025_E_point.nc')

for k in dataset_OMET.variables:
    print dataset_OMET.variables['%s' % (k)]
for l in dataset_AMET.variables:
    print dataset_AMET.variables['%s' % (l)]

# from 1993 to 2014
# from 30N - 90N
AMET_reverse = dataset_AMET.variables['E'][14:-2,:,:]/1000 # from Tera Watt to Peta Watt
OMET = dataset_OMET.variables['E'][:,:,576:]/1000 # from Tera Watt to Peta Watt # start from 1993

year = dataset_OMET.variables['year'][:]    # from 1993 to 2014
month = dataset_OMET.variables['month'][:]
latitude_OMET = dataset_OMET.variables['latitude_aux'][576:]
latitude_AMET_reverse = dataset_AMET.variables['latitude'][:]

# since OMET is from 30N - 90N, AMET is from 90N to 30N, we have to reverse it
# for interpolation, x should be monotonically increasing
latitude_AMET = latitude_AMET_reverse[::-1]
AMET = AMET_reverse[:,:,::-1]

print '*******************************************************************'
print '*************************** whitening *****************************'
print '*******************************************************************'
month_ind = np.arange(12)
year_ind = np.arange(len(year))
seansonal_cycle_AMET = np.mean(AMET,axis=0)
seansonal_cycle_OMET = np.mean(OMET,axis=0)
AMET_white = np.zeros(AMET.shape,dtype=float)
OMET_white = np.zeros(OMET.shape,dtype=float)
for i in year_ind:
    for j in month_ind:
        AMET_white[i,j,:] = AMET[i,j,:] - seansonal_cycle_AMET[j,:]
        OMET_white[i,j,:] = OMET[i,j,:] - seansonal_cycle_OMET[j,:]

print '*******************************************************************'
print '****************** prepare variables for plot *********************'
print '*******************************************************************'
# annual mean of AMET and OMET at different latitudes
AMET_mean = np.mean(np.mean(AMET,0),0)
OMET_mean = np.mean(np.mean(OMET,0),0)
# Interpolation through spline
OMET_mean_interpolate = np.zeros(AMET_mean.shape,dtype=float)
# 'kind' refer to the interpolation method, it includes:
# 'linear' 'nearest' and spline interpolation of 1,2,3 order 'slinear' 'quadratic' 'cubic'
ius = scipy.interpolate.interp1d(latitude_OMET, OMET_mean, kind='slinear',bounds_error=False,fill_value=0.0)
OMET_mean_interpolate = ius(latitude_AMET)

# dataset with seasonal cycle - time series
AMET_series = AMET.reshape(len(year)*len(month),len(latitude_AMET))
OMET_series = OMET.reshape(len(year)*len(month),len(latitude_OMET))
# dataset without seasonal cycle - time series
AMET_white_series = AMET_white.reshape(len(year)*len(month),len(latitude_AMET))
OMET_white_series = OMET_white.reshape(len(year)*len(month),len(latitude_OMET))

# interpolate OMET on the latitude of AMET
OMET_interpolate = np.zeros((len(year),len(month),len(latitude_AMET)),dtype=float)
for i in year_ind:
    for j in month_ind:
        ius = scipy.interpolate.interp1d(latitude_OMET, OMET[i,j,:], kind='slinear',bounds_error=False,fill_value=0.0)
        OMET_interpolate[i,j,:] = ius(latitude_AMET)

OMET_interpolate_series = OMET_interpolate.reshape(len(year)*len(month),len(latitude_AMET))

# remove the seasonal cycle after the interpolation of OMET
seansonal_cycle_OMET_interpolate = np.mean(OMET_interpolate,axis=0)
OMET_interpolate_white = np.zeros(OMET_interpolate.shape,dtype=float)
for i in year_ind:
    for j in month_ind:
        OMET_interpolate_white[i,j,:] = OMET_interpolate[i,j,:] - seansonal_cycle_OMET_interpolate[j,:]

OMET_interpolate_white_series = OMET_interpolate_white.reshape(len(year)*len(month),len(latitude_AMET))

#!!!!!!!!!! Test module for interpolation !!!!!!!!!!
fig99 = plt.figure()
plt.plot(OMET_interpolate_white_series[:,lat_AMET],'r-',label='interpolate')
plt.plot(OMET_white_series[:,lat_OMET_cut],'b-',label='original')
plt.legend()
plt.show()
print '*******************************************************************'
print '********************** Running mean/sum ***************************'
print '*******************************************************************'
# running mean is calculated on time series
# define the running window for the running mean
window = 12 # in month
#window = 60 # in month
#window = 120 # in month

# calculate the running mean of AMET and OMET at 60N
AMET_white_series_running_mean = np.zeros((len(AMET_white_series)-window+1,len(latitude_AMET)),dtype=float)
OMET_interpolate_white_series_running_mean = np.zeros((len(OMET_interpolate_white_series)-window+1,len(latitude_AMET)),dtype=float)

for i in np.arange(len(OMET_series)-window+1):
    for j in np.arange(len(latitude_AMET)):
        AMET_white_series_running_mean[i,j] = np.mean(AMET_white_series[i:i+window,j])
        OMET_interpolate_white_series_running_mean[i,j] = np.mean(OMET_interpolate_white_series[i:i+window,j])

print '*******************************************************************'
print '*************************** x-y plots *****************************'
print '*******************************************************************'
fig0 = plt.figure()
plt.plot(latitude_AMET,AMET_mean,'r-',label='ERA-Interim')
plt.plot(latitude_OMET,OMET_mean,'b-',label='GLORYS2V3')
plt.plot(latitude_AMET,AMET_mean + OMET_mean_interpolate,'g--',label='Total')
plt.title('Meridional Energy Transport at 60 N (1993-2014)')
plt.legend()
#fig1.set_size_inches(5, 5)
plt.xlabel("Latitude")
labels =['20','30','40','50','60','70','80','90']
plt.xticks(np.linspace(20, 90, 8),labels)
#plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig0.savefig(output_path + os.sep + 'ERA-Interim_GLORYS2V3_annual_mean_1993_2014.jpg', dpi = 500)

print '*******************************************************************'
print '*********************** time series plots *************************'
print '*******************************************************************'
# index and namelist of years for time series and running mean time series
index = np.arange(1,265,1)

#index_running_mean = np.arange(1,433-window+1,1)
#index_year_running_mean = np.arange(1993+window/12-1,2015,1)

# time series plot of meridional energy transport at 60N
fig1 = plt.figure()
plt.plot(index,AMET_series[:,lat_AMET],'r-',label='ERA-Interim')
plt.plot(index,OMET_series[:,lat_OMET_cut],'b-',label='GLORYS2V3')
plt.plot(index,AMET_series[:,lat_AMET]+OMET_interpolate_series[:,lat_AMET],'g--',label='Total')
plt.title('Meridional Energy Transport at 60 N (1993-2014)')
plt.legend()
fig1.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(0, 264, 23), year)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig1.savefig(output_path + os.sep + 'ERA-Interim_GLORYS2V3_60N_total_time_series_1993_2014.jpg', dpi = 500)

# time series plot of meridional energy transport anomalies at 60N
fig2 = plt.figure()
plt.plot(index,AMET_white_series[:,lat_AMET],'r-',label='ERA-Interim')
plt.plot(index,OMET_white_series[:,lat_OMET_cut],'b-',label='GLORYS2V3')
plt.plot(index,AMET_white_series[:,lat_AMET]+OMET_interpolate_white_series[:,lat_AMET],'g--',label='Total')
plt.title('Meridional Energy Transport Anomalies at 60 N (1993-2014)')
plt.legend()
fig2.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(0, 264, 23), year)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig2.savefig(output_path + os.sep + 'AMET_OMET_60N_anomaly_time_series_1993_2014.jpg', dpi = 500)

# time series plot of meridional energy transport anomalies at 60N with 10 years running mean
fig3 = plt.figure()
plt.plot(index[window-1:],AMET_white_series_running_mean[:,lat_AMET],'r-',label='ERA-Interim')
plt.plot(index[window-1:],OMET_interpolate_white_series_running_mean[:,lat_AMET],'b-',label='GLORYS2V3')
plt.plot(index[window-1:],AMET_white_series_running_mean[:,lat_AMET]+OMET_interpolate_white_series_running_mean[:,lat_AMET],'g--',label='Total')
plt.title('Meridional Energy Transport Anomalies with running mean of %d months at 60 N (1993-2014)' % (window))
plt.legend()
fig3.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(0, 264, 23), year)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig3.savefig(output_path + os.sep + 'AMET_OMET_60N_anomaly_running_mean_%dmtime_series_1993_2014.jpg' % (window), dpi = 500)

print '*******************************************************************'
print '*********************** Regression plots **************************'
print '*******************************************************************'
#Regression
# create an array to store the correlation coefficient
slope = np.zeros(len(latitude_AMET),dtype = float)
r_value = np.zeros(len(latitude_AMET),dtype = float)
p_value = np.zeros(len(latitude_AMET),dtype = float)

# regress OMET on AMET before removing seasonal cycling
for i in np.arange(len(latitude_AMET)):
        # return value: slope, intercept, r_value, p_value, stderr
        slope[i],_,r_value[i],p_value[i],_ = scipy.stats.linregress(AMET_series[:,i],OMET_interpolate_series[:,i])
# plot the correlation coefficient at each latitude
fig4 = plt.figure()
plt.plot(latitude_AMET,r_value,'r-',label='Compensation')
plt.title('Regression of OMET on AMET in the North Hemisphere (1993-2014)')
plt.legend()
fig4.set_size_inches(12, 5)
plt.xlabel("Latitude")
#plt.xticks(np.linspace(0, 432, 37), index_year)
#plt.xticks(rotation=60)
plt.ylabel("Correlation Coefficient")
plt.show()
fig4.savefig(output_path + os.sep + 'ERA-Interim_GLORYS2V3_regression_correlation_coef_1993_2014.jpg', dpi = 500)
#Regression with time lag

# regress OMET on AMET after removing seasonal cycling
for i in np.arange(len(latitude_AMET)):
        # return value: slope, intercept, r_value, p_value, stderr
        slope[i],_,r_value[i],p_value[i],_ = scipy.stats.linregress(AMET_white_series[:,i],OMET_interpolate_white_series[:,i])
# plot the correlation coefficient at each latitude
fig5 = plt.figure()
plt.plot(latitude_AMET,r_value,'r-',label='Compensation')
plt.title('Regression of OMET on AMET after remvoing climatology in the North Hemisphere (1993-2014)')
plt.legend()
fig5.set_size_inches(12, 5)
plt.xlabel("Latitude")
#plt.xticks(np.linspace(0, 432, 37), index_year)
#plt.xticks(rotation=60)
plt.ylabel("Correlation Coefficient")
plt.show()
fig5.savefig(output_path + os.sep + 'ERA-Interim_GLORYS2V3_white_regression_correlation_coef_1993_2014.jpg', dpi = 500)

# regress OMET on AMET after removing seasonal cycling with x months running means
for i in np.arange(len(latitude_AMET)):
        # return value: slope, intercept, r_value, p_value, stderr
        slope[i],_,r_value[i],p_value[i],_ = scipy.stats.linregress(AMET_white_series_running_mean[:,i],OMET_interpolate_white_series_running_mean[:,i])
# plot the correlation coefficient at each latitude
fig6 = plt.figure()
plt.plot(latitude_AMET,r_value,'r-',label='Compensation')
plt.title('Regression of OMET on AMET after remvoing climatology with running mean of %d months in the North Hemisphere (1993-2014)' % (window))
plt.legend()
fig6.set_size_inches(12, 5)
plt.xlabel("Latitude")
#plt.xticks(np.linspace(0, 432, 37), index_year)
#plt.xticks(rotation=60)
plt.ylabel("Correlation Coefficient")
plt.show()
fig6.savefig(output_path + os.sep + 'ERA-Interim_GLORYS2V3_white_running_mean_%dm_regression_correlation_coef_1993_2014.jpg' % (window), dpi = 500)

print '*******************************************************************'
print '******************* Regression Lead/Lag plots *********************'
print '*******************************************************************'
#Regression with time lag
#lead_index_ocean = np.arange(-120,121,1)
lead_index_ocean = np.arange(-180,181,1)

# create a 2D array to store the correlation coefficient
slope_2D = np.zeros((len(lead_index_ocean),len(latitude_AMET)),dtype = float)
r_value_2D = np.zeros((len(lead_index_ocean),len(latitude_AMET)),dtype = float)
p_value_2D = np.zeros((len(lead_index_ocean),len(latitude_AMET)),dtype = float)

# regress
for i in np.arange(len(lead_index_ocean)):
    for j in np.arange(len(latitude_AMET)):
        if lead_index_ocean[i]<0:
            # atmosphere lead the ocean
            slope_2D[i,j],_,r_value_2D[i,j],p_value_2D[i,j],_ = scipy.stats.linregress(AMET_white_series_running_mean[:lead_index_ocean[i],j],OMET_interpolate_white_series_running_mean[-lead_index_ocean[i]:,j])
        elif lead_index_ocean[i]>0:
            # ocean lead the atmosphere
            slope_2D[i,j],_,r_value_2D[i,j],p_value_2D[i,j],_ = scipy.stats.linregress(AMET_white_series_running_mean[lead_index_ocean[i]:,j],OMET_interpolate_white_series_running_mean[:-lead_index_ocean[i],j])
        else:
            slope_2D[i,j],_,r_value_2D[i,j],p_value_2D[i,j],_ = scipy.stats.linregress(AMET_white_series_running_mean[:,j],OMET_interpolate_white_series_running_mean[:,j])
# plot the correlation coefficient contour
x , y = np.meshgrid(lead_index_ocean,latitude_AMET)

fig7 = plt.figure()
# cmap 'jet' 'RdYlBu' 'coolwarm'
#contour_level = np.array([-1.0,-0.8,-0.6,-0.4,-0.2,0,0.5,1.0])
#contour_level = np.array([-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0.0])
contour_level = np.array([-0.8,-0.6,-0.4,-0.3,-0.2,-0.1,0.0])
#cs = plt.contour(x,y,slope_2D.transpose(), linewidth=0.05, colors='k') # negative contours will be dashed by default
#matplotlib.rcParams['contour.negative_linestyle'] = 'solid' #set negative contours to be solid instead of dashed
cs = plt.contour(x,y,slope_2D.transpose(), contour_level, linewidth=0.05, cmap='jet')
plt.clabel(cs, inline=1, fontsize=10)
#plt.contourf(x,y,T_series_E[181:,:]/1000,cmap='coolwarm') # from 20N-90N
plt.title('Lead/Lag regression of OMET on AMET with %d month running means(1993-2014)' % (window))
fig7.set_size_inches(12, 5)
#add color bar
cbar = plt.colorbar(cs,orientation='vertical',shrink =0.8)
#cbar.set_label('PW (1E+15W)')
plt.xlabel("Time Lag (year)")
#lead_year = ['-10','-8','-6','-4','-2','0','2','4','6','8','10']
lead_year = ['-15','-12','-9','-6','-3','0','3','6','9','12','15']
#plt.xticks(np.linspace(-120, 120, 11), lead_year)
plt.xticks(np.linspace(-180, 180, 11), lead_year)
#plt.xticks(rotation=60)
plt.ylabel("Latitude")
plt.show()
fig7.savefig(output_path + os.sep + 'ERA-Interim_GLORYS2V3_running_mean_%dm_regression_lead_lag.jpg' % (window), dpi = 500)


# time lead/lag regression of anomalies without running means
for i in np.arange(len(lead_index_ocean)):
    for j in np.arange(len(latitude_AMET)):
        if lead_index_ocean[i]<0:
            # atmosphere lead the ocean
            slope_2D[i,j],_,r_value_2D[i,j],p_value_2D[i,j],_ = scipy.stats.linregress(AMET_white_series[:lead_index_ocean[i],j],OMET_interpolate_white_series[-lead_index_ocean[i]:,j])
        elif lead_index_ocean[i]>0:
            # ocean lead the atmosphere
            slope_2D[i,j],_,r_value_2D[i,j],p_value_2D[i,j],_ = scipy.stats.linregress(AMET_white_series[lead_index_ocean[i]:,j],OMET_interpolate_white_series[:-lead_index_ocean[i],j])
        else:
            slope_2D[i,j],_,r_value_2D[i,j],p_value_2D[i,j],_ = scipy.stats.linregress(AMET_white_series[:,j],OMET_interpolate_white_series[:,j])
# plot the correlation coefficient contour
x , y = np.meshgrid(lead_index_ocean,latitude_AMET)

fig8 = plt.figure()
# cmap 'jet' 'RdYlBu' 'coolwarm'
#contour_level = np.array([-0.3,-0.2,-0.1,0.0,0.1,0.2,0.3])
contour_level = np.array([-0.3,-0.2,-0.1,0.0])
#cs = plt.contour(x,y,slope_2D.transpose(), linewidth=0.05, colors='k') # negative contours will be dashed by default
#matplotlib.rcParams['contour.negative_linestyle'] = 'solid' #set negative contours to be solid instead of dashed
cs = plt.contour(x,y,slope_2D.transpose(), contour_level, linewidth=0.05, cmap='jet')
plt.clabel(cs, inline=1, fontsize=10)
#plt.contourf(x,y,T_series_E[181:,:]/1000,cmap='coolwarm') # from 20N-90N
plt.title('Lead/Lag regression of OMET on AMET anomalies (1993-2014)')
fig8.set_size_inches(12, 5)
#add color bar
cbar = plt.colorbar(cs,orientation='vertical',shrink =0.8)
#cbar.set_label('PW (1E+15W)')
plt.xlabel("Time Lag (year)")
#lead_year = ['-10','-8','-6','-4','-2','0','2','4','6','8','10']
lead_year = ['-15','-12','-9','-6','-3','0','3','6','9','12','15']
#plt.xticks(np.linspace(-120, 120, 11), lead_year)
plt.xticks(np.linspace(-180, 180, 11), lead_year)
#plt.xticks(rotation=60)
plt.ylabel("Latitude")
plt.show()
fig8.savefig(output_path + os.sep + 'ERA-Interim_GLORYS2V3_anomalies_regression_lead_lag.jpg', dpi = 500)
print '*******************************************************************'
print '****************** maps (average of point data) *******************'
print '*******************************************************************'
