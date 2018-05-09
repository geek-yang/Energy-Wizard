#!/usr/bin/env python
"""
Copyright Netherlands eScience Center

Function        : Packing temperature transport from NEMO hindcast (NEMO ORCA0083)
Author          : Yang Liu
Date            : 2018.05.07
Last Update     : 2018.05.07
Description     : The code aims to reorganize the output from Ben Moat
                  regarding the computation of temperature transport from
                  NEMO ORCA0083 hindcast.
Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, matplotlib, sys
variables       : Meridional Energy Transport                       E         [Tera-Watt]
                  Meridional Overturning Stream Function (Globe)    Psi       [Sv]
                  Meridional Overturning Stream Function (Atlantic) Psi       [Sv]
                  Ocean Heat Content                                OHC       [J]

Caveat!!        : The data is from 0 deg north to 90 deg north (North Hemisphere).
                  Latitude: North to South(90 to 0)
                  Lontitude: West to East (0 to 360)
"""
import numpy as np
import time as tttt
from netCDF4 import Dataset,num2date
import os
import platform
#import logging
#import matplotlib
# Generate images without having a window appear
#matplotlib.use('Agg')
#import matplotlib.pyplot as plt

# print the system structure and the path of the kernal
print platform.architecture()
print os.path

# calculate the time for the code execution
start_time = tttt.time()
################################   Input zone  ######################################
# specify data path
datapath = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ORCA012_BenMoat/OMET'
# time of the data, which concerns with the name of input
# starting time (year)
start_year = 1979
# Ending time, if only for 1 year, then it should be the same as starting year
end_year = 2012
# specify output path for the netCDF4 file
output_path = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ORCA012_BenMoat/postprocessing'
#output_path_OHC = '/projects/0/blueactn/reanalysis/SODA3/'
# benchmark datasets for basic dimensions
benchmark_path = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ORCA012_BenMoat/OMET/vel_T_ORCA0083_select_1980.nc'
benchmark = Dataset(benchmark_path)
####################################################################################
# dimension
jj = 1565
ji = 4322
level = 75
# namelist of month and days for file manipulation
# function for packing zonal int data
def pack_netcdf_zonal_int(E_zonal_int, latitude_aux, output_path):
    print '*******************************************************************'
    print '*********************** create netcdf file*************************'
    print '*******************************************************************'
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path + os.sep + 'OMET_NEMO_ORCA0083_daily_1979_2012_E_zonal_int.nc', 'w',format = 'NETCDF4')
    # create dimensions for netcdf data
    year_wrap_dim = data_wrap.createDimension('year',len(period))
    month_wrap_dim = data_wrap.createDimension('month',12)
    lat_wrap_dim = data_wrap.createDimension('latitude_aux',len(latitude_aux))
    # create coordinate variables for 3-dimensions
    year_wrap_var = data_wrap.createVariable('year',np.int32,('year',))
    month_wrap_var = data_wrap.createVariable('month',np.int32,('month',))
    lat_wrap_var = data_wrap.createVariable('latitude_aux',np.float32,('latitude_aux',))
    # create the actual 3-d variable
    E_wrap_var = data_wrap.createVariable('E',np.float64,('year','month','latitude_aux'),zlib=True)
    # global attributes
    data_wrap.description = 'Monthly mean zonal integral of meridional energy transport'
    # variable attributes
    lat_wrap_var.units = 'degree_north'
    E_wrap_var.units = 'tera watt'

    lat_wrap_var.long_name = 'nominal latitude'
    E_wrap_var.long_name = 'oceanic meridional energy transport'
    # writing data
    year_wrap_var[:] = period
    lat_wrap_var[:] = latitude_aux
    month_wrap_var[:] = np.arange(1,13,1)
    E_wrap_var[:] = E_zonal_int
    # close the file
    data_wrap.close()

