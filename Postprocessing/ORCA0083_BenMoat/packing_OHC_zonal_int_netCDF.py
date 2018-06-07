#!/usr/bin/env python
"""
Copyright Netherlands eScience Center

Function        : Packing zonal integral of OHC from NEMO hindcast (NEMO ORCA0083)
Author          : Yang Liu
Date            : 2018.06.07
Last Update     : 2018.06.07
Description     : The code aims to reorganize the output from Ben Moat
                  regarding the computation of Ocean Heat Content from
                  NEMO ORCA0083 hindcast.

                  Here we only compute the zonal mean since the point-wise data is
                  too large to handle. (memory error)
Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, matplotlib, sys
variables       : Ocean Heat Content from surface to bottom          OHC       [J]

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
datapath = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ORCA012_BenMoat/OHC'
# mesh
datapath_mesh_NEMO = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ORCA012_BenMoat/ORCA083'
# time of the data, which concerns with the name of input
# starting time (year)
start_year = 1979
# Ending time, if only for 1 year, then it should be the same as starting year
end_year = 2012
# specify output path for the netCDF4 file
output_path = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ORCA012_BenMoat/postprocessing'
# benchmark datasets for basic dimensions
#benchmark_path = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ORCA012_BenMoat/OMET/vel_T_ORCA0083_select_1980.nc'
#benchmark = Dataset(benchmark_path)
####################################################################################
# dimension
jj = 3059 # from equator 1494
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
    data_wrap = Dataset(output_path + os.sep + 'OHC_NEMO_ORCA0083_daily_1979_2012_zonal_int.nc', 'w',format = 'NETCDF4')
    # create dimensions for netcdf data
    year_wrap_dim = data_wrap.createDimension('year',len(period))
    month_wrap_dim = data_wrap.createDimension('month',12)
    lat_wrap_dim = data_wrap.createDimension('latitude_aux',len(latitude_aux))
    # create coordinate variables for 3-dimensions
    year_wrap_var = data_wrap.createVariable('year',np.int32,('year',))
    month_wrap_var = data_wrap.createVariable('month',np.int32,('month',))
    lat_wrap_var = data_wrap.createVariable('latitude_aux',np.float32,('latitude_aux',))
    # create the actual 3-d variable
    OHC_wrap_var = data_wrap.createVariable('OHC_glo_vert',np.float64,('year','month','latitude_aux'),zlib=True)
    # global attributes
    data_wrap.description = 'Monthly mean zonal integral of ocean heat content'
    # variable attributes
    lat_wrap_var.units = 'degree_north'
    OHC_wrap_var.units = 'tera joule'

    lat_wrap_var.long_name = 'nominal latitude'
    OHC_wrap_var.long_name = 'Ocean heat content from surface to bottom'
    # writing data
    year_wrap_var[:] = period
    lat_wrap_var[:] = latitude_aux
    month_wrap_var[:] = np.arange(1,13,1)
    OHC_wrap_var[:] = OHC_zonal_int
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
    dataset_mesh_NEMO = Dataset(datapath_mesh_NEMO + os.sep + 'mesh_hgr.nc')
    latitude = dataset_mesh_NEMO.variables['gphiv'][0,1494:,:]
    latitude_aux = latitude[:,1142]
    #longitude = dataset_mesh_NEMO.variables['glamv'][0,1494:,:]
    # grid width
    e1v = dataset_mesh_NEMO.variables['e1v'][0,1494:,:]/1000
    e2v = dataset_mesh_NEMO.variables['e2v'][0,1494:,:]/1000
    lev = level
    #E_point = np.zeros((len(period),12,1494,ji),dtype=float) #not enough memory
    OHC_zonal_int = np.zeros((len(period),12,1565),dtype=float)
    for i in period:
        j = i - 1979
        dataset_path = datapath + os.sep + 'OHC_ORCA0083_select_{}.nc'.format(i)
        print "read file OHC_ORCA0083_select_{}.nc".format(i)
        dataset = Dataset(dataset_path)
        point = dataset.variables['OHC_bottom'][:,1494:,:] * e1v * e2v
        OHC_zonal_int[j,:,:] = np.sum(point,2)/1E+12 # change unit to tera joule
    print '*******************************************************************'
    print '*********************** create netcdf file*************************'
    print '*******************************************************************'
    pack_netcdf_zonal_int(OHC_zonal_int, latitude_aux, output_path)
    print 'Packing netcdf files complete!'
print "Create netcdf file successfully"

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
