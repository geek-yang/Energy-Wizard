#!/usr/bin/env python
"""
Copyright Netherlands eScience Center

Function        : Regression of climatological variable on AMET (JRA55) with whitening
Author          : Yang Liu
Date            : 2018.01.09
Last Update     : 2018.05.23
Description     : The code aims to explore the assotiation between climatological
                  variables with atmospheric meridional energy transport (AMET).
                  The statistical method employed here is linear regression. A
                  number of fields (SST, SLP, Sea ice, geopotential, etc.),
                  corresponding to the preexisting natural modes of variability,
                  will be projected on meridional energy transport. This will enhance
                  our understanding of climate change. Notice that the time series
                  of input data will be whitened (the seasonal cycles are removed)
Return Value    : Map of correlation
Dependencies    : os, time, numpy, scipy, netCDF4, matplotlib, basemap
variables       : Sea Surface Temperature                       SST
                  Sea Level Pressure                            SLP
                  Sea Ice Concentration                         ci
                  Geopotential                                  gz
                  Atmospheric meridional energy transport       AMET
Caveat!!        : The input data of AMET is from 90 deg south to 90 deg north (Northern Hemisphere).
                  Since there is no ice data from JRA55, here we will take SIC from ERA-Interim. As
                  there is no sea ice in atmospheric model, it is not a big matter.
"""

import numpy as np
import scipy as sp
from scipy import stats
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

# print the system structure and the path of the kernal
print platform.architecture()
print os.path

# calculate the time for the code execution
start_time = tttt.time()
# switch on the seaborn effect
sns.set()

################################   Input zone  ######################################
# specify data path
# AMET
datapath_AMET = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/JRA55/postprocessing'
# target climatological variables
datapath_y = "/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ERAI/regression"
# specify output path for figures
output_path = '/home/yang/NLeSC/Computation_Modeling/BlueAction/AMET/JRA55'
# the threshold ( index of latitude) of the AMET
# There is a cut to JRA, too
# index of latitude for insteret
# 20N
lat_JRA55_20 = 124
# 30N
lat_JRA55_30 = 106
# 40N
lat_JRA55_40 = 88
# 50N
lat_JRA55_50 = 70
# 60N
lat_JRA55_60 = 53
# 70N
lat_JRA55_70 = 35
# 80N
lat_JRA55_80 = 17
# make a dictionary for instereted sections (for process automation)
lat_interest = {}
lat_interest_list = [20,30,40,50,60,70,80]
lat_interest['JRA55'] = [lat_JRA55_20,lat_JRA55_30,lat_JRA55_40,lat_JRA55_50,lat_JRA55_60,lat_JRA55_70,lat_JRA55_80]

# from 90N to 20N --> 0:123
# the range ( index of latitude) of the projection field
lat_y = 94 # upto 20 N
####################################################################################
print '*******************************************************************'
print '*********************** extract variables *************************'
print '*******************************************************************'
dataset_AMET = Dataset(datapath_AMET + os.sep + 'AMET_JRA55_model_daily_1979_2015_E_zonal_int.nc')
dataset_y = Dataset(datapath_y + os.sep + 'surface_ERAI_monthly_regress_1979_2016.nc')
for k in dataset_AMET.variables:
    print dataset_AMET.variables['%s' % (k)]

for l in dataset_y.variables:
    print dataset_y.variables['%s' % (l)]

# extract atmospheric meridional energy transport
# dimension (year,month,latitude)
AMET = dataset_AMET.variables['E'][:,:,0:125]/1000 # from Tera Watt to Peta Watt
year = dataset_AMET.variables['year'][:]
lat_AMET = dataset_AMET.variables['latitude'][0:125]
# extract variables from 20N to 90 N
# sea level pressure
SLP = dataset_y.variables['msl'][:444,0:lat_y+1,:] # now to 2015
# sea surface temperature
SST = dataset_y.variables['sst'][:444,0:lat_y+1,:]
mask_SST = np.ma.getmaskarray(SST[0,:,:])
# sea ice cover
ci = dataset_y.variables['ci'][:444,0:lat_y+1,:]
mask_ci = np.ma.getmaskarray(ci[0,:,:])
# longitude
lon = dataset_y.variables['longitude'][:]
# latitude
lat = dataset_y.variables['latitude'][0:lat_y+1]
# time (number of months)
time = dataset_y.variables['time'][:444]

print 'The type of SLP is', type(SLP)
print 'The type of SST is', type(SST)
print 'The type of ci is', type(ci)

print '*******************************************************************'
print '*************************** whitening *****************************'
print '*******************************************************************'
# remove the seasonal cycling of target climatology for regression
# These climitology data comes from ERA-Interim surface level
month_ind = np.arange(12)
# remove climatology for Sea Level Pressure
SLP_seasonal_mean = np.zeros((12,len(lat),len(lon))) # from 20N - 90N
SLP_white = np.zeros(SLP.shape,dtype=float)
for i in month_ind:
    # calculate the monthly mean (seasonal cycling)
    SLP_seasonal_mean[i,:,:] = np.mean(SLP[i::12,:,:],axis=0)
    # remove seasonal mean
    SLP_white[i::12,:,:] = SLP[i::12,:,:] - SLP_seasonal_mean[i,:,:]

# remove climatology for Sea Surface Temperature
SST_seasonal_mean = np.zeros((12,len(lat),len(lon))) # from 20N - 90N
SST_white = np.zeros(SST.shape,dtype=float)
for i in month_ind:
    # calculate the monthly mean (seasonal cycling)
    SST_seasonal_mean[i,:,:] = np.mean(SST[i::12,:,:],axis=0)
    # remove seasonal mean
    SST_white[i::12,:,:] = SST[i::12,:,:] - SST_seasonal_mean[i,:,:]

