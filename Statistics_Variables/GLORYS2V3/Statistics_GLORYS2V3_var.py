#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : A statistical look into the temporal and spatial distribution of fields (GLORYS2V3)
Author          : Yang Liu
Date            : 2018.01.06
Last Update     : 2018.01.10
Description     : The code aims to statistically take a close look into each fields.
                  This could help understand the difference between each datasets, which
                  will explain the deviation in meridional energy transport. Specifically,
                  the script deals with oceanic reanalysis dataset GLORYS2V3 from Mercator Ocean.
                  The complete computaiton is accomplished on model level (original ORCA025_z75 grid).
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
Caveat!!        : The full dataset is from 1993 to 2014.
                  Direction of Axis:
                  Model Level: surface to bottom
                  The data is monthly mean
                  The variables (T,U,V) of GLORYS2V3 are saved in the form of masked
                  arrays. The mask has filled value of 1E+30 (in order to maintain
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
sys.stdout = open('/project/Reanalysis/GLORYS2V3/monthly/console_var.out','w')

# logging level 'DEBUG' 'INFO' 'WARNING' 'ERROR' 'CRITICAL'
#logging.basicConfig(filename = 'F:\DataBase\ORAS4\history.log', filemode = 'w',level = logging.DEBUG,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(filename = '/project/Reanalysis/GLORYS2V3/monthly/history_var.log',
                    filemode = 'w', level = logging.DEBUG,
                    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# define the constant:
constant ={'g' : 9.80616,      # gravititional acceleration [m / s2]
           'R' : 6371009,      # radius of the earth [m]
           'cp': 3987,         # heat capacity of sea water [J/(Kg*C)]
           'rho': 1027,        # sea water density [Kg/m3]
            }

################################   Input zone  ######################################
# specify data path
datapath = '/project/Reanalysis/GLORYS2V3/monthly'
# time of the data, which concerns with the name of input
# starting time (year)
start_year = 1993
# Ending time, if only for 1 year, then it should be the same as starting year
end_year = 2014
# specify output path for the netCDF4 file
output_path = '/project/Reanalysis/GLORYS2V3/monthly/output'
####################################################################################

def var_key(datapath, year, month):
    # get the path to each datasets
    print "Start retrieving datasets for %d (y) %s (m)" % (year,namelist_month[month])
    logging.info("Start retrieving variables theta,v for from %d (y) %s (m)" % (year,namelist_month[month]))
    ####################################################################
    #########  Pick up variables and deal with the naming rule #########
    ####################################################################
    if year < 2010:
        datapath_theta = datapath + os.sep + 'T' + os.sep + 'GLORYS2V3_ORCA025_%d%s15_R20130808_gridT.nc' % (year,namelist_month[month])
        datapath_uv = datapath + os.sep + 'UV' + os.sep + 'GLORYS2V3_ORCA025_%d%s15_R20130808_gridUV.nc' % (year,namelist_month[month])
    elif year == 2010:
        if month == index_month[-1]:
            datapath_theta = datapath + os.sep + 'T' + os.sep + 'GLORYS2V3_ORCA025_%d%s15_R20140520_gridT.nc' % (year,namelist_month[month])
            datapath_uv = datapath + os.sep + 'UV' + os.sep + 'GLORYS2V3_ORCA025_%d%s15_R20140520_gridUV.nc' % (year,namelist_month[month])
        else:
            datapath_theta = datapath + os.sep + 'T' + os.sep + 'GLORYS2V3_ORCA025_%d%s15_R20130808_gridT.nc' % (year,namelist_month[month])
            datapath_uv = datapath + os.sep + 'UV' + os.sep + 'GLORYS2V3_ORCA025_%d%s15_R20130808_gridUV.nc' % (year,namelist_month[month])
    elif year == 2011:
        if month == index_month[-1]:
            datapath_theta = datapath + os.sep + 'T' + os.sep + 'GLORYS2V3_ORCA025_%d%s15_R20151218_gridT.nc' % (year,namelist_month[month])
            datapath_uv = datapath + os.sep + 'UV' + os.sep + 'GLORYS2V3_ORCA025_%d%s15_R20151218_gridUV.nc' % (year,namelist_month[month])
        else:
            datapath_theta = datapath + os.sep + 'T' + os.sep + 'GLORYS2V3_ORCA025_%d%s15_R20140520_gridT.nc' % (year,namelist_month[month])
            datapath_uv = datapath + os.sep + 'UV' + os.sep + 'GLORYS2V3_ORCA025_%d%s15_R20140520_gridUV.nc' % (year,namelist_month[month])
    else:
        datapath_theta = datapath + os.sep + 'T' + os.sep + 'GLORYS2V3_ORCA025_%d%s15_R20151218_gridT.nc' % (year,namelist_month[month])
        datapath_uv = datapath + os.sep + 'UV' + os.sep + 'GLORYS2V3_ORCA025_%d%s15_R20151218_gridUV.nc' % (year,namelist_month[month])

    # get the variable keys
    theta_key = Dataset(datapath_theta)
    uv_key = Dataset(datapath_uv)

    print "Retrieving datasets for the %d (year) %s (month) successfully!" % (year, namelist_month[month])
    logging.info("Retrieving variables for the year %d month %s successfully!" % (year,namelist_month[month]))
    return theta_key, uv_key

def var_coordinate(datapath):
    print "Start retrieving the ORCA025 coordinate and mask info"
    logging.info('Start retrieving the ORCA025 coordinate and mask info')
    # get the variable keys
    mesh_mask_key = Dataset(datapath+ os.sep + 'G2V3_mesh_mask_myocean.nc')
    subbasin_mesh_key = Dataset(datapath+ os.sep + 'new_maskglo.nc') #sub-basin from Andreas
    #extract variables
    # lat-lon-depth coordinate info
    nav_lat = mesh_mask_key.variables['nav_lat'][:]
    nav_lon = mesh_mask_key.variables['nav_lon'][:]
    deptht = mesh_mask_key.variables['deptht'][:]
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
    tmaskatl = subbasin_mesh_key.variables['tmaskatl'][:,1:-1] # attention that the size is different!
    # grid spacing scale factors (zonal)
    e1t = mesh_mask_key.variables['e1t'][0,:,:]
    e2t = mesh_mask_key.variables['e2t'][0,:,:]
    e1u = mesh_mask_key.variables['e1u'][0,:,:]
    e2u = mesh_mask_key.variables['e2u'][0,:,:]
    e1v = mesh_mask_key.variables['e1v'][0,:,:]
    e2v = mesh_mask_key.variables['e2v'][0,:,:]
    # take the bathymetry
    mbathy = mesh_mask_key.variables['mbathy'][0,:,:]
    # depth of each layer
    e3t_0 = mesh_mask_key.variables['e3t_0'][0,:]
    # depth of partial cells
    e3t_ps = mesh_mask_key.variables['e3t_ps'][0,:,:]
    # depth of partial cell t point
    hdept = mesh_mask_key.variables['hdept'][0,:,:]

    print "Retrieve the ORCA025 coordinate and mask info successfully!"
    logging.info('Finish retrieving the ORCA025 coordinate and mask info')

    return nav_lat, nav_lon, deptht, tmask, umask, vmask, tmaskatl, e1t, e2t, e1u, e2u, e1v, e2v, gphiu, glamu, gphiv, glamv, mbathy, e3t_0, e3t_ps, hdept

def field_statistics(theta_key, uv_key):
    # extract variables
    print "Start extracting variables for the quantification of meridional energy transport."
    theta = theta_key.variables['votemper'][0,:,:,:] # the unit of theta is Celsius!
    u = uv_key.variables['vozocrtx'][0,:,:,:]
    v = uv_key.variables['vomecrty'][0,:,:,:]
    print 'Extracting variables successfully!'
    # set the filled value to be 0
    np.ma.set_fill_value(theta,0)
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
    e1u_3D = np.repeat(e1u[np.newaxis,:,:],level,0)
    e1v_3D = np.repeat(e1v[np.newaxis,:,:],level,0)

    # vertical mean
    theta_globe_vert_weight = np.zeros((level,jj,ji),dtype=float)
    u_globe_vert_weight = np.zeros((level,jj,ji),dtype=float)
    v_globe_vert_weight = np.zeros((level,jj,ji),dtype=float)

    for i in np.arange(level):
        theta_globe_vert_weight[i,:,:] = theta[i,:,:].filled() * e3t_0[i] * tmask[i,:,:] -\
                                         theta[i,:,:].filled() * e3t_adjust[i,:,:] * tmask[i,:,:]
        u_globe_vert_weight[i,:,:] = u[i,:,:].filled() * e3t_0[i] * umask[i,:,:] -\
                                     u[i,:,:].filled() * e3t_adjust[i,:,:] * umask[i,:,:]
        v_globe_vert_weight[i,:,:] = v[i,:,:].filled() * e3t_0[i] * vmask[i,:,:] -\
                                     v[i,:,:].filled() * e3t_adjust[i,:,:] * vmask[i,:,:]

    theta_globe_vert_mean = np.sum(theta_globe_vert_weight,0) / hdept
    u_globe_vert_mean = np.sum(u_globe_vert_weight,0) / hdept
    v_globe_vert_mean = np.sum(v_globe_vert_weight,0) / hdept

    # zonal mean
    # take the sum of variables
    theta_globe_zonal_weight = np.zeros((level,jj,ji),dtype=float)
    u_globe_zonal_weight = np.zeros((level,jj,ji),dtype=float)
    v_globe_zonal_weight = np.zeros((level,jj,ji),dtype=float)
    theta_atlantic_zonal_weight = np.zeros((level,jj,ji),dtype=float)
    u_atlantic_zonal_weight = np.zeros((level,jj,ji),dtype=float)
    v_atlantic_zonal_weight = np.zeros((level,jj,ji),dtype=float)

    for i in np.arange(level):
        theta_globe_zonal_weight[i,:,:] = theta[i,:,:].filled() * e1t_3D[i,:,:] * tmask[i,:,:]
        theta_atlantic_zonal_weight[i,:,:] = theta[i,:,:].filled() * e1t_3D[i,:,:] * tmask[i,:,:] * tmaskatl_3D[i,:,:]
        u_globe_zonal_weight[i,:,:] = u[i,:,:].filled() * e1u_3D[i,:,:] * umask[i,:,:]
        u_atlantic_zonal_weight[i,:,:] = u[i,:,:].filled() * e1u_3D[i,:,:] * umask[i,:,:] * tmaskatl_3D[i,:,:]
        v_globe_zonal_weight[i,:,:] = v[i,:,:].filled() * e1v_3D[i,:,:] * vmask[i,:,:]
        v_atlantic_zonal_weight[i,:,:] = v[i,:,:].filled() * e1v_3D[i,:,:] * vmask[i,:,:] * tmaskatl_3D[i,:,:]

    # take the zonal mean
    theta_globe_zonal_mean = np.sum(theta_globe_zonal_weight,2) / np.sum(e1t_3D * tmask,2)
    theta_atlantic_zonal_mean = np.sum(theta_atlantic_zonal_weight,2) / np.sum(e1t_3D * tmask * tmaskatl_3D,2)
    u_globe_zonal_mean = np.sum(u_globe_zonal_weight,2) / np.sum(e1u_3D * umask,2)
    u_atlantic_zonal_mean = np.sum(u_atlantic_zonal_weight,2) / np.sum(e1u_3D * umask * tmaskatl_3D,2)
    v_globe_zonal_mean = np.sum(v_globe_zonal_weight,2) / np.sum(e1v_3D * vmask,2)
    v_atlantic_zonal_mean = np.sum(v_atlantic_zonal_weight,2) / np.sum(e1v_3D * vmask * tmaskatl_3D,2)

    return theta_globe_vert_mean, u_globe_vert_mean, v_globe_vert_mean,\
           theta_globe_zonal_mean, theta_atlantic_zonal_mean, u_globe_zonal_mean,\
           u_atlantic_zonal_mean, v_globe_zonal_mean, v_atlantic_zonal_mean

def create_netcdf_point (theta_pool_glo_vert, u_pool_glo_vert, v_pool_glo_vert, theta_pool_glo_zonal, theta_pool_atl_zonal,\
                        u_pool_glo_zonal, u_pool_atl_zonal, v_pool_glo_zonal, v_pool_atl_zonal ,output_path):
    print '*******************************************************************'
    print '*********************** create netcdf file ************************'
    print '*********************   statistics on ORCA   **********************'
    print '*******************************************************************'
    logging.info("Start creating netcdf file for the statistics of fields at each grid point.")
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path + os.sep + 'GLORYS2V3_model_monthly_orca025_var_point.nc' ,'w',format = 'NETCDF3_64BIT')
    # create dimensions for netcdf data
    year_wrap_dim = data_wrap.createDimension('year',len(period))
    month_wrap_dim = data_wrap.createDimension('month',12)
    lat_wrap_dim = data_wrap.createDimension('j',jj)
    lon_wrap_dim = data_wrap.createDimension('i',ji)
    lev_wrap_dim = data_wrap.createDimension('lev',level)
    # create coordinate variables for 3-dimensions
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
    gphit_wrap_var.units = 'ORCA025_latitude_Tgrid'
    glamt_wrap_var.units = 'ORCA025_longitude_Tgrid'
    gphiu_wrap_var.units = 'ORCA025_latitude_ugrid'
    glamu_wrap_var.units = 'ORCA025_longitude_ugrid'
    gphiv_wrap_var.units = 'ORCA025_latitude_vgrid'
    glamv_wrap_var.units = 'ORCA025_longitude_vgrid'

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
    lat_wrap_var[:] = gphiv[:,1060]
    lev_wrap_var[:] = deptht
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
    logging.info("The generation of netcdf files for the statisticas of fields in GLORYS2V3 on each grid point is complete!!")

