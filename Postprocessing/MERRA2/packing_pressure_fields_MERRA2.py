#!/usr/bin/env python
"""
Copyright Netherlands eScience Center

Function        : Packing the climate fields on pressure level 200hPa 500hPa and 850hPa
Author          : Yang Liu
Date            : 2018.03.22
Last Update     : 2018.03.22
Description     : The code aims to pack the climate fields on pressure level from
                  reanalysis product MERRA2. For the purpose of post-processing, we
                  take the variabels on 3 levels, which are 200hPa (tropopause),
                  500hPa (mid-troposphere) and 850hPa (low-troposphere)

Return Value    : netCDF
Dependencies    : os, time, numpy, scipy, netCDF4, matplotlib, basemap
variables       : Absolute Temperature              T         [K]
                  Specific Humidity                 QV         [kg/kg]
                  Surface Pressure                  ps        [Pa]
                  Zonal Divergent Wind              u         [m/s]
                  Meridional Divergent Wind         v         [m/s]
		          Geopotential Height  	            H         [m]
Caveat!!        : The data used here is actually analysis rather than assimilation.
                  Assimilation includes adjustment from model after data assimilation,
                  whereas the analysis doesn't. However, since the geopotential is only
                  provided for the analysis, we will take it.
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
# specify starting and ending time
start_year = 1980
end_year = 2016
# specify data path
# MERRA2 3D fields on pressure level
datapath = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/MERRA2/regression/MERRA2_instM_3d_ana_Np'
# specify output path for figures
output_path = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/MERRA2/regression'
####################################################################################

def var_key_retrieve(datapath, year, month):
    # get the path to each datasets
    print "Start retrieving datasets %d (y) - %s (m)" % (year,namelist_month[month-1])
    # The shape of each variable is (361,576)
    # Sea Level Pressure
    if year < 1992:
        datapath = datapath + os.sep + 'MERRA2_100.instM_3d_ana_Np.%d%s.SUB.nc' % (year,namelist_month[month-1])
    elif year < 2001:
        datapath = datapath + os.sep + 'MERRA2_200.instM_3d_ana_Np.%d%s.SUB.nc' % (year,namelist_month[month-1])
    elif year < 2011:
        datapath = datapath + os.sep + 'MERRA2_300.instM_3d_ana_Np.%d%s.SUB.nc' % (year,namelist_month[month-1])
    else:
        datapath = datapath + os.sep + 'MERRA2_400.instM_3d_ana_Np.%d%s.SUB.nc' % (year,namelist_month[month-1])
    # get the variable keys
    var_key = Dataset(datapath)

    print "Retrieving datasets successfully and return the variable key!"
    return var_key

# save output datasets
def create_netcdf_point (pool_H, pool_QV, pool_T, pool_U, pool_V, layer, output_path):
    print '*******************************************************************'
    print '*********************** create netcdf file*************************'
    print '*******************************************************************'
    logging.info("Start creating netcdf file for the 2D fields of MERRA2 at each grid point.")
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path + os.sep + 'pressure_%s_MERRA2_monthly_regress_1980_2016.nc' % (layer),'w',format = 'NETCDF3_64BIT')
    # create dimensions for netcdf data
    year_wrap_dim = data_wrap.createDimension('year',Dim_year)
    month_wrap_dim = data_wrap.createDimension('month',Dim_month)
    lat_wrap_dim = data_wrap.createDimension('latitude',Dim_latitude)
    lon_wrap_dim = data_wrap.createDimension('longitude',Dim_longitude)
    # create coordinate variables for 3-dimensions
    year_wrap_var = data_wrap.createVariable('year',np.int32,('year',))
    month_wrap_var = data_wrap.createVariable('month',np.int32,('month',))
    lat_wrap_var = data_wrap.createVariable('latitude',np.float32,('latitude',))
    lon_wrap_var = data_wrap.createVariable('longitude',np.float32,('longitude',))
    # create the actual 3-d variable
    H_wrap_var = data_wrap.createVariable('H',np.float64,('year','month','latitude','longitude'))
    QV_wrap_var = data_wrap.createVariable('QV',np.float64,('year','month','latitude','longitude'))
    T_wrap_var = data_wrap.createVariable('T',np.float64,('year','month','latitude','longitude'))
    U_wrap_var = data_wrap.createVariable('U',np.float64,('year','month','latitude','longitude'))
    V_wrap_var = data_wrap.createVariable('V',np.float64,('year','month','latitude','longitude'))
    # global attributes
    data_wrap.description = 'Monthly mean 3D fields of MERRA2 on pressure level %s' % (layer)
    # variable attributes
    lat_wrap_var.units = 'degree_north'
    lon_wrap_var.units = 'degree_east'

    H_wrap_var.units = 'm'
    QV_wrap_var.units = 'kg/kg'
    T_wrap_var.units = 'Kelvin'
    U_wrap_var.units = 'm/s'
    V_wrap_var.units = 'm/s'

    H_wrap_var.long_name = 'geopotential height'
    QV_wrap_var.long_name = 'specific humidity'
    T_wrap_var.long_name = 'temperature'
    U_wrap_var.long_name = 'zonal velocity'
    V_wrap_var.long_name = 'meridional velocity'

    # writing data
    lat_wrap_var[:] = latitude
    lon_wrap_var[:] = longitude
    month_wrap_var[:] = index_month
    year_wrap_var[:] = period

    H_wrap_var[:] = pool_H
    QV_wrap_var[:] = pool_QV
    T_wrap_var[:] = pool_T
    U_wrap_var[:] = pool_U
    V_wrap_var[:] = pool_V

    # close the file
    data_wrap.close()
    print "The generation of netcdf files for fields on pressure level %s is complete!!" % (layer)

if __name__=="__main__":
    ####################################################################
    ######  Create time namelist matrix for variable extraction  #######
    ####################################################################
    # date and time arrangement
    # namelist of month and days for file manipulation
    namelist_month = ['01','02','03','04','05','06','07','08','09','10','11','12']
    # index of months
    period = np.arange(start_year,end_year+1,1)
    index_month = np.arange(1,13,1)
    ###########################################################for zonal integral#########
    ######       Extract invariant and calculate constants       #######
    ####################################################################
    # get invariant from benchmark file
    Dim_year = len(period)
    Dim_month = len(index_month)
    Dim_latitude = 361
    Dim_longitude = 576
    #############################################
    #####   Create space for stroing data   #####
    #############################################
    # data pool
    pool_H = {}
    pool_H['200hPa'] = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    pool_H['500hPa'] = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    pool_H['850hPa'] = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)

    pool_QV = {}
    pool_QV['200hPa'] = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    pool_QV['500hPa'] = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    pool_QV['850hPa'] = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)

    pool_T = {}
    pool_T['200hPa'] = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    pool_T['500hPa'] = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    pool_T['850hPa'] = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)

    pool_U = {}
    pool_U['200hPa'] = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    pool_U['500hPa'] = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    pool_U['850hPa'] = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)

    pool_V = {}
    pool_V['200hPa'] = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    pool_V['500hPa'] = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    pool_V['850hPa'] = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)

    latitude = np.zeros(Dim_latitude,dtype=float)
    longitude = np.zeros(Dim_longitude,dtype=float)

    # loop for calculation
    for i in period:
        for j in index_month:
                # get the key of each variable
            var_key = var_key_retrieve(datapath,i,j)
            latitude = var_key.variables['lat'][:]
            longitude = var_key.variables['lon'][:]
            # 200hPA
            pool_H['200hPa'][i-1980,j-1,:,:] = var_key.variables['H'][0,2,:,:]
            pool_QV['200hPa'][i-1980,j-1,:,:] = var_key.variables['QV'][0,2,:,:]
            pool_T['200hPa'][i-1980,j-1,:,:] = var_key.variables['T'][0,2,:,:]
            pool_U['200hPa'][i-1980,j-1,:,:] = var_key.variables['U'][0,2,:,:]
            pool_V['200hPa'][i-1980,j-1,:,:] = var_key.variables['V'][0,2,:,:]
            # 500hPA
            pool_H['500hPa'][i-1980,j-1,:,:] = var_key.variables['H'][0,1,:,:]
            pool_QV['500hPa'][i-1980,j-1,:,:] = var_key.variables['QV'][0,1,:,:]
            pool_T['500hPa'][i-1980,j-1,:,:] = var_key.variables['T'][0,1,:,:]
            pool_U['500hPa'][i-1980,j-1,:,:] = var_key.variables['U'][0,1,:,:]
            pool_V['500hPa'][i-1980,j-1,:,:] = var_key.variables['V'][0,1,:,:]
            # 850hPA
            pool_H['850hPa'][i-1980,j-1,:,:] = var_key.variables['H'][0,0,:,:]
            pool_QV['850hPa'][i-1980,j-1,:,:] = var_key.variables['QV'][0,0,:,:]
            pool_T['850hPa'][i-1980,j-1,:,:] = var_key.variables['T'][0,0,:,:]
            pool_U['850hPa'][i-1980,j-1,:,:] = var_key.variables['U'][0,0,:,:]
            pool_V['850hPa'][i-1980,j-1,:,:] = var_key.variables['V'][0,0,:,:]
    ####################################################################
    ######                 Data Wrapping (NetCDF)                #######
    ####################################################################
    level_list = ['200hPA','500hPA','850hPA']
    for i in level_list:
        create_netcdf_point(pool_H['%s' % (i)][:], pool_QV['%s' % (i)][:], pool_T['%s' % (i)][:],
                            pool_U['%s' % (i)][:], pool_V['%s' % (i)][:], i, output_path)
    print 'Packing 3D fields of MERRA2 on pressure level is complete!!!'
    print 'The output is in sleep, safe and sound!!!'

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
