#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : Compare oceanic variable fields (MERRA2,ERA-Interim,JRA55)
Author          : Yang Liu
Date            : 2018.01.14
Last Update     : 2018.03.27
Description     : The code aims to compare the spatial and temporal distribution of
                  different fields from difference atmospheric reanalysis datasets on pressure
                  level. In this,case, this includes ERA-Interim from ECMWF, MERRA2 from NASA
                  and JRA55 from JMA. The script works with pressure level data.
Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, sys, matplotlib
variables       : Absolute Temperature             T         [K]
                  Meridional Wind Velocity         v         [m/s]
Caveat!!        : The dataset has different arrangement.
                  Vertical coordinate
                  ERA-Interim       TOA to surface
                  MERRA2            surface to TOA

                  Longitude
                  ERA-Interim       0 - 360
                  MERRA2            -180 - 180

                  In order to make the comparison easy, we convert the variable fields from
                  ERA-Interim to -180 - 180, the vertical coordinate remains the same.

                  ERA-Interim contains values inside the topography. This is due to the extrapolation.
                  Those unrealistic values can be masked by surface pressure.
                  https://software.ecmwf.int/wiki/display/CKB/About+pressure+level+data+in+high+altitudes
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
###########################   Equation Channel   #########################
# Potential temperature
# theta = T * (P0/P)^(R/cp)
# where T in kelvin, P0 = 1000 hPa, R/cp = 0.286
##########################################################################
# define the constant:
constant ={'g' : 9.80616,      # gravititional acceleration [m / s2]
           'R' : 6371009,      # radius of the earth [m]
           'cp': 1004.64,      # heat capacity of air [J/(Kg*K)]
           'Lv': 2264670,      # Latent heat of vaporization [J/Kg]
           'R_dry' : 286.9,    # gas constant of dry air [J/(kg*K)]
           'R_vap' : 461.5,    # gas constant for water vapour [J/(kg*K)]
            }


################################   Input zone  ######################################
# specify data path
# OMET
datapath_ERAI = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ERAI/statistics/pressure'
datapath_MERRA2 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/MERRA2/statistics/pressure'
#datapath_JRA55 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/JRA55/statistics'
datapath_ERAI_surface = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ERAI/regression'
# specify output path for figures
output_path = '/home/yang/NLeSC/Computation_Modeling/BlueAction/AMET/Comparison/var'

print '****************************************************************************'
print '********************    latitude index of insteret     *********************'
print '****************************************************************************'
# index of latitude for insteret
# make a dictionary for instereted sections (for process automation)
# 20N
lat_ERAI_20 = 93
lat_MERRA2_20 = 0
lat_JRA55_20 = 124
# 30N
lat_ERAI_30 = 80
lat_MERRA2_30 = 20
lat_JRA55_30 = 106
# 40N
lat_ERAI_40 = 67
lat_MERRA2_40 = 40
lat_JRA55_40 = 88
# 50N
lat_ERAI_50 = 53
lat_MERRA2_50 = 60
lat_JRA55_50 = 70
# 60N
lat_ERAI_60 = 40
lat_MERRA2_60 = 80
lat_JRA55_60 = 53
# 70N
lat_ERAI_70 = 27
lat_MERRA2_70 = 100
lat_JRA55_70 = 35
# 80N
lat_ERAI_80 = 13
lat_MERRA2_80 = 120
lat_JRA55_80 = 17