if __name__=="__main__":
    print '*******************************************************************'
    print '******  Prepare all the constants and auxillary variables   *******'
    print '*******************************************************************'
    # create the year index
    period = np.arange(start_year,end_year+1,1)
    namelist_month = ['01','02','03','04','05','06','07','08','09','10','11','12']
    index_month = np.arange(12)
    # ORCA1_z42 info (Madec and Imbard 1996)
    ji = 1440
    jj = 1021
    level = 75
    # extract the mesh_mask and coordinate information
    nav_lat, nav_lon, deptht, tmask, umask, vmask, tmaskatl, e1t, e2t, e1u, e2u, e1v, e2v, gphiu, glamu, \
    gphiv, glamv, mbathy, e3t_0, e3t_ps, hdept = var_coordinate(datapath)
    print '*******************************************************************'
    print '*******************  Partial cells correction   *******************'
    print '*******************************************************************'
    # construct partial cell depth matrix
    # the size of partial cell is given by e3t_ps
    # for the sake of simplicity of the code, just calculate the difference between e3t_0 and e3t_ps
    # then minus this adjustment when calculate the OMET at each layer with mask
    # Attention! Since python start with 0, the partial cell info given in mbathy should incoporate with this
    e3t_adjust = np.zeros((level,jj,ji),dtype = float)
    for i in np.arange(1,level,1): # start from 1
        for j in np.arange(jj):
            for k in np.arange(ji):
                if i == mbathy[j,k]:
                    e3t_adjust[i-1,j,k] = e3t_0[i-1] - e3t_ps[j,k] # python start with 0, so i-1
    ####################################################################
    ###  Create space for stroing intermediate variables and outputs ###
    ####################################################################
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
        for j in index_month:
            ####################################################################
            #########################  Extract variables #######################
            ####################################################################
            # get the key of each variable
            theta_key, uv_key = var_key(datapath, i, j)
            ####################################################################
            ##############    Calculate the statistical matrix    ##############
            ####################################################################
            # statistical matrix
            # take zonal and vertical mean
            theta_glo_vert, u_glo_vert, v_glo_vert, theta_glo_zonal, theta_atl_zonal,\
            u_glo_zonal, u_atl_zonal, v_glo_zonal, v_atl_zonal= field_statistics(theta_key, uv_key)
            # save output to the pool
            theta_pool_glo_vert[i-1993,j,:,:] = theta_glo_vert
            u_pool_glo_vert[i-1993,j,:,:] = u_glo_vert
            v_pool_glo_vert[i-1993,j,:,:] = v_glo_vert
            theta_pool_glo_zonal[i-1993,j,:,:] = theta_glo_zonal
            theta_pool_atl_zonal[i-1993,j,:,:] = theta_atl_zonal
            u_pool_glo_zonal[i-1993,j,:,:] = u_glo_zonal
            u_pool_atl_zonal[i-1993,j,:,:] = u_atl_zonal
            v_pool_glo_zonal[i-1993,j,:,:] = v_glo_zonal
            v_pool_atl_zonal[i-1993,j,:,:] = v_atl_zonal
    # create NetCDF file and save the output
    create_netcdf_point(theta_pool_glo_vert, u_pool_glo_vert, v_pool_glo_vert, theta_pool_glo_zonal, theta_pool_atl_zonal,\
                        u_pool_glo_zonal, u_pool_atl_zonal, v_pool_glo_zonal, v_pool_atl_zonal, output_path)

    print 'Computation of statistical matrix on ORCA grid for GLORYS2V3 is complete!!!'
    print 'The output is in sleep, safe and sound!!!'
    logging.info("The full pipeline of the calculation of statistical matrix on ORCA grid for GLORYS2V3 is accomplished!")

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