# function for packing point data
def pack_netcdf_point(E_point, E_zonal, latitude, longitude, lev, mask, output_path):
    print '*******************************************************************'
    print '*********************** create netcdf file*************************'
    print '*******************************************************************'
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path + os.sep + 'OMET_NEMO_ORCA0083_daily_1979_2012_E_point.nc', 'w',format = 'NETCDF4')
    # create dimensions for netcdf data
    year_wrap_dim = data_wrap.createDimension('year',len(period))
    month_wrap_dim = data_wrap.createDimension('month',12)
    lat_wrap_dim = data_wrap.createDimension('latitude',jj)
    lon_wrap_dim = data_wrap.createDimension('longitude',ji)
    lev_wrap_dim = data_wrap.createDimension('lev',level)
    # create coordinate variables for 3-dimensions
    year_wrap_var = data_wrap.createVariable('year',np.int32,('year',))
    month_wrap_var = data_wrap.createVariable('month',np.int32,('month',))
    lat_wrap_var = data_wrap.createVariable('latitude',np.float32,('latitude','longitude'))
    lon_wrap_var = data_wrap.createVariable('longitude',np.float32,('latitude','longitude'))
    lev_wrap_var = data_wrap.createVariable('lev',np.float32,('lev',))
    mask_wrap_var = data_wrap.createVariable('mask',np.int32,('latitude','longitude'))
    # create the actual 3-d variable
    E_point_wrap_var = data_wrap.createVariable('E',np.float64,('year','month','latitude','longitude'),zlib=True)
    E_zonal_wrap_var = data_wrap.createVariable('E',np.float64,('year','month','lev','latitude'),zlib=True)
    # global attributes
    data_wrap.description = 'Monthly mean meridional energy transport'
    # variable attributes
    lat_wrap_var.units = 'ORCA0083_latitude'
    lon_wrap_var.units = 'ORCA0083_longitude'
    E_point_wrap_var.units = 'tera watt'
    E_zonal_wrap_var.units = 'tera watt'
    lev_wrap_var.units = 'm'

    E_point_wrap_var.long_name = 'oceanic meridional energy transport integrated over entire column'
    E_zonal_wrap_var.long_name = 'oceanic meridional energy transport integrated over longitude'
    lev_wrap_var.long_name = 'depth'
    # writing data
    year_wrap_var[:] = period
    lat_wrap_var[:] = latitude
    lon_wrap_var[:] = longitude
    month_wrap_var[:] = np.arange(1,13,1)
    lev_wrap_var[:] = lev
    mask_wrap_var[:] = mask
    E_point_wrap_var[:] = E_point
    E_zonal_wrap_var[:] = E_zonal
    # close the file
    data_wrap.close()

if __name__=="__main__":
    print '*******************************************************************'
    print '*********************** extract variables *************************'
    print '*******************************************************************'
    # create dimensions from an existing file
    period = np.arange(start_year,end_year+1,1)
    latitude = benchmark.variables['gphiv'][:]
    latitude_aux = latitude[:,1142]
    longitude = benchmark.variables['glamv'][:]
    lev = benchmark.variables['lev'][:]
    mask = benchmark.variables['mask'][:]
    E_point = np.zeros((len(period),12,jj,ji),dtype=float)
    E_zonal_int = np.zeros((len(period),12,jj),dtype=float)
    E_zonal = np.zeros((len(period),12,lev,jj),dtype=float)
    for i in period:
        j = i - 1979
        dataset_path = datapath + os.sep + 'vel_T_ORCA0083_select_{}.nc'.format(i)
        print "read file vel_T_ORCA0083_select_{}.nc".format(i)
        dataset = Dataset(dataset_path)
        E_point[j,:,:,:] = dataset.variables['vT_vert'][:]
        E_zonal_int[j,:,:] = np.sum(dataset.variables['vT_vert'][:],2)
        E_zonal[j,:,:,:] = dataset.variables['vT_zonal'][:]
    print '*******************************************************************'
    print '*********************** create netcdf file*************************'
    print '*******************************************************************'
    pack_netcdf_zonal_int(E_zonal_int, latitude_aux, output_path)
    pack_netcdf_point(E_point, E_zonal, latitude, longitude, lev, mask, output_path)
    print 'Packing netcdf files complete!'
print "Create netcdf file successfully"

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