# remove climatology for Sea Ice Concentration
ci_seasonal_mean = np.zeros((12,len(lat),len(lon))) # from 20N - 90N
ci_white = np.zeros(ci.shape)
for i in month_ind:
    # calculate the monthly mean (seasonal cycling)
    ci_seasonal_mean[i,:,:] = np.mean(ci[i::12,:,:],axis=0)
    # remove seasonal mean
    ci_white[i::12,:,:] = ci[i::12,:,:] - ci_seasonal_mean[i,:,:]

# remove the seasonal cycling of AMET at 60N
# dimension of AMET[year,month]
AMET_seansonal_cycle = np.mean(AMET,axis=0)
AMET_white = np.zeros(AMET.shape,dtype=float)
for i in month_ind:
    AMET_white[:,i,:] = AMET[:,i,:] - AMET_seansonal_cycle[i,:]
# Summer and winter only
# summer refers to June(5), July(6), August(7)
# winter refers to Dec(11), Jan(0), Feb(1)
# AMET_white_series_summer = np.zeros((len(AMET_white_series)/4),dtype=float)
# AMET_white_series_winter = np.zeros((len(AMET_white_series)/4),dtype=float)
#
# AMET_white_series_summer[0::3] = AMET_white_series[5::12] #June
# AMET_white_series_summer[1::3] = AMET_white_series[6::12] #July
# AMET_white_series_summer[2::3] = AMET_white_series[7::12] #August
# AMET_white_series_winter[2::3] = AMET_white_series[11::12] # December
# AMET_white_series_winter[0::3] = AMET_white_series[0::12] # Jan
# AMET_white_series_winter[1::3] = AMET_white_series[1::12] # Feb

print '*******************************************************************'
print '***************************  Detrend  *****************************'
print '*******************************************************************'
####################################################
######      detrend - polynomial fitting      ######
####################################################
poly_fit = np.zeros(ci_white.shape,dtype=float)
for i in np.arange(len(lat)):
    for j in np.arange(len(lon)):
        polynomial = np.polyfit(np.arange(len(time)), ci_white[:,i,j], 5)
        poly = np.poly1d(polynomial)
        poly_fit[:,i,j] = poly(np.arange(len(time)))

ci_white_detrend_poly = np.zeros(ci_white.shape,dtype=float)
ci_white_detrend_poly = ci_white - poly_fit
print '*******************************************************************'
print '*********************** prepare variables *************************'
print '*******************************************************************'
# take the time series of E
AMET_series = AMET.reshape(len(year)*len(month_ind),len(lat_AMET))
AMET_white_series = AMET_white.reshape(len(year)*len(month_ind),len(lat_AMET))
print '*******************************************************************'
print '********************** Running mean/sum ***************************'
print '*******************************************************************'
# running mean is calculated on time series
# define the running window for the running mean
#window = 12 # in month
window = 60 # in month
#window = 120 # in month
AMET_running_mean = np.zeros((len(year)*len(month_ind)-window+1,len(lat_AMET)),dtype=float)
#AMET_running_sum = np.zeros(len(AMET_series)-window+1)
for i in np.arange(len(year)*len(month_ind)-window+1):
    AMET_running_mean[i,:] = np.mean(AMET_series[i:i+window,:],0)

# calculate the running mean and sum of AMET after removing the seasonal cycling
AMET_white_running_mean = np.zeros((len(year)*len(month_ind)-window+1,len(lat_AMET)),dtype=float)
#AMET_running_sum = np.zeros(len(AMET_series)-window+1)
for i in np.arange(len(year)*len(month_ind)-window+1):
    AMET_white_running_mean[i,:] = np.mean(AMET_white_series[i:i+window,:],0)

SLP_white_running_mean = np.zeros((len(year)*len(month_ind)-window+1,len(lat),len(lon)),dtype=float)
for i in np.arange(len(year)*len(month_ind)-window+1):
    SLP_white_running_mean[i,:,:] = np.mean(SLP_white[i:i+window,:,:],0)

SST_white_running_mean = np.zeros((len(year)*len(month_ind)-window+1,len(lat),len(lon)),dtype=float)
for i in np.arange(len(year)*len(month_ind)-window+1):
    SST_white_running_mean[i,:,:] = np.mean(SST_white[i:i+window,:,:],0)

ci_white_running_mean = np.zeros((len(year)*len(month_ind)-window+1,len(lat),len(lon)),dtype=float)
for i in np.arange(len(year)*len(month_ind)-window+1):
    ci_white_running_mean[i,:,:] = np.mean(ci_white[i:i+window,:,:],0)

ci_white_detrend_poly_running_mean = np.zeros((len(year)*len(month_ind)-window+1,len(lat),len(lon)),dtype=float)
for i in np.arange(len(year)*len(month_ind)-window+1):
    ci_white_detrend_poly_running_mean[i,:,:] = np.mean(ci_white_detrend_poly[i:i+window,:,:],0)

print '*******************************************************************'
print '*************************** time series ***************************'
print '*******************************************************************'
# index and namelist of years for time series and running mean time series
index = np.arange(1,445,1)
index_year = np.arange(1979,2016,1)