# make a dictionary for instereted sections (for process automation)
lat_interest = {}
lat_interest_list = [20,30,40,50,60,70,80]
lat_interest['ERAI'] = [lat_ERAI_20,lat_ERAI_30,lat_ERAI_40,lat_ERAI_50,lat_ERAI_60,lat_ERAI_70,lat_ERAI_80]
lat_interest['MERRA2'] = [lat_MERRA2_20,lat_MERRA2_30,lat_MERRA2_40,lat_MERRA2_50,lat_MERRA2_60,lat_MERRA2_70,lat_MERRA2_80]
lat_interest['JRA55'] = [lat_JRA55_20,lat_JRA55_30,lat_JRA55_40,lat_JRA55_50,lat_JRA55_60,lat_JRA55_70,lat_JRA55_80]
####################################################################################
print '*******************************************************************'
print '*********************** extract variables *************************'
print '*******************************************************************'
print '-------------------------------------------------------------------'
print '----                    Time of inspection                     ----'
print '----                         1997.07                           ----'
print '----               annual mean 1994.01 - 1998.12               ----'
print '-------------------------------------------------------------------'

print '*******************************************************************'
print '************       Extract the invariant fields!      *************'

# take the variable keys
dataset_ERAI = Dataset(datapath_ERAI + os.sep + 'ERAI_1997_monthly_pressure.nc')
dataset_MERRA2 = Dataset(datapath_MERRA2 + os.sep + 'MERRA2_200.instM_3d_asm_Np.199707.SUB.nc4')
# use surface pressure to mask the ERA-Interim
dataset_ERAI_surface = Dataset(datapath_ERAI_surface + os.sep + 'surface_ERAI_monthly_regress_1979_2016.nc')
# level
level_ERAI = dataset_ERAI.variables['level'][:]  # from TOA to surface
level_MERRA2 = dataset_MERRA2.variables['lev'][:] # from surface to TOA
# latitude
latitude_ERAI = dataset_ERAI.variables['latitude'][0:95]
latitude_MERRA2 =dataset_MERRA2.variables['lat'][:]
# longitude
longitude_ERAI_convert = dataset_ERAI.variables['longitude'][:]
longitude_ERAI = np.zeros(longitude_ERAI_convert.shape,dtype=float)
longitude_ERAI[0:239] = longitude_ERAI_convert[241:]
longitude_ERAI[239:] = longitude_ERAI_convert[:241]
longitude_ERAI[longitude_ERAI > 180] = longitude_ERAI[longitude_ERAI > 180] -360
longitude_MERRA2 = dataset_MERRA2.variables['lon'][:]

month_ind = np.arange(12)
year_ind = np.arange(1994,1999,1)

# surface pressure for mask
sp_ERAI_convert = dataset_ERAI_surface.variables['sp'][223,0:95,:] / 100 # 1997.07
sp_ERAI = np.zeros(sp_ERAI_convert.shape,dtype=float)
sp_ERAI[:,0:239] = sp_ERAI_convert[:,241:]
sp_ERAI[:,239:] = sp_ERAI_convert[:,:241]
T_ERAI_mask = np.zeros((len(level_ERAI),len(latitude_ERAI),len(longitude_ERAI)),dtype=int)
for i in np.arange(len(level_ERAI)):
    T_ERAI_mask[i,sp_ERAI[:]<level_ERAI[i]] = 1 # mask the point where surface pressure is smaller than

# # Extend the mask to 4D for masking
# T_ERAI_mask_4D = np.repeat(T_ERAI_mask[np.newaxis,:,:,:],len(year_ind)*len(month_ind),0)

print '*******************************************************************'
print '************            Extract variabels!            *************'
namelist_month = ['01','02','03','04','05','06','07','08','09','10','11','12']
# MERRA2
T_MERRA2 = np.zeros((len(year_ind)*len(month_ind),len(level_MERRA2),len(latitude_MERRA2),len(longitude_MERRA2)),dtype=float)
v_MERRA2 = np.zeros((len(year_ind)*len(month_ind),len(level_MERRA2),len(latitude_MERRA2),len(longitude_MERRA2)),dtype=float)
for i in year_ind:
    for j in month_ind:
        dataset_MERRA2 = Dataset(datapath_MERRA2 + os.sep + 'MERRA2_200.instM_3d_asm_Np.%d%s.SUB.nc4' % (i,namelist_month[j]))
        T_MERRA2[(i-1994)*12:(i-1994)*12+12,:,:,:] = dataset_MERRA2.variables['T'][0,:,:,:]
        v_MERRA2[(i-1994)*12:(i-1994)*12+12,:,:,:] = dataset_MERRA2.variables['V'][0,:,:,:]

