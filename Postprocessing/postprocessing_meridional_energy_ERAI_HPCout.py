#!/usr/bin/env python
"""
Copyright Netherlands eScience Center

Function        : Postprocessing meridional energy transport from HPC cloud (ERA-Interim)
Author          : Yang Liu
Date            : 2017.7.23
Last Update     : 2017.7.29
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
datapath = 'F:\DataBase\HPC_out\ERAI\postprocessing'
# specify output path for the netCDF4 file
output_path = 'F:\DataBase\HPC_out\ERAI\postprocessing'
Lat_num = 60
####################################################################################
print '*******************************************************************'
print '*********************** extract variables *************************'
print '*******************************************************************'
dataset = Dataset(datapath + os.sep + 'model_daily_075_1979_2016_E_zonal_int.nc')
for k in dataset.variables:
    print dataset.variables['%s' % (k)]

E = dataset.variables['E'][:]
E_internal = dataset.variables['E_cpT'][:]
E_latent = dataset.variables['E_Lvq'][:]
E_geopotential = dataset.variables['E_gz'][:]
E_kinetic = dataset.variables['E_uv2'][:]

year = dataset.variables['year'][:]
month = dataset.variables['month'][:]
latitude = dataset.variables['latitude'][:]

print '*******************************************************************'
print '****************** prepare variables for plot *********************'
print '*******************************************************************'
# reshape the array into time series
series_E = E.reshape(len(year)*len(month),len(latitude))
series_E_internal = E_internal.reshape(len(year)*len(month),len(latitude))
series_E_latent = E_latent.reshape(len(year)*len(month),len(latitude))
series_E_geopotential = E_geopotential.reshape(len(year)*len(month),len(latitude))
series_E_kinetic = E_kinetic.reshape(len(year)*len(month),len(latitude))

T_series_E = np.transpose(series_E)
T_series_E_internal = np.transpose(series_E_internal)
T_series_E_latent = np.transpose(series_E_latent)
T_series_E_geopotential = np.transpose(series_E_geopotential)
T_series_E_kinetic = np.transpose(series_E_kinetic)

index = np.arange(1,len(year)*len(month)+1,1)
axis_ref = np.zeros(len(index))

print '*******************************************************************'
print '*********************** time series plots *************************'
print '*******************************************************************'
# 60 N total meridional energy transport time series
fig1 = plt.figure()
plt.plot(index,T_series_E[40,:]/1000,'b-',label='ECMWF')
plt.title('Atmospheric Meridional Energy Transport time series at %d N (1979-2016)' % (Lat_num))
#plt.legend()
fig1.set_size_inches(14, 4)
plt.xlabel("Time")
plt.xticks(np.linspace(1, 456, 38), year)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig1.savefig(output_path + os.sep + 'Meridional_Energy_%dN_total_time_series_1979_2016.jpg' % (Lat_num), dpi = 500)

fig2 = plt.figure()
plt.plot(index,T_series_E_internal[40,:]/1000,'b-',label='ECMWF')
plt.title('Atmospheric Meridional Internal Energy Transport time series at %d N (1979-2016)' % (Lat_num))
#plt.legend()
fig2.set_size_inches(14, 4)
plt.xlabel("Time")
plt.xticks(np.linspace(1, 456, 38), year)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig2.savefig(output_path + os.sep + 'Meridional_Energy_%dN_internal_time_series_1979_2016.jpg' % (Lat_num), dpi = 500)

fig3 = plt.figure()
plt.plot(index,T_series_E_latent[40,:]/1000,'b-',label='ECMWF')
plt.title('Atmospheric Meridional Latent Energy Transport time series at %d N (1979-2016)' % (Lat_num))
#plt.legend()
fig3.set_size_inches(14, 4)
plt.xlabel("Time")
plt.xticks(np.linspace(1, 456, 38), year)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig3.savefig(output_path + os.sep + 'Meridional_Energy_%dN_latent_time_series_1979_2016.jpg' % (Lat_num), dpi = 500)

fig4 = plt.figure()
plt.plot(index,T_series_E_geopotential[40,:]/1000,'b-',label='ECMWF')
plt.title('Atmospheric Meridional Geopotential Energy Transport time series at %d N (1979-2016)' % (Lat_num))
#plt.legend()
fig4.set_size_inches(14, 4)
plt.xlabel("Time")
plt.xticks(np.linspace(1, 456, 38), year)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig4.savefig(output_path + os.sep + 'Meridional_Energy_%dN_geopotential_time_series_1979_2016.jpg' % (Lat_num), dpi = 500)

fig5 = plt.figure()
plt.plot(index,T_series_E_kinetic[40,:]/1000,'b-',label='ECMWF')
plt.title('Atmospheric Meridional Kinetic Energy Transport time series at %d N (1979-2016)' % (Lat_num))
#plt.legend()
fig5.set_size_inches(14, 4)
plt.xlabel("Time")
plt.xticks(np.linspace(1, 456, 38), year)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig5.savefig(output_path + os.sep + 'Meridional_Energy_%dN_kinetic_time_series_1979_2016.jpg' % (Lat_num), dpi = 500)

# everything in one plot
fig6 = plt.figure()
plt.plot(index,T_series_E_internal[40,:]/1000,'r--',label='cpT')
plt.plot(index,T_series_E_latent[40,:]/1000,'m-.',label='Lvq')
plt.plot(index,T_series_E_geopotential[40,:]/1000,'g:',label='gz')
plt.plot(index,T_series_E_kinetic[40,:]/1000,'c:',label='u2')
plt.plot(index,T_series_E[40,:]/1000,'b-',label='total')
plt.title('Atmospheric Meridional Energy Transport time series at %d N (1979-2016)' % (Lat_num))
plt.legend()
fig6.set_size_inches(14, 4)
plt.xlabel("Time")
plt.xticks(np.linspace(1, 456, 38), year)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig6.savefig(output_path + os.sep + 'Meridional_Energy_%dN_eachComponent_time_series_1979_2016.jpg' % (Lat_num), dpi = 500)

print '*******************************************************************'
print '*********************** time series shades ************************'
print '*******************************************************************'

x , y = np.meshgrid(index,latitude)

fig7 = plt.figure()
#plt.contour(x,y,T_series_E/1000, linewidth=0.05, colors='k')
# cmap 'jet' 'RdYlBu' 'coolwarm'
plt.contourf(x,y,T_series_E/1000,cmap='coolwarm')
plt.title('Atmospheric Meridional Energy Transport time series(1979-2016)' )
fig7.set_size_inches(14, 4)
#add color bar
cbar = plt.colorbar()
cbar.set_label('PW (1E+15)')
plt.xlabel("Time")
plt.xticks(np.linspace(1, 456, 38), year)
plt.xticks(rotation=60)
plt.ylabel("Latitude (North Hemisphere)")
plt.show()
fig7.savefig(output_path + os.sep + 'Meridional_Energy_total_time_series_1979_2016_shades.jpg', dpi = 500)

print '*******************************************************************'
print '*************************** x-y lines  ****************************'
print '*******************************************************************'

fig8 = plt.figure()
plt.axhline(y=0, color='r',ls='--')
plt.plot(latitude,np.mean(series_E,0)/1000,'b-',label='ECMWF')
plt.title('Atmospheric Meridional Energy Transport (1979-2016)' )
#plt.legend()
plt.xlabel("Latitudes")
#plt.xticks()
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig8.savefig(output_path + os.sep + 'Meridional_Energy_total_mean_1979_2016.jpg', dpi = 500)

fig9 = plt.figure()
plt.axhline(y=0, color='r',ls='--')
plt.plot(latitude,np.mean(series_E_internal,0)/1000,'b-',label='ECMWF')
plt.title('Atmospheric Meridional Internal Energy Transport (1979-2016)' )
#plt.legend()
plt.xlabel("Latitudes")
#plt.xticks()
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig9.savefig(output_path + os.sep + 'Meridional_Energy_internal_mean_1979_2016.jpg', dpi = 500)

fig10 = plt.figure()
plt.axhline(y=0, color='r',ls='--')
plt.plot(latitude,np.mean(series_E_latent,0)/1000,'b-',label='ECMWF')
plt.title('Atmospheric Meridional Latent Energy Transport (1979-2016)' )
#plt.legend()
plt.xlabel("Latitudes")
#plt.xticks()
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig10.savefig(output_path + os.sep + 'Meridional_Energy_latent_mean_1979_2016.jpg', dpi = 500)

fig11 = plt.figure()
plt.axhline(y=0, color='r',ls='--')
plt.plot(latitude,np.mean(series_E_geopotential,0)/1000,'b-',label='ECMWF')
plt.title('Atmospheric Meridional Geopotential Energy Transport (1979-2016)' )
#plt.legend()
plt.xlabel("Latitudes")
#plt.xticks()
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig11.savefig(output_path + os.sep + 'Meridional_Energy_geopotential_mean_1979_2016.jpg', dpi = 500)

fig12 = plt.figure()
plt.axhline(y=0, color='r',ls='--')
plt.plot(latitude,np.mean(series_E_kinetic,0)/1000,'b-',label='ECMWF')
plt.title('Atmospheric Meridional kinetic Energy Transport (1979-2016)' )
#plt.legend()
plt.xlabel("Latitudes")
#plt.xticks()
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig12.savefig(output_path + os.sep + 'Meridional_Energy_kinetic_mean_1979_2016.jpg', dpi = 500)

fig13 = plt.figure()
plt.axhline(y=0, color='k',ls='-.')
plt.plot(latitude,np.mean(series_E_internal,0)/1000,'r--',label='cpT')
plt.plot(latitude,np.mean(series_E_latent,0)/1000,'m-.',label='Lvq')
plt.plot(latitude,np.mean(series_E_geopotential,0)/1000,'g:',label='gz')
plt.plot(latitude,np.mean(series_E_kinetic,0)/1000,'c:',label='u2')
plt.plot(latitude,np.mean(series_E,0)/1000,'b-',label='total')
#plt.plot(latitude,np.mean(T_series_E_kinetic,0)/1000,'b-',label='ECMWF')
plt.title('Atmospheric Meridional Energy Transport (1979-2016)' )
plt.legend()
plt.xlabel("Latitudes")
#plt.xticks()
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig13.savefig(output_path + os.sep + 'Meridional_Energy_eachComponent_mean_1979_2016.jpg', dpi = 500)

print '*******************************************************************'
print '************************* wind rose plots *************************'
print '*******************************************************************'

angle = np.linspace(0, 2 * np.pi, 13)
# np.repeat
angle_series = np.tile(angle[:-1],38)
month_str = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

fig14 = plt.figure()
plt.axes(polar = True)
plt.plot(angle_series,T_series_E[40,:]/1000,'b--',label='ECMWF')
plt.title('Atmospheric Meridional Energy Transport at %d N (1979-2016)' % (Lat_num), y=1.07)
#plt.legend()
#fig10.set_size_inches(14, 4)
#plt.xlabel("Time")
plt.xticks(angle[:-1], month_str)
plt.yticks(np.linspace(0,6,7),color='r',size =12)
#plt.xticks(rotation=60)
#plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig14.savefig(output_path + os.sep + 'Meridional_Energy_%dN_total_windrose_1979_2016.jpg' % (Lat_num), dpi = 500)

'''
3. basemap of average over 38 years
4. basemap variance
5. basemap stand deviation
6. basemap cumulative

'''
print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