# #index_running_mean = np.arange(1,457-window+1,1)
# #index_year_running_mean = np.arange(1979+window/12-1,2017,1)
#
# index_summer = np.arange(1,112,1) # 37 years * 12 months / 4 seasons
#
# # plot the AMET after removing seasonal cycle
# fig1 = plt.figure()
# plt.axhline(y=0, color='g',ls='--')
# plt.plot(index,AMET_white_series,'b-',label='JRA55')
# plt.title('Atmospheric Meridional Energy Transport Anomaly at 60N (1979-2015)')
# #plt.legend()
# fig1.set_size_inches(12, 5)
# plt.xlabel("Time")
# plt.xticks(np.linspace(0, 444, 38), index_year)
# plt.xticks(rotation=60)
# plt.ylabel("Meridional Energy Transport (PW)")
# plt.show()
# fig1.savefig(output_path + os.sep + 'AMET_anomaly_60N_time_series_1979_2015.jpg', dpi = 500)
#
# # plot the running mean of AMET after removing seasonal cycle
# fig0 = plt.figure()
# plt.axhline(y=0, color='g',ls='--')
# plt.plot(index[window-1:],AMET_white_running_mean,'b-',label='JRA55')
# plt.title('Running Mean of AMET Anomalies at 60N with a window of %d months (1979-2015)' % (window))
# #plt.legend()
# fig0.set_size_inches(12, 5)
# plt.xlabel("Time")
# plt.xticks(np.linspace(0, 444, 38), index_year)
# plt.xticks(rotation=60)
# plt.ylabel("Meridional Energy Transport (PW)")
# plt.show()
# fig0.savefig(output_path + os.sep + 'AMET_anomaly_60N_running_mean_window_%d_only.jpg' % (window), dpi = 500)
#
# # plot the AMET with running mean
# fig2 = plt.figure()
# plt.axhline(y=0, color='g',ls='--')
# plt.plot(index,AMET_series,'b--',label='time series')
# plt.plot(index[window-1:],AMET_running_mean,'r-',linewidth=2.0,label='running mean')
# plt.title('Running Mean of AMET at 60N with a window of %d months (1979-2015)' % (window))
# #plt.legend()
# fig2.set_size_inches(12, 5)
# plt.xlabel("Time")
# plt.xticks(np.linspace(0, 444, 38), index_year)
# plt.xticks(rotation=60)
# plt.ylabel("Meridional Energy Transport (PW)")
# plt.show()
# fig2.savefig(output_path + os.sep + 'AMET_60N_running_mean_window_%d_comp.jpg' % (window), dpi = 500)
#
# # plot the AMET after removing the seasonal cycling with running mean
# fig3 = plt.figure()
# plt.axhline(y=0, color='g',ls='--')
# plt.plot(index,AMET_white_series,'b--',label='time series')
# plt.plot(index[window-1:],AMET_white_running_mean,'r-',linewidth=2.0,label='running mean')
# plt.title('Running Mean of AMET Anomalies at 60N with a window of %d months (1979-2015)' % (window))
# #plt.legend()
# fig3.set_size_inches(12, 5)
# plt.xlabel("Time")
# plt.xticks(np.linspace(0, 444, 38), index_year)
# plt.xticks(rotation=60)
# plt.ylabel("Meridional Energy Transport (PW)")
# plt.show()
# fig3.savefig(output_path + os.sep + 'AMET_anomaly_60N_running_mean_window_%d_comp.jpg' % (window), dpi = 500)
#
# # plot the AMET anomalies at 60N in summer and winter after removing seasonal cycle
# fig4 = plt.figure()
# plt.axhline(y=0, color='g',ls='--')
# plt.plot(index_summer,AMET_white_series_summer,'r-',label='Summer')
# plt.plot(index_summer,AMET_white_series_winter,'b-',label='Winter')
# plt.title('Atmospheric Meridional Energy Transport Anomaly in Seasons at 60N (1979-2015)')
# plt.legend()
# fig4.set_size_inches(12, 5)
# plt.xlabel("Time")
# plt.xticks(np.linspace(0, 111, 38), index_year)
# plt.xticks(rotation=60)
# plt.ylabel("Meridional Energy Transport (PW)")
# plt.show()
# fig4.savefig(output_path + os.sep + 'AMET_anomaly_season_time_series_1979_2015.jpg', dpi = 500)
#
# print '*******************************************************************'
# print '********************* Fourier transform ***************************'
# print '*******************************************************************'
# # Fast Fourier Transform of AMET
# FFT_AMET = np.fft.fft(AMET_series)
# freq_FFT_AMET = np.fft.fftfreq(len(FFT_AMET),d=1)
# mag_FFT_AMET = abs(FFT_AMET)
# # Plot AMET in Frequency domain
# fig8 = plt.figure()
# plt.plot(freq_FFT_AMET[0:100],mag_FFT_AMET[0:100],'b-',label='JRA55')
# plt.title('Fourier Transform of AMET at 60N (1979-2015)')
# #plt.legend()
# fig8.set_size_inches(12, 5)
# plt.xlabel("Times per month")
# #plt.xticks(np.linspace(0, 456, 39), index_year)
# #plt.xticks(rotation=60)
# plt.ylabel("Power spectrum density (PW^2/month)")
# plt.show()
# fig8.savefig(output_path + os.sep + 'AMET_60N_FFT_1979_2015.jpg', dpi = 500)
#
# # Fast Fourier Transform of AMET anomalies
# FFT_AMET_white = np.fft.fft(AMET_white_series)
# freq_FFT_AMET_white = np.fft.fftfreq(len(FFT_AMET_white),d=1)
# mag_FFT_AMET_white = abs(FFT_AMET_white)
# # Plot the anomaly of AMET in Frequency domain
# fig9 = plt.figure()
# plt.plot(freq_FFT_AMET_white[0:100],mag_FFT_AMET_white[0:100],'b-',label='JRA55')
# plt.title('Fourier Transform of AMET Anomaly at 60N (1979-2015)')
# #plt.legend()
# fig9.set_size_inches(12, 5)
# plt.xlabel("Times per month")
# #plt.xticks(np.linspace(0, 456, 39), index_year)
# #plt.xticks(rotation=60)
# plt.ylabel("Power spectrum density (PW^2/month)")
# plt.show()
# fig9.savefig(output_path + os.sep + 'AMET_anomaly_60N_FFT_1979_2015.jpg', dpi = 500)
#
# # Plot the running mean of AMET anomaly in Frequency domain
# FFT_AMET_white_running_mean = np.fft.fft(AMET_white_running_mean)
# freq_FFT_AMET_white_running_mean = np.fft.fftfreq(len(FFT_AMET_white_running_mean),d=1)
# mag_FFT_AMET_white_running_mean = abs(FFT_AMET_white_running_mean)
# # Plot the running mean of AMET in Frequency domain
# fig10 = plt.figure()
# plt.plot(freq_FFT_AMET_white_running_mean[0:60],mag_FFT_AMET_white_running_mean[0:60],'b-',label='JRA55')
# plt.title('Fourier Transform of Running Mean (%d) of AMET Anomalies at 60N (1979-2015)' % (window))
# #plt.legend()
# fig10.set_size_inches(12, 5)
# plt.xlabel("Times per month")
# #plt.xticks(np.linspace(0, 456, 39), index_year)
# #plt.xticks(rotation=60)
# plt.ylabel("Power spectrum density (PW^2/month)")
# plt.show()
# fig10.savefig(output_path + os.sep + 'AMET_anomaly_60N_FFT_running_mean_%d_1979_2015.jpg' % (window), dpi = 500)

