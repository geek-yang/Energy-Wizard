#!/usr/bin/env python
"""
Copyright Netherlands eScience Center

Function        : Packing SLP and SIC from GRIB to netCDF files for JRA55
Author          : Yang Liu
Date            : 2018.07.04
Last Update     : 2018.12.17
Description     : The code aims to postprocess the output from the Cartesius
                  regarding the computation of atmospheric meridional energy
                  transport based on JRA55 output (atmosphere only run). The
                  complete procedure includes data extraction.
Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, matplotlib, sys
variables       : Mean Sea Level Pressure           SLP         [Pa]
                  Sea Ice Concentration             SIC         [Percentage]

Caveat!!        : The data is from 90 deg north to 90 deg south (Globe).
                  Latitude: North to South(90 to -90)
                  Lontitude: West to East (0 to 360)
"""
import numpy as np
import time as tttt
from netCDF4 import Dataset,num2date
import os
import platform
import pygrib
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

####################################################################################
################################   Input zone  #####################################
#datapath = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/JRA55/regression'
datapath = '/home/ESLT0068/WorkFlow/Core_Database_AMET_OMET_reanalysis/JRA55/regression'
# time of the data, which concerns with the name of input
# starting time (year)
start_year = 1958
# Ending time, if only for 1 year, then it should be the same as starting year
end_year = 2013
# specify output path for the netCDF4 file
output_path = '/home/ESLT0068/WorkFlow/Core_Database_AMET_OMET_reanalysis/JRA55/regression'
####################################################################################
# ==============================  Initial test   ==================================
# benchmark datasets for basic dimensions
#benchmark_path = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/JRA55/regression'
benchmark_path = '/home/ESLT0068/WorkFlow/Core_Database_AMET_OMET_reanalysis/JRA55/regression'
#benchmark_grbs_SIC = pygrib.open(os.path.join(benchmark_path,'ice_monthly_regrid','ice125.091_icec.198001_198012'))
benchmark_grbs_SIC = pygrib.open(os.path.join(benchmark_path,'ice_monthly_model','ice.091_icec.reg_tl319.198001_198012'))
print 'Number of messages',benchmark_grbs_SIC.messages
for messenger in benchmark_grbs_SIC:
    print messenger
benchmark_key_SIC = benchmark_grbs_SIC.message(1)
sample = benchmark_key_SIC.values
sample = np.ma.masked_where(sample==0,sample)
mask = np.ma.getmask(sample)
lats, lons = benchmark_key_SIC.latlons()
latitude_SIC = lats[:,0]
longitude_SIC = lons[0,:]
benchmark_grbs_SIC.close()

#benchmark_grbs_SLP = pygrib.open(os.path.join(benchmark_path,'SLP_monthly_regrid','anl_surf125.002_prmsl.198001_198012'))
#benchmark_grbs_SLP = pygrib.open(os.path.join(benchmark_path,'SP_monthly_model','anl_surf.001_pres.reg_tl319.198001_198012'))
benchmark_grbs_SLP = pygrib.open(os.path.join(benchmark_path,'SLP_monthly_model','fcst_surf.002_prmsl.reg_tl319.198001_198012'))
print 'Number of messages',benchmark_grbs_SLP.messages
for messenger in benchmark_grbs_SLP:
    print messenger
benchmark_key_SLP = benchmark_grbs_SLP.message(1)
lats, lons = benchmark_key_SLP.latlons()
latitude_SLP = lats[:,0]
longitude_SLP = lons[0,:]
benchmark_grbs_SLP.close()

#benchmark_grbs_ST = pygrib.open(os.path.join(benchmark_path,'st_monthly_regrid','anl_surf125.011_tmp.198001_198012'))
benchmark_grbs_T2M = pygrib.open(os.path.join(benchmark_path,'t2m_monthly_model','anl_surf.011_tmp.reg_tl319.198001_198012'))
print 'Number of messages',benchmark_grbs_T2M.messages
for messenger in benchmark_grbs_T2M:
    print messenger
benchmark_key_T2M = benchmark_grbs_T2M.message(1)
lats, lons = benchmark_key_T2M.latlons()
latitude_T2M = lats[:,0]
longitude_T2M = lons[0,:]
benchmark_grbs_T2M.close()
# =================================================================================

