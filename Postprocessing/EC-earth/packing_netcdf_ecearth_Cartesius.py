#!/usr/bin/env python
"""
Copyright Netherlands eScience Center

Function        : Postprocessing meridional energy transport from Cartesius (EC-earth)
Author          : Yang Liu
Date            : 2017.12.20
Last Update     : 2017.12.20
Description     : The code aims to postprocess the output from the Cartesius
                  regarding the computation of atmospheric meridional energy
                  transport based on EC-Earth output (atmosphere only run). The
                  complete procedure includes data extraction and making plots.
Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, matplotlib, sys
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
datapath_int = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/EC-earth/zonal_int'
datapath_point = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/EC-earth/point'
# time of the data, which concerns with the name of input
# starting time (year)
start_year = 1979
# Ending time, if only for 1 year, then it should be the same as starting year
end_year = 2016
# specify output path for the netCDF4 file
output_path = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/EC-earth/postprocessing'
# benchmark datasets for basic dimensions
benchmark_path_int = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/EC-earth/zonal_int/AMET_EC-earth_model_daily_197910_E_zonal_int.nc'
benchmark_path_point = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/EC-earth/point/AMET_EC-earth_model_daily_197910_E_point.nc'

benchmark_int = Dataset(benchmark_path_int)
benchmark_point = Dataset(benchmark_path_point)
####################################################################################

# namelist of month and days for file manipulation
namelist_month = ['01','02','03','04','05','06','07','08','09','10','11','12']

# function for packing zonal int data
def pack_netcdf_zonal_int(datapath,output_path,benchmark):
    print '*******************************************************************'
    print '*********************** extract variables *************************'
    print '*******************************************************************'
    # create dimensions from an existing file
    period = np.arange(start_year,end_year+1,1)
    month = np.arange(1,13,1)
    latitude = benchmark.variables['latitude'][:]

    E = np.zeros((len(period),len(month),len(latitude)),dtype=float)
    E_internal = np.zeros((len(period),len(month),len(latitude)),dtype=float)
    E_latent = np.zeros((len(period),len(month),len(latitude)),dtype=float)
    E_geopotential = np.zeros((len(period),len(month),len(latitude)),dtype=float)
    E_kinetic = np.zeros((len(period),len(month),len(latitude)),dtype=float)

    for i in period:
        j = i -1979
        for ii in np.arange(12): # loop for month
            dataset_path = datapath + os.sep + 'AMET_EC-earth_model_daily_%d%s_E_zonal_int.nc' % (i,namelist_month[ii])
            dataset = Dataset(dataset_path)
            E[j,ii,:] = dataset.variables['E'][:]
            E_internal[j,ii,:] = dataset.variables['E_cpT'][:]
            E_latent[j,ii,:] = dataset.variables['E_Lvq'][:]
            E_geopotential[j,ii,:] = dataset.variables['E_gz'][:]
            E_kinetic[j,ii,:] = dataset.variables['E_uv2'][:]

    print '*******************************************************************'
    print '*********************** create netcdf file*************************'
    print '*******************************************************************'
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path+os.sep + 'AMET_EC-earth_model_daily_1979_2016_E_zonal_int.nc', 'w',format = 'NETCDF3_64BIT')
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
    month = np.arange(1,13,1)
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
        for ii in np.arange(12):
            dataset_path = datapath + os.sep + 'AMET_EC-earth_model_daily_%d%s_E_point.nc' % (i,namelist_month[ii])
            dataset = Dataset(dataset_path)
            E[j,ii,:,:] = dataset.variables['E'][:]
            E_internal[j,ii,:,:] = dataset.variables['E_cpT'][:]
            E_latent[j,ii,:,:] = dataset.variables['E_Lvq'][:]
            E_geopotential[j,ii,:,:] = dataset.variables['E_gz'][:]
            E_kinetic[j,ii,:,:] = dataset.variables['E_uv2'][:]
            uc[j,ii,:,:] = dataset.variables['uc'][:]
            vc[j,ii,:,:] = dataset.variables['vc'][:]

    print '*******************************************************************'
    print '*********************** create netcdf file*************************'
    print '*******************************************************************'
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path+os.sep + 'AMET_EC-earth_model_daily_1979_2016_E_point.nc', 'w',format = 'NETCDF3_64BIT')
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
