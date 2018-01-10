#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : A statistical look into the temporal and spatial distribution of fields (GLORYS2V3)
Author          : Yang Liu
Date            : 2018.01.10
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
sys.stdout = open('/project/Reanalysis/GLORYS2V3/monthly/console_psi.out','w')

# logging level 'DEBUG' 'INFO' 'WARNING' 'ERROR' 'CRITICAL'
#logging.basicConfig(filename = 'F:\DataBase\ORAS4\history.log', filemode = 'w',level = logging.DEBUG,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(filename = '/project/Reanalysis/GLORYS2V3/monthly/history_psi.log',
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

def mass_transport(uv_key,e1v):
    '''
    This function is used to calculate the mass transport.
    The unit is Sv (1E+6 m3/s)
    '''
    print "Compute the mass transport for globle and Atlantic!"
    logging.info('Compute the mass transport for globle and Atlantic!')
    #dominant equation for stream function
    # psi = e1v(m) * rho(kg/m3) * v(m/s) * dz(m) = (kg/s)
    # extract variables
    #u = uv_key.variables['vozocrtx'][0,:,:,:]
    v = uv_key.variables['vomecrty'][0,:,:,:]
    # set the filled value to be 0
    #np.ma.set_fill_value(u,0)
    np.ma.set_fill_value(v,0)
    # define the stream function psi
    psi_globe = np.zeros((level,jj,ji),dtype=float)
    psi_atlantic = np.zeros((level,jj,ji),dtype=float)
    # expand the grid size matrix e1v to avoid more loops
    e1v_3D = np.repeat(e1v[np.newaxis,:,:],level,0)
    for i in np.arange(level):
        psi_globe[i,:,:] = e1v_3D[i,:,:] * v[i,:,:].filled() * vmask[i,:,:] * e3t_0[i] -\
                           e1v_3D[i,:,:] * v[i,:,:].filled() * vmask[i,:,:] * e3t_adjust[i,:,:]
        # avoid the filling value during summation (the default filling value is quite large)
        #psi_globe[i,:,:] = psi_globe[i,:,:] * vmask[i,:,:]
        # Mass transport at Atlantic
    for i in np.arange(level):
        psi_atlantic[i,:,:] = e1v_3D[i,:,:] * v[i,:,:].filled() * vmask[i,:,:] * tmaskatl * e3t_0[i] -\
                              e1v_3D[i,:,:] * v[i,:,:].filled() * vmask[i,:,:] * tmaskatl * e3t_adjust[i,:,:]
        # avoid the filling value during summation
        #psi_atlantic[i,:,:] = psi_atlantic[i,:,:] * tmaskatl * vmask[i,:,:]
    # take the zonal integral
    psi_globe_zonal_int = np.sum(psi_globe,2)/1e+6 # the unit is changed to Sv
    psi_atlantic_zonal_int = np.sum(psi_atlantic,2)/1e+6 # the unit is changed to Sv
    # take the vertical integral
    psi_globe_vert_int = np.sum(psi_globe,0)/1e+6 # the unit is changed to Sv
    psi_atlantic_vert_int = np.sum(psi_atlantic,0)/1e+6 # the unit is changed to Sv

    print "Compute the mass transport for globle and Atlantic successfully!"
    logging.info('Compute the mass transport for globle and Atlantic successfully!')

    return psi_globe_zonal_int, psi_atlantic_zonal_int, psi_globe_vert_int, psi_atlantic_vert_int

