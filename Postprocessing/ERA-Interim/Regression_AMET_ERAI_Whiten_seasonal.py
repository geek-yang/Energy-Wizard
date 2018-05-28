#!/usr/bin/env python
"""
Copyright Netherlands eScience Center

Function        : Regression of climatological variable on AMET (ERA-Interim) with whitening
Author          : Yang Liu
Date            : 2018.05.28
Last Update     : 2018.05.28
Description     : The code aims to explore the assotiation between climatological
                  variables with atmospheric meridional energy transport (AMET).
                  The statistical method employed here is linear regression. A
                  number of fields (SST, SLP, Sea ice, geopotential, etc.),
                  corresponding to the preexisting natural modes of variability,
                  will be projected on meridional energy transport. This will enhance
                  our understanding of climate change. Notice that the time series
                  of input data will be whitened (the seasonal cycles are removed).
                  This script will split summer and winter and look at them individually.

Return Value    : Map of correlation
Dependencies    : os, time, numpy, scipy, netCDF4, matplotlib, basemap
variables       : Sea Surface Temperature                       SST
                  Sea Level Pressure                            SLP
                  Sea Ice Concentration                         ci
                  Geopotential                                  gz
                  Atmospheric meridional energy transport       AMET
Caveat!!        : The input data of AMET is from 20 deg north to 90 deg north (Northern Hemisphere).
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
datapath_AMET = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ERAI/postprocessing'
# target climatological variables
datapath_y = "/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ERAI/regression"
# specify output path for figures
output_path = '/home/yang/NLeSC/Computation_Modeling/BlueAction/AMET/ERA-Interim'
# the threshold ( index of latitude) of the AMET
# 20N
lat_ERAI_20 = 93
# 30N
lat_ERAI_30 = 80
# 40N
lat_ERAI_40 = 67
# 50N
lat_ERAI_50 = 53
# 60N
lat_ERAI_60 = 40
# 70N
lat_ERAI_70 = 27
# 80N
lat_ERAI_80 = 13
lat_interest = {}
lat_interest_list = [20,30,40,50,60,70,80]
lat_interest['ERAI'] = [lat_ERAI_20,lat_ERAI_30,lat_ERAI_40,lat_ERAI_50,lat_ERAI_60,lat_ERAI_70,lat_ERAI_80]
lat_AMET = 40 # at 60 N
# the range ( index of latitude) of the projection field
lat_y = 40 # 60 N - 90 N
####################################################################################
print '*******************************************************************'
print '*********************** extract variables *************************'
print '*******************************************************************'
dataset_AMET = Dataset(datapath_AMET + os.sep + 'model_daily_075_1979_2016_E_zonal_int.nc')
dataset_y = Dataset(datapath_y + os.sep + 'surface_ERAI_monthly_regress_1979_2016.nc')
for k in dataset_AMET.variables:
    print dataset_AMET.variables['%s' % (k)]

for l in dataset_y.variables:
    print dataset_y.variables['%s' % (l)]

# extract atmospheric meridional energy transport
# dimension (year,month,latitude)
AMET = dataset_AMET.variables['E'][:]/1000 # from Tera Watt to Peta Watt
year = dataset_AMET.variables['year'][:]
lat_AMET = dataset_AMET.variables['latitude'][:]
# extract variables from 20N to 90 N
# sea level pressure
SLP = dataset_y.variables['msl'][:,0:lat_y+1,:]
# sea surface temperature
SST = dataset_y.variables['sst'][:,0:lat_y+1,:]
mask_SST = np.ma.getmaskarray(SST[0,:,:])
# sea ice cover
ci = dataset_y.variables['ci'][:,0:lat_y+1,:]
mask_ci = np.ma.getmaskarray(ci[0,:,:])
np.ma.set_fill_value(ci,0)
# longitude
lon = dataset_y.variables['longitude'][:]
# latitude
lat = dataset_y.variables['latitude'][0:lat_y+1]
# time (number of months)
time = dataset_y.variables['time'][:]

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
SLP_seasonal_mean = np.zeros((12,lat_y+1,len(lon))) # from 20N - 90N
SLP_white = np.zeros(SLP.shape,dtype=float)
for i in month_ind:
    # calculate the monthly mean (seasonal cycling)
    SLP_seasonal_mean[i,:,:] = np.mean(SLP[i:-1:12,:,:],axis=0)
    # remove seasonal mean
    SLP_white[i:-1:12,:,:] = SLP[i:-1:12,:,:] - SLP_seasonal_mean[i,:,:]

# remove climatology for Sea Surface Temperature
SST_seasonal_mean = np.zeros((12,lat_y+1,len(lon))) # from 20N - 90N
SST_white = np.zeros(SST.shape,dtype=float)
for i in month_ind:
    # calculate the monthly mean (seasonal cycling)
    SST_seasonal_mean[i,:,:] = np.mean(SST[i:-1:12,:,:],axis=0)
    # remove seasonal mean
    SST_white[i:-1:12,:,:] = SST[i:-1:12,:,:] - SST_seasonal_mean[i,:,:]

# remove climatology for Sea Ice Concentration
ci_seasonal_mean = np.zeros((12,lat_y+1,len(lon))) # from 20N - 90N
ci_white = np.zeros(ci.shape)
for i in month_ind:
    # calculate the monthly mean (seasonal cycling)
    ci_seasonal_mean[i,:,:] = np.mean(ci[i:-1:12,:,:].filled(),axis=0)
    # remove seasonal mean
    ci_white[i:-1:12,:,:] = ci[i:-1:12,:,:].filled() - ci_seasonal_mean[i,:,:]

# remove the seasonal cycling of AMET at 60N
# dimension of AMET[year,month]
AMET_seansonal_cycle = np.mean(AMET,axis=0)
AMET_white = np.zeros(AMET.shape,dtype=float)
for i in month_ind:
    AMET_white[:,i,:] = AMET[:,i,:] - AMET_seansonal_cycle[i,:]
print '*******************************************************************'
print '***************************  Detrend  *****************************'
print '*******************************************************************'
####################################################
######         detrend - running mean         ######
####################################################

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
print '***********************  summer / winter  *************************'
print '*******************************************************************'
# Summer and winter only
# summer refers to June(5), July(6), August(7)
# winter refers to Dec(11), Jan(0), Feb(1)
#AMET
AMET_white_series_summer = np.zeros((len(year)*len(month_ind)/4,len(lat_AMET)),dtype=float)
AMET_white_series_winter = np.zeros((len(year)*len(month_ind)/4,len(lat_AMET)),dtype=float)

AMET_white_series_summer[0::3,:] = AMET_white_series[5::12,:] #June
AMET_white_series_summer[1::3,:] = AMET_white_series[6::12,:] #July
AMET_white_series_summer[2::3,:] = AMET_white_series[7::12,:] #August
AMET_white_series_winter[2::3,:] = AMET_white_series[11::12,:] # December
AMET_white_series_winter[0::3,:] = AMET_white_series[0::12,:] # Jan
AMET_white_series_winter[1::3,:] = AMET_white_series[1::12,:] # Feb

# SIC after detrending
ci_white_detrend_summer = np.zeros((len(year)*len(month_ind)/4,lat_y+1,len(lon)),dtype=float)
ci_white_detrend_winter = np.zeros((len(year)*len(month_ind)/4,lat_y+1,len(lon)),dtype=float)

ci_white_detrend_summer[0::3,:,:] = ci_white_detrend_poly[5::12,:,:] #June
ci_white_detrend_summer[1::3,:,:] = ci_white_detrend_poly[6::12,:,:] #June
ci_white_detrend_summer[2::3,:,:] = ci_white_detrend_poly[7::12,:,:] #June
ci_white_detrend_winter[2::3,:,:] = ci_white_detrend_poly[11::12,:,:] #June
ci_white_detrend_winter[0::3,:,:] = ci_white_detrend_poly[0::12,:,:] #June
ci_white_detrend_winter[1::3,:,:] = ci_white_detrend_poly[1::12,:,:] #June
print '*******************************************************************'
print '********************** Running mean/sum ***************************'
print '*******************************************************************'
# running mean is calculated on time series
# define the running window for the running mean
#window = 3 # in month = 1 year
#window = 9 # in month = 3 year
window = 15 # in month = 5 year
# calculate the running mean of AMET summer/winter
AMET_white_series_summer_running_mean = np.zeros((len(year)*len(month_ind)/4-window+1,len(lat_AMET)),dtype=float)
for i in np.arange(len(year)*len(month_ind)/4-window+1):
    AMET_white_series_summer_running_mean[i,:] = np.mean(AMET_white_series_summer[i:i+window,:],0)

AMET_white_series_winter_running_mean = np.zeros((len(year)*len(month_ind)/4-window+1,len(lat_AMET)),dtype=float)
for i in np.arange(len(year)*len(month_ind)/4-window+1):
    AMET_white_series_winter_running_mean[i,:] = np.mean(AMET_white_series_winter[i:i+window,:],0)

ci_white_detrend_summer_running_mean = np.zeros((len(year)*len(month_ind)/4-window+1,lat_y+1,len(lon)),dtype=float)
for i in np.arange(len(year)*len(month_ind)/4-window+1):
    ci_white_detrend_summer_running_mean[i,:] = np.mean(ci_white_detrend_summer[i:i+window,:],0)

ci_white_detrend_winter_running_mean = np.zeros((len(year)*len(month_ind)/4-window+1,lat_y+1,len(lon)),dtype=float)
for i in np.arange(len(year)*len(month_ind)/4-window+1):
    ci_white_detrend_winter_running_mean[i,:] = np.mean(ci_white_detrend_winter[i:i+window,:],0)
print '*******************************************************************'
print '*************************** time series ***************************'
print '*******************************************************************'
# index and namelist of years for time series
#index = np.arange(1,457,1)
index_year = np.arange(1979,2017,1)
index_season = np.arange(1,115,1) # 38 years * 12 months / 4 seasons

# plot the AMET anomalies in summer and winter after removing seasonal cycle
for c in np.arange(len(lat_interest_list)):
    fig1 = plt.figure()
    plt.axhline(y=0, color='g',ls='--')
    plt.plot(index_season,AMET_white_series_summer[:,lat_interest['ERAI'][c]],'r-',label='Summer')
    plt.plot(index_season,AMET_white_series_winter[:,lat_interest['ERAI'][c]],'b-',label='Winter')
    plt.title('Atmospheric Meridional Energy Transport Anomaly in summer/winter at {}N (1979-2016)'.format(lat_interest_list[c]))
    plt.legend()
    fig1.set_size_inches(12, 5)
    plt.xlabel("Time")
    plt.xticks(np.linspace(0, 114, 39), index_year)
    plt.xticks(rotation=60)
    plt.ylabel("Meridional Energy Transport (PW)")
    plt.show()
    fig1.savefig(output_path + os.sep + 'AMET_season' + os.sep + 'AMET_anomaly_{}N_season_time_series_1979_2016.jpg'.format(lat_interest_list[c]), dpi = 400)

    fig2 = plt.figure()
    plt.axhline(y=0, color='g',ls='--')
    plt.plot(index_season[window-1:],AMET_white_series_summer_running_mean[:,lat_interest['ERAI'][c]],'r-',label='Summer')
    plt.plot(index_season[window-1:],AMET_white_series_winter_running_mean[:,lat_interest['ERAI'][c]],'b-',label='Winter')
    plt.title('Atmospheric Meridional Energy Transport Anomaly in summer/winter at {}N with a running mean of {} years (1979-2016)'.format(lat_interest_list[c],window/3))
    plt.legend()
    fig2.set_size_inches(12, 5)
    plt.xlabel("Time")
    plt.xticks(np.linspace(0, 114, 39), index_year)
    plt.xticks(rotation=60)
    plt.ylabel("Meridional Energy Transport (PW)")
    plt.show()
    fig2.savefig(output_path + os.sep + 'AMET_season' + os.sep + 'AMET_anomaly_{}N_season_time_series_lowpass_{}y_1979_2016.jpg'.format(lat_interest_list[c],window/3), dpi = 400)

# plot sea ice in both winter and summer
# plot the AMET anomalies at 60N in summer and winter after removing seasonal cycle
fig2 = plt.figure()
plt.axhline(y=0, color='g',ls='--')
plt.plot(index_season,np.mean(np.mean(ci_white_detrend_summer,2),1),'r-',label='Summer')
plt.plot(index_season,np.mean(np.mean(ci_white_detrend_winter,2),1),'b-',label='Winter')
plt.title('Detrended SIC Anomaly in summer/winter (1979-2016)')
plt.legend()
fig2.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(0, 114, 39), index_year)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig2.savefig(output_path + os.sep + 'SIC' + os.sep + 'Season' + os.sep + 'SIC_anomaly_detrend_season.jpg', dpi = 400)

fig3 = plt.figure()
plt.axhline(y=0, color='g',ls='--')
plt.plot(index_season[window-1:],np.mean(np.mean(ci_white_detrend_summer_running_mean,2),1),'r-',label='Summer')
plt.plot(index_season[window-1:],np.mean(np.mean(ci_white_detrend_winter_running_mean,2),1),'b-',label='Winter')
plt.title('Detrended SIC Anomaly in summer/winter with a running mean of {} years (1979-2016)'.format(window/3))
plt.legend()
fig3.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(0, 114, 39), index_year)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig3.savefig(output_path + os.sep + 'SIC' + os.sep + 'Season' + os.sep + 'SIC_anomaly_detrend_season_lowpass_{}y.jpg'.format(window/3), dpi = 400)

print '*******************************************************************'
print '**************************** trend ********************************'
print '*******************************************************************'
# the calculation of trend are based on target climatolory after removing seasonal cycles
# trend of SIC
# create an array to store the slope coefficient and residual
# a = np.zeros((len(lat),len(lon)),dtype = float)
# b = np.zeros((len(lat),len(lon)),dtype = float)
# # trend of Sea Ice concentration after detrending with polynomial fit
# A = np.vstack([index,np.ones(len(index))]).T
# # start the least square fitting
# for i in np.arange(len(lat)):
#     for j in np.arange(len(lon)):
#         # return value: coefficient matrix a and b, where a is the slope
#         a[i,j], b[i,j] = np.linalg.lstsq(A,ci_white_detrend_poly[:,i,j])[0]
# # visualization through basemap
# fig15 = plt.figure()
# m = Basemap(projection='npstere',boundinglat=60,round=True,lon_0=0,resolution='l')
# # draw coastlines
# m.drawcoastlines(linewidth=0.25)
# # fill continents, set lake color same as ocean color.
# # m.fillcontinents(color='coral',lake_color='aqua')
# # draw parallels and meridians
# m.drawparallels(np.arange(20,81,10),fontsize = 7,linewidth=0.75)
# m.drawmeridians(np.arange(0,360,30),labels=[1,1,1,1],fontsize = 7,linewidth=0.75)
# # x,y coordinate - lon, lat
# xx, yy = np.meshgrid(lon,lat)
# XX, YY = m(xx, yy)
# # define color range for the contourf
# color = np.linspace(-0.15,0.15,21)
# # !!!!!take care about the coordinate of contourf(Longitude, Latitude, data(Lat,Lon))
# cs = m.contourf(XX,YY,np.ma.masked_where(mask_ci,a*12*10),color,cmap='coolwarm')
# # add color bar
# cbar = m.colorbar(cs,location="bottom",size='4%',pad="8%",format='%.3f')
# cbar.ax.tick_params(labelsize=8)
# cbar.set_ticks(np.arange(-0.15,0.20,0.05))
# cbar_labels = ['-15%','-10%','-5%','0%','5%','10%','15%']
# cbar.ax.set_xticklabels(cbar_labels)
# cbar.set_label('Percentage/Decade',fontsize = 8)
# plt.title('Trend of the Sea Ice Concentration Anomalies after Detrending (1979-2016)',fontsize = 9, y=1.05)
# plt.show()
# fig15.savefig(output_path + os.sep + "Trend_ERAI_Detrend_polyfit_Ice.jpeg",dpi=400)
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
    # linear regress Sea Ice Concentration on AMET (anomalies) in different seasons
    # plot correlation coefficient
    for i in np.arange(lat_y+1):
        for j in np.arange(len(lon)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope[i,j],_,r_value[i,j],p_value_original[i,j],_ = stats.linregress(AMET_white_series_summer[:,lat_interest['ERAI'][c]],ci_white_detrend_summer[:,i,j])
    p_value_original[mask_ci==True] = 1.0
    # plot regression coefficient
    fig5 = plt.figure()
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
    i, j = np.where(p_value_original<=0.1)
    # get the coordinate on the map (lon,lat) and plot scatter dots
    m.scatter(XX[i,j],YY[i,j],2.2,marker='.',color='g',alpha=0.6, edgecolor='none') # alpha bleding factor with map
    plt.title('Regression of SIC Anomaly on AMET Anomaly in summer across %dN' % (lat_interest_list[c]),fontsize = 9, y=1.05)
    plt.show()
    fig5.savefig(output_path + os.sep + 'SIC' + os.sep + 'Season' + os.sep + 'Detrend' + os.sep + "Regression_AMET_Ice_ERAI_summer_white_%dN_regression_coef.jpeg" % (lat_interest_list[c]),dpi=400)

    for i in np.arange(lat_y+1):
        for j in np.arange(len(lon)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope[i,j],_,r_value[i,j],p_value[i,j],_ = stats.linregress(AMET_white_series_summer_running_mean[:,lat_interest['ERAI'][c]],ci_white_detrend_summer_running_mean[:,i,j])
    # plot regression coefficient
    fig6 = plt.figure()
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
    i, j = np.where(p_value_original<=0.1)
    # get the coordinate on the map (lon,lat) and plot scatter dots
    m.scatter(XX[i,j],YY[i,j],2.2,marker='.',color='g',alpha=0.6, edgecolor='none') # alpha bleding factor with map
    plt.title('Regression of Detrend SIC Anomaly on AMET Anomaly in summer across %dN with a running mean of %d years' % (lat_interest_list[c],window/3),fontsize = 9, y=1.05)
    plt.show()
    fig6.savefig(output_path + os.sep + 'SIC' + os.sep + 'Season' + os.sep + 'Interannual'+ os.sep + "Regression_AMET_Ice_ERAI_summer_white_%dN_running_mean_%dy_regression_coef.jpeg" % (lat_interest_list[c],window/3),dpi=400)
    #fig6.savefig(output_path + os.sep + 'SIC' + os.sep + 'Season' + os.sep + 'Annual'+ os.sep + "Regression_AMET_Ice_ERAI_summer_white_%dN_running_mean_%dy_regression_coef.jpeg" % (lat_interest_list[c],window/3),dpi=400)

    # plot correlation coefficient
    for i in np.arange(lat_y+1):
        for j in np.arange(len(lon)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope[i,j],_,r_value[i,j],p_value_original[i,j],_ = stats.linregress(AMET_white_series_winter[:,lat_interest['ERAI'][c]],ci_white_detrend_winter[:,i,j])
    p_value_original[mask_ci==True] = 1.0
    # plot regression coefficient
    fig7 = plt.figure()
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
    i, j = np.where(p_value_original<=0.1)
    # get the coordinate on the map (lon,lat) and plot scatter dots
    m.scatter(XX[i,j],YY[i,j],2.2,marker='.',color='g',alpha=0.6, edgecolor='none') # alpha bleding factor with map
    plt.title('Regression of SIC Anomaly on AMET Anomaly in winter across %dN' % (lat_interest_list[c]),fontsize = 9, y=1.05)
    plt.show()
    fig7.savefig(output_path + os.sep + 'SIC' + os.sep + 'Season' + os.sep + 'Detrend' + os.sep + "Regression_AMET_Ice_ERAI_winter_white_%dN_regression_coef.jpeg" % (lat_interest_list[c]),dpi=400)

    for i in np.arange(lat_y+1):
        for j in np.arange(len(lon)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope[i,j],_,r_value[i,j],p_value[i,j],_ = stats.linregress(AMET_white_series_winter_running_mean[:,lat_interest['ERAI'][c]],ci_white_detrend_winter_running_mean[:,i,j])
    # plot regression coefficient
    fig8 = plt.figure()
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
    i, j = np.where(p_value_original<=0.1)
    # get the coordinate on the map (lon,lat) and plot scatter dots
    m.scatter(XX[i,j],YY[i,j],2.2,marker='.',color='g',alpha=0.6, edgecolor='none') # alpha bleding factor with map
    plt.title('Regression of Detrend SIC Anomaly on AMET Anomaly in winter across %dN with a running mean of %d years' % (lat_interest_list[c],window/3),fontsize = 9, y=1.05)
    plt.show()
    fig8.savefig(output_path + os.sep + 'SIC' + os.sep + 'Season' + os.sep + 'Interannual'+ os.sep + "Regression_AMET_Ice_ERAI_winter_white_%dN_running_mean_%dy_regression_coef.jpeg" % (lat_interest_list[c],window/3),dpi=400)
    #fig8.savefig(output_path + os.sep + 'SIC' + os.sep + 'Season' + os.sep + 'Annual'+ os.sep + "Regression_AMET_Ice_ERAI_winter_white_%dN_running_mean_%dy_regression_coef.jpeg" % (lat_interest_list[c],window/3),dpi=400)

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