# get the mask array from MERRA2
T_MERRA2_mask = np.zeros((len(level_MERRA2),len(latitude_MERRA2),len(longitude_MERRA2)),dtype=int)
v_MERRA2_mask = np.zeros((len(level_MERRA2),len(latitude_MERRA2),len(longitude_MERRA2)),dtype=int)
for i in np.arange(len(level_MERRA2)):
    T_MERRA2_mask[i,:,:] = np.ma.getmaskarray(T_MERRA2[0,i,:,:])
    v_MERRA2_mask[i,:,:] = np.ma.getmaskarray(v_MERRA2[0,i,:,:])

np.ma.set_fill_value(T_MERRA2,0)
np.ma.set_fill_value(v_MERRA2,0)

#ERA Interim
T_ERAI = np.zeros((len(year_ind)*len(month_ind),len(level_ERAI),len(latitude_ERAI),len(longitude_ERAI)),dtype=float)
v_ERAI = np.zeros((len(year_ind)*len(month_ind),len(level_ERAI),len(latitude_ERAI),len(longitude_ERAI)),dtype=float)
T_ERAI_convert = np.zeros((len(month_ind),len(level_ERAI),len(latitude_ERAI),len(longitude_ERAI)),dtype=float)
v_ERAI_convert = np.zeros((len(month_ind),len(level_ERAI),len(latitude_ERAI),len(longitude_ERAI)),dtype=float)
for i in year_ind:
    dataset_ERAI = Dataset(datapath_ERAI + os.sep + 'ERAI_%d_monthly_pressure.nc' % (i))
    T_ERAI_convert = dataset_ERAI.variables['t'][:,:,0:95,:]
    v_ERAI_convert = dataset_ERAI.variables['v'][:,:,0:95,:]
    T_ERAI[(i-1994)*12:(i-1994)*12+12,:,:,0:239] = T_ERAI_convert[:,:,:,241:] # -180 - 0
    T_ERAI[(i-1994)*12:(i-1994)*12+12,:,:,239:] = T_ERAI_convert[:,:,:,:241] # 0 -180
    v_ERAI[(i-1994)*12:(i-1994)*12+12,:,:,0:239] = v_ERAI_convert[:,:,:,241:] # -180 - 0
    v_ERAI[(i-1994)*12:(i-1994)*12+12,:,:,239:] = v_ERAI_convert[:,:,:,:241] # 0 -180

# mask the values
# np.ma.masked_where(T_ERAI_mask_4D,T_ERAI)
# np.ma.masked_where(T_ERAI_mask_4D,v_ERAI)
# np.ma.set_fill_value(T_ERAI,0)
# np.ma.set_fill_value(v_ERAI,0)

# calculate potential temperature
theta_ERAI = np.zeros(T_ERAI.shape,dtype=float)
theta_MERRA2 = np.zeros(T_MERRA2.shape,dtype=float)

for i in np.arange(len(level_ERAI)):
    theta_ERAI[:,i,:,:] = T_ERAI[:,i,:,:] * (1000/level_ERAI[i])**0.286

for i in np.arange(len(level_MERRA2)):
    theta_MERRA2[:,i,:,:] = T_MERRA2[:,i,:,:] * (1000/level_MERRA2[i])**0.286

# dp
dp_ERAI = np.zeros(level_ERAI.shape)
dp_MERRA2 = np.zeros(level_MERRA2.shape)
for i in np.arange(len(level_ERAI)):
    if i == 0:
        dp_ERAI[i] = level_ERAI[i]
    else:
        dp_ERAI[i] = level_ERAI[i] - level_ERAI[i-1]

