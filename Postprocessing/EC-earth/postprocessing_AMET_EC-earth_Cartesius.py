#!/usr/bin/env python
"""
Copyright Netherlands eScience Center

Function        : Postprocessing meridional energy transport from Cartesius (EC-earth)
Author          : Yang Liu
Date            : 2017.12.20
Last Update     : 2018.01.12
Description     : The code aims to postprocess the output from the Cartesius
                  regarding the computation of atmospheric meridional energy
                  transport based on the output from EC-earth simulation (Atmosphere
                  only run). The complete procedure includes data extraction and
                  making plots.
Dependencies    : os, time, numpy, netCDF4, matplotlib
variables       : Meridional Total Energy Transport           E         [Tera-Watt]
                  Meridional Internal Energy Transport        E_cpT     [Tera-Watt]
                  Meridional Latent Energy Transport          E_Lvq     [Tera-Watt]
                  Meridional Geopotential Energy Transport    E_gz      [Tera-Watt]
                  Meridional Kinetic Energy Transport         E_uv2     [Tera-Watt]
Caveat!!        : The data is from 90 deg south to 90 deg north (Globe).
                  Latitude: South to Nouth (90 to -90)
                  Lontitude: West to East (0 to 360)
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
################################   Input zone  ######################################
# specify data path
datapath = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/EC-earth/postprocessing'
# specify output path for the netCDF4 file
output_path = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/EC-earth/postprocessing'
Lat_num = 60 # index 85
####################################################################################
print '*******************************************************************'
print '*********************** extract variables *************************'
print '*******************************************************************'
# zonal integral
dataset = Dataset(datapath + os.sep + 'AMET_EC-earth_model_daily_1979_2015_E_zonal_int.nc')
# spacial distribution
dataset_point = Dataset(datapath + os.sep + 'AMET_EC-earth_model_daily_1979_2015_E_point.nc')

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
index_year = np.arange(1979,1979+len(year)+1,1)
axis_ref = np.zeros(len(index))

print '*******************************************************************'
print '*********************** time series plots *************************'
print '*******************************************************************'
# 60 N total meridional energy transport time series
fig1 = plt.figure()
plt.plot(index,T_series_E[85,:]/1000,'b-',label='EC-earth')
plt.title('Atmospheric Meridional Energy Transport time series at %d N (1979-2015)' % (Lat_num))
#plt.legend()
fig1.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(0, 444, 38), index_year)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig1.savefig(output_path + os.sep + 'Meridional_Energy_%dN_total_time_series_1979_2015.jpg' % (Lat_num), dpi = 500)

fig2 = plt.figure()
plt.plot(index,T_series_E_internal[85,:]/1000,'b-',label='EC-earth')
plt.title('Atmospheric Meridional Internal Energy Transport time series at %d N (1979-2015)' % (Lat_num))
#plt.legend()
fig2.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(0, 444, 38), index_year)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig2.savefig(output_path + os.sep + 'Meridional_Energy_%dN_internal_time_series_1979_2015.jpg' % (Lat_num), dpi = 500)

fig3 = plt.figure()
plt.plot(index,T_series_E_latent[85,:]/1000,'b-',label='EC-earth')
plt.title('Atmospheric Meridional Latent Energy Transport time series at %d N (1979-2015)' % (Lat_num))
#plt.legend()
fig3.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(0, 444, 38), index_year)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig3.savefig(output_path + os.sep + 'Meridional_Energy_%dN_latent_time_series_1979_2015.jpg' % (Lat_num), dpi = 500)

fig4 = plt.figure()
plt.plot(index,T_series_E_geopotential[85,:]/1000,'b-',label='EC-earth')
plt.title('Atmospheric Meridional Geopotential Energy Transport time series at %d N (1979-2015)' % (Lat_num))
#plt.legend()
fig4.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(0, 444, 38), index_year)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig4.savefig(output_path + os.sep + 'Meridional_Energy_%dN_geopotential_time_series_1979_2015.jpg' % (Lat_num), dpi = 500)

fig5 = plt.figure()
plt.plot(index,T_series_E_kinetic[85,:]/1000,'b-',label='EC-earth')
plt.title('Atmospheric Meridional Kinetic Energy Transport time series at %d N (1979-2015)' % (Lat_num))
#plt.legend()
fig5.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(0, 444, 38), index_year)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig5.savefig(output_path + os.sep + 'Meridional_Energy_%dN_kinetic_time_series_1979_2015.jpg' % (Lat_num), dpi = 500)

# everything in one plot
fig6 = plt.figure()
plt.plot(index,T_series_E_internal[85,:]/1000,'r--',label='cpT')
plt.plot(index,T_series_E_latent[85,:]/1000,'m-.',label='Lvq')
plt.plot(index,T_series_E_geopotential[85,:]/1000,'g:',label='gz')
plt.plot(index,T_series_E_kinetic[85,:]/1000,'c:',label='u2')
plt.plot(index,T_series_E[85,:]/1000,'b-',label='total')
plt.title('Atmospheric Meridional Energy Transport time series at %d N (1979-2015)' % (Lat_num))
plt.legend()
fig6.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(0, 444, 38), index_year)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig6.savefig(output_path + os.sep + 'Meridional_Energy_%dN_eachComponent_time_series_1979_2015.jpg' % (Lat_num), dpi = 500)

print '*******************************************************************'
print '*********************** time series shades ************************'
print '*******************************************************************'

x , y = np.meshgrid(index,latitude)

fig7 = plt.figure()
#plt.contour(x,y,T_series_E/1000, linewidth=0.05, colors='k')
# cmap 'jet' 'RdYlBu' 'coolwarm'
plt.contourf(x,y,T_series_E/1000,cmap='coolwarm')
plt.title('Atmospheric Meridional Energy Transport time series(1979-2015)' )
fig7.set_size_inches(12, 5)
#add color bar
cbar = plt.colorbar()
cbar.set_label('PW (1E+15)')
plt.xlabel("Time")
plt.xticks(np.linspace(0, 444, 38), index_year)
plt.xticks(rotation=60)
plt.ylabel("Latitude")
plt.show()
fig7.savefig(output_path + os.sep + 'Meridional_Energy_total_time_series_1979_2015_shades.jpg', dpi = 500)

print '*******************************************************************'
print '*************************** x-y lines  ****************************'
print '*******************************************************************'

fig8 = plt.figure()
plt.axhline(y=0, color='r',ls='--')
plt.plot(latitude,np.mean(series_E,0)/1000,'b-',label='EC-earth')
plt.title('Atmospheric Meridional Energy Transport (1979-2015)' )
#plt.legend()
plt.xlabel("Latitudes")
#plt.xticks()
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig8.savefig(output_path + os.sep + 'Meridional_Energy_total_mean_1979_2015.jpg', dpi = 500)

fig9 = plt.figure()
plt.axhline(y=0, color='r',ls='--')
plt.plot(latitude,np.mean(series_E_internal,0)/1000,'b-',label='EC-earth')
plt.title('Atmospheric Meridional Internal Energy Transport (1979-2015)' )
#plt.legend()
plt.xlabel("Latitudes")
#plt.xticks()
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig9.savefig(output_path + os.sep + 'Meridional_Energy_internal_mean_1979_2015.jpg', dpi = 500)

fig10 = plt.figure()
plt.axhline(y=0, color='r',ls='--')
plt.plot(latitude,np.mean(series_E_latent,0)/1000,'b-',label='EC-earth')
plt.title('Atmospheric Meridional Latent Energy Transport (1979-2015)' )
#plt.legend()
plt.xlabel("Latitudes")
#plt.xticks()
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig10.savefig(output_path + os.sep + 'Meridional_Energy_latent_mean_1979_2015.jpg', dpi = 500)

fig11 = plt.figure()
plt.axhline(y=0, color='r',ls='--')
plt.plot(latitude,np.mean(series_E_geopotential,0)/1000,'b-',label='EC-earth')
plt.title('Atmospheric Meridional Geopotential Energy Transport (1979-2015)' )
#plt.legend()
plt.xlabel("Latitudes")
#plt.xticks()
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig11.savefig(output_path + os.sep + 'Meridional_Energy_geopotential_mean_1979_2015.jpg', dpi = 500)

fig12 = plt.figure()
plt.axhline(y=0, color='r',ls='--')
plt.plot(latitude,np.mean(series_E_kinetic,0)/1000,'b-',label='EC-earth')
plt.title('Atmospheric Meridional kinetic Energy Transport (1979-2015)' )
#plt.legend()
plt.xlabel("Latitudes")
#plt.xticks()
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig12.savefig(output_path + os.sep + 'Meridional_Energy_kinetic_mean_1979_2015.jpg', dpi = 500)

fig13 = plt.figure()
plt.axhline(y=0, color='k',ls='-.')
plt.plot(latitude,np.mean(series_E_internal,0)/1000,'r--',label='cpT')
plt.plot(latitude,np.mean(series_E_latent,0)/1000,'m-.',label='Lvq')
plt.plot(latitude,np.mean(series_E_geopotential,0)/1000,'g:',label='gz')
plt.plot(latitude,np.mean(series_E_kinetic,0)/1000,'c:',label='u2')
plt.plot(latitude,np.mean(series_E,0)/1000,'b-',label='total')
plt.title('Atmospheric Meridional Energy Transport (1979-2015)' )
plt.legend()
plt.xlabel("Latitudes")
#plt.xticks()
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig13.savefig(output_path + os.sep + 'Meridional_Energy_eachComponent_mean_1979_2015.jpg', dpi = 500)

print '*******************************************************************'
print '************************* wind rose plots *************************'
print '*******************************************************************'

angle = np.linspace(0, 2 * np.pi, 13)
# np.repeat
angle_series = np.tile(angle[:-1],29)
month_str = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

# wind rose of time series
fig14 = plt.figure()
plt.axes(polar = True)
plt.plot(angle_series,T_series_E[85,:]/1000,'b--',label='EC-earth')
plt.title('Atmospheric Meridional Energy Transport at %d N (1979-2015)' % (Lat_num), y=1.07)
#plt.legend()
#fig10.set_size_inches(14, 4)
#plt.xlabel("Time")
plt.xticks(angle[:-1], month_str)
plt.yticks(np.linspace(0,6,7),color='r',size =12)
#plt.xticks(rotation=60)
#plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig14.savefig(output_path + os.sep + 'Meridional_Energy_%dN_total_windrose_1979_2015.jpg' % (Lat_num), dpi = 500)

# wind rose of time series after removing seasonal cycles

fig15 = plt.figure()
plt.axes(polar = True)
plt.plot(angle_series,T_series_E_white[85,:]/1000,'b--',label='EC-earth')
plt.title('Atmospheric Meridional Energy Transport anomaly at %d N (1979-2015)' % (Lat_num), y=1.07)
#plt.legend()
#fig10.set_size_inches(14, 4)
#plt.xlabel("Time")
plt.xticks(angle[:-1], month_str)
plt.yticks(np.linspace(-1,1,11),color='r',size =12)
#plt.xticks(rotation=60)
#plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig15.savefig(output_path + os.sep + 'Meridional_Energy_%dN_total_windrose_white_1979_2015.jpg' % (Lat_num), dpi = 500)

print '*******************************************************************'
print '********************** spacial distribution ***********************'
print '*******************************************************************'

# spacial distribution of AMET - mean of 38 years
fig16 = plt.figure()
# setup north polar stereographic basemap
# resolution c(crude) l(low) i(intermidiate) h(high) f(full)
# lon_0 is at 6 o'clock
m = Basemap(projection='npstere',boundinglat=20,round=True,lon_0=0,resolution='l')
# draw coastlines
m.drawcoastlines()
# fill continents, set lake color same as ocean color.
# m.fillcontinents(color='coral',lake_color='aqua')
# draw parallels and meridians
# location labels=[left,right,top,bottom]
m.drawparallels(np.arange(-90,91,30),fontsize = 7)
m.drawmeridians(np.arange(0,360,30),labels=[1,1,1,1],fontsize = 7)
# x,y coordinate - lon, lat
xx, yy = np.meshgrid(longitude,latitude)
XX, YY = m(xx, yy)
# define color range for the contourf
color = np.linspace(-1,1,11)
# !!!!!take care about the coordinate of contourf(Longitude, Latitude, data(Lat,Lon))
cs = m.contourf(XX,YY,np.mean(np.mean(E_point,1),0)/1000,color,cmap='coolwarm')
# add color bar
cbar = m.colorbar(cs,location="bottom",size='4%',pad="8%",format='%.1f')
cbar.ax.tick_params(labelsize=8)
cbar.set_label('Peta Watt',fontsize = 8)
plt.title('Mean Meridional Energy Transport (1979-2015)',fontsize = 9, y=1.05)
plt.show()
fig16.savefig(output_path + os.sep + "Map_AMET_EC-earth_mean.jpeg",dpi=500)

# spacial distribution of AMET - mean of the anomaly of 38 years
# !!!!!!! The result is 0 !!!!!!
fig17 = plt.figure()
# setup north polar stereographic basemap
# resolution c(crude) l(low) i(intermidiate) h(high) f(full)
# lon_0 is at 6 o'clock
m = Basemap(projection='npstere',boundinglat=20,round=True,lon_0=0,resolution='l')
# draw coastlines
m.drawcoastlines()
# fill continents, set lake color same as ocean color.
# m.fillcontinents(color='coral',lake_color='aqua')
# draw parallels and meridians
# location labels=[left,right,top,bottom]
m.drawparallels(np.arange(-90,91,30),fontsize = 7)
m.drawmeridians(np.arange(0,360,30),labels=[1,1,1,1],fontsize = 7)
# x,y coordinate - lon, lat
xx, yy = np.meshgrid(longitude,latitude)
XX, YY = m(xx, yy)
# define color range for the contourf
color = np.linspace(-1,1,11)
# !!!!!take care about the coordinate of contourf(Longitude, Latitude, data(Lat,Lon))
cs = m.contourf(XX,YY,np.mean(np.mean(E_point_white,1),0)/1000,color,cmap='coolwarm')
# add color bar
cbar = m.colorbar(cs,location="bottom",size='4%',pad="8%",format='%.1f')
cbar.ax.tick_params(labelsize=8)
cbar.set_label('Peta Watt',fontsize = 8)
plt.title('Mean Meridional Energy Transport Anomaly (1979-2015)',fontsize = 9, y=1.05)
plt.show()
fig17.savefig(output_path + os.sep + "Map_AMET_EC-earth_anomaly_mean.jpeg",dpi=500)

# spacial distribution of AMET - trend of the anomaly of 38 years
# calculate trend
# create an array to store the slope coefficient and residual
a = np.zeros((len(latitude),len(longitude)),dtype = float)
b = np.zeros((len(latitude),len(longitude)),dtype = float)
# the least square fit equation is y = ax + b
# np.lstsq solves the equation ax=b, a & b are the input
# thus the input file should be reformed for the function
# we can rewrite the line y = Ap, with A = [x,1] and p = [[a],[b]]
A = np.vstack([index,np.ones(len(index))]).T
# start the least square fitting
for i in np.arange(len(latitude)):
    for j in np.arange(len(longitude)):
        # return value: coefficient matrix a and b, where a is the slope
        a[i,j], b[i,j] = np.linalg.lstsq(A,series_E_point_white[:,i,j]/1000)[0]

fig18 = plt.figure()
# setup north polar stereographic basemap
# resolution c(crude) l(low) i(intermidiate) h(high) f(full)
# lon_0 is at 6 o'clock
m = Basemap(projection='npstere',boundinglat=20,round=True,lon_0=0,resolution='l')
# draw coastlines
m.drawcoastlines()
# fill continents, set lake color same as ocean color.
# m.fillcontinents(color='coral',lake_color='aqua')
# draw parallels and meridians
# location labels=[left,right,top,bottom]
m.drawparallels(np.arange(-90,91,30),fontsize = 7)
m.drawmeridians(np.arange(0,360,30),labels=[1,1,1,1],fontsize = 7)
# x,y coordinate - lon, lat
xx, yy = np.meshgrid(longitude,latitude)
XX, YY = m(xx, yy)
# define color range for the contourf
color = np.linspace(-0.1,0.1,11)
# !!!!!take care about the coordinate of contourf(Longitude, Latitude, data(Lat,Lon))
cs = m.contourf(XX,YY,a*12*10,color,cmap='coolwarm')
# add color bar
cbar = m.colorbar(cs,location="bottom",size='4%',pad="8%",format='%.2f')
cbar.ax.tick_params(labelsize=8)
cbar.set_label('PW/decade',fontsize = 8)
plt.title('Trend of AMET anomaly (1979-2015)',fontsize = 9, y=1.05)
plt.show()
fig18.savefig(output_path + os.sep + "Map_AMET_EC-earth_anomaly_trend.jpeg",dpi=500)

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
