#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : Post-processing of the net heat flux from OAflux
Author          : Yang Liu
Date            : 2018.02.26
Last Update     : 2018.03.02
Description     : The code aims to calculate the energy flux within each grid.
                  The surface flux comes from the independent dataset OAflux from WHOI.
                  This dataset contains time series of ocean latent and sensible heat flux, which could be used to calculate
                  the net heat flux at the surface of the ocean with a combination of the
                  surface radiation product from ISCCP.

Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, sys, matplotlib
variables       : Ocean Surface Net Heat Flux               Qnet      [W/m2]
Caveat!!        : Dimension of OAflux dataset
                  OAflux (Geographic Grid)
                  Direction of Axis: from south to north, west to east
                  Latitude      180
                  Longitude     360
                  OAflux has a filled value of 3.2766E+04. We have to refill it with 0.
"""

import numpy as np
import seaborn as sns
import time as tttt
from netCDF4 import Dataset,num2date
import os
import platform
import sys
import numpy as np
import logging
import matplotlib
# generate images without having a window appear
#matplotlib.use('Agg')
import matplotlib.pyplot as plt

# print the system structure and the path of the kernal
print platform.architecture()
print os.path

# calculate the time for the code execution
start_time = tttt.time()
# switch on the seaborn effect
sns.set()

# define the constant:
constant ={'g' : 9.80616,      # gravititional acceleration [m / s2]
           'R' : 6371009,      # radius of the earth [m]
           'cp': 3987,         # heat capacity of sea water [J/(Kg*C)]
           'rho': 1027,        # sea water density [Kg/m3]
            }

################################   Input zone  ######################################
datapath_OAflux = '/mnt/Associate/DataBase/OAFlux/netheat'
# specify output path for figures
output_path = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/OAflux/postprocessing'
####################################################################################
# # OAflux grid info
# ji_oa = 180
# jj_oa = 360

####################################################################################
####################                 OAflux (WHOI)               ###################
####################          time: 1983 July - 2009 Dec         ###################
#######     qnet: monthly mean net surface heat flux, positive downward     ########
####################            qnet = SW - LW - LH - SH          ###################
####################                  unit: W/m2                 ###################
####################           spatial: lat 180 lon 360          ###################
####################################################################################
# load OAflux
year_OAflux = np.arange(1983,2010,1)
qnet_unit = np.zeros((27,12,180,360),dtype=float) # from 1983 July to 2009 Dec, 26.5 years in total
for i in year_OAflux:
    if i == 1983:
        dataset_OAflux = Dataset(datapath_OAflux + os.sep + 'qnet_%d.nc' % (i))
        qnet_yearly = dataset_OAflux.variables['qnet'][:]
        np.ma.set_fill_value(qnet_yearly,0)
        qnet_unit[0,6:,:,:] = qnet_yearly
        # get all the constants and the grid info
        lat = dataset_OAflux.variables['lat'][:]
        lon = dataset_OAflux.variables['lon'][:]
        # due to ice formation and melting, the mask is changing all the time
        #mask = np.ma.getmask(qnet_yearly[4,:,:])
    else:
        dataset_OAflux = Dataset(datapath_OAflux + os.sep + 'qnet_%d.nc' % (i))
        qnet_yearly = dataset_OAflux.variables['qnet'][:]
        np.ma.set_fill_value(qnet_yearly,0)
        qnet_unit[i-1983,:,:,:] = qnet_yearly

qnet_unit[qnet_unit==32766] = 0
# calculate net surface heat flux per area
qnet = np.zeros(qnet_unit.shape)
# calculate zonal & meridional grid size on earth
# the earth is taken as a perfect sphere, instead of a ellopsoid
dx = 2 * np.pi * constant['R'] * np.cos(2 * np.pi * lat / 360) / len(lon)
dy = np.pi * constant['R'] / (180-1)
# calculate ocean surface net heat flux by area
for i in np.arange(len(lat)):
    qnet[:,:,i,:] = qnet_unit[:,:,i,:] * dx[i] * dy / 1E+12 # change the unit to tera watt

print '*******************************************************************'
print '*********************** create netcdf file ************************'
print '*******************************************************************'
# wrap the datasets into netcdf file
# 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
data_wrap = Dataset(output_path + os.sep + 'OAflux_qnet_point.nc','w',format = 'NETCDF3_64BIT')
# create dimensions for netcdf data
year_wrap_dim = data_wrap.createDimension('year',len(year_OAflux))
month_wrap_dim = data_wrap.createDimension('month',12)
lat_wrap_dim = data_wrap.createDimension('lat',len(lat))
lon_wrap_dim = data_wrap.createDimension('lon',len(lon))
# create coordinate variables for 3-dimensions
# 1D
year_wrap_var = data_wrap.createVariable('year',np.int32,('year',))
month_wrap_var = data_wrap.createVariable('month',np.int32,('month',))
lat_wrap_var = data_wrap.createVariable('latitude',np.float32,('lat',))
lon_wrap_var = data_wrap.createVariable('longitude',np.float32,('lon',))
# 2D
#mask_wrap_var = data_wrap.createVariable('mask',np.int32,('lat','lon'))
# 4D
qnet_unit_wrap_var = data_wrap.createVariable('qnet_unit',np.float64,('year','month','lat','lon'))
qnet_wrap_var = data_wrap.createVariable('qnet',np.float64,('year','month','lat','lon'))
# global attributes
data_wrap.description = 'Ocean surface net heat flux at each point (positive downward)'
# variable attributes
lat_wrap_var.units = 'latitude'
lon_wrap_var.units = 'longitude'
qnet_unit_wrap_var.units = 'watt per square meter'
qnet_wrap_var.units = 'tera watt'

lat_wrap_var.long_name = 'Geographical grid latitude'
lon_wrap_var.long_name = 'Geographical grid longitude'
qnet_wrap_var.long_name = 'Ocean surface net heat flux per square meter'
qnet_wrap_var.long_name = 'Ocean surface net heat flux'
# writing data
#year_wrap_var[:] = period
lat_wrap_var[:] = lat
lon_wrap_var[:] = lon
year_wrap_var[:] = year_OAflux
month_wrap_var[:] = np.arange(1,13,1)
qnet_unit_wrap_var[:] = qnet_unit
qnet_wrap_var[:] = qnet
# close the file
data_wrap.close()
print "Create netcdf file successfully"

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