for i in np.arange(len(level_MERRA2)):
    if i == len(level_MERRA2) - 1:
        dp_MERRA2[i] = level_MERRA2[i]
    else:
        dp_MERRA2[i] = level_MERRA2[i] - level_MERRA2[i+1]

print '*******************************************************************'
print '************************ data preparation *************************'
print '*******************************************************************'
# # zonal mean at 60N July
# T_zonal_ERAI = np.mean(T_ERAI,2)
# T_zonal_MERRA2 = np.mean(T_MERRA2,2)
# v_zonal_ERAI = np.mean(v_ERAI,2)
# v_zonal_MERRA2 = np.mean(v_MERRA2,2)
# # vertical mean at 60N July
# T_vert_ERAI_weight = np.zeros(T_ERAI.shape)
# T_vert_MERRA2_weight = np.zeros(T_MERRA2.shape)
# v_vert_ERAI_weight = np.zeros(v_ERAI.shape)
# v_vert_MERRA2_weight = np.zeros(T_MERRA2.shape)
#
# for i in np.arange(len(level_ERAI)):
#     T_vert_ERAI_weight[i,:,:] = T_ERAI[i,:,:] * dp_ERAI[i]
#     v_vert_ERAI_weight[i,:,:] = v_ERAI[i,:,:] * dp_ERAI[i]
#
# for i in np.arange(len(level_MERRA2)):
#     T_vert_MERRA2_weight[i,:,:] = T_MERRA2[i,:,:] * dp_MERRA2[i]
#     v_vert_MERRA2_weight[i,:,:] = v_MERRA2[i,:,:] * dp_MERRA2[i]
#
# T_vert_ERAI = np.sum(T_vert_ERAI_weight,0)/level_ERAI[-1]
# T_vert_MERRA2 = np.sum(T_vert_MERRA2_weight,0)/level_MERRA2[0]
# v_vert_ERAI = np.sum(v_vert_ERAI_weight,0)/level_ERAI[-1]
# v_vert_MERRA2 = np.sum(v_vert_MERRA2_weight,0)/level_MERRA2[0]

print '*******************************************************************'
print '********************** horizontal profile *************************'
print '*******************************************************************'
########################      control panel      #########################
# time: 1997.07 lat lon : 20N - 80N

##########################################################################
print 'Contour plots for certain fields'

# print 'Dot plots of the integral of variables'
# # temperature
# fig1 = plt.figure()
# #plt.axhline(y=0, color='k',ls='-')
# plt.scatter(longitude_ERAI,T_vert_ERAI[40,:],c='c',marker='.',label='ERA-Interim')
# plt.scatter(longitude_MERRA2,T_vert_MERRA2[80,:],c='m',marker='.',label='MERRA2')
# plt.title('Monthly Mean T Field of 1997-07 at 60N (horizontal profile)' )
# fig1.set_size_inches(8, 5)
# #plt.legend()
# plt.xlabel("Longitude")
# #plt.xticks()
# plt.ylabel("Temperature (Celsius)")
# plt.legend()
# plt.show()
# fig1.savefig(output_path + os.sep + 'Comp_var_monthly_vert_mean_T_199707_60N.jpg', dpi = 500)
#
# # velocity
# # meridional velocity time: 2001.01 lat lon : 60N
# fig2 = plt.figure()
# plt.axhline(y=0, color='k',ls='-')
# plt.scatter(longitude_ERAI,v_vert_ERAI[40,:],c='c',marker='.',label='ERA-Interim')
# plt.scatter(longitude_MERRA2,v_vert_MERRA2[80,:],c='m',marker='.',label='MERRA2')
# plt.title('Monthly Mean v Field of 1997-07 at 60N (horizontal profile)' )
# fig2.set_size_inches(8, 5)
# #plt.legend()
# plt.xlabel("Longitude")
# #plt.xticks()
# plt.ylabel("Meridional Wind Velocity (m/s)")
# plt.legend()
# plt.show()
# fig2.savefig(output_path + os.sep + 'Comp_var_monthly_vert_mean_v_199707_60N.jpg', dpi = 500)

