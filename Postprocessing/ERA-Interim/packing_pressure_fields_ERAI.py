#!/usr/bin/env python
"""
Copyright Netherlands eScience Center

Function        : Packing the climate fields on pressure level 200hPa 500hPa and 850hPa
Author          : Yang Liu
Date            : 2018.03.22
Last Update     : 2018.04.20
Description     : The code aims to pack the climate fields on pressure level from
                  reanalysis product ERA-Interim. For the purpose of post-processing,
                  we take the variabels on 3 levels, which are 200hPa (tropopause, 10km),
                  500hPa (mid-troposphere, 5km) and 850hPa (low-troposphere, 1km)

Return Value    : netCDF
Dependencies    : os, time, numpy, scipy, netCDF4, matplotlib, basemap
variables       : Absolute Temperature              T         [K]
                  Specific Humidity                 q         [kg/kg]
                  Surface Pressure                  ps        [Pa]
                  Zonal Divergent Wind              u         [m/s]
                  Meridional Divergent Wind         v         [m/s]
		          Geopotential  	                z         [m2/s2]
Caveat!!        :
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
start_year = 1979
end_year = 2016
# specify data path
# ERAI 3D fields on pressure level
datapath = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ERAI/regression/pressure'
# specify output path for figures
output_path = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ERAI/regression'
####################################################################################

def var_key_retrieve(datapath, year):
    # get the path to each datasets
    print "Start retrieving datasets %d (y)" % (year)
    # The shape of each variable is (241,480)
    datapath = datapath + os.sep + 'pressure_monthly_075_%d_200_500_850.nc' % (year)
    # get the variable keys
    var_key = Dataset(datapath)

    print "Retrieving datasets successfully and return the variable key!"
    return var_key

# save output datasets
def create_netcdf_point (pool_z, pool_q, pool_t, pool_u, pool_v, layer, output_path):
    print '*******************************************************************'
    print '*********************** create netcdf file*************************'
    print '*******************************************************************'
    logging.info("Start creating netcdf file for the 2D fields of ERAI at each grid point.")
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path + os.sep + 'pressure_%s_ERAI_monthly_regress_1979_2016.nc' % (layer),'w',format = 'NETCDF4')
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
    z_wrap_var = data_wrap.createVariable('z',np.float64,('year','month','latitude','longitude'),zlib=True)
    q_wrap_var = data_wrap.createVariable('q',np.float64,('year','month','latitude','longitude'),zlib=True)
    t_wrap_var = data_wrap.createVariable('t',np.float64,('year','month','latitude','longitude'),zlib=True)
    u_wrap_var = data_wrap.createVariable('u',np.float64,('year','month','latitude','longitude'),zlib=True)
    v_wrap_var = data_wrap.createVariable('v',np.float64,('year','month','latitude','longitude'),zlib=True)
    # global attributes
    data_wrap.description = 'Monthly mean 3D fields of ERA-Interim on pressure level %s' % (layer)
    # variable attributes
    lat_wrap_var.units = 'degree_north'
    lon_wrap_var.units = 'degree_east'

    z_wrap_var.units = 'm2/s2'
    q_wrap_var.units = 'kg/kg'
    t_wrap_var.units = 'Kelvin'
    u_wrap_var.units = 'm/s'
    v_wrap_var.units = 'm/s'

    z_wrap_var.long_name = 'geopotential height'
    q_wrap_var.long_name = 'specific humidity'
    t_wrap_var.long_name = 'temperature'
    u_wrap_var.long_name = 'zonal velocity'
    v_wrap_var.long_name = 'meridional velocity'

    # writing data
    lat_wrap_var[:] = latitude
    lon_wrap_var[:] = longitude
    month_wrap_var[:] = index_month
    year_wrap_var[:] = period

    z_wrap_var[:] = pool_z
    q_wrap_var[:] = pool_q
    t_wrap_var[:] = pool_t
    u_wrap_var[:] = pool_u
    v_wrap_var[:] = pool_v

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
    Dim_latitude = 241
    Dim_longitude = 480
    #############################################
    #####   Create space for stroing data   #####
    #############################################
    # data pool
    pool_z = {}
    pool_z['200hPa'] = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    pool_z['500hPa'] = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    pool_z['850hPa'] = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)

    pool_q = {}
    pool_q['200hPa'] = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    pool_q['500hPa'] = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    pool_q['850hPa'] = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)

    pool_t = {}
    pool_t['200hPa'] = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    pool_t['500hPa'] = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    pool_t['850hPa'] = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)

    pool_u = {}
    pool_u['200hPa'] = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    pool_u['500hPa'] = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    pool_u['850hPa'] = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)

    pool_v = {}
    pool_v['200hPa'] = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    pool_v['500hPa'] = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    pool_v['850hPa'] = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)

    latitude = np.zeros(Dim_latitude,dtype=float)
    longitude = np.zeros(Dim_longitude,dtype=float)

    # loop for calculation
    for i in period:
        # get the key of each variable
        var_key = var_key_retrieve(datapath,i)
        latitude = var_key.variables['latitude'][:]
        longitude = var_key.variables['longitude'][:]
        # 200hPA
        pool_z['200hPa'][i-1979,:,:,:] = var_key.variables['z'][:,0,:,:]
        pool_q['200hPa'][i-1979,:,:,:] = var_key.variables['q'][:,0,:,:]
        pool_t['200hPa'][i-1979,:,:,:] = var_key.variables['t'][:,0,:,:]
        pool_u['200hPa'][i-1979,:,:,:] = var_key.variables['u'][:,0,:,:]
        pool_v['200hPa'][i-1979,:,:,:] = var_key.variables['v'][:,0,:,:]
        # 500hPA
        pool_z['500hPa'][i-1979,:,:,:] = var_key.variables['z'][:,1,:,:]
        pool_q['500hPa'][i-1979,:,:,:] = var_key.variables['q'][:,1,:,:]
        pool_t['500hPa'][i-1979,:,:,:] = var_key.variables['t'][:,1,:,:]
        pool_u['500hPa'][i-1979,:,:,:] = var_key.variables['u'][:,1,:,:]
        pool_v['500hPa'][i-1979,:,:,:] = var_key.variables['v'][:,1,:,:]
        # 850hPA
        pool_z['850hPa'][i-1979,:,:,:] = var_key.variables['z'][:,2,:,:]
        pool_q['850hPa'][i-1979,:,:,:] = var_key.variables['q'][:,2,:,:]
        pool_t['850hPa'][i-1979,:,:,:] = var_key.variables['t'][:,2,:,:]
        pool_u['850hPa'][i-1979,:,:,:] = var_key.variables['u'][:,2,:,:]
        pool_v['850hPa'][i-1979,:,:,:] = var_key.variables['v'][:,2,:,:]
    ####################################################################
    ######                 Data Wrapping (NetCDF)                #######
    ####################################################################
    level_list = ['200hPa','500hPa','850hPa']
    for i in level_list:
        create_netcdf_point(pool_z['%s' % (i)][:], pool_q['%s' % (i)][:], pool_t['%s' % (i)][:],
                            pool_u['%s' % (i)][:], pool_v['%s' % (i)][:], i, output_path)
    print 'Packing 3D fields of ERA-Interim on pressure level is complete!!!'
    print 'The output is in sleep, safe and sound!!!'

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
