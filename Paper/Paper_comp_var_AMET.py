#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : Compare oceanic variable fields (MERRA2,ERA-Interim,JRA55)
Author          : Yang Liu
Date            : 2018.06.06
Last Update     : 2018.07.19
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
import scipy
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
#sns.set_style("ticks")
#sns.despine()

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
output_path = '/home/yang/NLeSC/PhD/Paperwork/Article/AMET_OMET/figures'
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

# get the mask from MERRA2
T_MERRA2_sample = dataset_MERRA2.variables['T'][0,:,:,:]
v_MERRA2_sample = dataset_MERRA2.variables['V'][0,:,:,:]
T_MERRA2_mask = np.zeros((len(level_MERRA2),len(latitude_MERRA2),len(longitude_MERRA2)),dtype=int)
v_MERRA2_mask = np.zeros((len(level_MERRA2),len(latitude_MERRA2),len(longitude_MERRA2)),dtype=int)
for i in np.arange(len(level_MERRA2)):
    T_MERRA2_mask[i,:,:] = np.ma.getmaskarray(T_MERRA2_sample[i,:,:])
    v_MERRA2_mask[i,:,:] = np.ma.getmaskarray(v_MERRA2_sample[i,:,:])

month_ind = np.arange(12)
year_ind = np.arange(1994,1999,1)

# surface pressure for mask
sp_ERAI_convert = dataset_ERAI_surface.variables['sp'][222,0:95,:] / 100 # 1997.07
sp_ERAI = np.zeros(sp_ERAI_convert.shape,dtype=float)
sp_ERAI[:,0:239] = sp_ERAI_convert[:,241:]
sp_ERAI[:,239:] = sp_ERAI_convert[:,:241]
T_ERAI_mask = np.zeros((len(level_ERAI),len(latitude_ERAI),len(longitude_ERAI)),dtype=int)
for i in np.arange(len(level_ERAI)):
    T_ERAI_mask[i,sp_ERAI[:]<level_ERAI[i]] = 1 # mask the point where surface pressure is smaller than certain level pressure

# # Extend the mask to 4D for masking
# T_ERAI_mask_4D = np.repeat(T_ERAI_mask[np.newaxis,:,:,:],len(year_ind)*len(month_ind),0)

print '*******************************************************************'
print '************            Extract variabels!            *************'
print '*******************************************************************'
namelist_month = ['01','02','03','04','05','06','07','08','09','10','11','12']
# MERRA2
T_MERRA2 = np.zeros((len(year_ind)*len(month_ind),len(level_MERRA2),len(latitude_MERRA2),len(longitude_MERRA2)),dtype=float)
v_MERRA2 = np.zeros((len(year_ind)*len(month_ind),len(level_MERRA2),len(latitude_MERRA2),len(longitude_MERRA2)),dtype=float)
for i in year_ind:
    for j in month_ind:
        dataset_MERRA2 = Dataset(datapath_MERRA2 + os.sep + 'MERRA2_200.instM_3d_asm_Np.{}{}.SUB.nc4'.format(i,namelist_month[j]))
        # Since we dispatch the fields in MERRA2 to a different matrix, which is defined as numpy array
        # there is no mask in this array. Hence there is no filled values.
        T_MERRA2[(i-1994)*12+j,:,:,:] = dataset_MERRA2.variables['T'][0,:,:,:]
        v_MERRA2[(i-1994)*12+j,:,:,:] = dataset_MERRA2.variables['V'][0,:,:,:]

T_MERRA2[T_MERRA2>5000] = 0
v_MERRA2[v_MERRA2>5000] = 0

#np.ma.set_fill_value(T_MERRA2,0)
#np.ma.set_fill_value(v_MERRA2,0)

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

# calculate potential temperature
theta_ERAI = np.zeros(T_ERAI.shape,dtype=float)
theta_MERRA2 = np.zeros(T_MERRA2.shape,dtype=float)

for i in np.arange(len(level_ERAI)):
    theta_ERAI[:,i,:,:] = T_ERAI[:,i,:,:] * (1000.0/level_ERAI[i])**0.286