print '*******************************************************************'
print '*********************** vertical profile **************************'
print '*******************************************************************'

print '*******************************************************************'
print '************         1997.07 instaneous fields        *************'

print 'Contour plots for temperature fields'
for c in np.arange(len(lat_interest_list)):
    fig0 = plt.figure()
    X , Y = np.meshgrid(longitude_ERAI,level_ERAI)
    contour_level = np.arange(-90,30,3)
    #plt.contour(X,Y,T_ERAI[:,lat_ERAI_60,:],linewidth= 0.2)
    #cs = plt.contourf(X,Y,T_ERAI[42,:,lat_ERAI_60,:]- 273.15,contour_level,linewidth= 0.2,cmap='coolwarm')
    cs = plt.contourf(X,Y,np.ma.masked_where(T_ERAI_mask[:,lat_interest['ERAI'][c],:],T_ERAI[42,:,lat_interest['ERAI'][c],:]- 273.15),contour_level,linewidth= 0.2,cmap='coolwarm')
    plt.title('Vertical profile of temperature (ERA-interim)(1997.7) at %dN' % (lat_interest_list[c]),fontsize = 7,y=0.93)
    plt.xlabel("Longitude")
    plt.xticks(np.linspace(-180,180,13))
    plt.ylabel("pressure (hPa)")
    cbar = plt.colorbar(orientation='horizontal')
    cbar.set_label('Temperature (Celsius)')
    #invert the y axis
    plt.gca().invert_yaxis()
    plt.show()
    fig0.savefig(output_path + os.sep + 'T' + os.sep + "Comp_var_monthly_ERAI_vert_distrib_T_199707_60N.png",dpi=300)

fig1 = plt.figure()
X , Y = np.meshgrid(longitude_MERRA2,level_MERRA2)
contour_level = np.arange(-90,30,3)
#plt.contour(X,Y,T_ERAI[:,lat_ERAI_60,:],linewidth= 0.2)
cs = plt.contourf(X,Y,T_MERRA2[42,:,lat_MERRA2_60,:]- 273.15,contour_level,linewidth= 0.2,cmap='coolwarm')
plt.title('Vertical profile of temperature (MERRA2)(1997.7)')
plt.xlabel("Longitude")
plt.xticks(np.linspace(-180,180,13))
plt.ylabel("Pressure (hPa)")
cbar = plt.colorbar(orientation='horizontal')
cbar.set_label('Temperature (Celsius)')
#invert the y axis
plt.gca().invert_yaxis()
plt.show()
fig1.savefig(output_path + os.sep + "Comp_var_monthly_MERRA2_vert_distrib_T_199707_60N.png",dpi=300)

print 'Contour plots for meridional velocity fields'
fig2 = plt.figure()
X , Y = np.meshgrid(longitude_ERAI,level_ERAI)
contour_level = np.arange(-30,30,1)
#plt.contour(X,Y,T_ERAI[:,lat_ERAI_60,:],linewidth= 0.2)
cs = plt.contourf(X,Y,np.ma.masked_where(T_ERAI_mask[:,lat_ERAI_60,:],v_ERAI[42,:,lat_ERAI_60,:]),contour_level,linewidth= 0.2,cmap='coolwarm')
plt.title('Vertical profile of meridional velocity (ERA-interim)(1997.7)')
plt.xlabel("Longitude")
plt.xticks(np.linspace(-180,180,13))
plt.ylabel("Pressure (hPa)")
cbar = plt.colorbar(orientation='horizontal')
cbar.set_label('Meridional velocity (m/s)')
#invert the y axis
plt.gca().invert_yaxis()
plt.show()
fig2.savefig(output_path + os.sep + "Comp_var_monthly_ERAI_vert_distrib_v_199707_60N.png",dpi=300)