print '*******************************************************************'
print '**************************** trend ********************************'
print '*******************************************************************'
# the calculation of trend are based on target climatolory after removing seasonal cycles
# trend of SLP
# create an array to store the slope coefficient and residual
a = np.zeros((lat_y+1,len(lon)),dtype = float)
b = np.zeros((lat_y+1,len(lon)),dtype = float)
# the least square fit equation is y = ax + b
# np.lstsq solves the equation ax=b, a & b are the input
# thus the input file should be reformed for the function
# we can rewrite the line y = Ap, with A = [x,1] and p = [[a],[b]]
A = np.vstack([index,np.ones(len(index))]).T
# start the least square fitting
for i in np.arange(lat_y+1):
    for j in np.arange(len(lon)):
        # return value: coefficient matrix a and b, where a is the slope
        a[i,j], b[i,j] = np.linalg.lstsq(A,SLP_white[:,i,j])[0]
# visualization through basemap
fig11 = plt.figure()
# setup north polar stereographic basemap
# resolution c(crude) l(low) i(intermidiate) h(high) f(full)
# lon_0 is at 6 o'clock
m = Basemap(projection='npstere',boundinglat=60,round=True,lon_0=0,resolution='l')
# draw coastlines
m.drawcoastlines(linewidth=0.25)
# fill continents, set lake color same as ocean color.
# m.fillcontinents(color='coral',lake_color='aqua')
# draw parallels and meridians
m.drawparallels(np.arange(20,81,10),fontsize = 7,linewidth=0.75)
m.drawmeridians(np.arange(0,360,30),labels=[1,1,1,1],fontsize = 7,linewidth=0.75)
# x,y coordinate - lon, lat
xx, yy = np.meshgrid(lon,lat)
XX, YY = m(xx, yy)
# define color range for the contourf
color = np.linspace(-45,45,19) # for SLP
# !!!!!take care about the coordinate of contourf(Longitude, Latitude, data(Lat,Lon))
#cs = m.contour(XX,YY,a*12,color)
#plt.clabel(cs, fontsize=7, inline=1)
cs = m.contourf(XX,YY,a*12*10,color,cmap='coolwarm')
# add color bar
cbar = m.colorbar(cs,location="bottom",size='4%',pad="8%",format='%d')
cbar.ax.tick_params(labelsize=8)
#cbar.set_ticks(np.arange(-1,1.1,0.2))
#cbar.set_ticklabels(np.arange(-1,1.1,0.2))
cbar.set_label('Pa/Decade',fontsize = 8)
plt.title('Trend of Sea Level Pressure Anomalies (1979-2015)',fontsize = 9, y=1.05)
plt.show()
fig11.savefig(output_path + os.sep + "Trend_JRA55_SLP.jpeg",dpi=500)

# trend of SST
# start the least square fitting
for i in np.arange(lat_y+1):
    for j in np.arange(len(lon)):
        # return value: coefficient matrix a and b, where a is the slope
        a[i,j], b[i,j] = np.linalg.lstsq(A,SST_white[:,i,j])[0]
# visualization through basemap
fig12 = plt.figure()
m = Basemap(projection='npstere',boundinglat=60,round=True,lon_0=0,resolution='l')
# draw coastlines
m.drawcoastlines(linewidth=0.25)
# fill continents, set lake color same as ocean color.
# m.fillcontinents(color='coral',lake_color='aqua')
# draw parallels and meridians
m.drawparallels(np.arange(20,81,10),fontsize = 7,linewidth=0.75)
m.drawmeridians(np.arange(0,360,30),labels=[1,1,1,1],fontsize = 7,linewidth=0.75)
# x,y coordinate - lon, lat
xx, yy = np.meshgrid(lon,lat)
XX, YY = m(xx, yy)
# define color range for the contourf
color = np.linspace(-0.8,0.8,17)
# !!!!!take care about the coordinate of contourf(Longitude, Latitude, data(Lat,Lon))
cs = m.contourf(XX,YY,np.ma.masked_where(mask_SST,a*12*10),color,cmap='coolwarm')
# add color bar
cbar = m.colorbar(cs,location="bottom",size='4%',pad="8%",format='%.1f')
cbar.ax.tick_params(labelsize=8)
cbar.set_label('Celsius/Decade',fontsize = 8)
plt.title('Trend of Sea Surface Temperature Anomalies (1979-2015)',fontsize = 9, y=1.05)
plt.show()
fig12.savefig(output_path + os.sep + "Trend_JRA55_SST.jpeg",dpi=500)

