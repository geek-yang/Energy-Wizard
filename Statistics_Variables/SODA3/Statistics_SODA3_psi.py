#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : A statistical look into the temporal and spatial distribution of fields (GLORYS2V3)
Author          : Yang Liu
Date            : 2018.06.16
Last Update     : 2018.06.16
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
sys.stdout = open('/home/lwc16308/reanalysis/SODA3/console_psi.out','w+')

# logging level 'DEBUG' 'INFO' 'WARNING' 'ERROR' 'CRITICAL'
#logging.basicConfig(filename = 'F:\DataBase\ORAS4\history.log', filemode = 'w',level = logging.DEBUG,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(filename = '/home/lwc16308/reanalysis/SODA3/history_psi.log',
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

def create_netcdf_point (psi_pool_glo_zonal, psi_pool_atl_zonal, psi_pool_glo_vert, psi_pool_atl_vert, output_path):
    print '*******************************************************************'
    print '*********************** create netcdf file ************************'
    print '*********************   statistics on MOM   **********************'
    print '*******************************************************************'
    logging.info("Start creating netcdf file for the statistics of fields at each grid point.")
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path + os.sep + 'SODA3_model_5daily_mom5_statistics_point_%d.nc' % (input_year),'w',format = 'NETCDF4')
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
    psi_glo_zonal_wrap_var = data_wrap.createVariable('psi_glo_zonal',np.float64,('lev','j'),zlib=True)
    psi_atl_zonal_wrap_var = data_wrap.createVariable('psi_atl_zonal',np.float64,('lev','j'),zlib=True)

    psi_glo_vert_wrap_var = data_wrap.createVariable('psi_glo_vert',np.float64,('j','i'),zlib=True)
    psi_atl_vert_wrap_var = data_wrap.createVariable('psi_atl_vert',np.float64,('j','i'),zlib=True)
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

    psi_glo_vert_wrap_var.units = 'Sv'
    psi_atl_vert_wrap_var.units = 'Sv'

    lat_wrap_var.long_name = 'auxillary latitude'
    lev_wrap_var.long_name = 'depth'
    gphit_wrap_var.long_name = 'MOM5 Tgrid latitude'
    glamt_wrap_var.long_name = 'MOM5 Tgrid longitude'
    gphic_wrap_var.long_name = 'MOM5 cgrid latitude'
    glamc_wrap_var.long_name = 'MOM5 cgrid longitude'

    psi_glo_zonal_wrap_var.long_name = 'Global Meridional Mass Transport (zonal integral)'
    psi_atl_zonal_wrap_var.long_name = 'Atlantic Meridional Mass Transport (zonal integral)'

    psi_glo_vert_wrap_var.long_name = 'Global Meridional Mass Transport (vertical integral)'
    psi_atl_vert_wrap_var.long_name = 'Atlantic Meridional Mass Transport (vertical integral)'

    # writing data
    lat_wrap_var[:] = grid_y_C
    lev_wrap_var[:] = zt
    gphit_wrap_var[:] = y_T
    glamt_wrap_var[:] = x_T
    gphic_wrap_var[:] = y_C
    glamc_wrap_var[:] = x_C

    psi_glo_zonal_wrap_var[:] = psi_pool_glo_zonal
    psi_atl_zonal_wrap_var[:] = psi_pool_atl_zonal

    psi_glo_vert_wrap_var[:] = psi_pool_glo_vert
    psi_atl_vert_wrap_var[:] = psi_pool_atl_vert
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
    # create a data pool to save the mass transport for each year and month
    # zonal integral (vertical profile)
    psi_pool_glo_zonal = np.zeros((len(namelist),level,jj),dtype = float)
    psi_pool_atl_zonal = np.zeros((len(namelist),level,jj),dtype = float)
    # vertical integral (horizontal profile)
    psi_pool_glo_vert = np.zeros((len(namelist),jj,ji),dtype = float)
    psi_pool_atl_vert = np.zeros((len(namelist),jj,ji),dtype = float)
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
    # take the monthly mean
    psi_pool_glo_zonal_mean = np.mean(psi_pool_glo_zonal,0)
    psi_pool_atl_zonal_mean = np.mean(psi_pool_atl_zonal_glo,0)
    psi_pool_glo_vert_mean = np.mean(psi_pool_glo_vert,0)
    psi_pool_atl_vert_mean = np.mean(psi_pool_atl_vert,0)
    # create NetCDF file and save the output
    create_netcdf_point(psi_pool_glo_zonal_mean, psi_pool_atl_zonal_mean, psi_pool_glo_vert_mean, psi_pool_atl_vert_mean, output_path)

    print 'Computation of meridional energy transport on MOM5 grid for SODA3 is complete!!!'
    print 'The output is in sleep, safe and sound!!!'
    logging.info("The full pipeline of the quantification of meridional energy transport in the ocean is accomplished!")

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