fig3 = plt.figure()
X , Y = np.meshgrid(longitude_MERRA2,level_MERRA2)
contour_level = np.arange(-30,30,1)
#plt.contour(X,Y,T_ERAI[:,lat_ERAI_60,:],linewidth= 0.2)
cs = plt.contourf(X,Y,v_MERRA2[42,:,lat_MERRA2_60,:],contour_level,linewidth= 0.2,cmap='coolwarm')
plt.title('Vertical profile of meridional velocity (MERRA2)(1997.7)')
plt.xlabel("Longitude")
plt.xticks(np.linspace(-180,180,13))
plt.ylabel("pressure (hPa)")
cbar = plt.colorbar(orientation='horizontal')
cbar.set_label('Meridional velocity (m/s)')
#invert the y axis
plt.gca().invert_yaxis()
plt.show()
fig3.savefig(output_path + os.sep + "Comp_var_monthly_MERRA2_vert_distrib_v_199707_60N.png",dpi=300)

print '*******************************************************************'
print '*********      1994.01 - 1998.12 annual mean fields      **********'

print 'Contour plots for temperature fields'
fig4 = plt.figure()
X , Y = np.meshgrid(longitude_ERAI,level_ERAI)
contour_level = np.arange(-90,30,3)
#plt.contour(X,Y,T_ERAI[:,lat_ERAI_60,:],linewidth= 0.2)
#cs = plt.contourf(X,Y,T_ERAI[42,:,lat_ERAI_60,:]- 273.15,contour_level,linewidth= 0.2,cmap='coolwarm')
cs = plt.contourf(X,Y,np.ma.masked_where(T_ERAI_mask[:,lat_ERAI_60,:],T_ERAI[42,:,lat_ERAI_60,:]- 273.15),contour_level,linewidth= 0.2,cmap='coolwarm')
plt.title('Vertical profile of temperature (ERA-interim)(1997.7)')
plt.xlabel("Longitude")
plt.xticks(np.linspace(-180,180,13))
plt.ylabel("pressure (hPa)")
cbar = plt.colorbar(orientation='horizontal')
cbar.set_label('Temperature (Celsius)')
#invert the y axis
plt.gca().invert_yaxis()
plt.show()
fig4.savefig(output_path + os.sep + "Comp_var_monthly_ERAI_vert_distrib_T_1994_1998_60N.png",dpi=300)

fig5 = plt.figure()
X , Y = np.meshgrid(longitude_MERRA2,level_MERRA2)
contour_level = np.arange(-90,30,3)
#plt.contour(X,Y,T_ERAI[:,lat_ERAI_60,:],linewidth= 0.2)
cs = plt.contourf(X,Y,T_MERRA2[42,:,lat_MERRA2_60,:]- 273.15,contour_level,linewidth= 0.2,cmap='coolwarm')
plt.title('Vertical profile of temperature (MERRA2)(1997.7)')
plt.xlabel("Longitude")
plt.xticks(np.linspace(-180,180,13))
plt.ylabel("Pressure (hPa)")
cbar = plt.colorbar(orientation='horizontal')
cbar.set_label('Temperature (Celsius)')
#invert the y axis
plt.gca().invert_yaxis()
plt.show()
fig5.savefig(output_path + os.sep + "Comp_var_monthly_MERRA2_vert_distrib_T_1994_1998_60N.png",dpi=300)

