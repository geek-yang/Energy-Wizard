#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : A statistical look into the temporal and spatial distribution of fields (GLORYS2V3)
Author          : Yang Liu
Date            : 2018.04.14
Last Update     : 2018.04.16
Description     : The code aims to statistically take a close look into each fields.
                  This could help understand the difference between each datasets, which
                  will explain the deviation in meridional energy transport. Specifically,
                  the script deals with oceanic reanalysis dataset SODA3 from Mercator Ocean.
                  The complete computaiton is accomplished on model level (original MOM5_z50 grid).
                  All the interpolations are made on the V grid, including scalars.
                  For the sake of accuracy, the zonal integrations are taken on
                  i-j coordinate, which follows i-coord.
                  The script also calculates the ocean heat content for certain layers.
Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, sys, matplotlib, logging
variables       : Potential Temperature                     temp
                  Zonal Current Velocity                    u
                  Meridional Current Velocity               v
                  Zonal Grid Spacing Scale Factors          e1
                  Meridional Grid Spacing Scale Factors     e2
                  Land-Sea Mask                             mask
Caveat!!        : The full dataset is from 1980 to 2015.
                  Direction of Axis:
                  Model Level: surface to bottom
                  The data is monthly mean
                  The variables (T,U,V) of SODA3 are saved in the form of masked
                  arrays. The mask has filled value of 1E+20 (in order to maintain
                  the size of the netCDF file and make full use of the storage). When
                  take the mean of intergral, this could result in abnormal large results.
                  With an aim to avoid this problem, it is important to re-set the filled
                  value to be 0 and then take the array with filled value during calculation.
                  (use "masked_array.filled()")