# trend of Sea Ice concentration
# start the least square fitting
for i in np.arange(lat_y+1):
    for j in np.arange(len(lon)):
        # return value: coefficient matrix a and b, where a is the slope
        a[i,j], b[i,j] = np.linalg.lstsq(A,ci_white[:,i,j])[0]
# visualization through basemap
fig13 = plt.figure()
m = Basemap(projection='npstere',boundinglat=60,round=True,lon_0=0,resolution='l')
# draw coastlines
m.drawcoastlines(linewidth=0.25)
# fill continents, set lake color same as ocean color.
# m.fillcontinents(color='coral',lake_color='aqua')
# draw parallels and meridians
m.drawparallels(np.arange(20,81,10),fontsize = 7,linewidth=0.75)
m.drawmeridians(np.arange(0,360,30),labels=[1,1,1,1],fontsize = 7,linewidth=0.75)
# x,y coordinate - lon, lat
xx, yy = np.meshgrid(lon,lat)
XX, YY = m(xx, yy)
# define color range for the contourf
color = np.linspace(-0.15,0.15,21)
# !!!!!take care about the coordinate of contourf(Longitude, Latitude, data(Lat,Lon))
cs = m.contourf(XX,YY,np.ma.masked_where(mask_ci,a*12*10),color,cmap='coolwarm')
# add color bar
cbar = m.colorbar(cs,location="bottom",size='4%',pad="8%",format='%.3f')
cbar.ax.tick_params(labelsize=8)
cbar.set_ticks(np.arange(-0.15,0.20,0.05))
cbar_labels = ['-15%','-10%','-5%','0%','5%','10%','15%']
cbar.ax.set_xticklabels(cbar_labels)
cbar.set_label('Percentage/Decade',fontsize = 8)
plt.title('Trend of the Sea Ice Concentration Anomalies (1979-2015)',fontsize = 9, y=1.05)
plt.show()
fig13.savefig(output_path + os.sep + "Trend_JRA55_Ice.jpeg",dpi=500)

print '*******************************************************************'
print '************************** regression *****************************'
print '*******************************************************************'
# calculate the standard deviation of AMET anomaly
AMET_white_std = np.std(AMET_white_series)
print 'The standard deviation of AMET anomaly is (in peta Watt):'
print AMET_white_std
# all the regression are taken on anomalies of variables
# this is because the seasonal cycles are always too strong

# create an array to store the correlation coefficient
slope = np.zeros((lat_y+1,len(lon)),dtype = float)
r_value = np.zeros((lat_y+1,len(lon)),dtype = float)
p_value = np.zeros((lat_y+1,len(lon)),dtype = float)
#######################################################################################################
# Since running mean will make the points more correlated with each other
# Apparently the T-test based on running mean time series will overestime the level of significance
# However, it is difficult to determine the degress of freedom as the points are actually correlated
# with space and time domain. As a compromise, we use the T-test results from the regression of SIC on
# original time series.
#######################################################################################################
p_value_original = np.zeros((lat_y+1,len(lon)),dtype = float)

