#!/usr/bin/env python
"""
Copyright Netherlands eScience Center

Function        : Regression of AMET on eddy (ERA-Interim)
Author          : Yang Liu
Date            : 2018.05.31
Last Update     : 2018.06.04
Description     : The code aims to explore the assotiation between standing &
                  transient eddies with atmospheric meridional energy transport (AMET).
                  The statistical method employed here is linear regression. Notice
                  that the time series of input data will be whitened (the seasonal
                  cycles are removed).

                  Regarding the detrending, as we want to remove linear trend as
                  much as we can and keep the oscillation as much as we could, we
                  only use the polynomial fitting upto 3rd order.

Return Value    : Map of correlation
Dependencies    : os, time, numpy, scipy, netCDF4, matplotlib, basemap
variables       : Transient Eddy                                v'v'
                  Transient Mean Eddy                           [v]'[v]'
                  Standing Eddy                                 v*v*
                  Stationary Mean Eddy                          [v]*[v]*
                  Steady Mean Meridional Circulation            [v][v]
                  Overall Transport                             vv
                  Atmospheric meridional energy transport       AMET
Caveat!!        : The input data of AMET is from 30 deg north to 90 deg north (Northern Hemisphere).
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
datapath_eddy = "/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ERAI/eddy"
# specify output path for figures
output_path = '/home/yang/NLeSC/Computation_Modeling/BlueAction/AMET/ERA-Interim/Eddy'
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
####################################################################################
print '*******************************************************************'
print '*********************** extract variables *************************'
print '*******************************************************************'
dataset_AMET = Dataset(datapath_AMET + os.sep + 'model_daily_075_1979_2016_E_zonal_int.nc')
dataset_eddy = Dataset(datapath_eddy + os.sep + 'model_daily_075_v2_eddies_point.nc')
for k in dataset_AMET.variables:
    print dataset_AMET.variables['%s' % (k)]

for l in dataset_eddy.variables:
    print dataset_eddy.variables['%s' % (l)]

# extract atmospheric meridional energy transport
# dimension (year,month,latitude)
AMET = dataset_AMET.variables['E'][:]/1000 # from Tera Watt to Peta Watt
year = dataset_AMET.variables['year'][:]
lat_AMET = dataset_AMET.variables['latitude'][:]

# extract eddies
v2_transient_zonal = dataset_eddy.variables['v2_transient_zonal'][:]
v2_standing_zonal = dataset_eddy.variables['v2_standing_zonal'][:]
v2_overall_zonal = dataset_eddy.variables['v2_overall_zonal'][:]
v2_mean_zonal = dataset_eddy.variables['v2_steady_mean'][:]
levels = dataset_eddy.variables['level'][:]

v2_transient_point = dataset_eddy.variables['v2_transient'][:]
v2_standing_point = dataset_eddy.variables['v2_standing'][:]
v2_overall_point = dataset_eddy.variables['v2_overall'][:]

lat = dataset_eddy.variables['latitude'][:]
lon = dataset_eddy.variables['longitude'][:]

print '*******************************************************************'
print '*************************** whitening *****************************'
print '*******************************************************************'
# remove the seasonal cycling of target climatology for regression
# These climitology data comes from ERA-Interim surface level
# zonal mean
month_ind = np.arange(12)
AMET_seansonal_cycle = np.mean(AMET,axis=0)
AMET_white = np.zeros(AMET.shape,dtype=float)
for i in month_ind:
    AMET_white[:,i,:] = AMET[:,i,:] - AMET_seansonal_cycle[i,:]

v2_transient_zonal_seansonal_cycle = np.mean(v2_transient_zonal,axis=0)
v2_transient_zonal_white = np.zeros(v2_transient_zonal.shape,dtype=float)
for i in month_ind:
    v2_transient_zonal_white[:,i,:,:] = v2_transient_zonal[:,i,:,:] - v2_transient_zonal_seansonal_cycle[i,:,:]

v2_standing_zonal_seansonal_cycle = np.mean(v2_standing_zonal,axis=0)
v2_standing_zonal_white = np.zeros(v2_standing_zonal.shape,dtype=float)
for i in month_ind:
    v2_standing_zonal_white[:,i,:,:] = v2_standing_zonal[:,i,:,:] - v2_standing_zonal_seansonal_cycle[i,:,:]

v2_overall_zonal_seansonal_cycle = np.mean(v2_overall_zonal,axis=0)
v2_overall_zonal_white = np.zeros(v2_overall_zonal.shape,dtype=float)
for i in month_ind:
    v2_overall_zonal_white[:,i,:,:] = v2_overall_zonal[:,i,:,:] - v2_overall_zonal_seansonal_cycle[i,:,:]

# on grid point
v2_transient_point_seansonal_cycle = np.mean(v2_transient_point,axis=0)
v2_transient_point_white = np.zeros(v2_transient_point.shape,dtype=float)
for i in month_ind:
    v2_transient_point_white[:,i,:,:,:] = v2_transient_point[:,i,:,:,:] - v2_transient_point_seansonal_cycle[i,:,:,:]

v2_standing_point_seansonal_cycle = np.mean(v2_standing_point,axis=0)
v2_standing_point_white = np.zeros(v2_standing_point.shape,dtype=float)
for i in month_ind:
    v2_standing_point_white[:,i,:,:,:] = v2_standing_point[:,i,:,:,:] - v2_standing_point_seansonal_cycle[i,:,:,:]

v2_overall_point_seansonal_cycle = np.mean(v2_overall_point,axis=0)
v2_overall_point_white = np.zeros(v2_overall_point.shape,dtype=float)
for i in month_ind:
    v2_overall_point_white[:,i,:,:,:] = v2_overall_point[:,i,:,:,:] - v2_overall_point_seansonal_cycle[i,:,:,:]

print '*******************************************************************'
print '*********************** prepare variables *************************'
print '*******************************************************************'
# take the time series of E
# zonal mean
AMET_series = AMET.reshape(len(year)*len(month_ind),len(lat_AMET))
AMET_white_series = AMET_white.reshape(len(year)*len(month_ind),len(lat_AMET))
v2_transient_zonal_series = v2_transient_zonal.reshape(len(year)*len(month_ind),len(levels),len(lat_AMET))
v2_standing_zonal_series = v2_standing_zonal.reshape(len(year)*len(month_ind),len(levels),len(lat_AMET))
v2_overall_zonal_series = v2_overall_zonal.reshape(len(year)*len(month_ind),len(levels),len(lat_AMET))
v2_transient_zonal_white_series = v2_transient_zonal_white.reshape(len(year)*len(month_ind),len(levels),len(lat_AMET))
v2_standing_zonal_white_series = v2_standing_zonal_white.reshape(len(year)*len(month_ind),len(levels),len(lat_AMET))
v2_overall_zonal_white_series = v2_overall_zonal_white.reshape(len(year)*len(month_ind),len(levels),len(lat_AMET))
# point-wise
v2_transient_point_white_series = v2_transient_point_white.reshape(len(year)*len(month_ind),len(levels),len(lat),len(lon))
v2_standing_point_white_series = v2_standing_point_white.reshape(len(year)*len(month_ind),len(levels),len(lat),len(lon))
v2_overall_point_white_series = v2_overall_point_white.reshape(len(year)*len(month_ind),len(levels),len(lat),len(lon))
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

# zonal mean transient eddy anomalies
v2_transient_zonal_white_series_summer = np.zeros((len(year)*len(month_ind)/4,len(levels),len(lat)),dtype=float)
v2_transient_zonal_white_series_winter = np.zeros((len(year)*len(month_ind)/4,len(levels),len(lat)),dtype=float)

v2_transient_zonal_white_series_summer[0::3,:,:] = v2_transient_zonal_white_series[5::12,:,:]  # June
v2_transient_zonal_white_series_summer[1::3,:,:] = v2_transient_zonal_white_series[6::12,:,:]  # July
v2_transient_zonal_white_series_summer[2::3,:,:] = v2_transient_zonal_white_series[7::12,:,:]  # August
v2_transient_zonal_white_series_winter[2::3,:,:] = v2_transient_zonal_white_series[11::12,:,:] # December
v2_transient_zonal_white_series_winter[0::3,:,:] = v2_transient_zonal_white_series[0::12,:,:]  # January
v2_transient_zonal_white_series_winter[1::3,:,:] = v2_transient_zonal_white_series[1::12,:,:]  # February

# zonal mean standing eddy anomalies
v2_standing_zonal_white_series_summer = np.zeros((len(year)*len(month_ind)/4,len(levels),len(lat)),dtype=float)
v2_standing_zonal_white_series_winter = np.zeros((len(year)*len(month_ind)/4,len(levels),len(lat)),dtype=float)

v2_standing_zonal_white_series_summer[0::3,:,:] = v2_standing_zonal_white_series[5::12,:,:]  # June
v2_standing_zonal_white_series_summer[1::3,:,:] = v2_standing_zonal_white_series[6::12,:,:]  # July
v2_standing_zonal_white_series_summer[2::3,:,:] = v2_standing_zonal_white_series[7::12,:,:]  # August
v2_standing_zonal_white_series_winter[2::3,:,:] = v2_standing_zonal_white_series[11::12,:,:] # December
v2_standing_zonal_white_series_winter[0::3,:,:] = v2_standing_zonal_white_series[0::12,:,:]  # January
v2_standing_zonal_white_series_winter[1::3,:,:] = v2_standing_zonal_white_series[1::12,:,:]  # February

# transient eddy anomalies
v2_transient_point_white_series_summer = np.zeros((len(year)*len(month_ind)/4,len(levels),len(lat),len(lon)),dtype=float)
v2_transient_point_white_series_winter = np.zeros((len(year)*len(month_ind)/4,len(levels),len(lat),len(lon)),dtype=float)

v2_transient_point_white_series_summer[0::3,:,:,:] = v2_transient_point_white_series[5::12,:,:,:] #June
v2_transient_point_white_series_summer[1::3,:,:,:] = v2_transient_point_white_series[6::12,:,:,:] #June
v2_transient_point_white_series_summer[2::3,:,:,:] = v2_transient_point_white_series[7::12,:,:,:] #June
v2_transient_point_white_series_winter[2::3,:,:,:] = v2_transient_point_white_series[11::12,:,:,:]#June
v2_transient_point_white_series_winter[0::3,:,:,:] = v2_transient_point_white_series[0::12,:,:,:] #June
v2_transient_point_white_series_winter[1::3,:,:,:] = v2_transient_point_white_series[1::12,:,:,:] #June

# standing eddy anomalies
v2_standing_point_white_series_summer = np.zeros((len(year)*len(month_ind)/4,len(levels),len(lat),len(lon)),dtype=float)
v2_standing_point_white_series_winter = np.zeros((len(year)*len(month_ind)/4,len(levels),len(lat),len(lon)),dtype=float)

v2_standing_point_white_series_summer[0::3,:,:,:] = v2_standing_point_white_series[5::12,:,:,:] #June
v2_standing_point_white_series_summer[1::3,:,:,:] = v2_standing_point_white_series[6::12,:,:,:] #June
v2_standing_point_white_series_summer[2::3,:,:,:] = v2_standing_point_white_series[7::12,:,:,:] #June
v2_standing_point_white_series_winter[2::3,:,:,:] = v2_standing_point_white_series[11::12,:,:,:]#June
v2_standing_point_white_series_winter[0::3,:,:,:] = v2_standing_point_white_series[0::12,:,:,:] #June
v2_standing_point_white_series_winter[1::3,:,:,:] = v2_standing_point_white_series[1::12,:,:,:] #June
print '*******************************************************************'
print '*************************** time series ***************************'
print '*******************************************************************'
# index and namelist of years for time series and running mean time series
index = np.arange(1,457,1)
index_year = np.arange(1979,2017,1)

index_season = np.arange(1,115,1)

for c in np.arange(len(lat_interest_list)):
    for l in np.arange(len(levels)):
        fig1 = plt.figure()
        plt.axhline(y=0, color='k',ls='-')
        plt.plot(index,v2_overall_zonal_series[:,l,lat_interest['ERAI'][c]],'g-',linewidth = 2.0,label='Overall')
        plt.plot(index,v2_transient_zonal_series[:,l,lat_interest['ERAI'][c]],'b--',linewidth = 2.0,label='Transient')
        plt.plot(index,v2_standing_zonal_series[:,l,lat_interest['ERAI'][c]],'r-',linewidth = 2.0,label='Standing')
        plt.title('Meridional Transport of Momentum by eddies at {}N on {}hPa(1979-2016)'.format(lat_interest_list[c],levels[l]))
        plt.legend()
        fig1.set_size_inches(12, 5)
        plt.xlabel("Time")
        plt.xticks(np.linspace(0, 456, 39), index_year)
        plt.xticks(rotation=60)
        plt.ylabel("v2 (m2/s2)")
        plt.show()
        fig1.savefig(os.path.join(output_path,'Momentum_v2','TimeSeries','Eddies_{}N_{}hPa_series.jpg'.format(lat_interest_list[c],levels[l])), dpi = 400)
        plt.close(fig1)

for c in np.arange(len(lat_interest_list)):
    for l in np.arange(len(levels)):
        fig2 = plt.figure()
        plt.axhline(y=0, color='k',ls='-')
        plt.plot(index,v2_overall_zonal_white_series[:,l,lat_interest['ERAI'][c]],'g-',linewidth = 2.0,label='Overall')
        plt.plot(index,v2_transient_zonal_white_series[:,l,lat_interest['ERAI'][c]],'b--',linewidth = 2.0,label='Transient')
        plt.plot(index,v2_standing_zonal_white_series[:,l,lat_interest['ERAI'][c]],'r-',linewidth = 2.0,label='Standing')
        plt.title('Meridional Transport of Momentum by eddies anomalies at {}N on {}hPa(1979-2016)'.format(lat_interest_list[c],levels[l]))
        plt.legend()
        fig2.set_size_inches(12, 5)
        plt.xlabel("Time")
        plt.xticks(np.linspace(0, 456, 39), index_year)
        plt.xticks(rotation=60)
        plt.ylabel("v2 (m2/s2)")
        plt.show()
        fig2.savefig(os.path.join(output_path,'Momentum_v2','Whiten','Eddies_{}N_{}hPa_series.jpg'.format(lat_interest_list[c],levels[l])), dpi = 400)
        plt.close(fig2)

for c in np.arange(len(lat_interest_list)):
    for l in np.arange(len(levels)):
        fig3 = plt.figure()
        plt.axhline(y=0, color='k',ls='-')
        plt.plot(index_season,v2_transient_zonal_white_series_winter[:,l,lat_interest['ERAI'][c]],'b-',linewidth = 2.0,label='Transient Winter')
        plt.plot(index_season,v2_standing_zonal_white_series_winter[:,l,lat_interest['ERAI'][c]],'r-',linewidth = 2.0,label='Standing Winter')
        plt.plot(index_season,v2_transient_zonal_white_series_summer[:,l,lat_interest['ERAI'][c]],'c--',linewidth = 1.2,label='Transient Summer')
        plt.plot(index_season,v2_standing_zonal_white_series_summer[:,l,lat_interest['ERAI'][c]],'m--',linewidth = 1.2,label='Standing Summer')
        plt.title('Meridional Transport of Momentum by eddies anomalies at {}N on {}hPa(1979-2016)'.format(lat_interest_list[c],levels[l]))
        plt.legend()
        fig3.set_size_inches(12, 5)
        plt.xlabel("Time")
        plt.xticks(np.linspace(0, 114, 39), index_year)
        plt.xticks(rotation=60)
        plt.ylabel("v2 (m2/s2)")
        plt.show()
        fig3.savefig(os.path.join(output_path,'Momentum_v2','Whiten','seasonal','Eddies_{}N_{}hPa_series_seasonal.jpg'.format(lat_interest_list[c],levels[l])), dpi = 400)
        plt.close(fig3)

print '*******************************************************************'
print '**************************  x-y plot  *****************************'
print '*******************************************************************'
for l in np.arange(len(levels)):
    fig4 = plt.figure()
    plt.axhline(y=0, color='k',ls='-')
    plt.plot(lat_AMET,np.mean(np.mean(v2_overall_zonal[:,:,l,:],0),0),'g-',linewidth = 2.0,label='Overall')
    plt.plot(lat_AMET,np.mean(np.mean(v2_transient_zonal[:,:,l,:],0),0),'b--',linewidth = 2.0,label='Transient')
    plt.plot(lat_AMET,np.mean(np.mean(v2_standing_zonal[:,:,l,:],0),0),'r-',linewidth = 2.0,label='Standing')
    plt.plot(lat_AMET,np.mean(v2_mean_zonal[:,l,:],0),'y-',linewidth = 2.0,label='Steady Mean')
    plt.title('Meridional Transport of Momentum by eddies on {}hPa(1979-2016)'.format(levels[l]))
    plt.legend()
    plt.xlabel("Latitude")
    plt.ylabel("v2 (m2/s2)")
    plt.show()
    fig4.savefig(os.path.join(output_path,'Momentum_v2','Eddies_{}hPa_mean.jpg'.format(levels[l])), dpi = 400)
    plt.close(fig4)

print '*******************************************************************'
print '************************** regression *****************************'
print '*******************************************************************'
# create an array to store the correlation coefficient
slope_transient = np.zeros(len(lat_AMET),dtype = float)
r_value_transient = np.zeros(len(lat_AMET),dtype = float)
p_value_transient = np.zeros(len(lat_AMET),dtype = float)

slope_standing = np.zeros(len(lat_AMET),dtype = float)
r_value_standing = np.zeros(len(lat_AMET),dtype = float)
p_value_standing = np.zeros(len(lat_AMET),dtype = float)

#slope_overall = np.zeros(len(lat_AMET),dtype = float)
#r_value_overall = np.zeros(len(lat_AMET),dtype = float)
#p_value_overall = np.zeros(len(lat_AMET),dtype = float)

for c in np.arange(len(lat_interest_list)):
    for l in np.arange(len(levels)):
        for i in np.arange(len(lat_AMET)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope_transient[i],_,r_value_transient[i],p_value_transient[i],_ = stats.linregress(v2_transient_zonal_white_series[:,l,i],AMET_white_series[:,lat_interest['ERAI'][c]])
            slope_standing[i],_,r_value_standing[i],p_value_standing[i],_ = stats.linregress(v2_standing_zonal_white_series[:,l,i],AMET_white_series[:,lat_interest['ERAI'][c]])
            #slope_overall[i],_,r_value_overall[i],p_value_overall[i],_ = stats.linregress(v2_overall_zonal_white_series[:,l,i],AMET_white_series[:,lat_interest['ERAI'][c]])
        # plot of regression coefficient
        fig5 = plt.figure()
        #plt.plot(lat_AMET,slope_transient,'b-',linewidth=2.0,label='Transient')
        #plt.plot(lat_AMET,slope_standing,'r-',linewidth=2.0,label='standing')
        plt.plot(lat_AMET,p_value_transient,'b-',linewidth=2.0,label='Transient')
        plt.plot(lat_AMET,p_value_standing,'r-',linewidth=2.0,label='Standing')
        #plt.plot(lat_AMET,slope_overall,'g-',linewidth=2.0,label='Overall')
        plt.title('Regression of AMET Anomaly across {}N on Eddies anomalies on {}hPa'.format(lat_interest_list[c],levels[l]))
        plt.legend()
        plt.xlabel("Latitude")
        plt.ylabel("AMET/v2 (PW/(m2/s2))")
        plt.show()
        #fig5.savefig(os.path.join(output_path,'Momentum_v2','Regression','Zonal','regression_coef','regress_AMET_{}N_eddy_{}hPa_regression_coef'.format(lat_interest_list[c],levels[l])),dpi=400)
        fig5.savefig(os.path.join(output_path,'Momentum_v2','Regression','Zonal','correlation_coef','regress_AMET_{}N_eddy_{}hPa_correlation_coef'.format(lat_interest_list[c],levels[l])),dpi=400)
        plt.close(fig5)

# spatial regression point-wise
slope = np.zeros((len(lat[:40]),len(lon)),dtype = float)
r_value = np.zeros((len(lat[:40]),len(lon)),dtype = float)
p_value = np.zeros((len(lat[:40]),len(lon)),dtype = float)

for c in np.arange(len(lat_interest_list)):
    for l in np.arange(len(levels)):
        #******************* regression AMET on transient eddies ********************#
        #*******************              four seasons           ********************#
        for i in np.arange(len(lat[:40])):
            for j in np.arange(len(lon)):
                slope[i,j],_,r_value[i,j],p_value[i,j],_ = stats.linregress(v2_transient_point_white_series[:,l,i,j],AMET_white_series[:,lat_interest['ERAI'][c]])
        fig6 = plt.figure()
        m = Basemap(projection='npstere',boundinglat=60,round=True,lon_0=0,resolution='l')
        m.drawcoastlines(linewidth=0.25)
        m.drawparallels(np.arange(60,81,20),fontsize = 7,linewidth=0.75)
        m.drawmeridians(np.arange(0,360,30),labels=[1,1,1,1],fontsize = 7,linewidth=0.75)
        xx, yy = np.meshgrid(lon,lat[:40])
        XX, YY = m(xx, yy)
        color = np.linspace(-0.005,0.005,11)
        # !!!!!take care about the coordinate of contourf(Longitude, Latitude, data(Lat,Lon))
        cs = m.contourf(XX,YY,slope,color,cmap='coolwarm',extend='both') # SLP_white
        # add color bar
        cbar = m.colorbar(cs,location="bottom",size='4%',pad="8%",format='%.3f')
        cbar.ax.tick_params(labelsize=8)
        cbar.set_label('Regression Coefficient AMET/v2 (PW/(m2/s2))',fontsize = 7)
        ii, jj = np.where(p_value<=0.05)
        m.scatter(XX[ii,jj],YY[ii,jj],2.2,marker='.',color='g',alpha=0.6, edgecolor='none') # alpha bleding factor with map
        plt.title('Regression of AMET Anomaly across {}N on transient eddy anomalies on {}hPa'.format(lat_interest_list[c],levels[l]),fontsize = 9, y=1.05)
        plt.show()
        fig6.savefig(os.path.join(output_path,'Momentum_v2','Regression','Spatial','transient','regress_AMET_{}N_transient_eddy_{}hPa'.format(lat_interest_list[c],levels[l])),dpi=400)
        plt.close(fig6)

        #******************* regression AMET on standing eddies ********************#
        #*******************              four seasons          ********************#
        for i in np.arange(len(lat[:40])):
            for j in np.arange(len(lon)):
                slope[i,j],_,r_value[i,j],p_value[i,j],_ = stats.linregress(v2_standing_point_white_series[:,l,i,j],AMET_white_series[:,lat_interest['ERAI'][c]])
        fig7 = plt.figure()
        m = Basemap(projection='npstere',boundinglat=60,round=True,lon_0=0,resolution='l')
        m.drawcoastlines(linewidth=0.25)
        m.drawparallels(np.arange(60,81,20),fontsize = 7,linewidth=0.75)
        m.drawmeridians(np.arange(0,360,30),labels=[1,1,1,1],fontsize = 7,linewidth=0.75)
        xx, yy = np.meshgrid(lon,lat[:40])
        XX, YY = m(xx, yy)
        color = np.linspace(-0.005,0.005,11)
        # !!!!!take care about the coordinate of contourf(Longitude, Latitude, data(Lat,Lon))
        cs = m.contourf(XX,YY,slope,color,cmap='coolwarm',extend='both') # SLP_white
        # add color bar
        cbar = m.colorbar(cs,location="bottom",size='4%',pad="8%",format='%.3f')
        cbar.ax.tick_params(labelsize=8)
        cbar.set_label('Regression Coefficient AMET/v2 (PW/(m2/s2))',fontsize = 7)
        ii, jj = np.where(p_value<=0.05)
        m.scatter(XX[ii,jj],YY[ii,jj],2.2,marker='.',color='g',alpha=0.6, edgecolor='none') # alpha bleding factor with map
        plt.title('Regression of AMET Anomaly across {}N on standing eddy anomalies on {}hPa'.format(lat_interest_list[c],levels[l]),fontsize = 9, y=1.05)
        plt.show()
        fig7.savefig(os.path.join(output_path,'Momentum_v2','Regression','Spatial','standing','regress_AMET_{}N_transient_eddy_{}hPa'.format(lat_interest_list[c],levels[l])),dpi=400)
        plt.close(fig7)

        #******************* regression AMET on transient eddies ********************#
        #*******************              winter only            ********************#
        for i in np.arange(len(lat[:40])):
            for j in np.arange(len(lon)):
                slope[i,j],_,r_value[i,j],p_value[i,j],_ = stats.linregress(v2_transient_point_white_series_winter[:,l,i,j],AMET_white_series_winter[:,lat_interest['ERAI'][c]])
        fig8 = plt.figure()
        m = Basemap(projection='npstere',boundinglat=60,round=True,lon_0=0,resolution='l')
        m.drawcoastlines(linewidth=0.25)
        m.drawparallels(np.arange(60,81,20),fontsize = 7,linewidth=0.75)
        m.drawmeridians(np.arange(0,360,30),labels=[1,1,1,1],fontsize = 7,linewidth=0.75)
        xx, yy = np.meshgrid(lon,lat[:40])
        XX, YY = m(xx, yy)
        color = np.linspace(-0.005,0.005,11)
        # !!!!!take care about the coordinate of contourf(Longitude, Latitude, data(Lat,Lon))
        cs = m.contourf(XX,YY,slope,color,cmap='coolwarm',extend='both') # SLP_white
        # add color bar
        cbar = m.colorbar(cs,location="bottom",size='4%',pad="8%",format='%.3f')
        cbar.ax.tick_params(labelsize=8)
        cbar.set_label('Regression Coefficient AMET/v2 (PW/(m2/s2))',fontsize = 7)
        ii, jj = np.where(p_value<=0.05)
        m.scatter(XX[ii,jj],YY[ii,jj],2.2,marker='.',color='g',alpha=0.6, edgecolor='none') # alpha bleding factor with map
        plt.title('Regression of AMET Anomaly across {}N on transient eddy anomalies on {}hPa in winter'.format(lat_interest_list[c],levels[l]),fontsize = 9, y=1.05)
        plt.show()
        fig8.savefig(os.path.join(output_path,'Momentum_v2','Regression','Spatial','transient','seasonal','regress_AMET_{}N_transient_eddy_{}hPa_winter'.format(lat_interest_list[c],levels[l])),dpi=400)
        plt.close(fig8)

        #******************* regression AMET on standing eddies ********************#
        #*******************              winter only           ********************#
        for i in np.arange(len(lat[:40])):
            for j in np.arange(len(lon)):
                slope[i,j],_,r_value[i,j],p_value[i,j],_ = stats.linregress(v2_standing_point_white_series_winter[:,l,i,j],AMET_white_series_winter[:,lat_interest['ERAI'][c]])
        fig9 = plt.figure()
        m = Basemap(projection='npstere',boundinglat=60,round=True,lon_0=0,resolution='l')
        m.drawcoastlines(linewidth=0.25)
        m.drawparallels(np.arange(60,81,20),fontsize = 7,linewidth=0.75)
        m.drawmeridians(np.arange(0,360,30),labels=[1,1,1,1],fontsize = 7,linewidth=0.75)
        xx, yy = np.meshgrid(lon,lat[:40])
        XX, YY = m(xx, yy)
        color = np.linspace(-0.005,0.005,11)
        # !!!!!take care about the coordinate of contourf(Longitude, Latitude, data(Lat,Lon))
        cs = m.contourf(XX,YY,slope,color,cmap='coolwarm',extend='both') # SLP_white
        # add color bar
        cbar = m.colorbar(cs,location="bottom",size='4%',pad="8%",format='%.3f')
        cbar.ax.tick_params(labelsize=8)
        cbar.set_label('Regression Coefficient AMET/v2 (PW/(m2/s2))',fontsize = 7)
        ii, jj = np.where(p_value<=0.05)
        m.scatter(XX[ii,jj],YY[ii,jj],2.2,marker='.',color='g',alpha=0.6, edgecolor='none') # alpha bleding factor with map
        plt.title('Regression of AMET Anomaly across {}N on standing eddy anomalies on {}hPa in winter'.format(lat_interest_list[c],levels[l]),fontsize = 9, y=1.05)
        plt.show()
        fig9.savefig(os.path.join(output_path,'Momentum_v2','Regression','Spatial','standing','seasonal','regress_AMET_{}N_transient_eddy_{}hPa_winter'.format(lat_interest_list[c],levels[l])),dpi=400)
        plt.close(fig9)
        
print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
