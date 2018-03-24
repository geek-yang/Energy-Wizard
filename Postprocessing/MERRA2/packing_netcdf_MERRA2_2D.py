#!/usr/bin/env python
"""
Copyright Netherlands eScience Center

Function        : Packing 2D fields from MERRA2
Author          : Yang Liu
Date            : 2018.03.16
Last Update     : 2018.03.24
Description     : The code aims to pack 2D fields from MERRA2 for further inspection.
                  The fields of insterest are Sea Level Pressure (SLP), Sea
                  Surface Tmperature (SST) and Sea Ice Concentration (SIC).
Return Value    : netCDF
Dependencies    : os, time, numpy, scipy, netCDF4, matplotlib, basemap
variables       : Sea Surface Temperature                       SST
                  Sea Level Pressure                            SLP
                  Sea Ice Concentration                         FRSEAICE
                  Sea Ice Skin Temperature                      TSKINICE
                  Open Water Skin Temperature                   TSKINWTR
                  Surface Pressure                              PS
                  2-Meter Air Temperature                       T2M
                  Surface Skin Temperature                      TS

Caveat!!        : The input data of 2D fields cover the entire globe.
                  Sea surface temperature is divided into 2 parts:
                  sea ice skin temperature
                  open water skin temperature

                  The filled values for tiles with either open water or sea ice is
                  9.9999987e+14

                  The datasets covers 1980 - 2016.
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
# MERRA2 2D fields including Sea Level Pressure
datapath_asm = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/MERRA2/regression/MERRA2_instM_2d_asm_Nx'
# MERRA2 2D fields including Sea Surface Temperature and Sea Ice Concentration
datapath_ocn = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/MERRA2/regression/MERRA2_tavgM_2d_ocn_Nx'
# specify output path for figures
output_path = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/MERRA2/regression'
####################################################################################

def var_key_retrieve(datapath_asm, datapath_ocn, year, month):
    # get the path to each datasets
    print "Start retrieving datasets %d (y) - %s (m)" % (year,namelist_month[month-1])
    # The shape of each variable is (361,576)
    # Sea Level Pressure
    if year < 1992:
        datapath_asm = datapath_asm + os.sep + 'MERRA2_100.instM_2d_asm_Nx.%d%s.SUB.nc4' % (year,namelist_month[month-1])
    elif year < 2001:
        datapath_asm = datapath_asm + os.sep + 'MERRA2_200.instM_2d_asm_Nx.%d%s.SUB.nc4' % (year,namelist_month[month-1])
    elif year < 2011:
        datapath_asm = datapath_asm + os.sep + 'MERRA2_300.instM_2d_asm_Nx.%d%s.SUB.nc4' % (year,namelist_month[month-1])
    else:
        datapath_asm = datapath_asm + os.sep + 'MERRA2_400.instM_2d_asm_Nx.%d%s.SUB.nc4' % (year,namelist_month[month-1])
    # get the variable keys
    var_key_asm = Dataset(datapath_asm)

    #Sea Surface Temperature and Sea Ice Concentration
    if year < 1992:
        datapath_ocn = datapath_ocn + os.sep + 'MERRA2_100.tavgM_2d_ocn_Nx.%d%s.SUB.nc4' % (year,namelist_month[month-1])
    elif year < 2001:
        datapath_ocn = datapath_ocn + os.sep + 'MERRA2_200.tavgM_2d_ocn_Nx.%d%s.SUB.nc4' % (year,namelist_month[month-1])
    elif year < 2011:
        datapath_ocn = datapath_ocn + os.sep + 'MERRA2_300.tavgM_2d_ocn_Nx.%d%s.SUB.nc4' % (year,namelist_month[month-1])
    else:
        datapath_ocn = datapath_ocn + os.sep + 'MERRA2_400.tavgM_2d_ocn_Nx.%d%s.SUB.nc4' % (year,namelist_month[month-1])
    # get the variable keys
    var_key_ocn = Dataset(datapath_ocn)

    print "Retrieving datasets successfully and return the variable key!"
    return var_key_asm, var_key_ocn

# save output datasets
def create_netcdf_point (pool_SLP,pool_SIC,pool_SST_ice,pool_SST_water, pool_T2M,
                         pool_TS, pool_PS, output_path):
    print '*******************************************************************'
    print '*********************** create netcdf file*************************'
    print '*******************************************************************'
    logging.info("Start creating netcdf file for the 2D fields of MERRA2 at each grid point.")
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path + os.sep + 'surface_MERRA2_monthly_regress_1980_2016.nc','w',format = 'NETCDF3_64BIT')
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
    SLP_wrap_var = data_wrap.createVariable('SLP',np.float64,('year','month','latitude','longitude'))
    SIC_wrap_var = data_wrap.createVariable('SIC',np.float64,('year','month','latitude','longitude'))
    SST_ice_wrap_var = data_wrap.createVariable('SST_ice',np.float64,('year','month','latitude','longitude'))
    SST_water_wrap_var = data_wrap.createVariable('SST_water',np.float64,('year','month','latitude','longitude'))
    T2M_wrap_var = data_wrap.createVariable('t2m',np.float64,('year','month','latitude','longitude'))
    TS_wrap_var = data_wrap.createVariable('ts',np.float64,('year','month','latitude','longitude'))
    PS_wrap_var = data_wrap.createVariable('ps',np.float64,('year','month','latitude','longitude'))

    # global attributes
    data_wrap.description = 'Monthly mean 2D fields (SLP,SST,SIC,T2M,TS) of MERRA at each grid point'
    # variable attributes
    lat_wrap_var.units = 'degree_north'
    lon_wrap_var.units = 'degree_east'

    SLP_wrap_var.units = 'Pa'
    SIC_wrap_var.units = '1'
    SST_ice_wrap_var.units = 'Kelvin'
    SST_water_wrap_var.units = 'Kelvin'
    T2M_wrap_var.units = 'Kelvin'
    TS_wrap_var.units = 'Kelvin'
    PS_wrap_var.units = 'Pa'

    SLP_wrap_var.long_name = 'sea level pressure'
    SIC_wrap_var.long_name = 'ice covered fraction of tile'
    SST_ice_wrap_var.long_name = 'sea ice skin temperature'
    SST_water_wrap_var.long_name = 'open water skin temperature'
    T2M_wrap_var.long_name = '2-meter air temperature'
    TS_wrap_var.long_name = 'surface skin temperature'
    PS_wrap_var.long_name = 'surface pressure'

    # writing data
    lat_wrap_var[:] = latitude
    lon_wrap_var[:] = longitude
    month_wrap_var[:] = index_month
    year_wrap_var[:] = period

    SLP_wrap_var[:] = pool_SLP
    SIC_wrap_var[:] = pool_SIC
    SST_ice_wrap_var[:] = pool_SST_ice
    SST_water_wrap_var[:] = pool_SST_water
    T2M_wrap_var[:] = pool_T2M
    TS_wrap_var[:] = pool_TS
    PS_wrap_var[:] = pool_PS

    # close the file
    data_wrap.close()
    print "Create netcdf file successfully"
    logging.info("The generation of netcdf files for the total meridional energy transport and each component on each grid point is complete!!")

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
    Dim_latitude = 361
    Dim_longitude = 576
    #############################################
    #####   Create space for stroing data   #####
    #############################################
    # data pool for zonal integral
    pool_SLP = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    pool_SST_ice = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float) # sea ice skin temperature
    pool_SST_water = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float) # open water skin temperature
    pool_SIC = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    pool_T2M = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    pool_TS = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    pool_PS = np.zeros((Dim_year,Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    latitude = np.zeros(Dim_latitude,dtype=float)
    longitude = np.zeros(Dim_longitude,dtype=float)
    # loop for calculation
    for i in period:
        for j in index_month:
                # get the key of each variable
            var_key_asm, var_key_ocn = var_key_retrieve(datapath_asm,datapath_ocn,i,j)
            pool_SLP[i-1980,j-1,:,:] = var_key_asm.variables['SLP'][0,:,:]
            pool_T2M[i-1980,j-1,:,:] = var_key_asm.variables['T2M'][0,:,:]
            pool_TS[i-1980,j-1,:,:] = var_key_asm.variables['TS'][0,:,:]
            pool_PS[i-1980,j-1,:,:] = var_key_asm.variables['PS'][0,:,:]
            latitude = var_key_asm.variables['lat'][:]
            longitude = var_key_asm.variables['lon'][:]
            pool_SIC[i-1980,j-1,:,:] = var_key_ocn.variables['FRSEAICE'][0,:,:]
            pool_SST_ice[i-1980,j-1,:,:] = var_key_ocn.variables['TSKINICE'][0,:,:] # unit 'K'
            pool_SST_water[i-1980,j-1,:,:] = var_key_ocn.variables['TSKINWTR'][0,:,:] # unit 'K'
    ####################################################################
    ######                 Data Wrapping (NetCDF)                #######
    ####################################################################
    create_netcdf_point(pool_SLP,pool_SIC,pool_SST_ice,pool_SST_water,pool_T2M,
                        pool_TS, pool_PS, output_path)
    print 'Packing 2D fields of MERRA2 is complete!!!'
    print 'The output is in sleep, safe and sound!!!'

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