for i in np.arange(len(level_MERRA2)):
    theta_MERRA2[:,i,:,:] = T_MERRA2[:,i,:,:] * (1000/level_MERRA2[i])**0.286

theta_MERRA2[theta_MERRA2>5000] = 0

#np.ma.set_fill_value(theta_MERRA2,0)
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

def contour_plot(fields,longitude,level,contour_level,contourf_level,title,c_label,output,cmap):
    fig0 = plt.figure()
    X , Y = np.meshgrid(longitude,level)
    cs = plt.contour(X,Y,fields,contour_level, linewidth= 0.1, extend='both',color='k')
    #plt.clabel(cs, inline=1, format="%.1f", fontsize=8)
    cs = plt.contourf(X,Y,fields,contourf_level, linewidth= 0.2, extend='both',cmap=cmap)
    fig0.set_size_inches(6.5, 5)
    plt.xlabel("Longitude",fontsize = 10)
    plt.xticks(np.linspace(-180,180,13),size = 10)
    plt.ylabel("pressure (hPa)",fontsize = 10)
    plt.tick_params(labelsize=10)
    cbar = plt.colorbar(orientation='horizontal')
    cbar.set_label(c_label,size = 10)
    cbar.ax.tick_params(labelsize = 10)
    #invert the y axis
    plt.gca().invert_yaxis()
    plt.show()
    fig0.savefig(output,dpi=400)
    plt.close(fig0)

