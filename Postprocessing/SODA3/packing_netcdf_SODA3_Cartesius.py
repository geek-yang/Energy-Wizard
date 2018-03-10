#!/usr/bin/env python
"""
Copyright Netherlands eScience Center

Function        : Packing netCDF files for the monthly output from Cartesius (JRA55)
Author          : Yang Liu
Date            : 2018.02.28
Last Update     : 2018.03.10
Description     : The code aims to reorganize the output from the Cartesius
                  regarding the computation of oceanic meridional energy
                  transport based on SODA3 output.
Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, matplotlib, sys
variables       : Meridional Energy Transport                       E         [Tera-Watt]
                  Meridional Overturning Stream Function (Globe)    Psi       [Sv]
                  Meridional Overturning Stream Function (Atlantic) Psi       [Sv]

Caveat!!        : The data is from 90 deg north to 90 deg south (Globe).
                  Latitude: North to South(90 to -90)
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
datapath_int = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/SODA3/zonal_int'
datapath_point = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/SODA3/point'
# time of the data, which concerns with the name of input
# starting time (year)
start_year = 1980
# Ending time, if only for 1 year, then it should be the same as starting year
end_year = 2015
# specify output path for the netCDF4 file
output_path = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/SODA3/postprocessing'
# benchmark datasets for basic dimensions
benchmark_path_int = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/SODA3/zonal_int/SODA3_model_5daily_mom5_E_zonal_int_201509.nc'
benchmark_path_point = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/SODA3/point/SODA3_model_5daily_mom5_E_point_201509.nc'

benchmark_int = Dataset(benchmark_path_int)
benchmark_point = Dataset(benchmark_path_point)
####################################################################################
# dimension
ji = 1440
jj = 1070
level = 50
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
    latitude_aux = benchmark.variables['latitude_aux'][:]
    lev = benchmark.variables['lev'][:]

    E = np.zeros((len(period),len(month),len(latitude_aux)),dtype=float)
    Psi_glo = np.zeros((len(period),len(month),len(lev),len(latitude_aux)),dtype=float)
    Psi_atl = np.zeros((len(period),len(month),len(lev),len(latitude_aux)),dtype=float)

    for i in period:
        j = i - 1980
        for ii in np.arange(12): # loop for month
            dataset_path = datapath + os.sep + 'SODA3_model_5daily_mom5_E_zonal_int_%d%s.nc' % (i,namelist_month[ii])
            dataset = Dataset(dataset_path)
            E[j,ii,:] = dataset.variables['E'][:]
            Psi_glo[j,ii,:,:] = dataset.variables['Psi_glo'][:]
            Psi_atl[j,ii,:,:] = dataset.variables['Psi_atl'][:]

    print '*******************************************************************'
    print '*********************** create netcdf file*************************'
    print '*******************************************************************'
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path+os.sep + 'OMET_SODA3_model_5daily_1980_2015_E_zonal_int.nc', 'w',format = 'NETCDF3_64BIT')
    # create dimensions for netcdf data
    year_wrap_dim = data_wrap.createDimension('year',len(period))
    month_wrap_dim = data_wrap.createDimension('month',len(month))
    lat_wrap_dim = data_wrap.createDimension('latitude_aux',len(latitude_aux))
    lev_wrap_dim = data_wrap.createDimension('lev',len(lev))
    # create coordinate variables for 3-dimensions
    year_wrap_var = data_wrap.createVariable('year',np.int32,('year',))
    month_wrap_var = data_wrap.createVariable('month',np.int32,('month',))
    lat_wrap_var = data_wrap.createVariable('latitude_aux',np.float32,('latitude_aux',))
    lev_wrap_var = data_wrap.createVariable('lev',np.float32,('lev',))
    # create the actual 3-d variable
    E_wrap_var = data_wrap.createVariable('E',np.float64,('year','month','latitude_aux'))
    Psi_glo_wrap_var = data_wrap.createVariable('Psi_glo',np.float64,('year','month','lev','latitude_aux'))
    Psi_atl_wrap_var = data_wrap.createVariable('Psi_atl',np.float64,('year','month','lev','latitude_aux'))
    # global attributes
    data_wrap.description = 'Monthly mean zonal integral of meridional energy transport and overturning stream function'
    # variable attributes
    lat_wrap_var.units = 'degree_north'
    E_wrap_var.units = 'tera watt'
    Psi_glo_wrap_var.units = 'Sv'
    Psi_atl_wrap_var.units = 'Sv'
    lev_wrap_var.units = 'm'

    E_wrap_var.long_name = 'oceanic meridional energy transport'
    Psi_glo_wrap_var.long_name = 'Global meridional overturning stream function'
    Psi_atl_wrap_var.long_name = 'Atlantic meridional overturning stream function'
    lev_wrap_var.long_name = 'depth'
    # writing data
    year_wrap_var[:] = period
    lat_wrap_var[:] = latitude_aux
    month_wrap_var[:] = month
    lev_wrap_var[:] = lev
    E_wrap_var[:] = E
    Psi_glo_wrap_var[:] = Psi_glo
    Psi_atl_wrap_var[:] = Psi_atl

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

    E = np.zeros((len(period),len(month),jj,ji),dtype=float)

    for i in period:
        j = i - 1980
        for ii in np.arange(12):
            dataset_path = datapath + os.sep + 'SODA3_model_5daily_mom5_E_point_%d%s.nc' % (i,namelist_month[ii])
            dataset = Dataset(dataset_path)
            E[j,ii,:,:] = dataset.variables['E'][:]

    print '*******************************************************************'
    print '*********************** create netcdf file*************************'
    print '*******************************************************************'
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path+os.sep + 'OMET_SODA3_model_5daily_1980_2015_E_point.nc', 'w',format = 'NETCDF3_64BIT')
    # create dimensions for netcdf data
    year_wrap_dim = data_wrap.createDimension('year',len(period))
    month_wrap_dim = data_wrap.createDimension('month',len(month))
    lat_wrap_dim = data_wrap.createDimension('latitude',jj)
    lon_wrap_dim = data_wrap.createDimension('longitude',ji)
    # create coordinate variables for 3-dimensions
    year_wrap_var = data_wrap.createVariable('year',np.int32,('year',))
    month_wrap_var = data_wrap.createVariable('month',np.int32,('month',))
    lat_wrap_var = data_wrap.createVariable('latitude',np.float32,('latitude','longitude'))
    lon_wrap_var = data_wrap.createVariable('longitude',np.float32,('latitude','longitude'))
    # create the actual 3-d variable
    E_wrap_var = data_wrap.createVariable('E',np.float64,('year','month','latitude','longitude'))

    # global attributes
    data_wrap.description = 'Monthly mean zonal integral of meridional energy transport and each component'
    # variable attributes
    lat_wrap_var.units = 'MOM5_latitude'
    lon_wrap_var.units = 'MOM5_longitude'
    E_wrap_var.units = 'tera watt'

    E_wrap_var.long_name = 'oceanic meridional energy transport'

    # writing data
    year_wrap_var[:] = period
    lat_wrap_var[:] = latitude
    lon_wrap_var[:] = longitude
    month_wrap_var[:] = month
    E_wrap_var[:] = E

    # close the file
    data_wrap.close()

if __name__=="__main__":
    pack_netcdf_zonal_int(datapath_int,output_path,benchmark_int)
    pack_netcdf_point(datapath_point,output_path,benchmark_point)
    print 'Packing netcdf files complete!'

print "Create netcdf file successfully"

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