"""
import numpy as np
#import seaborn as sns
#import scipy as sp
import time as tttt
from netCDF4 import Dataset,num2date
import os
import platform
import sys
import logging
import matplotlib
# generate images without having a window appear
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, cm
#import cartopy.crs as ccrs
#from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
#import iris
#import iris.plot as iplt
#import iris.quickplot as qplt

##########################################################################
###########################   Units vacabulory   #########################
# cpT:  [J / kg C] * [C]     = [J / kg]
# rho cpT dxdydz = [m/s] * [J / kg] * [kg/m3] * m * m * m = [J]
##########################################################################
##########################################################################

# print the system structure and the path of the kernal
print platform.architecture()
print os.path

# switch on the seaborn effect
#sns.set()

# calculate the time for the code execution
start_time = tttt.time()

# Redirect all the console output to a file
sys.stdout = open('/home/lwc16308/reanalysis/SODA3/console_statistics.out','w+')

# logging level 'DEBUG' 'INFO' 'WARNING' 'ERROR' 'CRITICAL'
#logging.basicConfig(filename = 'F:\DataBase\ORAS4\history.log', filemode = 'w',level = logging.DEBUG,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(filename = '/home/lwc16308/reanalysis/SODA3/history_statistics.log',
                    filemode = 'w+', level = logging.DEBUG,
                    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# define the constant:
constant ={'g' : 9.80616,      # gravititional acceleration [m / s2]
           'R' : 6371009,      # radius of the earth [m]
           'cp': 3987,         # heat capacity of sea water [J/(Kg*C)]
           'rho': 1027,        # sea water density [Kg/m3]
            }

################################   Input zone  ######################################
folder_name_in = sys.stdin.readline()
input_year = int(folder_name_in)
# specify data path
datapath = '/projects/0/blueactn/reanalysis/SODA3/5day/soda%d' % (input_year)
# path of mask file
datapath_mask = '/projects/0/blueactn/reanalysis/SODA3'
# the input files are 5 days data
# each file has a name with date
# we have to load files for each month seperately, for the sake of monthly mean
# each record for each month is placed in folders by month
# the names are listed in a txt file line by line
# we will load the name from the txt file
datapath_namelist = '/projects/0/blueactn/reanalysis/SODA3/5day/soda%d' % (input_year)
ff = open(datapath_namelist + os.sep + 'namelist.txt','r')
# can not skip \n
#namelist = ff.readlines()
# remember to skip \n
namelist = ff.read().splitlines()
print namelist
ff.close()

# specify output path for the netCDF4 file
output_path = '/projects/0/blueactn/reanalysis/SODA3/statistics'
####################################################################################

def var_key(datapath, file_name):
    # get the path to each datasets
    print "Start retrieving datasets %s" % (file_name)
    logging.info("Start retrieving variables from %s" % (file_name))
    ####################################################################
    #########  Pick up variables and deal with the naming rule #########
    ####################################################################
    datapath_var = datapath + os.sep + '%s' % (file_name)
    # get the variable keys
    soda_key = Dataset(datapath_var)

    print "Retrieving datasets from %s successfully!" % (file_name)
    logging.info("Retrieving variables from %s successfully!" % (file_name))
    return soda_key

def var_coordinate(datapath_mask):
    print "Start retrieving the MOM5 coordinate and mask info"
    logging.info('Start retrieving the MOM5 coordinate and mask info')
    # get the variable keys
    mesh_mask_key = Dataset(datapath_mask + os.sep + 'topog.nc')
    #extract variables
    # nominal coordinate info (1D)
    grid_x_T = mesh_mask_key.variables['grid_x_T'][:]           # Nominal Longitude of T-cell center
    grid_y_T = mesh_mask_key.variables['grid_y_T'][:]           # Nominal Latitude of T-cell center
    grid_x_C = mesh_mask_key.variables['grid_x_C'][:]           # Nominal Longitude of C-cell center
    grid_y_C = mesh_mask_key.variables['grid_y_C'][:]           # Nominal Latitude of C-cell center
    # lat-lon-depth coordinate info (2D)
    x_T = mesh_mask_key.variables['x_T'][:]                     # Geographic Longitude of T-cell center
    y_T = mesh_mask_key.variables['y_T'][:]                     # Geographic Latitude of T-cell center
    x_C = mesh_mask_key.variables['x_C'][:]                     # Geographic Longitude of C-cell center
    y_C = mesh_mask_key.variables['y_C'][:]                     # Geographic Latitude of C-cell center
    # depth
    zt = mesh_mask_key.variables['zt'][:]                       # Depth of T cell (z50)
    zb = mesh_mask_key.variables['zb'][:]                       # Depth of T cell edges (z50)
    # calculate the depth of each layer
    dz = np.zeros(zt.shape)
    dz[0] = zb[0]
    dz[1:] = zb[1:] - zb[:-1]
    # area of T cell - for the computation of ocean heat content
    area_T = mesh_mask_key.variables['area_T'][:]               # Area of T-cell
    # width (e1t) and height (e2t) of T-cell
    e1t = mesh_mask_key.variables['ds_01_21_T'][:]
    e2t = mesh_mask_key.variables['ds_10_12_T'][:]
    # width (e1c) and height (e2c) of C-cell
    e1c = mesh_mask_key.variables['ds_01_21_C'][:]
    e2c = mesh_mask_key.variables['ds_10_12_C'][:]
    # land-sea mask (2D)
    tmask = mesh_mask_key.variables['wet'][:]                   # land/sea flag (0=land) for T-cell
    cmask = mesh_mask_key.variables['wet_c'][:]                 # land/sea flag (0=land) for C-cell
    # number of vertical cells - topography
    # this number also indicates the partial cells
    mbathy_t = mesh_mask_key.variables['num_levels'][:]         # number of vertical T-cells
    mbathy_c = mesh_mask_key.variables['num_levels_c'][:]       # number of vertical C-cells
    # topographic depth of cell
    topo_depth_t = mesh_mask_key.variables['depth'][:]          # topographic depth of T-cell
    topo_depth_c = mesh_mask_key.variables['depth_c'][:]        # topographic depth of C-cell
    # calculate the atlantic land sea mask
    tmaskatl = np.empty_like(tmask)                             # avoid address pointer issue
    tmaskatl[:] = tmask
    tmaskatl[0:225,:] = 0 # boundary south
    tmaskatl[:,0:727] = 0 # boundary west
    tmaskatl[:,1200:] = 0 # boundary east
    tmaskatl[y_T>70] = 0 # boundary north
    # correction Mediterranean
    tmaskatl[614:680,1100:1240] = 0
    tmaskatl[660:720,1140:1280] = 0
    # correction Pacific
    tmaskatl[225:522,759:839] = 0
    tmaskatl[225:545,670:780] = 0
    tmaskatl[225:560,670:759] = 0

    print "Retrieve the MOM5 coordinate and mask info successfully!"
    logging.info('Finish retrieving the MOM5 coordinate and mask info')

    return grid_x_T, grid_y_T, grid_x_C, grid_y_C, x_T, y_T, x_C, y_C, zt, zb, dz, area_T,\
           e1t, e2t, e1c, e2c, tmask, tmaskatl, cmask, mbathy_t, mbathy_c, topo_depth_t, topo_depth_c

def mass_transport(soda_key,e1c):
    '''
    This function is used to calculate the mass transport.
    The unit is Sv (1E+6 m3/s)
    '''
    print "Compute the mass transport for globle and Atlantic!"
    logging.info('Compute the mass transport for globle and Atlantic!')
    #dominant equation for stream function
    # psi = e1c(m) * rho(kg/m3) * v(m/s) * dz(m) = (kg/s)
    # extract variables
    #u = soda_key.variables['vozocrtx'][0,:,:,:]
    v = soda_key.variables['v'][0,:,:,:]
    # set the filled value to be 0
    #np.ma.set_fill_value(u,0)
    np.ma.set_fill_value(v,0)
    # define the stream function psi
    psi_globe = np.zeros((level,jj,ji),dtype=float)
    psi_atlantic = np.zeros((level,jj,ji),dtype=float)
    for i in np.arange(level):
        psi_globe[i,:,:] = e1c * v[i,:,:] * cmask * dz[i] -\
                           e1c * v[i,:,:] * cmask * dz_adjust_c[i,:,:]
        # avoid the filling value during summation (the default filling value is quite large)
        psi_globe[i,:,:] = psi_globe[i,:,:] * cmask
    # Mass transport at Atlantic
    for i in np.arange(level):
        psi_atlantic[i,:,:] = e1c * v[i,:,:] * cmask * tmaskatl * dz[i] -\
                              e1c * v[i,:,:] * cmask * tmaskatl * dz_adjust_c[i,:,:]
        # avoid the filling value during summation
        psi_atlantic[i,:,:] = psi_atlantic[i,:,:] * tmaskatl * cmask
    # take the zonal integral
    psi_globe_zonal_int = np.sum(psi_globe,2)/1e+6 # the unit is changed to Sv
    psi_atlantic_zonal_int = np.sum(psi_atlantic,2)/1e+6 # the unit is changed to Sv
    # take the vertical integral
    psi_globe_vert_int = np.sum(psi_globe,0)/1e+6 # the unit is changed to Sv
    psi_atlantic_vert_int = np.sum(psi_atlantic,0)/1e+6 # the unit is changed to Sv

    print "Compute the mass transport for globle and Atlantic successfully!"
    logging.info('Compute the mass transport for globle and Atlantic successfully!')

    return psi_globe_zonal_int, psi_atlantic_zonal_int, psi_globe_vert_int, psi_atlantic_vert_int

def ocean_heat_content(soda_key):
    '''
    This function is used to compute the ocean heat content.
    '''
    # extract variables
    print "Start extracting variables for the quantification of meridional energy transport."
    temp = soda_key.variables['temp'][0,:,:,:]                      # potential temperature, the unit is Celsius!
    # set the filled value to be 0
    np.ma.set_fill_value(temp,0)
    # check the filled Value
    #print temp.filled()
    print 'Extracting variables successfully!'
    # calculate heat flux at each grid point
    OHC_globe = np.zeros((level,jj,ji),dtype=float)
    OHC_atlantic = np.zeros((level,jj,ji),dtype=float)
    # expand the grid size matrix e1v to avoid more loops
    #e1t_3D = np.repeat(e1t[np.newaxis,:,:],level,0)
    #e2t_3D = np.repeat(e2t[np.newaxis,:,:],level,0)
    #tmaskatl_3D = np.repeat(tmaskatl[np.newaxis,:,:],level,0)
    for i in np.arange(level):
        OHC_globe[i,:,:] = constant['rho'] * constant['cp'] * temp[i,:,:] * e1t * e2t * dz[i] * tmask -\
                           constant['rho'] * constant['cp'] * temp[i,:,:] * e1t * e2t * dz_adjust_t[i,:,:] * tmask
        OHC_atlantic[i,:,:] = constant['rho'] * constant['cp'] * temp[i,:,:] * e1t * e2t * dz[i] * tmask * tmaskatl -\
                              constant['rho'] * constant['cp'] * temp[i,:,:] * e1t * e2t * dz_adjust_t[i,:,:] * tmask * tmaskatl
        OHC_globe[i,:,:] = OHC_globe[i,:,:] * tmask
        OHC_atlantic[i,:,:] = OHC_atlantic[i,:,:] * tmask * tmaskatl
    # take the zonal integral
    OHC_globe_zonal_int = np.sum(OHC_globe,2)/1e+12 # the unit is changed to tera joule
    OHC_atlantic_zonal_int = np.sum(OHC_atlantic,2)/1e+12 # the unit is changed to tera joule
    # take the vertical integral
    OHC_globe_vert_int = np.sum(OHC_globe,0)/1e+12 # the unit is changed to tera joule
    OHC_atlantic_vert_int = np.sum(OHC_atlantic,0)/1e+12 # the unit is changed to tera joule
    # ocean heat content for certain layers
    # surface to 500m
    OHC_globe_vert_0_500 = np.sum(OHC_globe[0:24,:,:],0)/1e+12 # the unit is changed to tera joule
    OHC_atlantic_vert_0_500 = np.sum(OHC_atlantic[0:24,:,:],0)/1e+12 # the unit is changed to tera joule
    # 500m to 1000m
    OHC_globe_vert_500_1000 = np.sum(OHC_globe[24:29,:,:],0)/1e+12         # layer 26 is in between 800 - 1200
    OHC_atlantic_vert_500_1000 = np.sum(OHC_atlantic[24:29,:,:],0)/1e+12
    # 1000m to 2000m
    OHC_globe_vert_1000_2000 = np.sum(OHC_globe[29:34,:,:],0)/1e+12
    OHC_atlantic_vert_1000_2000 = np.sum(OHC_atlantic[29:34,:,:],0)/1e+12
    # 2000 to bottom
    OHC_globe_vert_2000_inf = np.sum(OHC_globe[34:,:,:],0)/1e+12
    OHC_atlantic_vert_2000_inf = np.sum(OHC_atlantic[34:,:,:],0)/1e+12
    print '*****************************************************************************'
    print "****     Computation of ocean heat content in the ocean is finished      ****"
    print "************         The result is in tera-watt (1E+12)          ************"
    print '*****************************************************************************'
    return OHC_globe_zonal_int, OHC_atlantic_zonal_int, OHC_globe_vert_int, OHC_atlantic_vert_int,\
           OHC_globe_vert_0_500, OHC_atlantic_vert_0_500, OHC_globe_vert_500_1000, OHC_atlantic_vert_500_1000,\
           OHC_globe_vert_1000_2000, OHC_atlantic_vert_1000_2000, OHC_globe_vert_2000_inf, OHC_atlantic_vert_2000_inf

def field_statistics(soda_key):
    # extract variables
    print "Start extracting variables for the quantification of meridional energy transport."
    temp = soda_key.variables['temp'][0,:,:,:] # the unit of temp is Celsius!
    u = soda_key.variables['u'][0,:,:,:]
    v = soda_key.variables['v'][0,:,:,:]
    print 'Extracting variables successfully!'
    # set the filled value to be 0
    np.ma.set_fill_value(temp,0)
    np.ma.set_fill_value(u,0)
    np.ma.set_fill_value(v,0)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
    # Due to the nature of the land-sea mask, when we take the mean value we can not
    # use the np.mean to calculate it from the original field, as there are so many
    # empty points. Instead, we must calculate the sum of each variable and then
    # devide the sum of mask.
    # For the mean, we also have to take the cell scale (length, width, height) into
    # consider
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
    # increase the dimension of mask array
    tmaskatl_3D = np.repeat(tmaskatl[np.newaxis,:,:],level,0)
    # expand the grid size matrix e1v to avoid more loops
    e1t_3D = np.repeat(e1t[np.newaxis,:,:],level,0)
    e1c_3D = np.repeat(e1u[np.newaxis,:,:],level,0)

    # vertical mean
    temp_globe_vert_weight = np.zeros((level,jj,ji),dtype=float)
    u_globe_vert_weight = np.zeros((level,jj,ji),dtype=float)
    v_globe_vert_weight = np.zeros((level,jj,ji),dtype=float)

    for i in np.arange(level):
        temp_globe_vert_weight[i,:,:] = temp[i,:,:] * dz_0[i] * tmask -\
                                         temp[i,:,:] * dz_adjust_t[i,:,:] * tmask
        u_globe_vert_weight[i,:,:] = u[i,:,:] * dz[i] * cmask -\
                                     u[i,:,:] * dz_adjust_c[i,:,:] * cmask
        v_globe_vert_weight[i,:,:] = v[i,:,:] * dz[i] * cmask -\
                                     v[i,:,:] * dz_adjust_c[i,:,:] * cmask

    temp_globe_vert_mean = np.sum(temp_globe_vert_weight,0) / topo_depth_t
    u_globe_vert_mean = np.sum(u_globe_vert_weight,0) / topo_depth_c
    v_globe_vert_mean = np.sum(v_globe_vert_weight,0) / topo_depth_c

    # zonal mean
    # take the sum of variables
    temp_globe_zonal_weight = np.zeros((level,jj,ji),dtype=float)
    u_globe_zonal_weight = np.zeros((level,jj,ji),dtype=float)
    v_globe_zonal_weight = np.zeros((level,jj,ji),dtype=float)
    temp_atlantic_zonal_weight = np.zeros((level,jj,ji),dtype=float)
    u_atlantic_zonal_weight = np.zeros((level,jj,ji),dtype=float)
    v_atlantic_zonal_weight = np.zeros((level,jj,ji),dtype=float)

    for i in np.arange(level):
        temp_globe_zonal_weight[i,:,:] = temp[i,:,:] * e1t * tmask
        temp_atlantic_zonal_weight[i,:,:] = temp[i,:,:] * e1t * tmask * tmaskatl
        u_globe_zonal_weight[i,:,:] = u[i,:,:] * e1c * cmask
        u_atlantic_zonal_weight[i,:,:] = u[i,:,:] * e1c * cmask * tmaskatl
        v_globe_zonal_weight[i,:,:] = v[i,:,:] * e1c * cmask
        v_atlantic_zonal_weight[i,:,:] = v[i,:,:] * e1c * cmask * tmaskatl

    # take the zonal mean
    temp_globe_zonal_mean = np.sum(temp_globe_zonal_weight,2) / np.sum(e1t * tmask,2)
    temp_atlantic_zonal_mean = np.sum(temp_atlantic_zonal_weight,2) / np.sum(e1t * tmask * tmaskatl,2)
    u_globe_zonal_mean = np.sum(u_globe_zonal_weight,2) / np.sum(e1c * cmask,2)
    u_atlantic_zonal_mean = np.sum(u_atlantic_zonal_weight,2) / np.sum(e1c * cmask * tmaskatl,2)
    v_globe_zonal_mean = np.sum(v_globe_zonal_weight,2) / np.sum(e1c * cmask,2)
    v_atlantic_zonal_mean = np.sum(v_atlantic_zonal_weight,2) / np.sum(e1c * cmask * tmaskatl,2)

    return temp_globe_vert_mean, u_globe_vert_mean, v_globe_vert_mean,\
           temp_globe_zonal_mean, temp_atlantic_zonal_mean, u_globe_zonal_mean,\
           u_atlantic_zonal_mean, v_globe_zonal_mean, v_atlantic_zonal_mean

def create_netcdf_point (psi_pool_glo_zonal, psi_pool_atl_zonal, psi_pool_glo_vert, psi_pool_atl_vert,\
                        OHC_pool_glo_zonal, OHC_pool_atl_zonal, OHC_pool_glo_vert, OHC_pool_atl_vert,\
                        OHC_pool_glo_vert_0_500, OHC_pool_atl_vert_0_500, OHC_pool_glo_vert_500_1000,\
                        OHC_pool_atl_vert_500_1000, OHC_pool_glo_vert_1000_2000, OHC_pool_atl_vert_1000_2000,\
                        OHC_pool_glo_vert_2000_inf, OHC_pool_atl_vert_2000_inf, temp_pool_glo_vert,\
                        u_pool_glo_vert, v_pool_glo_vert, temp_pool_glo_zonal, temp_pool_atl_zonal,\
                        u_pool_glo_zonal, u_pool_atl_zonal, v_pool_glo_zonal, v_pool_atl_zonal ,output_path):
    print '*******************************************************************'
    print '*********************** create netcdf file ************************'
    print '*********************   statistics on MOM   **********************'
    print '*******************************************************************'
    logging.info("Start creating netcdf file for the statistics of fields at each grid point.")
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path + os.sep + 'SODA3_model_5daily_mom5_statistics_point_%d.nc' % (input_year),'w',format = 'NETCDF3_64BIT')
    # create dimensions for netcdf data
    lat_wrap_dim = data_wrap.createDimension('j',jj)
    lon_wrap_dim = data_wrap.createDimension('i',ji)
    lev_wrap_dim = data_wrap.createDimension('lev',level)
    # create coordinate variables for 3-dimensions
    # 1D
    lat_wrap_var = data_wrap.createVariable('latitude_aux',np.float32,('j',))
    lev_wrap_var = data_wrap.createVariable('lev',np.float32,('lev',))
    # 2D
    gphit_wrap_var = data_wrap.createVariable('y_T',np.float32,('j','i'))
    glamt_wrap_var = data_wrap.createVariable('x_T',np.float32,('j','i'))
    gphic_wrap_var = data_wrap.createVariable('y_C',np.float32,('j','i'))
    glamc_wrap_var = data_wrap.createVariable('x_C',np.float32,('j','i'))
    # 2D
    psi_glo_zonal_wrap_var = data_wrap.createVariable('psi_glo_zonal',np.float64,('lev','j'))
    psi_atl_zonal_wrap_var = data_wrap.createVariable('psi_atl_zonal',np.float64,('lev','j'))
    OHC_glo_zonal_wrap_var = data_wrap.createVariable('OHC_glo_zonal',np.float64,('lev','j'))
    OHC_atl_zonal_wrap_var = data_wrap.createVariable('OHC_atl_zonal',np.float64,('lev','j'))
    temp_glo_zonal_wrap_var = data_wrap.createVariable('temp_glo_zonal',np.float64,('lev','j'))
    temp_atl_zonal_wrap_var = data_wrap.createVariable('temp_atl_zonal',np.float64,('lev','j'))
    u_glo_zonal_wrap_var = data_wrap.createVariable('u_glo_zonal',np.float64,('lev','j'))
    u_atl_zonal_wrap_var = data_wrap.createVariable('u_atl_zonal',np.float64,('lev','j'))
    v_glo_zonal_wrap_var = data_wrap.createVariable('v_glo_zonal',np.float64,('lev','j'))
    v_atl_zonal_wrap_var = data_wrap.createVariable('v_atl_zonal',np.float64,('lev','j'))

    psi_glo_vert_wrap_var = data_wrap.createVariable('psi_glo_vert',np.float64,('j','i'))
    psi_atl_vert_wrap_var = data_wrap.createVariable('psi_atl_vert',np.float64,('j','i'))
    OHC_glo_vert_wrap_var = data_wrap.createVariable('OHC_glo_vert',np.float64,('j','i'))
    OHC_atl_vert_wrap_var = data_wrap.createVariable('OHC_atl_vert',np.float64,('j','i'))
    OHC_glo_vert_0_500_wrap_var = data_wrap.createVariable('OHC_glo_vert_0_500',np.float64,('j','i'))
    OHC_atl_vert_0_500_wrap_var = data_wrap.createVariable('OHC_atl_vert_0_500',np.float64,('j','i'))
    OHC_glo_vert_500_1000_wrap_var = data_wrap.createVariable('OHC_glo_vert_500_1000',np.float64,('j','i'))
    OHC_atl_vert_500_1000_wrap_var = data_wrap.createVariable('OHC_atl_vert_500_1000',np.float64,('j','i'))
    OHC_glo_vert_1000_2000_wrap_var = data_wrap.createVariable('OHC_glo_vert_1000_2000',np.float64,('j','i'))
    OHC_atl_vert_1000_2000_wrap_var = data_wrap.createVariable('OHC_atl_vert_1000_2000',np.float64,('j','i'))
    OHC_glo_vert_2000_inf_wrap_var = data_wrap.createVariable('OHC_glo_vert_2000_inf',np.float64,('j','i'))
    OHC_atl_vert_2000_inf_wrap_var = data_wrap.createVariable('OHC_atl_vert_2000_inf',np.float64,('j','i'))
    temp_glo_vert_wrap_var = data_wrap.createVariable('temp_glo_vert',np.float64,('j','i'))
    u_glo_vert_wrap_var = data_wrap.createVariable('u_glo_vert',np.float64,('j','i'))
    v_glo_vert_wrap_var = data_wrap.createVariable('v_glo_vert',np.float64,('j','i'))

    # global attributes
    data_wrap.description = 'Monthly mean statistics of fields on MOM grid'
    # variable attributes
    lev_wrap_var.units = 'm'
    gphit_wrap_var.units = 'MOM5_latitude_Tgrid'
    glamt_wrap_var.units = 'MOM5_longitude_Tgrid'
    gphic_wrap_var.units = 'MOM5_latitude_vgrid'
    glamc_wrap_var.units = 'MOM5_longitude_vgrid'

    psi_glo_zonal_wrap_var.units = 'Sv'
    psi_atl_zonal_wrap_var.units = 'Sv'
    OHC_glo_zonal_wrap_var.units = 'tera joule'
    OHC_atl_zonal_wrap_var.units = 'tera joule'
    temp_glo_zonal_wrap_var.units = 'Celsius'
    temp_atl_zonal_wrap_var.units = 'Celsius'
    u_glo_zonal_wrap_var.units = 'm/s'
    u_atl_zonal_wrap_var.units = 'm/s'
    v_glo_zonal_wrap_var.units = 'm/s'
    v_atl_zonal_wrap_var.units = 'm/s'

    psi_glo_vert_wrap_var.units = 'Sv'
    psi_atl_vert_wrap_var.units = 'Sv'
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
    temp_glo_vert_wrap_var.units = 'Celsius'
    u_glo_vert_wrap_var.units = 'm/s'
    v_glo_vert_wrap_var.units = 'm/s'

    lat_wrap_var.long_name = 'auxillary latitude'
    lev_wrap_var.long_name = 'depth'
    gphit_wrap_var.long_name = 'MOM5 Tgrid latitude'
    glamt_wrap_var.long_name = 'MOM5 Tgrid longitude'
    gphic_wrap_var.long_name = 'MOM5 cgrid latitude'
    glamc_wrap_var.long_name = 'MOM5 cgrid longitude'

    psi_glo_zonal_wrap_var.long_name = 'Global Meridional Mass Transport (zonal integral)'
    psi_atl_zonal_wrap_var.long_name = 'Atlantic Meridional Mass Transport (zonal integral)'
    OHC_glo_zonal_wrap_var.long_name = 'Global Ocean Heat Content (zonal integral)'
    OHC_atl_zonal_wrap_var.long_name = 'Atlantic Ocean Heat Content (zonal integral)'
    temp_glo_zonal_wrap_var.long_name = 'Global Potential Temperature (zonal mean)'
    temp_atl_zonal_wrap_var.long_name = 'Atlantic Potential Temperature (zonal mean)'
    u_glo_zonal_wrap_var.long_name = 'Global Zonal Velocity (zonal mean)'
    u_atl_zonal_wrap_var.long_name = 'Atlantic Zonal Velocity (zonal mean)'
    v_glo_zonal_wrap_var.long_name = 'Global Meridional Velocity (zonal mean)'
    v_atl_zonal_wrap_var.long_name = 'Atlantic Meridional Velocity (zonal mean)'

    psi_glo_vert_wrap_var.long_name = 'Global Meridional Mass Transport (vertical integral)'
    psi_atl_vert_wrap_var.long_name = 'Atlantic Meridional Mass Transport (vertical integral)'
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
    temp_glo_vert_wrap_var.long_name = 'Global Potential Temperature (vertical mean)'
    u_glo_vert_wrap_var.long_name = 'Global Zonal Velocity (vertical mean)'
    v_glo_vert_wrap_var.long_name = 'Global Meridional Velocity (vertical mean)'

    # writing data
    lat_wrap_var[:] = grid_y_C
    lev_wrap_var[:] = zt
    gphit_wrap_var[:] = y_T
    glamt_wrap_var[:] = x_T
    gphic_wrap_var[:] = y_C
    glamc_wrap_var[:] = x_C

    psi_glo_zonal_wrap_var[:] = psi_pool_glo_zonal
    psi_atl_zonal_wrap_var[:] = psi_pool_atl_zonal
    OHC_glo_zonal_wrap_var[:] = OHC_pool_glo_zonal
    OHC_atl_zonal_wrap_var[:] = OHC_pool_atl_zonal
    temp_glo_zonal_wrap_var[:] = temp_pool_glo_zonal
    temp_atl_zonal_wrap_var[:] = temp_pool_atl_zonal
    u_glo_zonal_wrap_var[:] = u_pool_glo_zonal
    u_atl_zonal_wrap_var[:] = u_pool_atl_zonal
    v_glo_zonal_wrap_var[:] = v_pool_glo_zonal
    v_atl_zonal_wrap_var[:] = v_pool_atl_zonal

    psi_glo_vert_wrap_var[:] = psi_pool_glo_vert
    psi_atl_vert_wrap_var[:] = psi_pool_atl_vert
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
    temp_glo_vert_wrap_var[:] = temp_pool_glo_vert
    u_glo_vert_wrap_var[:] = u_pool_glo_vert
    v_glo_vert_wrap_var[:] = v_pool_glo_vert
    # close the file
    data_wrap.close()
    print "Create netcdf file successfully"
    logging.info("The generation of netcdf files for the statisticas of fields in GLORYS2V3 on each grid point is complete!!")

if __name__=="__main__":
    print '*******************************************************************'
    print '******  Prepare all the constants and auxillary variables   *******'
    print '*******************************************************************'
    # create the year index
    #period = np.arange(start_year,end_year+1,1)
    namelist_month = ['01','02','03','04','05','06','07','08','09','10','11','12']
    #index_month = np.arange(12)
    #index_filename = len(namelist)
    ji = 1440
    jj = 1070
    level = 50
    # extract the mesh_mask and coordinate information
    grid_x_T, grid_y_T, grid_x_C, grid_y_C, x_T, y_T, x_C, y_C, zt, zb, dz, area_T, e1t,\
    e2t, e1c, e2c, tmask, tmaskatl, cmask, mbathy_t, mbathy_c, topo_depth_t, topo_depth_c = var_coordinate(datapath_mask)
    print '*******************************************************************'
    print '*******************  Partial cells correction   *******************'
    print '*******************************************************************'
    # construct partial cell depth matrix
    # the depth including partial cell is given by topo_depth_t&c
    # topo_depth_t and topo_depth_c are totally different
    # for the sake of simplicity of the code, just calculate the difference between e3t_0 and e3t_ps
    # then minus this adjustment when calculate the OMET at each layer with mask
    # Attention! Since python start with 0, the partial cell info given in mbathy should incoporate with this
    # !!!
    dz_adjust_t = np.zeros((level,jj,ji),dtype = float)
    dz_adjust_c = np.zeros((level,jj,ji),dtype = float)
    for i in np.arange(jj):
        for j in np.arange(ji):
            if mbathy_t[i,j] != 0:
                counter_t = int(mbathy_t[i,j] - 1)
                dz_adjust_t[counter_t,i,j] = zb[counter_t] - topo_depth_t[i,j]    # python start with 0, so i-1
            if mbathy_c[i,j] != 0:
                counter_c = int(mbathy_c[i,j] - 1)
                dz_adjust_c[counter_c,i,j] = zb[counter_c] - topo_depth_c[i,j]    # python start with 0, so i-1
    ####################################################################
    ###  Create space for stroing intermediate variables and outputs ###
    ####################################################################
    # create a data pool to save the OHC for each year and month
    # zonal integral (vertical profile)
    OHC_pool_glo_zonal = np.zeros((len(namelist),level,jj),dtype = float)
    OHC_pool_atl_zonal = np.zeros((len(namelist),level,jj),dtype = float)
    # vertical integral (horizontal profile)
    OHC_pool_glo_vert = np.zeros((len(namelist),jj,ji),dtype = float)
    OHC_pool_atl_vert = np.zeros((len(namelist),jj,ji),dtype = float)
    # vertical integral (horizontal profile) and OHC for certain layers
    OHC_pool_glo_vert_0_500 = np.zeros((len(namelist),jj,ji),dtype = float)
    OHC_pool_atl_vert_0_500 = np.zeros((len(namelist),jj,ji),dtype = float)
    OHC_pool_glo_vert_500_1000 = np.zeros((len(namelist),jj,ji),dtype = float)
    OHC_pool_atl_vert_500_1000 = np.zeros((len(namelist),jj,ji),dtype = float)
    OHC_pool_glo_vert_1000_2000 = np.zeros((len(namelist),jj,ji),dtype = float)
    OHC_pool_atl_vert_1000_2000 = np.zeros((len(namelist),jj,ji),dtype = float)
    OHC_pool_glo_vert_2000_inf = np.zeros((len(namelist),jj,ji),dtype = float)
    OHC_pool_atl_vert_2000_inf = np.zeros((len(namelist),jj,ji),dtype = float)
    # create a data pool to save the mass transport for each year and month
    # zonal integral (vertical profile)
    psi_pool_glo_zonal = np.zeros((len(namelist),level,jj),dtype = float)
    psi_pool_atl_zonal = np.zeros((len(namelist),level,jj),dtype = float)
    # vertical integral (horizontal profile)
    psi_pool_glo_vert = np.zeros((len(namelist),jj,ji),dtype = float)
    psi_pool_atl_vert = np.zeros((len(namelist),jj,ji),dtype = float)
    # create a data pool to save the mean of fields for each year and month
    # zonal mean (vertical profile)
    temp_pool_glo_zonal = np.zeros((len(namelist),level,jj),dtype = float)
    temp_pool_atl_zonal = np.zeros((len(namelist),level,jj),dtype = float)
    u_pool_glo_zonal = np.zeros((len(namelist),level,jj),dtype = float)
    u_pool_atl_zonal = np.zeros((len(namelist),level,jj),dtype = float)
    v_pool_glo_zonal = np.zeros((len(namelist),level,jj),dtype = float)
    v_pool_atl_zonal = np.zeros((len(namelist),level,jj),dtype = float)
    # vertical mean (horizontal profile)
    temp_pool_glo_vert = np.zeros((len(namelist),jj,ji),dtype = float)
    u_pool_glo_vert = np.zeros((len(namelist),jj,ji),dtype = float)
    v_pool_glo_vert = np.zeros((len(namelist),jj,ji),dtype = float)
    # loop for calculation
    for i in np.arange(len(namelist)):
        ####################################################################
        #########################  Extract variables #######################
        ####################################################################
        # get the key of each variable
        soda_key = var_key(datapath, namelist[i])
        ####################################################################
        #########      Calculate meridional mass transport        ##########
        ####################################################################
        # calculate the mass transport
        psi_globe_zonal, psi_atlantic_zonal, psi_globe_vert, psi_atlantic_vert = mass_transport(soda_key,e1c)
        # save output to the pool
        psi_pool_glo_zonal[i,:,:] = psi_globe_zonal
        psi_pool_atl_zonal[i,:,:] = psi_atlantic_zonal
        psi_pool_glo_vert[i,:,:] = psi_globe_vert
        psi_pool_atl_vert[i,:,:] = psi_atlantic_vert
        ####################################################################
        ##############      Calculate ocean heat content      ##############
        ####################################################################
        # calculate the meridional energy transport in the ocean
        # calculate the meridional energy transport in the ocean
        OHC_glo_zonal, OHC_atl_zonal, OHC_glo_vert, OHC_atl_vert,\
        OHC_glo_vert_0_500, OHC_atl_vert_0_500, OHC_glo_vert_500_1000, OHC_atl_vert_500_1000,\
        OHC_glo_vert_1000_2000, OHC_atl_vert_1000_2000, OHC_glo_vert_2000_inf, OHC_atl_vert_2000_inf\
        = ocean_heat_content(soda_key)
        # save output to the pool
        OHC_pool_glo_zonal[i,:,:] = OHC_glo_zonal
        OHC_pool_atl_zonal[i,:,:] = OHC_atl_zonal
        OHC_pool_glo_vert[i,:,:] = OHC_glo_vert
        OHC_pool_atl_vert[i,:,:] = OHC_atl_vert
        OHC_pool_glo_vert_0_500[i,:,:] = OHC_glo_vert_0_500
        OHC_pool_atl_vert_0_500[i,:,:] = OHC_atl_vert_0_500
        OHC_pool_glo_vert_500_1000[i,:,:] = OHC_glo_vert_500_1000
        OHC_pool_atl_vert_500_1000[i,:,:] = OHC_atl_vert_500_1000
        OHC_pool_glo_vert_1000_2000[i,:,:] = OHC_glo_vert_1000_2000
        OHC_pool_atl_vert_1000_2000[i,:,:] = OHC_atl_vert_1000_2000
        OHC_pool_glo_vert_2000_inf[i,:,:] = OHC_glo_vert_2000_inf
        OHC_pool_atl_vert_2000_inf[i,:,:] = OHC_atl_vert_2000_inf
        ####################################################################
        ##############    Calculate the statistical matrix    ##############
        ####################################################################
        # statistical matrix
        # take zonal and vertical mean
        temp_glo_vert, u_glo_vert, v_glo_vert, temp_glo_zonal, temp_atl_zonal,\
        u_glo_zonal, u_atl_zonal, v_glo_zonal, v_atl_zonal= field_statistics(soda_key)
        # save output to the pool
        temp_pool_glo_vert[i,:,:] = temp_glo_vert
        u_pool_glo_vert[i,:,:] = u_glo_vert
        v_pool_glo_vert[i,:,:] = v_glo_vert
        temp_pool_glo_zonal[i,:,:] = temp_glo_zonal
        temp_pool_atl_zonal[i,:,:] = temp_atl_zonal
        u_pool_glo_zonal[i,:,:] = u_glo_zonal
        u_pool_atl_zonal[i,:,:] = u_atl_zonal
        v_pool_glo_zonal[i,:,:] = v_glo_zonal
        v_pool_atl_zonal[i,:,:] = v_atl_zonal
    # take the monthly mean
    psi_pool_glo_zonal_mean = np.mean(psi_pool_glo_zonal,0)
    psi_pool_atl_zonal_mean = np.mean(psi_pool_atl_zonal_glo,0)
    psi_pool_glo_vert_mean = np.mean(psi_pool_glo_vert,0)
    psi_pool_atl_vert_mean = np.mean(psi_pool_atl_vert,0)
    OHC_pool_glo_zonal_mean = np.mean(OHC_pool_glo_zonal,0)
    OHC_pool_atl_zonal_mean = np.mean(OHC_pool_atl_zonal,0)
    OHC_pool_glo_vert_mean = np.mean(OHC_pool_glo_vert,0)
    OHC_pool_atl_vert_mean = np.mean(OHC_pool_atl_vert,0)
    OHC_pool_glo_vert_0_500_mean = np.mean(OHC_pool_glo_vert_0_500,0)
    OHC_pool_atl_vert_0_500_mean = np.mean(OHC_pool_atl_vert_0_500,0)
    OHC_pool_glo_vert_500_1000_mean = np.mean(OHC_pool_glo_vert_500_1000,0)
    OHC_pool_atl_vert_500_1000_mean = np.mean(OHC_pool_atl_vert_500_1000,0)
    OHC_pool_glo_vert_1000_2000_mean = np.mean(OHC_pool_glo_vert_1000_2000,0)
    OHC_pool_atl_vert_1000_2000_mean = np.mean(OHC_pool_atl_vert_1000_2000,0)
    OHC_pool_glo_vert_2000_inf_mean = np.mean(OHC_pool_glo_vert_2000_inf,0)
    OHC_pool_atl_vert_2000_inf_mean = np.mean(OHC_pool_atl_vert_2000_inf,0)
    temp_pool_glo_vert_mean = np.mean(temp_pool_glo_vert,0)
    u_pool_glo_vert_mean = np.mean(u_pool_glo_vert,0)
    v_pool_glo_vert_mean = np.mean(v_pool_glo_vert,0)
    temp_pool_glo_zonal_mean = np.mean(temp_pool_glo_zonal,0)
    temp_pool_atl_zonal_mean = np.mean(temp_pool_atl_zonal,0)
    u_pool_glo_zonal_mean = np.mean(u_pool_glo_zonal,0)
    u_pool_atl_zonal_mean = np.mean(u_pool_atl_zonal,0)
    v_pool_glo_zonal_mean = np.mean(v_pool_glo_zonal,0)
    v_pool_atl_zonal_mean = np.mean(v_pool_atl_zonal,0)
    # create NetCDF file and save the output
    create_netcdf_point(psi_pool_glo_zonal_mean, psi_pool_atl_zonal_mean, psi_pool_glo_vert_mean, psi_pool_atl_vert_mean,\
                        OHC_pool_glo_zonal_mean, OHC_pool_atl_zonal_mean, OHC_pool_glo_vert_mean, OHC_pool_atl_vert_mean,\
                        OHC_pool_glo_vert_0_500_mean, OHC_pool_atl_vert_0_500_mean, OHC_pool_glo_vert_500_1000_mean,\
                        OHC_pool_atl_vert_500_1000_mean, OHC_pool_glo_vert_1000_2000_mean, OHC_pool_atl_vert_1000_2000_mean,\
                        OHC_pool_glo_vert_2000_inf_mean, OHC_pool_atl_vert_2000_inf_mean, temp_pool_glo_vert_mean,\
                        u_pool_glo_vert_mean, v_pool_glo_vert_mean, temp_pool_glo_zonal_mean, temp_pool_atl_zonal_mean,\
                        u_pool_glo_zonal_mean, u_pool_atl_zonal_mean, v_pool_glo_zonal_mean, v_pool_atl_zonal_mean, output_path)

    print 'Computation of meridional energy transport on MOM5 grid for SODA3 is complete!!!'
    print 'The output is in sleep, safe and sound!!!'
    logging.info("The full pipeline of the quantification of meridional energy transport in the ocean is accomplished!")

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
