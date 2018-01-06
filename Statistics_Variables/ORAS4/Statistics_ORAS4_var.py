#!/usr/bin/env python
"""
Copyright Netherlands eScience Center

Function        : A statistical look into the temporal and spatial distribution of fields (ORAS4)
Author          : Yang Liu
Date            : 2018.1.4
Last Update     : 2018.1.5
Description     : The code aims to statistically take a close look into each fields.
                  This could help understand the difference between each datasets, which
                  will explain the deviation in meridional energy transport. Specifically,
                  the script deals with oceanic reanalysis dataset ORAS4 from ECMWF.
                  The complete computaiton is accomplished on model level (original ORCA1_z42 grid).
                  All the interpolations are made on the V grid, including scalars.
                  For the sake of accuracy, the zonal integrations are taken on
                  i-j coordinate, which follows i-coord.
                  The script also calculates the ocean heat content for certain layers.

Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, sys, matplotlib, logging
variables       : Potential Temperature                     Theta
                  Zonal Current Velocity                    u
                  Meridional Current Velocity               v
                  Zonal Grid Spacing Scale Factors          e1
                  Meridional Grid Spacing Scale Factors     e2
                  Land-Sea Mask                             mask

Caveat!!        : The full dataset is from 1958. However, a quality report from
                  Magdalena from ECMWF indicates the quality of data for the first
                  two decades are very poor. Hence we use the data from 1979. which
                  is the start of satellite era.
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

# print the system structure and the path of the kernal
print platform.architecture()
print os.path

# switch on the seaborn effect
#sns.set()

# calculate the time for the code execution
start_time = tttt.time()# gz in [m2 / s2] = [ kg m2 / kg s2 ] = [J / kg]

# Redirect all the console output to a file
#sys.stdout = open('F:\DataBase\ORAS4\console.out','w')
sys.stdout = open('/project/Reanalysis/ORAS4/Monthly/Model/console_var.out','w')

# logging level 'DEBUG' 'INFO' 'WARNING' 'ERROR' 'CRITICAL'
#logging.basicConfig(filename = 'F:\DataBase\ORAS4\history.log', filemode = 'w',level = logging.DEBUG,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(filename = '/project/Reanalysis/ORAS4/Monthly/Model/history_var.log',
                    filemode = 'w', level = logging.DEBUG,
                    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# define the constant:
constant ={'g' : 9.80616,      # gravititional acceleration [m / s2]
           'R' : 6371009,      # radius of the earth [m]
           'cp': 3987,         # heat capacity of sea water [J/(Kg*K)]
           'rho': 1027,        # sea water density [Kg/m3]
            }

################################   Input zone  ######################################
# specify data path
#datapath = 'F:\DataBase\ORAS\ORAS4\Monthly\model'
datapath = '/project/Reanalysis/ORAS4/Monthly/Model'
# time of the data, which concerns with the name of input
# starting time (year)
start_year = 1958
# Ending time, if only for 1 year, then it should be the same as starting year
end_year = 2014
# specify output path for the netCDF4 file
#output_path_fig = 'C:\Yang\PhD\Computation and Modeling\Blue Action\OMET\ORAS4'
output_path = '/project/Reanalysis/ORAS4/Monthly/Model/output'
# benchmark datasets for basic dimensions
#benchmark_path = 'F:\DataBase\ORAS\ORAS4\Monthly\model\\thetao_oras4_1m_1979_grid_T.nc'
#benchmark = Dataset(benchmark_path)
####################################################################################

def var_key(datapath, year):
    # get the path to each datasets
    print "Start retrieving datasets"
    logging.info("Start retrieving variables theta,s,u,v from %d (y)" % (year))
    datapath_theta = datapath + os.sep + 'theta' + os.sep + 'thetao_oras4_1m_%d_grid_T.nc' % (year)
    datapath_s = datapath + os.sep + 's' + os.sep + 'so_oras4_1m_%d_grid_T.nc' % (year)
    datapath_u = datapath + os.sep + 'u' + os.sep + 'uo_oras4_1m_%d_grid_U.nc' % (year)
    datapath_v = datapath + os.sep + 'v' + os.sep + 'vo_oras4_1m_%d_grid_V.nc' % (year)

    # get the variable keys
    theta_key = Dataset(datapath_theta)
    s_key = Dataset(datapath_s)
    u_key = Dataset(datapath_u)
    v_key = Dataset(datapath_v)

    print "Retrieving datasets for the year %d successfully!" % (year)
    logging.info("Retrieving variables for the year %d successfully!" % (year))
    return theta_key, s_key, u_key, v_key

def var_coordinate(datapath):
    '''
    Retrive ORCA1_Z42 grid information and land-sea mask
    '''
    print "Start retrieving the datasets of ORCA1 coordinate and mask info"
    logging.info('Start retrieving the datasets of ORCA1 coordinate and mask info')
    # get the variable keys
    mesh_mask_key = Dataset(datapath+ os.sep + 'mesh_mask.nc')
    subbasin_mesh_key = Dataset(datapath+ os.sep + 'basinmask_050308_UKMO.nc') #sub-basin from DRAKKER project
    #grid_T_key = Dataset(datapath+ os.sep + 'coordinates_grid_T.nc')
    #grid_U_key = Dataset(datapath+ os.sep + 'coordinates_grid_U.nc')
    #grid_V_key = Dataset(datapath+ os.sep + 'coordinates_grid_V.nc')
    #extract variables
    # lat-lon-depth coordinate info
    nav_lat = mesh_mask_key.variables['nav_lat'][:]
    nav_lon = mesh_mask_key.variables['nav_lon'][:]
    nav_lev = mesh_mask_key.variables['nav_lev'][:]
    # lat-lon coordinate of V grid
    gphiv = mesh_mask_key.variables['gphiv'][0,:,:] # lat from -78 to -89
    glamv = mesh_mask_key.variables['glamv'][0,:,:] # lon from -179 to 179
    gphiu = mesh_mask_key.variables['gphiu'][0,:,:] # lat from -78 to -89
    glamu = mesh_mask_key.variables['glamu'][0,:,:] # lon from -179 to 179
    # land-sea mask
    tmask = mesh_mask_key.variables['tmask'][0,:,:,:]
    umask = mesh_mask_key.variables['umask'][0,:,:,:]
    vmask = mesh_mask_key.variables['vmask'][0,:,:,:]
    # land-sea mask for sub-basin
    tmaskatl = subbasin_mesh_key.variables['tmaskatl'][:] # attention that the size is different!
    # grid spacing scale factors (zonal)
    e1t = mesh_mask_key.variables['e1t'][0,:,:]
    e2t = mesh_mask_key.variables['e2t'][0,:,:]
    #e1u = mesh_mask_key.variables['e1u'][0,:,:]
    #e2u = mesh_mask_key.variables['e2u'][0,:,:]
    e1v = mesh_mask_key.variables['e1v'][0,:,:]
    e2v = mesh_mask_key.variables['e2v'][0,:,:]
    # take the bathymetry
    mbathy = mesh_mask_key.variables['mbathy'][0,:,:]
    # depth of each layer
    e3t_0 = mesh_mask_key.variables['e3t_0'][0,:]
    # comparison between variables
    #lat_grid_T = grid_T_key.variables['lat'][:]
    #lon_grid_T = grid_T_key.variables['lon'][:]
    #tmask_grid_T = grid_T_key.variables['tmask'][:]

    #lat_grid_U = grid_U_key.variables['lat'][:]
    #lon_grid_U = grid_U_key.variables['lon'][:]
    #umask_grid_U = grid_U_key.variables['umask'][:]

    #lat_grid_V = grid_V_key.variables['lat'][:]
    #lon_grid_V = grid_V_key.variables['lon'][:]
    #vmask_grid_V = grid_V_key.variables['vmask'][:]

    return nav_lat, nav_lon, nav_lev, tmask, umask, vmask, tmaskatl, e1t, e2t, e1v, e2v, gphiu, glamu, gphiv, glamv, mbathy, e3t_0

def field_statistics(theta_key, u_key, v_key):
    # extract variables
    print "Start extracting variables for the quantification of meridional energy transport."
    theta = theta_key.variables['thetao'][:] # the unit of theta is Celsius!
    u = u_key.variables['uo'][:]
    v = v_key.variables['vo'][:]
    print 'Extracting variables successfully!'
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
    # Due to the nature of the land-sea mask, when we take the mean value we can not
    # use the np.mean to calculate it from the original field, as there are so many
    # empty points. Instead, we must calculate the sum of each variable and then
    # devide the sum of mask.
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
    # increase the dimension of mask array
    tmask_4D = np.repeat(tmask[np.newaxis,:,:,:],len(index_month),0)
    tmaskatl_3D = np.repeat(tmaskatl[np.newaxis,:,:],level,0)
    tmaskatl_4D = np.repeat(tmaskatl_3D[np.newaxis,:,:,:],len(index_month),0)
    # vertical mean
    theta_globe_vert_mean = np.mean(theta*tmask_4D,1)
    u_globe_vert_mean = np.mean(u*tmask_4D,1)
    v_globe_vert_mean = np.mean(v*tmask_4D,1)
    # zonal mean
    # take the sum of variables
    theta_globe_zonal_sum = np.sum(theta*tmask_4D,3)
    theta_atlantic_zonal_sum = np.sum(theta*tmask_4D*tmaskatl_4D,3)
    u_globe_zonal_sum = np.sum(u*tmask_4D,3)
    u_atlantic_zonal_sum = np.sum(u*tmask_4D*tmaskatl_4D,3)
    v_globe_zonal_sum = np.sum(v*tmask_4D,3)
    v_atlantic_zonal_sum = np.sum(v*tmask_4D*tmaskatl_4D,3)
    # take the sum of land-sea mask
    mask_globe_zonal_sum = np.sum(tmask_4D,3)
    mask_atlantic_zonal_sum = np.sum(tmaskatl_4D,3)
    # take the zonal mean
    theta_globe_zonal_mean = theta_globe_zonal_sum / mask_globe_zonal_sum
    theta_atlantic_zonal_mean = theta_atlantic_zonal_sum / mask_atlantic_zonal_sum
    u_globe_zonal_mean = u_globe_zonal_sum / mask_globe_zonal_sum
    u_atlantic_zonal_mean = u_atlantic_zonal_sum / mask_atlantic_zonal_sum
    v_globe_zonal_mean = v_globe_zonal_sum / mask_globe_zonal_sum
    v_atlantic_zonal_mean = v_atlantic_zonal_sum / mask_atlantic_zonal_sum

    return theta_globe_vert_mean, u_globe_vert_mean, v_globe_vert_mean,\
           theta_globe_zonal_mean, theta_atlantic_zonal_mean, u_globe_zonal_mean,\
           u_atlantic_zonal_mean, v_globe_zonal_mean, v_atlantic_zonal_mean

def create_netcdf_point (theta_pool_glo_vert, u_pool_glo_vert, v_pool_glo_vert, theta_pool_glo_zonal, theta_pool_atl_zonal,\
                        u_pool_glo_zonal, u_pool_atl_zonal, v_pool_glo_zonal, v_pool_atl_zonal ,output_path):
    print '*******************************************************************'
    print '*********************** create netcdf file ************************'
    print '********************    statistics on ORCA   **********************'
    print '*******************************************************************'
    logging.info("Start creating netcdf file for the statistics of fields at each grid point.")
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path + os.sep + 'oras4_model_monthly_orca1_var_point.nc' ,'w',format = 'NETCDF3_64BIT')
    # create dimensions for netcdf data
    year_wrap_dim = data_wrap.createDimension('year',len(period))
    month_wrap_dim = data_wrap.createDimension('month',12)
    lat_wrap_dim = data_wrap.createDimension('j',jj)
    lon_wrap_dim = data_wrap.createDimension('i',ji)
    lev_wrap_dim = data_wrap.createDimension('lev',level)
    # create variables
    # 1D
    year_wrap_var = data_wrap.createVariable('year',np.int32,('year',))
    month_wrap_var = data_wrap.createVariable('month',np.int32,('month',))
    lat_wrap_var = data_wrap.createVariable('latitude_aux',np.float32,('j',))
    lev_wrap_var = data_wrap.createVariable('lev',np.float32,('lev',))
    # 2D
    gphit_wrap_var = data_wrap.createVariable('gphit',np.float32,('j','i'))
    glamt_wrap_var = data_wrap.createVariable('glamt',np.float32,('j','i'))
    gphiu_wrap_var = data_wrap.createVariable('gphiu',np.float32,('j','i'))
    glamu_wrap_var = data_wrap.createVariable('glamu',np.float32,('j','i'))
    gphiv_wrap_var = data_wrap.createVariable('gphiv',np.float32,('j','i'))
    glamv_wrap_var = data_wrap.createVariable('glamv',np.float32,('j','i'))
    # 4D
    theta_glo_zonal_wrap_var = data_wrap.createVariable('theta_glo_zonal',np.float64,('year','month','lev','j'))
    theta_atl_zonal_wrap_var = data_wrap.createVariable('theta_atl_zonal',np.float64,('year','month','lev','j'))
    u_glo_zonal_wrap_var = data_wrap.createVariable('u_glo_zonal',np.float64,('year','month','lev','j'))
    u_atl_zonal_wrap_var = data_wrap.createVariable('u_atl_zonal',np.float64,('year','month','lev','j'))
    v_glo_zonal_wrap_var = data_wrap.createVariable('v_glo_zonal',np.float64,('year','month','lev','j'))
    v_atl_zonal_wrap_var = data_wrap.createVariable('v_atl_zonal',np.float64,('year','month','lev','j'))

    theta_glo_vert_wrap_var = data_wrap.createVariable('theta_glo_vert',np.float64,('year','month','j','i'))
    u_glo_vert_wrap_var = data_wrap.createVariable('u_glo_vert',np.float64,('year','month','j','i'))
    v_glo_vert_wrap_var = data_wrap.createVariable('v_glo_vert',np.float64,('year','month','j','i'))
    # global attributes
    data_wrap.description = 'Monthly mean statistics of fields on ORCA grid'
    # variable attributes
    lev_wrap_var.units = 'm'
    gphit_wrap_var.units = 'ORCA1_latitude_Tgrid'
    glamt_wrap_var.units = 'ORCA1_longitude_Tgrid'
    gphiu_wrap_var.units = 'ORCA1_latitude_ugrid'
    glamu_wrap_var.units = 'ORCA1_longitude_ugrid'
    gphiv_wrap_var.units = 'ORCA1_latitude_vgrid'
    glamv_wrap_var.units = 'ORCA1_longitude_vgrid'

    theta_glo_zonal_wrap_var.units = 'Celsius'
    theta_atl_zonal_wrap_var.units = 'Celsius'
    u_glo_zonal_wrap_var.units = 'm/s'
    u_atl_zonal_wrap_var.units = 'm/s'
    v_glo_zonal_wrap_var.units = 'm/s'
    v_atl_zonal_wrap_var.units = 'm/s'

    theta_glo_vert_wrap_var.units = 'Celsius'
    u_glo_vert_wrap_var.units = 'm/s'
    v_glo_vert_wrap_var.units = 'm/s'

    lat_wrap_var.long_name = 'auxillary latitude'
    lev_wrap_var.long_name = 'depth'
    gphit_wrap_var.long_name = 'ORCA1 Tgrid latitude'
    glamt_wrap_var.long_name = 'ORCA1 Tgrid longitude'
    gphiu_wrap_var.long_name = 'ORCA1 ugrid latitude'
    glamu_wrap_var.long_name = 'ORCA1 ugrid longitude'
    gphiv_wrap_var.long_name = 'ORCA1 vgrid latitude'
    glamv_wrap_var.long_name = 'ORCA1 vgrid longitude'

    theta_glo_zonal_wrap_var.long_name = 'Global Potential Temperature (zonal mean)'
    theta_atl_zonal_wrap_var.long_name = 'Atlantic Potential Temperature (zonal mean)'
    u_glo_zonal_wrap_var.long_name = 'Global Zonal Velocity (zonal mean)'
    u_atl_zonal_wrap_var.long_name = 'Atlantic Zonal Velocity (zonal mean)'
    v_glo_zonal_wrap_var.long_name = 'Global Meridional Velocity (zonal mean)'
    v_atl_zonal_wrap_var.long_name = 'Atlantic Meridional Velocity (zonal mean)'

    theta_glo_vert_wrap_var.long_name = 'Global Potential Temperature (vertical mean)'
    u_glo_vert_wrap_var.long_name = 'Global Zonal Velocity (vertical mean)'
    v_glo_vert_wrap_var.long_name = 'Global Meridional Velocity (vertical mean)'
    # writing data
    year_wrap_var[:] = period
    month_wrap_var[:] = np.arange(1,13,1)
    lat_wrap_var[:] = gphiv[:,96]
    lev_wrap_var[:] = nav_lev
    gphit_wrap_var[:] = nav_lat
    glamt_wrap_var[:] = nav_lon
    gphiu_wrap_var[:] = gphiu
    glamu_wrap_var[:] = glamu
    gphiv_wrap_var[:] = gphiv
    glamv_wrap_var[:] = glamv

    theta_glo_zonal_wrap_var[:] = theta_pool_glo_zonal
    theta_atl_zonal_wrap_var[:] = theta_pool_atl_zonal
    u_glo_zonal_wrap_var[:] = u_pool_glo_zonal
    u_atl_zonal_wrap_var[:] = u_pool_atl_zonal
    v_glo_zonal_wrap_var[:] = v_pool_glo_zonal
    v_atl_zonal_wrap_var[:] = v_pool_atl_zonal

    theta_glo_vert_wrap_var[:] = theta_pool_glo_vert
    u_glo_vert_wrap_var[:] = u_pool_glo_vert
    v_glo_vert_wrap_var[:] = v_pool_glo_vert
    # close the file
    data_wrap.close()
    print "Create netcdf file successfully"
    logging.info("The generation of netcdf files for the statisticas of fields in ORAS4 on each grid point is complete!!")

if __name__=="__main__":
    # create the year index
    period = np.arange(start_year,end_year+1,1)
    index_month = np.arange(12)
    # ORCA1_z42 grid infor (Madec and Imbard 1996)
    ji = 362
    jj = 292
    level = 42
    # extract the mesh_mask and coordinate information
    nav_lat, nav_lon, nav_lev, tmask, umask, vmask, tmaskatl, e1t, e2t, e1v, e2v,\
    gphiu, glamu, gphiv, glamv, mbathy, e3t_0 = var_coordinate(datapath)
    print '*******************************************************************'
    print '************************ create data pool *************************'
    print '*******************************************************************'
    # create a data pool to save the mean of fields for each year and month
    # zonal mean (vertical profile)
    theta_pool_glo_zonal = np.zeros((len(period),12,level,jj),dtype = float)
    theta_pool_atl_zonal = np.zeros((len(period),12,level,jj),dtype = float)
    u_pool_glo_zonal = np.zeros((len(period),12,level,jj),dtype = float)
    u_pool_atl_zonal = np.zeros((len(period),12,level,jj),dtype = float)
    v_pool_glo_zonal = np.zeros((len(period),12,level,jj),dtype = float)
    v_pool_atl_zonal = np.zeros((len(period),12,level,jj),dtype = float)
    # vertical mean (horizontal profile)
    theta_pool_glo_vert = np.zeros((len(period),12,jj,ji),dtype = float)
    u_pool_glo_vert = np.zeros((len(period),12,jj,ji),dtype = float)
    v_pool_glo_vert = np.zeros((len(period),12,jj,ji),dtype = float)
    # loop for calculation
    for i in period:
        # get the key of each variable
        theta_key, s_key, u_key, v_key = var_key(datapath, i)
        # statistical matrix
        # take zonal and vertical mean
        theta_glo_vert, u_glo_vert, v_glo_vert, theta_glo_zonal, theta_atl_zonal,\
        u_glo_zonal, u_atl_zonal, v_glo_zonal, v_atl_zonal= field_statistics(theta_key, u_key, v_key)
        # save output to the pool
        theta_pool_glo_vert[i-1958,:,:,:] = theta_glo_vert
        u_pool_glo_vert[i-1958,:,:,:] = u_glo_vert
        v_pool_glo_vert[i-1958,:,:,:] = v_glo_vert
        theta_pool_glo_zonal[i-1958,:,:,:] = theta_glo_zonal
        theta_pool_atl_zonal[i-1958,:,:,:] = theta_atl_zonal
        u_pool_glo_zonal[i-1958,:,:,:] = u_glo_zonal
        u_pool_atl_zonal[i-1958,:,:,:] = u_atl_zonal
        v_pool_glo_zonal[i-1958,:,:,:] = v_glo_zonal
        v_pool_atl_zonal[i-1958,:,:,:] = v_atl_zonal
    # create NetCDF file and save the output
    create_netcdf_point(theta_pool_glo_vert, u_pool_glo_vert, v_pool_glo_vert, theta_pool_glo_zonal, theta_pool_atl_zonal,\
                        u_pool_glo_zonal, u_pool_atl_zonal, v_pool_glo_zonal, v_pool_atl_zonal, output_path)

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