for c in np.arange(len(lat_interest_list)):
    # linear regress SLP on AMET (anomalies)
    # plot correlation coefficient
    for i in np.arange(lat_y+1):
        for j in np.arange(len(lon)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope[i,j],_,r_value[i,j],p_value[i,j],_ = stats.linregress(AMET_white_series[:,lat_interest['JRA55'][c]],SLP_white[:,i,j])
    # visualization through basemap
    fig14 = plt.figure()
    # setup north polar stereographic basemap
    # resolution c(crude) l(low) i(intermidiate) h(high) f(full)
    # lon_0 is at 6 o'clock
    m = Basemap(projection='npstere',boundinglat=60,round=True,lon_0=0,resolution='l')
    # draw coastlines
    m.drawcoastlines(linewidth=0.25)
    # fill continents, set lake color same as ocean color.
    # m.fillcontinents(color='coral',lake_color='aqua')
    # draw parallels and meridians
    m.drawparallels(np.arange(60,81,10),fontsize = 7,linewidth=0.75)
    m.drawmeridians(np.arange(0,360,30),labels=[1,1,1,1],fontsize = 7,linewidth=0.75)
    # x,y coordinate - lon, lat
    xx, yy = np.meshgrid(lon,lat[0:lat_y+1])
    XX, YY = m(xx, yy)
    # define color range for the contourf
    color = np.linspace(-0.25,0.25,11) # SLP_white
    # !!!!!take care about the coordinate of contourf(Longitude, Latitude, data(Lat,Lon))
    cs = m.contourf(XX,YY,r_value,color,cmap='coolwarm',extend='both') # SLP_white
    # add color bar
    cbar = m.colorbar(cs,location="bottom",size='4%',pad="8%",format='%.2f')
    cbar.ax.tick_params(labelsize=8)
    cbar.set_label('Correlation Coefficient',fontsize = 8)
    # fancy layout of maps
    # label of contour lines on the map
    #plt.clabel(cs,incline=True, format='%.1f', fontsize=12, colors='k')
    # draw significance stippling on the map
    # locate the indices of p_value matrix where error p<0.05 (99.5% confident)
    i, j = np.where(p_value<=0.05)
    # get the coordinate on the map (lon,lat) and plot scatter dots
    m.scatter(XX[i,j],YY[i,j],2.2,marker='.',color='g',alpha=0.6, edgecolor='none') # alpha bleding factor with map
    plt.title('Regression of SLP Anomaly on AMET Anomaly across %dN' % (lat_interest_list[c]),fontsize = 9, y=1.05)
    plt.show()
    fig14.savefig(output_path + os.sep + 'SLP' + os.sep + "Regression_AMET_SLP_JRA55_white_%dN_correlation_coef.jpeg" % (lat_interest_list[c]),dpi=400)

    # plot regression coefficient
    fig15 = plt.figure()
    # setup north polar stereographic basemap
    m = Basemap(projection='npstere',boundinglat=60,round=True,lon_0=0,resolution='l')
    # draw coastlines
    m.drawcoastlines(linewidth=0.25)
    # draw parallels and meridians
    m.drawparallels(np.arange(60,81,10),fontsize = 7,linewidth=0.75)
    m.drawmeridians(np.arange(0,360,30),labels=[1,1,1,1],fontsize = 7,linewidth=0.75)
    # x,y coordinate - lon, lat
    xx, yy = np.meshgrid(lon,lat[0:lat_y+1])
    XX, YY = m(xx, yy)
    # define color range for the contourf
    color = np.linspace(-0.5,0.5,21) # SLP_white
    # !!!!!take care about the coordinate of contourf(Longitude, Latitude, data(Lat,Lon))
    cs = m.contourf(XX,YY,slope/1000,color,cmap='coolwarm',extend='both') # unit from Pa to kPa
    # add color bar
    cbar = m.colorbar(cs,location="bottom",size='4%',pad="8%",format='%.2f')
    cbar.ax.tick_params(labelsize=8)
    cbar.set_label('Regression Coefficient kPa/PW',fontsize = 8)
    i, j = np.where(p_value<=0.05)
    # get the coordinate on the map (lon,lat) and plot scatter dots
    m.scatter(XX[i,j],YY[i,j],2.2,marker='.',color='g',alpha=0.6, edgecolor='none') # alpha bleding factor with map
    plt.title('Regression of SLP Anomaly on AMET Anomaly across %dN' % (lat_interest_list[c]),fontsize = 9, y=1.05)
    plt.show()
    fig15.savefig(output_path + os.sep + 'SLP' + os.sep + "Regression_AMET_SLP_JRA55_white_%dN_regression_coef.jpeg" % (lat_interest_list[c]),dpi=400)

    # linear regress SST on AMET (anomalies)
    # plot correlation coefficient
    for i in np.arange(lat_y+1):
        for j in np.arange(len(lon)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope[i,j],_,r_value[i,j],p_value[i,j],_ = stats.linregress(AMET_white_series[:,lat_interest['JRA55'][c]],SST_white[:,i,j])
    # visualization through basemap
    fig16 = plt.figure()
    # setup north polar stereographic basemap
    m = Basemap(projection='npstere',boundinglat=60,round=True,lon_0=0,resolution='l')
    # draw coastlines
    m.drawcoastlines(linewidth=0.25)
    # draw parallels and meridians
    m.drawparallels(np.arange(60,81,10),fontsize = 7)
    m.drawmeridians(np.arange(0,360,30),labels=[1,1,1,1],fontsize = 7)
    # x,y coordinate - lon, lat
    xx, yy = np.meshgrid(lon,lat[0:lat_y+1])
    XX, YY = m(xx, yy)
    # define color range for the contourf
    color = np.linspace(-0.2,0.2,11) # SST_white
    # !!!!!take care about the coordinate of contourf(Longitude, Latitude, data(Lat,Lon))
    cs = m.contourf(XX,YY,np.ma.masked_where(mask_SST,r_value),color,cmap='coolwarm',extend='both') # SST_white
    # add color bar
    cbar = m.colorbar(cs,location="bottom",size='4%',pad="8%",format='%.2f')
    cbar.ax.tick_params(labelsize=8)
    #cbar.set_ticks(np.arange(-1,1.1,0.2))
    #cbar.set_ticklabels(np.arange(-1,1.1,0.2))
    cbar.set_label('Correlation Coefficient',fontsize = 8)
    # locate the indices of p_value matrix where p<0.05 (99.5% confident)
    i, j = np.where(p_value<=0.05)
    # get the coordinate on the map (lon,lat) and plot scatter dots
    m.scatter(XX[i,j],YY[i,j],2.2,marker='.',color='g',alpha=0.6, edgecolor='none') # alpha bleding factor with map
    plt.title('Regression of SST Anomaly on AMET Anomaly across %dN ' % (lat_interest_list[c]),fontsize = 9, y=1.05)
    plt.show()
    fig16.savefig(output_path + os.sep + 'SST' + os.sep + "Regression_AMET_SST_JRA55_white_%d_correlation_coef.jpeg" % (lat_interest_list[c]),dpi=400)

    # plot regression coefficient
    fig17 = plt.figure()
    # setup north polar stereographic basemap
    m = Basemap(projection='npstere',boundinglat=60,round=True,lon_0=0,resolution='l')
    # draw coastlines
    m.drawcoastlines(linewidth=0.25)
    # draw parallels and meridians
    m.drawparallels(np.arange(60,81,10),fontsize = 7,linewidth=0.75)
    m.drawmeridians(np.arange(0,360,30),labels=[1,1,1,1],fontsize = 7,linewidth=0.75)
    # x,y coordinate - lon, lat
    xx, yy = np.meshgrid(lon,lat[0:lat_y+1])
    XX, YY = m(xx, yy)
    # define color range for the contourf
    color = np.linspace(-0.6,0.6,13)
    # !!!!!take care about the coordinate of contourf(Longitude, Latitude, data(Lat,Lon))
    cs = m.contourf(XX,YY,np.ma.masked_where(mask_SST,slope),color,cmap='coolwarm',extend='both')
    # add color bar
    cbar = m.colorbar(cs,location="bottom",size='4%',pad="8%",format='%.1f')
    cbar.ax.tick_params(labelsize=8)
    cbar.set_label('Regression Coefficient Celsius/PW',fontsize = 8)
    i, j = np.where(p_value<=0.05)
    # get the coordinate on the map (lon,lat) and plot scatter dots
    m.scatter(XX[i,j],YY[i,j],2.2,marker='.',color='g',alpha=0.6, edgecolor='none') # alpha bleding factor with map
    plt.title('Regression of SST Anomaly on AMET Anomaly across %dN' % (lat_interest_list[c]),fontsize = 9, y=1.05)
    plt.show()
    fig17.savefig(output_path + os.sep + 'SST' + os.sep + "Regression_AMET_SST_JRA55_white_%dN_regression_coef.jpeg" % (lat_interest_list[c]),dpi=400)

    # linear regress Sea Ice Concentration on AMET (anomalies)
    # plot correlation coefficient
    for i in np.arange(lat_y+1):
        for j in np.arange(len(lon)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope[i,j],_,r_value[i,j],p_value[i,j],_ = stats.linregress(AMET_white_series[:,lat_interest['JRA55'][c]],ci_white[:,i,j])
    # visualization through basemap
    fig18 = plt.figure()
    # setup north polar stereographic basemap
    m = Basemap(projection='npstere',boundinglat=60,round=True,lon_0=0,resolution='l')
    # draw coastlines
    m.drawcoastlines(linewidth=0.25)
    # draw parallels and meridians
    m.drawparallels(np.arange(60,81,10),fontsize = 7)
    m.drawmeridians(np.arange(0,360,30),labels=[1,1,1,1],fontsize = 7)
    # x,y coordinate - lon, lat
    xx, yy = np.meshgrid(lon,lat[0:lat_y+1])
    XX, YY = m(xx, yy)
    # define color range for the contourf
    color = np.linspace(-0.25,0.25,11)
    # !!!!!take care about the coordinate of contourf(Longitude, Latitude, data(Lat,Lon))
    cs = m.contourf(XX,YY,np.ma.masked_where(mask_ci[0:lat_y+1,:],r_value),color,cmap='coolwarm',extend='both') # ci_white
    # add color bar
    cbar = m.colorbar(cs,location="bottom",size='4%',pad="8%",format='%.2f')
    cbar.ax.tick_params(labelsize=8)
    cbar.set_label('Correlation Coefficient',fontsize = 8)
    # locate the indices of p_value matrix where p<0.05 (99.5% confident)
    i, j = np.where(p_value<=0.05)
    # get the coordinate on the map (lon,lat) and plot scatter dots
    m.scatter(XX[i,j],YY[i,j],2.2,marker='.',color='g',alpha=0.6, edgecolor='none') # alpha bleding factor with map
    plt.title('Regression of SIC Anomaly on AMET Anomaly across %dN' % (lat_interest_list[c]),fontsize = 9, y=1.05)
    plt.show()
    fig18.savefig(output_path + os.sep + 'SIC' + os.sep + 'LongTermTrend' + os.sep + "Regression_AMET_Ice_JRA55_white_%dN_correlation_coef.jpeg" % (lat_interest_list[c]),dpi=400)

    # plot regression coefficient
    fig19 = plt.figure()
    # setup north polar stereographic basemap
    m = Basemap(projection='npstere',boundinglat=60,round=True,lon_0=0,resolution='l')
    # draw coastlines
    m.drawcoastlines(linewidth=0.25)
    # draw parallels and meridians
    m.drawparallels(np.arange(60,81,10),fontsize = 7,linewidth=0.75)
    m.drawmeridians(np.arange(0,360,30),labels=[1,1,1,1],fontsize = 7,linewidth=0.75)
    # x,y coordinate - lon, lat
    xx, yy = np.meshgrid(lon,lat[0:lat_y+1])
    XX, YY = m(xx, yy)
    # define color range for the contourf
    color = np.linspace(-0.20,0.20,21)
    # !!!!!take care about the coordinate of contourf(Longitude, Latitude, data(Lat,Lon))
    cs = m.contourf(XX,YY,np.ma.masked_where(mask_ci[0:lat_y+1,:],slope),color,cmap='coolwarm',extend='both')
    # add color bar
    cbar = m.colorbar(cs,location="bottom",size='4%',pad="8%",format='%.2f',ticks=[-0.20,-0.10,0,0.10,0.20])
    cbar.ax.tick_params(labelsize=8)
    #cbar.set_ticks(np.arange(0,6))
    cbar_labels = ['-20%','-10%','0%','10%','20%']
    cbar.ax.set_xticklabels(cbar_labels)
    cbar.set_label('Regression Coefficient Percentage/PW',fontsize = 8)
    i, j = np.where(p_value<=0.05)
    # get the coordinate on the map (lon,lat) and plot scatter dots
    m.scatter(XX[i,j],YY[i,j],2.2,marker='.',color='g',alpha=0.6, edgecolor='none') # alpha bleding factor with map
    plt.title('Regression of SIC Anomaly on AMET Anomaly across %dN' % (lat_interest_list[c]),fontsize = 9, y=1.05)
    plt.show()
    fig19.savefig(output_path + os.sep + 'SIC' + os.sep + 'LongTermTrend' + os.sep + "Regression_AMET_Ice_JRA55_white_%dN_regression_coef.jpeg" % (lat_interest_list[c]),dpi=400)

    # linear regress Sea Ice Concentration after detrending on AMET (anomalies)
    # plot correlation coefficient
    for i in np.arange(lat_y+1):
        for j in np.arange(len(lon)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope[i,j],_,r_value[i,j],p_value_original[i,j],_ = stats.linregress(AMET_white_series[:,lat_interest['JRA55'][c]],ci_white_detrend_poly[:,i,j])
            #slope[i,j],_,r_value[i,j],p_value_original[i,j],_ = stats.linregress(AMET_white_series[window_detrend-1:,lat_interest['ERAI'][c]],ci_white_detrend_poly[:,i,j])
    p_value_original[mask_ci==True] = 1.0
    # plot regression coefficient
    fig22 = plt.figure()
    # setup north polar stereographic basemap
    m = Basemap(projection='npstere',boundinglat=60,round=True,lon_0=0,resolution='l')
    # draw coastlines
    m.drawcoastlines(linewidth=0.25)
    # draw parallels and meridians
    m.drawparallels(np.arange(60,81,10),fontsize = 7,linewidth=0.75)
    m.drawmeridians(np.arange(0,360,30),labels=[1,1,1,1],fontsize = 7,linewidth=0.75)
    # x,y coordinate - lon, lat
    xx, yy = np.meshgrid(lon,lat[0:lat_y+1])
    XX, YY = m(xx, yy)
    # define color range for the contourf
    color = np.linspace(-0.20,0.20,21)
    # !!!!!take care about the coordinate of contourf(Longitude, Latitude, data(Lat,Lon))
    cs = m.contourf(XX,YY,np.ma.masked_where(mask_ci[0:lat_y+1,:],slope),color,cmap='coolwarm',extend='both')
    # add color bar
    cbar = m.colorbar(cs,location="bottom",size='4%',pad="8%",format='%.2f',ticks=[-0.20,-0.10,0,0.10,0.20])
    cbar.ax.tick_params(labelsize=8)
    #cbar.set_ticks(np.arange(0,6))
    cbar_labels = ['-20%','-10%','0%','10%','20%']
    cbar.ax.set_xticklabels(cbar_labels)
    cbar.set_label('Regression Coefficient Percentage/PW',fontsize = 8)
    i, j = np.where(p_value_original<=0.05)
    # get the coordinate on the map (lon,lat) and plot scatter dots
    m.scatter(XX[i,j],YY[i,j],2.2,marker='.',color='g',alpha=0.6, edgecolor='none') # alpha bleding factor with map
    plt.title('Regression of Detrend SIC Anomaly on AMET Anomaly across %dN' % (lat_interest_list[c]),fontsize = 9, y=1.05)
    plt.show()
    fig22.savefig(output_path + os.sep + 'SIC' + os.sep + 'Detrend' + os.sep + "Regression_AMET_Ice_ERAI_white_%dN_regression_coef.jpeg" % (lat_interest_list[c]),dpi=400)

    # linear regress Sea Ice Concentration after detrending on AMET (anomalies)
    # plot correlation coefficient
    for i in np.arange(lat_y+1):
        for j in np.arange(len(lon)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope[i,j],_,r_value[i,j],p_value[i,j],_ = stats.linregress(AMET_white_running_mean[:,lat_interest['JRA55'][c]],ci_white_detrend_poly_running_mean[:,i,j])
    # plot regression coefficient
    fig23 = plt.figure()
    # setup north polar stereographic basemap
    m = Basemap(projection='npstere',boundinglat=60,round=True,lon_0=0,resolution='l')
    # draw coastlines
    m.drawcoastlines(linewidth=0.25)
    # draw parallels and meridians
    m.drawparallels(np.arange(60,81,10),fontsize = 7,linewidth=0.75)
    m.drawmeridians(np.arange(0,360,30),labels=[1,1,1,1],fontsize = 7,linewidth=0.75)
    # x,y coordinate - lon, lat
    xx, yy = np.meshgrid(lon,lat[0:lat_y+1])
    XX, YY = m(xx, yy)
    # define color range for the contourf
    color = np.linspace(-0.20,0.20,21)
    # !!!!!take care about the coordinate of contourf(Longitude, Latitude, data(Lat,Lon))
    cs = m.contourf(XX,YY,np.ma.masked_where(mask_ci[0:lat_y+1,:],slope),color,cmap='coolwarm',extend='both')
    # add color bar
    cbar = m.colorbar(cs,location="bottom",size='4%',pad="8%",format='%.2f',ticks=[-0.20,-0.10,0,0.10,0.20])
    cbar.ax.tick_params(labelsize=8)
    #cbar.set_ticks(np.arange(0,6)
    cbar_labels = ['-20%','-10%','0%','10%','20%']
    cbar.ax.set_xticklabels(cbar_labels)
    cbar.set_label('Regression Coefficient Percentage/PW',fontsize = 8)
    i, j = np.where(p_value_original<=0.05)
    # get the coordinate on the map (lon,lat) and plot scatter dots
    m.scatter(XX[i,j],YY[i,j],2.2,marker='.',color='g',alpha=0.6, edgecolor='none') # alpha bleding factor with map
    plt.title('Regression of Detrend SIC Anomaly on AMET Anomaly across %dN with a running mean of %d months' % (lat_interest_list[c],window),fontsize = 9, y=1.05)
    plt.show()
    fig23.savefig(output_path + os.sep + 'SIC' + os.sep + 'Interannual'+ os.sep + "Regression_AMET_Ice_ERAI_white_%dN_running_mean_%dm_regression_coef.jpeg" % (lat_interest_list[c],window),dpi=400)
    #fig23.savefig(output_path + os.sep + 'SIC' + os.sep + 'Annual'+ os.sep + "Regression_AMET_Ice_ERAI_white_%dN_regression_coef.jpeg" % (lat_interest_list[c]),dpi=400)

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
