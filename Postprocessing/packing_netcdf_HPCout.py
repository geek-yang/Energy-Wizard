#!/usr/bin/env python
"""
Copyright Netherlands eScience Center

Function        : Postprocessing meridional energy transport from HPC cloud (ERA-Interim)
Author          : Yang Liu
Date            : 2017.7.23
Last Update     : 2017.7.28
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
datapath_int = 'F:\DataBase\HPC_out\ERAI\zonal_int'
datapath_point = 'F:\DataBase\HPC_out\ERAI\point'
#datapath = '/project/Reanalysis/ERA_Interim/Subdaily/Model'
# time of the data, which concerns with the name of input
# starting time (year)
start_year = 1979
# Ending time, if only for 1 year, then it should be the same as starting year
end_year = 2016
# specify output path for the netCDF4 file
output_path = 'F:\DataBase\HPC_out\ERAI\postprocessing'
#output_path = '/project/Reanalysis/ERA_Interim/Subdaily/Model'
# benchmark datasets for basic dimensions
#benchmark_path = '/project/Reanalysis/ERA_Interim/Subdaily/Model/era1980/model_daily_075_1980_1_z_lnsp.nc'
benchmark_path_int = 'F:\DataBase\HPC_out\ERAI\zonal_int\\model_daily_075_1980_E_zonal_int.nc'
benchmark_path_point = 'F:\DataBase\HPC_out\ERAI\point\\model_daily_075_1980_E_point.nc'

benchmark_int = Dataset(benchmark_path_int)
benchmark_point = Dataset(benchmark_path_point)
####################################################################################


# function for packing zonal int data
def pack_netcdf_zonal_int(datapath,output_path,benchmark):    
    print '*******************************************************************'
    print '*********************** extract variables *************************'
    print '*******************************************************************'
    # create dimensions from an existing file
    period = np.arange(start_year,end_year+1,1)
    month = benchmark.variables['month'][:]
    latitude = benchmark.variables['latitude'][:]

    E = np.zeros((len(period),len(month),len(latitude)),dtype=float)
    E_internal = np.zeros((len(period),len(month),len(latitude)),dtype=float)
    E_latent = np.zeros((len(period),len(month),len(latitude)),dtype=float)
    E_geopotential = np.zeros((len(period),len(month),len(latitude)),dtype=float)
    E_kinetic = np.zeros((len(period),len(month),len(latitude)),dtype=float)

    for i in period:
        j = i -1979
        dataset_path = datapath + os.sep + 'model_daily_075_%d_E_zonal_int.nc' % (i)
        dataset = Dataset(dataset_path)
        E[j,:,:] = dataset.variables['E'][:]
        E_internal[j,:,:] = dataset.variables['E_cpT'][:]
        E_latent[j,:,:] = dataset.variables['E_Lvq'][:]
        E_geopotential[j,:,:] = dataset.variables['E_gz'][:]
        E_kinetic[j,:,:] = dataset.variables['E_uv2'][:]

    print '*******************************************************************'
    print '*********************** create netcdf file*************************'
    print '*******************************************************************'
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path+os.sep + 'model_daily_075_1979_2016_E_zonal_int.nc', 'w',format = 'NETCDF3_64BIT')
    # create dimensions for netcdf data
    year_wrap_dim = data_wrap.createDimension('year',len(period))
    month_wrap_dim = data_wrap.createDimension('month',len(month))
    lat_wrap_dim = data_wrap.createDimension('latitude',len(latitude))
    # create coordinate variables for 3-dimensions
    year_wrap_var = data_wrap.createVariable('year',np.int32,('year',))
    month_wrap_var = data_wrap.createVariable('month',np.int32,('month',))
    lat_wrap_var = data_wrap.createVariable('latitude',np.float32,('latitude',))
    # create the actual 3-d variable
    E_total_wrap_var = data_wrap.createVariable('E',np.float64,('year','month','latitude'))
    E_internal_wrap_var = data_wrap.createVariable('E_cpT',np.float64,('year','month','latitude'))
    E_latent_wrap_var = data_wrap.createVariable('E_Lvq',np.float64,('year','month','latitude'))
    E_geopotential_wrap_var = data_wrap.createVariable('E_gz',np.float64,('year','month','latitude'))
    E_kinetic_wrap_var = data_wrap.createVariable('E_uv2',np.float64,('year','month','latitude'))
    # global attributes
    data_wrap.description = 'Monthly mean zonal integral of meridional energy transport and each component'
    # variable attributes
    lat_wrap_var.units = 'degree_north'
    E_total_wrap_var.units = 'tera watt'
    E_internal_wrap_var.units = 'tera watt'
    E_latent_wrap_var.units = 'tera watt'
    E_geopotential_wrap_var.units = 'tera watt'
    E_kinetic_wrap_var.units = 'tera watt'
    E_total_wrap_var.long_name = 'atmospheric meridional energy transport'
    E_internal_wrap_var.long_name = 'atmospheric meridional internal energy transport'
    E_latent_wrap_var.long_name = 'atmospheric meridional latent heat transport'
    E_geopotential_wrap_var.long_name = 'atmospheric meridional geopotential transport'
    E_kinetic_wrap_var.long_name = 'atmospheric meridional kinetic energy transport'
    # writing data
    year_wrap_var[:] = period
    lat_wrap_var[:] = latitude
    month_wrap_var[:] = month
    E_total_wrap_var[:] = E
    E_internal_wrap_var[:] = E_internal
    E_latent_wrap_var[:] = E_latent
    E_geopotential_wrap_var[:] = E_geopotential
    E_kinetic_wrap_var[:] = E_kinetic

    # close the file
    data_wrap.close()

# function for packing point data
def pack_netcdf_point(datapath,output_path,benchmark):    
    print '*******************************************************************'
    print '*********************** extract variables *************************'
    print '*******************************************************************'
    # create dimensions from an existing file
    period = np.arange(start_year,end_year+1,1)
    month = benchmark.variables['month'][:]
    latitude = benchmark.variables['latitude'][:]
    longitude = benchmark.variables['longitude'][:]

    E = np.zeros((len(period),len(month),len(latitude),len(longitude)),dtype=float)
    E_internal = np.zeros((len(period),len(month),len(latitude),len(longitude)),dtype=float)
    E_latent = np.zeros((len(period),len(month),len(latitude),len(longitude)),dtype=float)
    E_geopotential = np.zeros((len(period),len(month),len(latitude),len(longitude)),dtype=float)
    E_kinetic = np.zeros((len(period),len(month),len(latitude),len(longitude)),dtype=float)
    uc = np.zeros((len(period),len(month),len(latitude),len(longitude)),dtype=float)
    vc = np.zeros((len(period),len(month),len(latitude),len(longitude)),dtype=float)

    for i in period:
        j = i -1979
        dataset_path = datapath + os.sep + 'model_daily_075_%d_E_point.nc' % (i)
        dataset = Dataset(dataset_path)
        E[j,:,:,:] = dataset.variables['E'][:]
        E_internal[j,:,:,:] = dataset.variables['E_cpT'][:]
        E_latent[j,:,:,:] = dataset.variables['E_Lvq'][:]
        E_geopotential[j,:,:,:] = dataset.variables['E_gz'][:]
        E_kinetic[j,:,:,:] = dataset.variables['E_uv2'][:]
        uc[j,:,:,:] = dataset.variables['uc'][:]
        vc[j,:,:,:] = dataset.variables['vc'][:]

    print '*******************************************************************'
    print '*********************** create netcdf file*************************'
    print '*******************************************************************'
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path+os.sep + 'model_daily_075_1979_2016_E_point.nc', 'w',format = 'NETCDF3_64BIT')
    # create dimensions for netcdf data
    year_wrap_dim = data_wrap.createDimension('year',len(period))
    month_wrap_dim = data_wrap.createDimension('month',len(month))
    lat_wrap_dim = data_wrap.createDimension('latitude',len(latitude))
    lon_wrap_dim = data_wrap.createDimension('longitude',len(longitude))
    # create coordinate variables for 3-dimensions
    year_wrap_var = data_wrap.createVariable('year',np.int32,('year',))
    month_wrap_var = data_wrap.createVariable('month',np.int32,('month',))
    lat_wrap_var = data_wrap.createVariable('latitude',np.float32,('latitude',))
    lon_wrap_var = data_wrap.createVariable('longitude',np.float32,('longitude',))
    # create the actual 3-d variable
    E_total_wrap_var = data_wrap.createVariable('E',np.float64,('year','month','latitude','longitude'))
    E_internal_wrap_var = data_wrap.createVariable('E_cpT',np.float64,('year','month','latitude','longitude'))
    E_latent_wrap_var = data_wrap.createVariable('E_Lvq',np.float64,('year','month','latitude','longitude'))
    E_geopotential_wrap_var = data_wrap.createVariable('E_gz',np.float64,('year','month','latitude','longitude'))
    E_kinetic_wrap_var = data_wrap.createVariable('E_uv2',np.float64,('year','month','latitude','longitude'))
    uc_wrap_var = data_wrap.createVariable('uc',np.float32,('year','month','latitude','longitude'))
    vc_wrap_var = data_wrap.createVariable('vc',np.float32,('year','month','latitude','longitude'))
    # global attributes
    data_wrap.description = 'Monthly mean zonal integral of meridional energy transport and each component'
    # variable attributes
    lat_wrap_var.units = 'degree_north'
    lon_wrap_var.units = 'degree_east'
    E_total_wrap_var.units = 'tera watt'
    E_internal_wrap_var.units = 'tera watt'
    E_latent_wrap_var.units = 'tera watt'
    E_geopotential_wrap_var.units = 'tera watt'
    E_kinetic_wrap_var.units = 'tera watt'
    uc_wrap_var.units = 'm/s'
    vc_wrap_var.units = 'm/s'

    uc_wrap_var.long_name = 'zonal barotropic correction wind'
    vc_wrap_var.long_name = 'meridional barotropic correction wind'
    E_total_wrap_var.long_name = 'atmospheric meridional energy transport'
    E_internal_wrap_var.long_name = 'atmospheric meridional internal energy transport'
    E_latent_wrap_var.long_name = 'atmospheric meridional latent heat transport'
    E_geopotential_wrap_var.long_name = 'atmospheric meridional geopotential transport'
    E_kinetic_wrap_var.long_name = 'atmospheric meridional kinetic energy transport'
    # writing data
    year_wrap_var[:] = period
    lat_wrap_var[:] = latitude
    lon_wrap_var[:] = longitude    
    month_wrap_var[:] = month
    uc_wrap_var[:] = uc
    vc_wrap_var[:] = vc
    E_total_wrap_var[:] = E
    E_internal_wrap_var[:] = E_internal
    E_latent_wrap_var[:] = E_latent
    E_geopotential_wrap_var[:] = E_geopotential
    E_kinetic_wrap_var[:] = E_kinetic

    # close the file
    data_wrap.close()

if __name__=="__main__":
    pack_netcdf_zonal_int(datapath_int,output_path,benchmark_int)
    pack_netcdf_point(datapath_point,output_path,benchmark_point)
    print 'Packing netcdf files complete!'

print "Create netcdf file successfully"

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
