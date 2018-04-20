#!/usr/bin/env python
"""
Copyright Netherlands eScience Center

Function        : Packing 2D fields from ERA-Interim
Author          : Yang Liu
Date            : 2018.03.26
Last Update     : 2018.04.20
Description     : The code aims to pack 2D fields from ERA-Interim for further inspection.
                  The fields of insterest are Surface Temperature (SKT), and 2-meter Air Temperature (T2M), 
                  instantaneous surface sensible heat flux (ISHF), instantaneous moisture flux (IE).
Return Value    : netCDF
Dependencies    : os, time, numpy, scipy, netCDF4, matplotlib, basemap
variables       :
                  2-Meter Air Temperature                       t2m
                  Surface Skin Temperature                      skt

Caveat!!        : The input data of 2D fields cover the entire globe.

                  The datasets covers 1979 - 2016.
"""
import numpy as np
import scipy as sp
import time as tttt
from netCDF4 import Dataset,num2date
import os
import seaborn as sns
import platform
import logging
#import matplotlib
# Generate images without having a window appear
#matplotlib.use('Agg')

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
datapath_ts_t2m = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ERAI/regression/surface/t2m_ts'
datapath_turbulent = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ERAI/regression/surface/turbulent'
# specify output path for figures
output_path = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ERAI/regression'
####################################################################################

def var_key_retrieve(datapath_ts_t2m, datapath_turbulent, year):
    # get the path to each datasets
    print "Start retrieving datasets %d (y)" % (year)
    # The shape of each variable is (241,480)
    datapath_1 = datapath_ts_t2m + os.sep + 'surface_monthly_075_%d_t2m_ts.nc' % (year)
    datapath_2 = datapath_turbulent + os.sep + 'surface_monthly_075_%d_turbulent.nc' % (year)
    # get the variable keys
    var_key_ts_t2m = Dataset(datapath_1)
    var_key_turbulent = Dataset(datapath_2)

    print "Retrieving datasets successfully and return the variable key!"
    return var_key_ts_t2m, var_key_turbulent

# save output datasets
def create_netcdf_point (pool_t2m, pool_ts, pool_sensible, pool_latent, output_path):
    print '*******************************************************************'
    print '*********************** create netcdf file*************************'
    print '*******************************************************************'
    logging.info("Start creating netcdf file for the 2D fields of ERAI at each grid point.")
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path + os.sep + 'surface_ERAI_monthly_regress_1979_2016_extra.nc','w',format = 'NETCDF4')
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
    t2m_wrap_var = data_wrap.createVariable('t2m',np.float64,('year','month','latitude','longitude'),zlib=True)
    ts_wrap_var = data_wrap.createVariable('ts',np.float64,('year','month','latitude','longitude'),zlib=True)
    sensible_wrap_var = data_wrap.createVariable('ishf',np.float64,('year','month','latitude','longitude'),zlib=True)
    latent_wrap_var = data_wrap.createVariable('ie',np.float64,('year','month','latitude','longitude'),zlib=True)
    # global attributes
    data_wrap.description = 'Monthly mean 2D fields of ERA-Interim on surface level'
    # variable attributes
    lat_wrap_var.units = 'degree_north'
    lon_wrap_var.units = 'degree_east'

    t2m_wrap_var.units = 'Kelvin'
    ts_wrap_var.units = 'Kelvin'
    sensible_wrap_var.units = 'W/m2'
    latent_wrap_var.units = 'Kg/s*m2'

    ts_wrap_var.long_name = 'surface skin temperature'
    t2m_wrap_var.long_name = '2-meter air temperature'
    sensible_wrap_var.long_name = 'instantaneous surface sensible heat flux'
    latent_wrap_var.long_name = 'instantaneous moisture flux'

    # writing data
    lat_wrap_var[:] = latitude
    lon_wrap_var[:] = longitude
    month_wrap_var[:] = index_month
    year_wrap_var[:] = period

    ts_wrap_var[:] = pool_ts
    t2m_wrap_var[:] = pool_t2m
    sensible_wrap_var[:] = pool_sensible
    latent_wrap_var[:] = pool_latent

    # close the file
    data_wrap.close()
    print "The generation of netcdf files for fields on surface is complete!!"

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
    ####################################################################
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
    pool_ts = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    pool_t2m = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    pool_sensible = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    pool_latent = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)

    latitude = np.zeros(Dim_latitude,dtype=float)
    longitude = np.zeros(Dim_longitude,dtype=float)
    # loop for calculation
    for i in period:
        # get the key of each variable
        var_key_ts_t2m, var_key_turbulent = var_key_retrieve(datapath_ts_t2m, datapath_turbulent,i)
        latitude = var_key_ts_t2m.variables['latitude'][:]
        longitude = var_key_ts_t2m.variables['longitude'][:]

        pool_ts[i-1979,:,:,:] = var_key_ts_t2m.variables['skt'][:]
        pool_t2m[i-1979,:,:,:] = var_key_ts_t2m.variables['t2m'][:]
        pool_sensible[i-1979,:,:,:] = var_key_turbulent.variables['ishf'][:]
        pool_latent[i-1979,:,:,:] = var_key_turbulent.variables['ie'][:]
    ####################################################################
    ######                 Data Wrapping (NetCDF)                #######
    ####################################################################
    create_netcdf_point(pool_t2m, pool_ts, pool_sensible, pool_latent, output_path)
    print 'Packing 2D fields of ERA-Interim on surface level is complete!!!'
    print 'The output is in sleep, safe and sound!!!'

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