print 'Contour plots for meridional velocity fields'
fig6 = plt.figure()
X , Y = np.meshgrid(longitude_ERAI,level_ERAI)
contour_level = np.arange(-30,30,1)
#plt.contour(X,Y,T_ERAI[:,lat_ERAI_60,:],linewidth= 0.2)
cs = plt.contourf(X,Y,np.ma.masked_where(T_ERAI_mask[:,lat_ERAI_60,:],v_ERAI[42,:,lat_ERAI_60,:]),contour_level,linewidth= 0.2,cmap='coolwarm')
plt.title('Vertical profile of meridional velocity (ERA-interim)(1997.7)')
plt.xlabel("Longitude")
plt.xticks(np.linspace(-180,180,13))
plt.ylabel("Pressure (hPa)")
cbar = plt.colorbar(orientation='horizontal')
cbar.set_label('Meridional velocity (m/s)')
#invert the y axis
plt.gca().invert_yaxis()
plt.show()
fig6.savefig(output_path + os.sep + "Comp_var_monthly_ERAI_vert_distrib_v_1994_1998_60N.png",dpi=300)

fig7 = plt.figure()
X , Y = np.meshgrid(longitude_MERRA2,level_MERRA2)
contour_level = np.arange(-30,30,1)
#plt.contour(X,Y,T_ERAI[:,lat_ERAI_60,:],linewidth= 0.2)
cs = plt.contourf(X,Y,v_MERRA2[42,:,lat_MERRA2_60,:],contour_level,linewidth= 0.2,cmap='coolwarm')
plt.title('Mean Vertical profile of meridional velocity (MERRA2) from 1994 to 1998')
plt.xlabel("Longitude")
plt.xticks(np.linspace(-180,180,13))
plt.ylabel("pressure (hPa)")
cbar = plt.colorbar(orientation='horizontal')
cbar.set_label('Meridional velocity (m/s)')
#invert the y axis
plt.gca().invert_yaxis()
plt.show()
fig7.savefig(output_path + os.sep + "Comp_var_monthly_MERRA2_vert_distrib_v_1994_1998_60N.png",dpi=300)

# print 'Dot plots of the integral of variables'
# # temperature
# fig3 = plt.figure()
# #plt.axhline(y=0, color='k',ls='-')
# #plt.scatter(depth_ORAS4,theta_glo_zonal_ORAS4[43,0,:,233],c='c',marker='o',label='ORAS4')
# #plt.scatter(depth_GLORYS2V3,theta_glo_zonal_GLORYS2V3[8,0,:,788],c='m',marker='o',label='GLORYS2V3')
# plt.scatter(T_zonal_ERAI[:,40],level_ERAI,c='c',marker='.',label='ERA-Interim')
# plt.scatter(T_zonal_MERRA2[:,80],level_MERRA2,c='m',marker='.',label='MERRA2')
# plt.title('Monthly Mean T Field of 1997-07 at 60N (vertical profile)' )
# fig3.set_size_inches(5, 8)
# #plt.legend()
# plt.xlabel("Temperature (Celsius)")
# #plt.xticks()
# plt.ylabel("Height (hPa)")
# plt.legend()
# #invert the y axis
# plt.gca().invert_yaxis()
# plt.show()
# fig3.savefig(output_path + os.sep + 'Comp_var_monthly_zonal_mean_T_199707_60N.jpg', dpi = 500)
#
# fig4 = plt.figure()
# #plt.axhline(y=0, color='k',ls='-')
# plt.scatter(v_zonal_ERAI[:,40],level_ERAI,c='c',marker='.',label='ORAS4')
# plt.scatter(v_zonal_MERRA2[:,80],level_MERRA2,c='m',marker='.',label='GLORYS2V3')
# plt.title('Monthly Mean v Field of 1997-07 at 60N (vertical profile)' )
# fig4.set_size_inches(5, 8)
# #plt.legend()
# plt.xlabel("Meridional Wind Velocity (m/s)")
# #plt.xticks()
# plt.ylabel("Height (hPa)")
# plt.legend()
# #invert the y axis
# plt.gca().invert_yaxis()
# plt.show()
# fig4.savefig(output_path + os.sep + 'Comp_var_monthly_zonal_mean_v_199707_60N.jpg', dpi = 500)