# function for packing point data
def pack_netcdf_point(datapath,output_path):
    print '*******************************************************************'
    print '*********************** extract variables *************************'
    print '*******************************************************************'
    # create dimensions from an existing file
    period = np.arange(start_year,end_year+1,1)
    month = np.arange(1,13,1)

    SLP = np.zeros((len(period),len(month),len(latitude_SLP),len(longitude_SLP)),dtype=float)
    SIC = np.zeros((len(period),len(month),len(latitude_SIC),len(longitude_SIC)),dtype=float)
    #ST = np.zeros((len(period),len(month),len(latitude_ST),len(longitude_ST)),dtype=float)
    T2M = np.zeros((len(period),len(month),len(latitude_T2M),len(longitude_T2M)),dtype=float)

    for i in period:
        j = i -1958
        #datapath_grbs_SIC = pygrib.open(os.path.join(benchmark_path,'ice_monthly_regrid','ice125.091_icec.{}01_{}12'.format(i,i)))
        #datapath_grbs_SLP = pygrib.open(os.path.join(benchmark_path,'SLP_monthly_regrid','anl_surf125.002_prmsl.{}01_{}12'.format(i,i)))
        #datapath_grbs_ST = pygrib.open(os.path.join(benchmark_path,'st_monthly_regrid','anl_surf125.011_tmp.{}01_{}12'.format(i,i)))

        datapath_grbs_SIC = pygrib.open(os.path.join(benchmark_path,'ice_monthly_model','ice.091_icec.reg_tl319.{}01_{}12'.format(i,i)))
        datapath_grbs_SLP = pygrib.open(os.path.join(benchmark_path,'SLP_monthly_model','fcst_surf.002_prmsl.reg_tl319.{}01_{}12'.format(i,i)))
        datapath_grbs_T2M = pygrib.open(os.path.join(benchmark_path,'t2m_monthly_model','anl_surf.011_tmp.reg_tl319.{}01_{}12'.format(i,i)))
        for k in month:
            key_SIC = datapath_grbs_SIC.message(k)
            key_SLP = datapath_grbs_SLP.message(k)
            key_T2M = datapath_grbs_T2M.message(k)
            SIC_temp = key_SIC.values
            SIC_temp[mask==True] = 0
            SIC[j,k-1,:,:] = SIC_temp
            T2M[j,k-1,:,:] = key_T2M.values
            SLP[j,k-1,:,:] = key_SLP.values

    print '*******************************************************************'
    print '*********************** create netcdf file*************************'
    print '*******************************************************************'
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(os.path.join(output_path,'surface_JRA55_monthly_model_regress_SLP_SIC_T2M_1958_2013.nc'), 'w',format = 'NETCDF4')
    # create dimensions for netcdf data
    year_wrap_dim = data_wrap.createDimension('year',len(period))
    month_wrap_dim = data_wrap.createDimension('month',len(month))
    lat_wrap_dim = data_wrap.createDimension('latitude',len(latitude_SLP))
    lon_wrap_dim = data_wrap.createDimension('longitude',len(longitude_SLP))
    # create coordinate variables for 1-dimensions
    year_wrap_var = data_wrap.createVariable('year',np.int32,('year',))
    month_wrap_var = data_wrap.createVariable('month',np.int32,('month',))
    lat_wrap_var = data_wrap.createVariable('latitude',np.float32,('latitude',))
    lon_wrap_var = data_wrap.createVariable('longitude',np.float32,('longitude',))
    # create coordinate variables for 1-dimensions
    mask_wrap_var = data_wrap.createVariable('mask',np.int32,('latitude','longitude'))
    # create the actual 4-d variable
    SIC_wrap_var = data_wrap.createVariable('SIC',np.float64,('year','month','latitude','longitude'),zlib=True)
    SLP_wrap_var = data_wrap.createVariable('SLP',np.float64,('year','month','latitude','longitude'),zlib=True)
    #ST_wrap_var = data_wrap.createVariable('ST',np.float64,('year','month','latitude','longitude'),zlib=True)
    T2M_wrap_var = data_wrap.createVariable('T2M',np.float64,('year','month','latitude','longitude'),zlib=True)
    # global attributes
    data_wrap.description = 'Monthly mean surface fields from JRA55'
    # variable attributes
    lat_wrap_var.units = 'degree_north'
    lon_wrap_var.units = 'degree_east'
    SIC_wrap_var.units = 'Percentage'
    SLP_wrap_var.units = 'Pa'
    #ST_wrap_var.units = 'Kelvin'
    T2M_wrap_var.units = 'Kelvin'

    SIC_wrap_var.long_name = 'sea ice concentration'
    SLP_wrap_var.long_name = 'sea level pressure'
    #ST_wrap_var.long_name = 'surface temperature'
    T2M_wrap_var.long_name = '2 meter temperature'

    # writing data
    year_wrap_var[:] = period
    lat_wrap_var[:] = latitude_SLP
    lon_wrap_var[:] = longitude_SLP
    month_wrap_var[:] = month
    SIC_wrap_var[:] = SIC
    SLP_wrap_var[:] = SLP
    #ST_wrap_var[:] = ST
    T2M_wrap_var[:] = T2M
    mask_wrap_var[:] = mask

    # close the file
    data_wrap.close()

if __name__=="__main__":
    pack_netcdf_point(datapath,output_path)
    print 'Packing netcdf files complete!'

print "Create netcdf file successfully"

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
