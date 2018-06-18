#!/usr/bin/env python
"""
Copyright Netherlands eScience Center

Function        : Packing netCDF files for the monthly output from Cartesius (SODA3)
Author          : Yang Liu
Date            : 2018.02.28
Last Update     : 2018.06.16
Description     : The code aims to reorganize the output from the Cartesius
                  regarding the computation of oceanic meridional energy
                  transport based on SODA3 output. It also works with diagnostic
                  of fields, like OHC.
Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, matplotlib, sys
variables       : Meridional Energy Transport                       E         [Tera-Watt]
                  Meridional Overturning Stream Function (Globe)    Psi       [Sv]
                  Meridional Overturning Stream Function (Atlantic) Psi       [Sv]
                  Ocean Heat Content                                OHC       [J]

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
#datapath_int = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/SODA3/zonal_int'
#datapath_point = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/SODA3/point'
#datapath_OHC = '/projects/0/blueactn/reanalysis/SODA3/statistics/'
datapath_psi = '/projects/0/blueactn/reanalysis/SODA3/statistics/'
# time of the data, which concerns with the name of input
# starting time (year)
start_year = 1980
# Ending time, if only for 1 year, then it should be the same as starting year
end_year = 2015
# specify output path for the netCDF4 file
#output_path = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/SODA3/postprocessing'
#output_path_OHC = '/projects/0/blueactn/reanalysis/SODA3/'
output_path_psi = '/projects/0/blueactn/reanalysis/SODA3/'
# benchmark datasets for basic dimensions
#benchmark_path_int = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/SODA3/zonal_int/SODA3_model_5daily_mom5_E_zonal_int_201509.nc'
#benchmark_path_point = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/SODA3/point/SODA3_model_5daily_mom5_E_point_201509.nc'
#benchmark_path_OHC = '/projects/0/blueactn/reanalysis/SODA3/topog.nc'
benchmark_path_psi = '/projects/0/blueactn/reanalysis/SODA3/topog.nc'
#benchmark_int = Dataset(benchmark_path_int)
#benchmark_point = Dataset(benchmark_path_point)
#benchmark_OHC = Dataset(benchmark_path_OHC)
benchmark_OHC = Dataset(benchmark_path_psi)
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
    data_wrap = Dataset(output_path+os.sep + 'OMET_SODA3_model_5daily_1980_2015_E_zonal_int.nc', 'w',format = 'NETCDF4')
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
    E_wrap_var = data_wrap.createVariable('E',np.float64,('year','month','latitude_aux'),zlib=True)
    Psi_glo_wrap_var = data_wrap.createVariable('Psi_glo',np.float64,('year','month','lev','latitude_aux'),zlib=True)
    Psi_atl_wrap_var = data_wrap.createVariable('Psi_atl',np.float64,('year','month','lev','latitude_aux'),zlib=True)
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
    data_wrap = Dataset(output_path+os.sep + 'OMET_SODA3_model_5daily_1980_2015_E_point.nc', 'w',format = 'NETCDF4')
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
    E_wrap_var = data_wrap.createVariable('E',np.float64,('year','month','latitude','longitude'),zlib=True)

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

# function for packing OHC data
def pack_netcdf_OHC(datapath,output_path,benchmark):
    print '*******************************************************************'
    print '*********************** extract variables *************************'
    print '*******************************************************************'
    # create dimensions from an existing file
    period = np.arange(start_year,end_year+1,1)
    month = np.arange(1,13,1)
    grid_y_C = benchmark.variables['grid_y_C'][:]
    x_T = benchmark.variables['x_T'][:]              # Geographic Longitude of T-cell center
    y_T = benchmark.variables['y_T'][:]
    zt = benchmark.variables['zt'][:]

    OHC_pool_glo_zonal = np.zeros((len(period),len(month),level,jj),dtype = float)
    OHC_pool_atl_zonal = np.zeros((len(period),len(month),level,jj),dtype = float)
    # vertical integral (horizontal profile)
    OHC_pool_glo_vert = np.zeros((len(period),len(month),jj,ji),dtype = float)
    OHC_pool_atl_vert = np.zeros((len(period),len(month),jj,ji),dtype = float)
    # vertical integral (horizontal profile) and OHC for certain layers
    OHC_pool_glo_vert_0_500 = np.zeros((len(period),len(month),jj,ji),dtype = float)
    OHC_pool_atl_vert_0_500 = np.zeros((len(period),len(month),jj,ji),dtype = float)
    OHC_pool_glo_vert_500_1000 = np.zeros((len(period),len(month),jj,ji),dtype = float)
    OHC_pool_atl_vert_500_1000 = np.zeros((len(period),len(month),jj,ji),dtype = float)
    OHC_pool_glo_vert_1000_2000 = np.zeros((len(period),len(month),jj,ji),dtype = float)
    OHC_pool_atl_vert_1000_2000 = np.zeros((len(period),len(month),jj,ji),dtype = float)
    OHC_pool_glo_vert_2000_inf = np.zeros((len(period),len(month),jj,ji),dtype = float)
    OHC_pool_atl_vert_2000_inf = np.zeros((len(period),len(month),jj,ji),dtype = float)
    for i in period:
        j = i - 1980
        for ii in np.arange(12):
            dataset_path = datapath + os.sep + 'SODA3_model_5daily_mom5_OHC_point_%d%s.nc' % (i,namelist_month[ii])
            dataset = Dataset(dataset_path)
            OHC_pool_glo_zonal[j,ii,:,:] = dataset.variables['OHC_glo_zonal'][:]
            OHC_pool_atl_zonal[j,ii,:,:] = dataset.variables['OHC_atl_zonal'][:]
            OHC_pool_glo_vert[j,ii,:,:] = dataset.variables['OHC_glo_vert'][:]
            OHC_pool_atl_vert[j,ii,:,:] = dataset.variables['OHC_atl_vert'][:]
            OHC_pool_glo_vert_0_500[j,ii,:,:] = dataset.variables['OHC_glo_vert_0_500'][:]
            OHC_pool_atl_vert_0_500[j,ii,:,:] = dataset.variables['OHC_atl_vert_0_500'][:]
            OHC_pool_glo_vert_500_1000[j,ii,:,:] = dataset.variables['OHC_glo_vert_500_1000'][:]
            OHC_pool_atl_vert_500_1000[j,ii,:,:] = dataset.variables['OHC_atl_vert_500_1000'][:]
            OHC_pool_glo_vert_1000_2000[j,ii,:,:] = dataset.variables['OHC_glo_vert_1000_2000'][:]
            OHC_pool_atl_vert_1000_2000[j,ii,:,:] = dataset.variables['OHC_atl_vert_1000_2000'][:]
            OHC_pool_glo_vert_2000_inf[j,ii,:,:] = dataset.variables['OHC_glo_vert_2000_inf'][:]
            OHC_pool_atl_vert_2000_inf[j,ii,:,:] = dataset.variables['OHC_atl_vert_2000_inf'][:]

    print '*******************************************************************'
    print '*********************** create netcdf file*************************'
    print '*******************************************************************'
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path+os.sep + 'OMET_SODA3_model_5daily_1980_2015_OHC.nc', 'w',format = 'NETCDF4')
    # create dimensions for netcdf data
    year_wrap_dim = data_wrap.createDimension('year',len(period))
    month_wrap_dim = data_wrap.createDimension('month',len(month))
    lat_wrap_dim = data_wrap.createDimension('j',jj)
    lon_wrap_dim = data_wrap.createDimension('i',ji)
    lev_wrap_dim = data_wrap.createDimension('lev',level)
    # create coordinate variables for 3-dimensions
    year_wrap_var = data_wrap.createVariable('year',np.int32,('year',))
    month_wrap_var = data_wrap.createVariable('month',np.int32,('month',))
    # 1D
    lat_wrap_var = data_wrap.createVariable('latitude_aux',np.float32,('j',))
    lev_wrap_var = data_wrap.createVariable('lev',np.float32,('lev',))
    # 2D
    gphit_wrap_var = data_wrap.createVariable('y_T',np.float32,('j','i'))
    glamt_wrap_var = data_wrap.createVariable('x_T',np.float32,('j','i'))
    # create target variables 4D
    OHC_glo_zonal_wrap_var = data_wrap.createVariable('OHC_glo_zonal',np.float64,('year','month','lev','j'),zlib=True)
    OHC_atl_zonal_wrap_var = data_wrap.createVariable('OHC_atl_zonal',np.float64,('year','month','lev','j'),zlib=True)

    OHC_glo_vert_wrap_var = data_wrap.createVariable('OHC_glo_vert',np.float64,('year','month','j','i'),zlib=True)
    OHC_atl_vert_wrap_var = data_wrap.createVariable('OHC_atl_vert',np.float64,('year','month','j','i'),zlib=True)
    OHC_glo_vert_0_500_wrap_var = data_wrap.createVariable('OHC_glo_vert_0_500',np.float64,('year','month','j','i'),zlib=True)
    OHC_atl_vert_0_500_wrap_var = data_wrap.createVariable('OHC_atl_vert_0_500',np.float64,('year','month','j','i'),zlib=True)
    OHC_glo_vert_500_1000_wrap_var = data_wrap.createVariable('OHC_glo_vert_500_1000',np.float64,('year','month','j','i'),zlib=True)
    OHC_atl_vert_500_1000_wrap_var = data_wrap.createVariable('OHC_atl_vert_500_1000',np.float64,('year','month','j','i'),zlib=True)
    OHC_glo_vert_1000_2000_wrap_var = data_wrap.createVariable('OHC_glo_vert_1000_2000',np.float64,('year','month','j','i'),zlib=True)
    OHC_atl_vert_1000_2000_wrap_var = data_wrap.createVariable('OHC_atl_vert_1000_2000',np.float64,('year','month','j','i'),zlib=True)
    OHC_glo_vert_2000_inf_wrap_var = data_wrap.createVariable('OHC_glo_vert_2000_inf',np.float64,('year','month','j','i'),zlib=True)
    OHC_atl_vert_2000_inf_wrap_var = data_wrap.createVariable('OHC_atl_vert_2000_inf',np.float64,('year','month','j','i'),zlib=True)

    # global attributes
    data_wrap.description = 'Monthly mean statistics of fields on MOM grid'
    # variable attributes
    lev_wrap_var.units = 'm'
    gphit_wrap_var.units = 'MOM5_latitude_Tgrid'
    glamt_wrap_var.units = 'MOM5_longitude_Tgrid'

    OHC_glo_zonal_wrap_var.units = 'tera joule'
    OHC_atl_zonal_wrap_var.units = 'tera joule'

    OHC_glo_vert_wrap_var.units = 'tera joule'
    OHC_atl_vert_wrap_var.units = 'tera joule'
    OHC_glo_vert_0_500_wrap_var.units = 'tera joule'
    OHC_atl_vert_0_500_wrap_var.units = 'tera joule'
    OHC_glo_vert_500_1000_wrap_var.units = 'tera joule'
    OHC_atl_vert_500_1000_wrap_var.units = 'tera joule'
    OHC_glo_vert_1000_2000_wrap_var.units = 'tera joule'
    OHC_atl_vert_1000_2000_wrap_var.units = 'tera joule'
    OHC_glo_vert_2000_inf_wrap_var.units = 'tera joule'
    OHC_atl_vert_2000_inf_wrap_var.units = 'tera joule'

    lat_wrap_var.long_name = 'auxillary latitude'
    lev_wrap_var.long_name = 'depth'
    gphit_wrap_var.long_name = 'MOM5 Tgrid latitude'
    glamt_wrap_var.long_name = 'MOM5 Tgrid longitude'

    OHC_glo_zonal_wrap_var.long_name = 'Global Ocean Heat Content (zonal integral)'
    OHC_atl_zonal_wrap_var.long_name = 'Atlantic Ocean Heat Content (zonal integral)'

    OHC_glo_vert_wrap_var.long_name = 'Global Ocean Heat Content (vertical integral)'
    OHC_atl_vert_wrap_var.long_name = 'Atlantic Ocean Heat Content (vertical integral)'
    OHC_glo_vert_0_500_wrap_var.long_name = 'Global Ocean Heat Content from surface to 500 m (vertical integral)'
    OHC_atl_vert_0_500_wrap_var.long_name = 'Atlantic Ocean Heat Content from surface to 500 m (vertical integral)'
    OHC_glo_vert_500_1000_wrap_var.long_name = 'Global Ocean Heat Content from 500 m to 1000 m (vertical integral)'
    OHC_atl_vert_500_1000_wrap_var.long_name = 'Atlantic Ocean Heat Content from 500 m to 1000 m (vertical integral)'
    OHC_glo_vert_1000_2000_wrap_var.long_name = 'Global Ocean Heat Content from 1000 m to 2000 m (vertical integral)'
    OHC_atl_vert_1000_2000_wrap_var.long_name = 'Atlantic Ocean Heat Content from 1000 m to 2000 m (vertical integral)'
    OHC_glo_vert_2000_inf_wrap_var.long_name = 'Global Ocean Heat Content from 2000 m to bottom (vertical integral)'
    OHC_atl_vert_2000_inf_wrap_var.long_name = 'Atlantic Ocean Heat Content from 2000 m to bottom (vertical integral)'

    # writing data
    year_wrap_var[:] = period
    month_wrap_var[:] = month

    lat_wrap_var[:] = grid_y_C
    lev_wrap_var[:] = zt
    gphit_wrap_var[:] = y_T
    glamt_wrap_var[:] = x_T

    OHC_glo_zonal_wrap_var[:] = OHC_pool_glo_zonal
    OHC_atl_zonal_wrap_var[:] = OHC_pool_atl_zonal

    OHC_glo_vert_wrap_var[:] = OHC_pool_glo_vert
    OHC_atl_vert_wrap_var[:] = OHC_pool_atl_vert
    OHC_glo_vert_0_500_wrap_var[:] = OHC_pool_glo_vert_0_500
    OHC_atl_vert_0_500_wrap_var[:] = OHC_pool_atl_vert_0_500
    OHC_glo_vert_500_1000_wrap_var[:] = OHC_pool_glo_vert_500_1000
    OHC_atl_vert_500_1000_wrap_var[:] = OHC_pool_atl_vert_500_1000
    OHC_glo_vert_1000_2000_wrap_var[:] = OHC_pool_glo_vert_1000_2000
    OHC_atl_vert_1000_2000_wrap_var[:] = OHC_pool_atl_vert_1000_2000
    OHC_glo_vert_2000_inf_wrap_var[:] = OHC_pool_glo_vert_2000_inf
    OHC_atl_vert_2000_inf_wrap_var[:] = OHC_pool_atl_vert_2000_inf

    # close the file
    data_wrap.close()

# function for packing mass transport data
def pack_netcdf_psi(datapath,output_path,benchmark):
    print '*******************************************************************'
    print '*********************** extract variables *************************'
    print '*******************************************************************'
    # create dimensions from an existing file
    period = np.arange(start_year,end_year+1,1)
    month = np.arange(1,13,1)
    grid_y_C = benchmark.variables['grid_y_C'][:]
    x_C = benchmark.variables['x_C'][:]              # Geographic Longitude of T-cell center
    y_C = benchmark.variables['y_C'][:]
    zt = benchmark.variables['zt'][:]
    # horizontal integral
    psi_pool_glo_zonal = np.zeros((len(period),len(month),level,jj),dtype = float)
    psi_pool_atl_zonal = np.zeros((len(period),len(month),level,jj),dtype = float)
    # vertical integral (horizontal profile)
    psi_pool_glo_vert = np.zeros((len(period),len(month),jj,ji),dtype = float)
    psi_pool_atl_vert = np.zeros((len(period),len(month),jj,ji),dtype = float)

    for i in period:
        j = i - 1980
        for ii in np.arange(12):
            dataset_path = datapath + os.sep + 'SODA3_model_5daily_mom5_psi_point_%d%s.nc' % (i,namelist_month[ii])
            dataset = Dataset(dataset_path)
            psi_pool_glo_zonal[j,ii,:,:] = dataset.variables['psi_glo_zonal'][:]
            psi_pool_atl_zonal[j,ii,:,:] = dataset.variables['psi_atl_zonal'][:]
            psi_pool_glo_vert[j,ii,:,:] = dataset.variables['psi_glo_vert'][:]
            psi_pool_atl_vert[j,ii,:,:] = dataset.variables['psi_atl_vert'][:]

    print '*******************************************************************'
    print '*********************** create netcdf file*************************'
    print '*******************************************************************'
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path+os.sep + 'OMET_SODA3_model_5daily_1980_2015_psi.nc', 'w',format = 'NETCDF4')
    # create dimensions for netcdf data
    year_wrap_dim = data_wrap.createDimension('year',len(period))
    month_wrap_dim = data_wrap.createDimension('month',len(month))
    lat_wrap_dim = data_wrap.createDimension('j',jj)
    lon_wrap_dim = data_wrap.createDimension('i',ji)
    lev_wrap_dim = data_wrap.createDimension('lev',level)
    # create coordinate variables for 3-dimensions
    year_wrap_var = data_wrap.createVariable('year',np.int32,('year',))
    month_wrap_var = data_wrap.createVariable('month',np.int32,('month',))
    # 1D
    lat_wrap_var = data_wrap.createVariable('latitude_aux',np.float32,('j',))
    lev_wrap_var = data_wrap.createVariable('lev',np.float32,('lev',))
    # 2D
    gphit_wrap_var = data_wrap.createVariable('y_C',np.float32,('j','i'))
    glamt_wrap_var = data_wrap.createVariable('x_C',np.float32,('j','i'))
    # create target variables 4D
    psi_glo_zonal_wrap_var = data_wrap.createVariable('psi_glo_zonal',np.float64,('year','month','lev','j'),zlib=True)
    psi_atl_zonal_wrap_var = data_wrap.createVariable('psi_atl_zonal',np.float64,('year','month','lev','j'),zlib=True)

    psi_glo_vert_wrap_var = data_wrap.createVariable('psi_glo_vert',np.float64,('year','month','j','i'),zlib=True)
    psi_atl_vert_wrap_var = data_wrap.createVariable('psi_atl_vert',np.float64,('year','month','j','i'),zlib=True)

    # global attributes
    data_wrap.description = 'Monthly mean statistics of fields on MOM grid'
    # variable attributes
    lev_wrap_var.units = 'm'
    gphit_wrap_var.units = 'MOM5_latitude_Cgrid'
    glamt_wrap_var.units = 'MOM5_longitude_Cgrid'

    psi_glo_zonal_wrap_var.units = 'Sv'
    psi_atl_zonal_wrap_var.units = 'Sv'

    psi_glo_vert_wrap_var.units = 'Sv'
    psi_atl_vert_wrap_var.units = 'Sv'

    lat_wrap_var.long_name = 'auxillary latitude'
    lev_wrap_var.long_name = 'depth'
    gphit_wrap_var.long_name = 'MOM5 Cgrid latitude'
    glamt_wrap_var.long_name = 'MOM5 Cgrid longitude'

    psi_glo_zonal_wrap_var.long_name = 'Global Meridional Mass Transport (zonal integral)'
    psi_atl_zonal_wrap_var.long_name = 'Atlantic Meridional Mass Transport (zonal integral)'

    psi_glo_vert_wrap_var.long_name = 'Global Meridional Mass Transport (vertical integral)'
    psi_atl_vert_wrap_var.long_name = 'Atlantic Meridional Mass Transport (vertical integral)'

    # writing data
    year_wrap_var[:] = period
    month_wrap_var[:] = month

    lat_wrap_var[:] = grid_y_C
    lev_wrap_var[:] = zt
    gphit_wrap_var[:] = y_C
    glamt_wrap_var[:] = x_C

    psi_glo_zonal_wrap_var[:] = psi_pool_glo_zonal
    psi_atl_zonal_wrap_var[:] = psi_pool_atl_zonal

    psi_glo_vert_wrap_var[:] = psi_pool_glo_vert
    psi_atl_vert_wrap_var[:] = psi_pool_atl_vert

    # close the file
    data_wrap.close()

if __name__=="__main__":
    #pack_netcdf_zonal_int(datapath_int,output_path,benchmark_int)
    #pack_netcdf_point(datapath_point,output_path,benchmark_point)
    #pack_netcdf_OHC(datapath_OHC,output_path_OHC,benchmark_OHC)
    pack_netcdf_psi(datapath_psi,output_path_psi,benchmark_psi)
    print 'Packing netcdf files complete!'

print "Create netcdf file successfully"

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