def create_netcdf_point (psi_pool_glo_zonal, psi_pool_atl_zonal, psi_pool_glo_vert, psi_pool_atl_vert,output_path):
    print '*******************************************************************'
    print '*********************** create netcdf file ************************'
    print '*********************   statistics on ORCA   **********************'
    print '*******************************************************************'
    logging.info("Start creating netcdf file for the statistics of fields at each grid point.")
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path + os.sep + 'GLORYS2V3_model_monthly_orca025_psi_point.nc' ,'w',format = 'NETCDF3_64BIT')
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
    gphiv_wrap_var = data_wrap.createVariable('gphiv',np.float32,('j','i'))
    glamv_wrap_var = data_wrap.createVariable('glamv',np.float32,('j','i'))
    # 4D
    psi_glo_zonal_wrap_var = data_wrap.createVariable('psi_glo_zonal',np.float64,('year','month','lev','j'))
    psi_atl_zonal_wrap_var = data_wrap.createVariable('psi_atl_zonal',np.float64,('year','month','lev','j'))

    psi_glo_vert_wrap_var = data_wrap.createVariable('psi_glo_vert',np.float64,('year','month','j','i'))
    psi_atl_vert_wrap_var = data_wrap.createVariable('psi_atl_vert',np.float64,('year','month','j','i'))
    # global attributes
    data_wrap.description = 'Monthly mean statistics of fields on ORCA grid'
    # variable attributes
    lev_wrap_var.units = 'm'
    gphiv_wrap_var.units = 'ORCA025_latitude_vgrid'
    glamv_wrap_var.units = 'ORCA025_longitude_vgrid'

    psi_glo_zonal_wrap_var.units = 'Sv'
    psi_atl_zonal_wrap_var.units = 'Sv'

    psi_glo_vert_wrap_var.units = 'Sv'
    psi_atl_vert_wrap_var.units = 'Sv'

    lat_wrap_var.long_name = 'auxillary latitude'
    lev_wrap_var.long_name = 'depth'
    gphiv_wrap_var.long_name = 'ORCA1 vgrid latitude'
    glamv_wrap_var.long_name = 'ORCA1 vgrid longitude'

    psi_glo_zonal_wrap_var.long_name = 'Global Meridional Mass Transport (zonal integral)'
    psi_atl_zonal_wrap_var.long_name = 'Atlantic Meridional Mass Transport (zonal integral)'

    psi_glo_vert_wrap_var.long_name = 'Global Meridional Mass Transport (vertical integral)'
    psi_atl_vert_wrap_var.long_name = 'Atlantic Meridional Mass Transport (vertical integral)'
    # writing data
    year_wrap_var[:] = period
    month_wrap_var[:] = np.arange(1,13,1)
    lat_wrap_var[:] = gphiv[:,96]
    lev_wrap_var[:] = deptht
    gphiv_wrap_var[:] = gphiv
    glamv_wrap_var[:] = glamv

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
    # create a data pool to save the mass transport for each year and month
    # zonal integral (vertical profile)
    psi_pool_glo_zonal = np.zeros((len(period),12,level,jj),dtype = float)
    psi_pool_atl_zonal = np.zeros((len(period),12,level,jj),dtype = float)
    # vertical integral (horizontal profile)
    psi_pool_glo_vert = np.zeros((len(period),12,jj,ji),dtype = float)
    psi_pool_atl_vert = np.zeros((len(period),12,jj,ji),dtype = float)
    # loop for calculation
    for i in period:
        for j in index_month:
            ####################################################################
            #########################  Extract variables #######################
            ####################################################################
            # get the key of each variable
            theta_key, uv_key = var_key(datapath, i, j)
            ####################################################################
            #########      Calculate meridional mass transport        ##########
            ####################################################################
            # calculate the mass transport
            psi_globe_zonal, psi_atlantic_zonal, psi_globe_vert, psi_atlantic_vert = mass_transport(uv_key,e1v)
            # save output to the pool
            psi_pool_glo_zonal[i-1993,j,:,:] = psi_globe_zonal
            psi_pool_atl_zonal[i-1993,j,:,:] = psi_atlantic_zonal
            psi_pool_glo_vert[i-1993,j,:,:] = psi_globe_vert
            psi_pool_atl_vert[i-1993,j,:,:] = psi_atlantic_vert
    # create NetCDF file and save the output
    create_netcdf_point(psi_pool_glo_zonal, psi_pool_atl_zonal, psi_pool_glo_vert, psi_pool_atl_vert, output_path)

    print 'Computation of statistical matrix on ORCA grid for GLORYS2V3 is complete!!!'
    print 'The output is in sleep, safe and sound!!!'
    logging.info("The full pipeline of the calculation of statistical matrix on ORCA grid for GLORYS2V3 is accomplished!")

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