if __name__=="__main__":
    '''
    This function aims to make plots.
    '''
    contour_level_T = np.arange(-80,40,2)
    # contour_level_theta = np.array([-30,-20,-10,0,1,2,3,4,5,6,7,8,9,10,12,14,16,18,20,
    #                                 25,30,35,40,45,50,55,60,70,80,90,100,120,140,160,180,
    #                                 200,250,300,400],dtype=int)
    contour_level_theta = np.array([-30,-20,-10,0,1,2,3,4,5,6,7,8,9,10,12,14,16,18,20,
                                    25,30,35,40,45,50,55,60,70,80,90,100],dtype=int)
    contour_level_v = np.array([-20,-15,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,
                                8,9,10,15,20],dtype=int)
    contour_minus_theta = np.arange(-2,2.1,0.2)
    contour_minus_v = np.arange(-1,1.1,0.1)
    contour_minus_T = np.arange(-1.0,1.1,0.1)
    contour_minus_vT = np.arange(-200,201,5)
    c_label_T = 'Absolute temperature (Celsius)'
    c_label_theta = 'Potential temperature (Celsius)'
    c_label_v = 'Meridional velocity (m/s)'
    c_label_vT = 'Temperature transport (Celsius m/s)'
    c_label_T_weight = 'Absolute temperature weight by pressure(Celsius hPa)'
    c_label_theta_weight = 'Potential temperature weight by pressure(Celsius hPa)'
    c_label_v_weight = 'Meridional velocity weight by pressure(m hPa/s )'
    c_label_vT_weight = 'Temperature transport weight by pressure(Celsius m hPa/s )'
    cmap_jet = 'jet'
    cmap_coolwarm = 'coolwarm'
    print '*******************************************************************'
    print '********************** horizontal profile *************************'
    print '*******************************************************************'
    #
    print '*******************************************************************'
    print '*********************** vertical profile **************************'
    print '*******************************************************************'
    c = 4 # we only need values at 60N
    print '*********      1994.01 - 1998.12 annual mean fields      **********'
    print '*********            MERRA2 minus ERA-Interim            **********'
    # take out vertical slice
    slice_level_ERAI = [0,1,2,3,4,
                        5,6,7,8,9,
                        10,12,14,16,17,
                        18,19,20,21,22,
                        23,24,25,26,27,
                        28,29,30,31,32,
                        33,34,35,36]
    slice_level_MERRA2 = [36,35,34,32,31,
                          30,29,28,26,25,
                          24,23,22,21,20,
                          19,18,17,16,15,
                          14,13,12,10,9,
                          8,7,6,5,4,
                          3,2,1,0]
    # take the slice of mask and level
    T_ERAI_mask_slice = np.zeros((len(slice_level_ERAI),len(longitude_ERAI)), dtype=int)
    level_ERAI_slice = np.zeros(len(slice_level_ERAI), dtype=int)
    for i in np.arange(len(slice_level_ERAI)):
        T_ERAI_mask_slice[i,:] = T_ERAI_mask[slice_level_ERAI[i],lat_interest['ERAI'][c],:]
        level_ERAI_slice[i] = level_ERAI[slice_level_ERAI[i]]
    # interpolate MERRA2 on ERA-Interim and do the subtraction
    T_MERRA2_interpolate = np.zeros(len(longitude_ERAI),dtype=float)
    theta_MERRA2_interpolate = np.zeros(len(longitude_ERAI),dtype=float)
    v_MERRA2_interpolate = np.zeros(len(longitude_ERAI),dtype=float)

    T_MERRA2_minus_ERAI = np.zeros((len(year_ind)*len(month_ind),len(slice_level_ERAI),len(longitude_ERAI)),dtype=float)
    theta_MERRA2_minus_ERAI = np.zeros((len(year_ind)*len(month_ind),len(slice_level_ERAI),len(longitude_ERAI)),dtype=float)
    v_MERRA2_minus_ERAI = np.zeros((len(year_ind)*len(month_ind),len(slice_level_ERAI),len(longitude_ERAI)),dtype=float)
    # for the temperature transport
    vT_MERRA2_minus_ERAI = np.zeros((len(year_ind)*len(month_ind),len(slice_level_ERAI),len(longitude_ERAI)),dtype=float)

    # determine the comtribution from the difference between temperature or velocity
    # the product of v * delta T and delta v * T
    v_ERAI_delta_T = np.zeros((len(year_ind)*len(month_ind),len(slice_level_ERAI),len(longitude_ERAI)),dtype=float)
    T_ERAI_delta_v = np.zeros((len(year_ind)*len(month_ind),len(slice_level_ERAI),len(longitude_ERAI)),dtype=float)
    # reference v*T from ERAI
    vT_ERAI = np.zeros((len(year_ind)*len(month_ind),len(slice_level_ERAI),len(longitude_ERAI)),dtype=float)

    for i in np.arange(len(year_ind)*len(month_ind)):
        for j in np.arange(len(slice_level_ERAI)):
            # interpolate MERRA2 on ERA-Interim
            ius = scipy.interpolate.interp1d(longitude_MERRA2, T_MERRA2[i,slice_level_MERRA2[j],lat_interest['MERRA2'][c],:], kind='slinear',bounds_error=False, fill_value=0) # fill_value='extrapolate'
            T_MERRA2_interpolate = ius(longitude_ERAI)
            ius = scipy.interpolate.interp1d(longitude_MERRA2, theta_MERRA2[i,slice_level_MERRA2[j],lat_interest['MERRA2'][c],:], kind='slinear',bounds_error=False, fill_value=0)
            theta_MERRA2_interpolate = ius(longitude_ERAI)
            ius = scipy.interpolate.interp1d(longitude_MERRA2, v_MERRA2[i,slice_level_MERRA2[j],lat_interest['MERRA2'][c],:], kind='slinear',bounds_error=False, fill_value=0)
            v_MERRA2_interpolate = ius(longitude_ERAI)

            T_MERRA2_minus_ERAI[i,j,:] = T_MERRA2_interpolate - T_ERAI[i,slice_level_ERAI[j],lat_interest['ERAI'][c],:]
            theta_MERRA2_minus_ERAI[i,j,:] = theta_MERRA2_interpolate - theta_ERAI[i,slice_level_ERAI[j],lat_interest['ERAI'][c],:]
            v_MERRA2_minus_ERAI[i,j,:] = v_MERRA2_interpolate - v_ERAI[i,slice_level_ERAI[j],lat_interest['ERAI'][c],:]
            vT_MERRA2_minus_ERAI[i,j,:] = T_MERRA2_interpolate * v_MERRA2_interpolate - T_ERAI[i,slice_level_ERAI[j],lat_interest['ERAI'][c],:]\
                                          * v_ERAI[i,slice_level_ERAI[j],lat_interest['ERAI'][c],:]
            # diagnostic of the contribution
            v_ERAI_delta_T[i,j,:] = v_ERAI[i,slice_level_ERAI[j],lat_interest['ERAI'][c],:] * T_MERRA2_minus_ERAI[i,j,:]
            T_ERAI_delta_v[i,j,:] = T_ERAI[i,slice_level_ERAI[j],lat_interest['ERAI'][c],:] * v_MERRA2_minus_ERAI[i,j,:]
            vT_ERAI[i,j,:] = v_ERAI[i,slice_level_ERAI[j],lat_interest['ERAI'][c],:] * T_ERAI[i,slice_level_ERAI[j],lat_interest['ERAI'][c],:]
    # correct the subtration due to the interpolation of filled values
    T_MERRA2_minus_ERAI[T_MERRA2_minus_ERAI>30] = 0
    T_MERRA2_minus_ERAI[T_MERRA2_minus_ERAI<-30] = 0
    theta_MERRA2_minus_ERAI[theta_MERRA2_minus_ERAI>30] = 0
    theta_MERRA2_minus_ERAI[theta_MERRA2_minus_ERAI<-30] = 0
    v_MERRA2_minus_ERAI[v_MERRA2_minus_ERAI>30] = 0
    v_MERRA2_minus_ERAI[v_MERRA2_minus_ERAI<-30] = 0
    print '*******************************************************************'
    print '**********    subtraction without weight by pressure     **********'
    # temperature difference
    fields = np.ma.masked_where(T_ERAI_mask_slice,np.mean(T_MERRA2_minus_ERAI,0))
    title = 'Vertical profile of the subtraction of temperature (MERRA2-ERAI)(1994-1998) at {}N'.format(lat_interest_list[c])
    output = os.path.join(output_path,"Comp_var_monthly_MERRA2_minus_ERAI_T_1994_1998_{}N.png".format(lat_interest_list[c]))
    contour_plot(fields,longitude_ERAI,level_ERAI_slice,contour_minus_T[::4],contour_minus_T,title,c_label_T,output,cmap_coolwarm)
    # meridional velocity difference
    fields = np.ma.masked_where(T_ERAI_mask_slice,np.mean(v_MERRA2_minus_ERAI,0))
    title = 'Vertical profile of the subtraction of meridional velocity (MERRA2-ERAI)(1994-1998) at {}N'.format(lat_interest_list[c])
    output = os.path.join(output_path,"Comp_var_monthly_MERRA2_minus_ERAI_v_1994_1998_{}N.png".format(lat_interest_list[c]))
    contour_plot(fields,longitude_ERAI,level_ERAI_slice,contour_minus_v[::4],contour_minus_v,title,c_label_v,output,cmap_coolwarm)
    # v * delta T
    fields = np.ma.masked_where(T_ERAI_mask_slice,np.mean(v_ERAI_delta_T,0))
    title = 'Vertical profile of v(ERAI)*dT(ERAI-MERRA2) (1994-1998) at {}N'.format(lat_interest_list[c])
    output = os.path.join(output_path,"Comp_var_monthly_ERAI_v_delta_T_1994_1998_{}N.png".format(lat_interest_list[c]))
    contour_plot(fields,longitude_ERAI,level_ERAI_slice,contour_minus_vT[::4],contour_minus_vT,title,c_label_vT,output,cmap_coolwarm)
    # delta v * T
    fields = np.ma.masked_where(T_ERAI_mask_slice,np.mean(T_ERAI_delta_v,0))
    title = 'Vertical profile of T(ERAI)*dv(ERAI-MERRA2) (1994-1998) at {}N'.format(lat_interest_list[c])
    output = os.path.join(output_path,"Comp_var_monthly_ERAI_T_delta_v_1994_1998_{}N.png".format(lat_interest_list[c]))
    contour_plot(fields,longitude_ERAI,level_ERAI_slice,contour_minus_vT[::12],contour_minus_vT,title,c_label_vT,output,cmap_coolwarm)
    # v * T from ERAI as reference


print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
