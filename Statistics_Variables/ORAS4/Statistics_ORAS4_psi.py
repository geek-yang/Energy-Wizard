#!/usr/bin/env python
"""
Copyright Netherlands eScience Center

Function        : A statistical look into the temporal and spatial distribution of fields (ORAS4)
Author          : Yang Liu
Date            : 2018.1.4
Last Update     : 2018.1.6
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
sys.stdout = open('/project/Reanalysis/ORAS4/Monthly/Model/console_psi.out','w')

# logging level 'DEBUG' 'INFO' 'WARNING' 'ERROR' 'CRITICAL'
#logging.basicConfig(filename = 'F:\DataBase\ORAS4\history.log', filemode = 'w',level = logging.DEBUG,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(filename = '/project/Reanalysis/ORAS4/Monthly/Model/history_psi.log',
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
    e3t_ps = mesh_mask_key.variables['e3t_ps'][0,:,:]
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

    return nav_lat, nav_lon, nav_lev, tmask, umask, vmask, tmaskatl, e1t, e2t, e1v, e2v, gphiu, glamu, gphiv, glamv, mbathy, e3t_0, e3t_ps

def mass_transport(v_key,e1v):
    '''
    This function is used to calculate the mass transport.
    The unit is Sv (1E+6 m3/s)
    '''
    print "Compute the meridional overturning stream function for globle and Atlantic!"
    logging.info('Compute the meridional overturning stream function for globle and Atlantic!')
    #dominant equation for stream function
    # psi = e1v(m) * rho(kg/m3) * v(m/s) * dz(m) = (kg/s)
    # extract variables
    #u = u_key.variables['uo'][:]
    v = v_key.variables['vo'][:]
    # define the stream function psi
    psi_globe = np.zeros((len(index_month),level,jj,ji),dtype=float)
    psi_atlantic = np.zeros((len(index_month),level,jj,ji),dtype=float)
    # expand the grid size matrix e1v to avoid more loops
    e1v_3D = np.repeat(e1v[np.newaxis,:,:],level,0)
    e1v_4D = np.repeat(e1v_3D[np.newaxis,:,:,:],len(index_month),0)
    # increase the dimension of vmask
    vmask_4D = np.repeat(vmask[np.newaxis,:,:,:],len(index_month),0)
    tmaskatl_3D = np.repeat(tmaskatl[np.newaxis,:,:],level,0)
    tmaskatl_4D = np.repeat(tmaskatl_3D[np.newaxis,:,:,:],len(index_month),0)
    # increase the dimension of partial cell adjustment matrix
    e3t_adjust_4D = np.repeat(e3t_adjust[np.newaxis,:,:,:],len(index_month),0)
    # take the integral from sea botton to the surface
    for i in np.arange(level):
        psi_globe[:,i,:,:] = e1v_4D[:,i,:,:] * v[:,i,:,:] * vmask_4D[:,i,:,:] * e3t_0[i] -\
                             e1v_4D[:,i,:,:] * v[:,i,:,:] * vmask_4D[:,i,:,:] * e3t_adjust_4D[:,i,:,:]
        psi_atlantic[:,i,:,:] = e1v_4D[:,i,:,:] * v[:,i,:,:] * vmask_4D[:,i,:,:] * e3t_0[i] * tmaskatl_4D[:,i,:,:] -\
                                e1v_4D[:,i,:,:] * v[:,i,:,:] * vmask_4D[:,i,:,:] * e3t_adjust_4D[:,i,:,:] * tmaskatl_4D[:,i,:,:]
    # take the zonal integral
    psi_globe_zonal_int = np.sum(psi_globe,3)/1e+6 # the unit is changed to Sv
    psi_atlantic_zonal_int = np.sum(psi_atlantic,3)/1e+6 # the unit is changed to Sv
    # take the vertical integral
    psi_globe_vert_int = np.sum(psi_globe,1)/1e+6 # the unit is changed to Sv
    psi_atlantic_vert_int = np.sum(psi_atlantic,1)/1e+6 # the unit is changed to Sv

    print "Compute the mass transport for globle and Atlantic successfully!"
    logging.info('Compute the mass transport for globle and Atlantic successfully!')

    return psi_globe_zonal_int, psi_atlantic_zonal_int, psi_globe_vert_int, psi_atlantic_vert_int

def create_netcdf_point (psi_pool_glo_zonal, psi_pool_atl_zonal, psi_pool_glo_vert, psi_pool_atl_vert,output_path):
    print '*******************************************************************'
    print '*********************** create netcdf file ************************'
    print '********************    statistics on ORCA   **********************'
    print '*******************************************************************'
    logging.info("Start creating netcdf file for the statistics of fields at each grid point.")
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path + os.sep + 'oras4_model_monthly_orca1_psi_point.nc' ,'w',format = 'NETCDF3_64BIT')
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
    gphiv_wrap_var = data_wrap.createVariable('gphiv',np.float32,('j','i'))
    glamv_wrap_var = data_wrap.createVariable('glamv',np.float32,('j','i'))
    # 4D
    psi_glo_zonal_wrap_var = data_wrap.createVariable('psi_glo_zonal',np.float64,('year','month','lev','j'))
    psi_atl_zonal_wrap_var = data_wrap.createVariable('psi_atl_zonal',np.float64,('year','month','lev','j'))

    psi_glo_vert_wrap_var = data_wrap.createVariable('psi_glo_vert',np.float64,('year','month','j','i'))
    psi_atl_vert_wrap_var = data_wrap.createVariable('psi_atl_vert',np.float64,('year','month','j','i'))

    # global attributes
    data_wrap.description = 'Monthly mean mass transport on ORCA grid'
    # variable attributes
    lev_wrap_var.units = 'm'
    gphiv_wrap_var.units = 'ORCA1_latitude_vgrid'
    glamv_wrap_var.units = 'ORCA1_longitude_vgrid'

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
    lev_wrap_var[:] = nav_lev
    gphiv_wrap_var[:] = gphiv
    glamv_wrap_var[:] = glamv

    psi_glo_zonal_wrap_var[:] = psi_pool_glo_zonal
    psi_atl_zonal_wrap_var[:] = psi_pool_atl_zonal

    psi_glo_vert_wrap_var[:] = psi_pool_glo_vert
    psi_atl_vert_wrap_var[:] = psi_pool_atl_vert
    # close the file
    data_wrap.close()
    print "Create netcdf file successfully"
    logging.info("The generation of netcdf files for the mass transport in ORAS4 on each grid point is complete!!")

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
    gphiu, glamu, gphiv, glamv, mbathy, e3t_0, e3t_ps = var_coordinate(datapath)
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
    print '*******************************************************************'
    print '************************ create data pool *************************'
    print '*******************************************************************'
    # create a data pool to save the mass transport for each year and month
    # zonal integral (vertical profile)
    psi_pool_glo_zonal = np.zeros((len(period),12,level,jj),dtype = float)
    psi_pool_atl_zonal = np.zeros((len(period),12,level,jj),dtype = float)
    # vertical integral (horizontal profile)
    psi_pool_glo_vert = np.zeros((len(period),12,jj,ji),dtype = float)
    psi_pool_atl_vert = np.zeros((len(period),12,jj,ji),dtype = float)
    # loop for calculation
    for i in period:
        # get the key of each variable
        theta_key, s_key, u_key, v_key = var_key(datapath, i)
        # calculate the stokes stream function and plot
        psi_globe_zonal, psi_atlantic_zonal, psi_globe_vert, psi_atlantic_vert = mass_transport(v_key,e1v)
        # save output to the pool
        psi_pool_glo_zonal[i-1958,:,:,:] = psi_globe_zonal
        psi_pool_atl_zonal[i-1958,:,:,:] = psi_atlantic_zonal
        psi_pool_glo_vert[i-1958,:,:,:] = psi_globe_vert
        psi_pool_atl_vert[i-1958,:,:,:] = psi_atlantic_vert
    # create NetCDF file and save the output
    create_netcdf_point(psi_pool_glo_zonal, psi_pool_atl_zonal, psi_pool_glo_vert, psi_pool_atl_vert, output_path)

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
