#!/usr/bin/env python
"""
Copyright Netherlands eScience Center

Function        : Calculate Oceanic Meridional Energy Transport (ORAS4)
Author          : Yang Liu
Date            : 2017.9.18
Last Update     : 2018.1.6
Description     : The code aims to calculate the oceanic meridional energy
                  transport based on oceanic reanalysis dataset ORAS4 from ECMWF.
                  The complete computaiton is accomplished on model level (original ORCA1_z42 grid).
                  All the interpolations are made on the V grid, including scalars.
                  For the sake of accuracy, the zonal integrations are taken on
                  i-j coordinate, which follows i-coord. For visualization on the
                  map, interpolation is made based on 'point in cell' interpolation.
                  There are two candidates following this rule - nearest neighbour
                  interpolation and bilinear interpolation. No angle adjustment
                  towards velocity field is suggested.

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
# v*rho cpT dxdz = [m/s] * [J / kg] * [kg/m3] * m * m = [J / s] = [Wat]

# gz in [m2 / s2] = [ kg m2 / kg s2 ] = [J / kg]
##########################################################################

# print the system structure and the path of the kernal
print platform.architecture()
print os.path

# switch on the seaborn effect
#sns.set()

# calculate the time for the code execution
start_time = tttt.time()

# Redirect all the console output to a file
#sys.stdout = open('F:\DataBase\ORAS4\console.out','w')
sys.stdout = open('/project/Reanalysis/ORAS4/Monthly/Model/console_E.out','w')

# logging level 'DEBUG' 'INFO' 'WARNING' 'ERROR' 'CRITICAL'
#logging.basicConfig(filename = 'F:\DataBase\ORAS4\history.log', filemode = 'w',level = logging.DEBUG,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(filename = '/project/Reanalysis/ORAS4/Monthly/Model/history_E.log',
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
    # land-sea mask
    tmask = mesh_mask_key.variables['tmask'][0,:,:,:]
    #umask = mesh_mask_key.variables['umask'][0,:,:,:]
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

    #Comparison
    #print 'The tmask file from mesh_mask.nc and the grid T are the same %s' % \
    #       np.array_equal(tmask,tmask_grid_T)

    return nav_lat, nav_lon, nav_lev, tmask, vmask, tmaskatl, e1t, e2t, e1v, e2v, gphiv, glamv, mbathy, e3t_0, e3t_ps

def stream_function(v_key,e1v):
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
    # increase the dimension and adjustment matrix
    e3t_adjust_4D = np.repeat(e3t_adjust[np.newaxis,:,:,:],len(index_month),0)
    # choose the integration order
    int_order = 1  # 1 - from sea bottom to sea surface 2 from sea surfaca to sea bottom
    if int_order == 1:
        # take the integral from sea botton to the surface
        for i in (level - np.arange(level) -1 ):
            if i == level -1:
                psi_globe[:,i,:,:] = e1v_4D[:,i,:,:] * v[:,i,:,:] * vmask_4D[:,i,:,:] * e3t_0[i] -\
                                     e1v_4D[:,i,:,:] * v[:,i,:,:] * vmask_4D[:,i,:,:] * e3t_adjust_4D[:,i,:,:]
            else:
                psi_globe[:,i,:,:] = e1v_4D[:,i,:,:] * v[:,i,:,:] * vmask_4D[:,i,:,:] * e3t_0[i] + psi_globe[:,i+1,:,:] -\
                                     e1v_4D[:,i,:,:] * v[:,i,:,:] * vmask_4D[:,i,:,:] * e3t_adjust_4D[:,i,:,:]
    if int_order == 1:
        # take the integral from sea botton to the surface
        for i in (level - np.arange(level) -1 ):
            if i == level -1:
                psi_atlantic[:,i,:,:] = e1v_4D[:,i,:,:] * v[:,i,:,:] * vmask_4D[:,i,:,:] * e3t_0[i] * tmaskatl_4D[:,i,:,:] -\
                                        e1v_4D[:,i,:,:] * v[:,i,:,:] * vmask_4D[:,i,:,:] * e3t_adjust_4D[:,i,:,:] * tmaskatl_4D[:,i,:,:]
            else:
                psi_atlantic[:,i,:,:] = e1v_4D[:,i,:,:] * v[:,i,:,:] * vmask_4D[:,i,:,:] * e3t_0[i] * tmaskatl_4D[:,i,:,:] + psi_atlantic[:,i+1,:,:] -\
                                        e1v_4D[:,i,:,:] * v[:,i,:,:] * vmask_4D[:,i,:,:] * e3t_adjust_4D[:,i,:,:] * tmaskatl_4D[:,i,:,:]
    elif int_order == 2:
        # take the integral from sea surface to the bottom
        for i in np.arange(level):
            if i == 0:
                psi_globe[:,i,:,:] = e1v_4D[:,i,:,:] * v[:,i,:,:] * vmask_4D[:,i,:,:] * e3t_0[i] -\
                                     e1v_4D[:,i,:,:] * v[:,i,:,:] * vmask_4D[:,i,:,:] * e3t_adjust_4D[:,i,:,:]
            else:
                psi_globe[:,i,:,:] = e1v_4D[:,i,:,:] * v[:,i,:,:] * vmask_4D[:,i,:,:] * e3t_0[i] + psi_globe[:,i+1,:,:] -\
                                     e1v_4D[:,i,:,:] * v[:,i,:,:] * vmask_4D[:,i,:,:] * e3t_adjust_4D[:,i,:,:]
    # take the zonal integral
    psi_stream_globe = np.sum(psi_globe,3)/1e+6 # the unit is changed to Sv
    psi_stream_atlantic = np.sum(psi_atlantic,3)/1e+6 # the unit is changed to Sv

    print "Compute the meridional overturning stream function for globle and Atlantic successfully!"
    logging.info('Compute the meridional overturning stream function for globle and Atlantic successfully!')

    return psi_stream_globe, psi_stream_atlantic

def meridional_energy_transport(theta_key, s_key, u_key, v_key):
    '''
    Compute the meridional energy transport in the ocean
    '''
    # extract variables
    print "Start extracting variables for the quantification of meridional energy transport."
    theta = theta_key.variables['thetao'][:] # the unit of theta is Celsius!
    #u = u_key.variables['uo'][:]
    v = v_key.variables['vo'][:]
    print 'Extracting variables successfully!'
    #logging.info("Extracting variables successfully!")
    # calculate the meridional velocity at T grid
    T_vgrid = np.zeros((len(index_month),level,jj,ji),dtype=float)
    # Interpolation of T on V grid through Nearest-Neighbor method
    for i in np.arange(jj):
        if i == jj-1:
            T_vgrid[:,:,i,:] = theta[:,:,i,:]
        else:
            T_vgrid[:,:,i,:] = (theta[:,:,i,:] + theta[:,:,i+1,:])/2
    # calculate heat flux at each grid point
    Internal_E_flux = np.zeros((len(index_month),level,jj,ji),dtype=float)
    partial = 1 # switch for the partial cells 1 = include & 0 = exclude
    for i in index_month:
        for j in np.arange(level):
                if partial == 1: # include partial cells
                    Internal_E_flux[i,j,:,:] = constant['rho'] * constant['cp'] * v[i,j,:,:] *\
                                               T_vgrid[i,j,:,:] * e1v * e3t_0[j] * vmask[j,:,:] -\
                                               constant['rho'] * constant['cp'] * v[i,j,:,:] *\
                                               T_vgrid[i,j,:,:] * e1v * e3t_adjust * vmask[j,:,:]
                else:
                    Internal_E_flux[i,j,:,:] = constant['rho'] * constant['cp'] * v[i,j,:,:] *\
                                               T_vgrid[i,j,:,:] * e1v * e3t_0[j] * vmask[j,:,:]
    # take the vertical integral
    Internal_E_int = np.zeros((len(index_month),jj,ji))
    Internal_E_int = np.sum(Internal_E_flux,1)/1e+12
    print '*****************************************************************************'
    print "**** Computation of meridional energy transport in the ocean is finished ****"
    print "************         The result is in tera-watt (1E+12)          ************"
    print '*****************************************************************************'
    return Internal_E_int

def zonal_int_plot(E_point,year):
    '''
    Calculate the zonal intergral of meridional energy transport
    '''
    # take the zonal means
    E_zonal_int = np.sum(E_point,2)
    E_zonal_int_mean = np.mean(E_zonal_int,0)/1000
    fig3 = plt.figure()
    plt.plot(gphiv[:,96],E_zonal_int_mean)
    plt.xlabel("Latitude")
    plt.ylabel("Meridional Energy Transport (PW)")
    plt.show()
    fig3.savefig(output_path + os.sep + 'zonal' + os.sep + 'OMET_ORAS4_zonal_int_%d.png' % (year),dpi = 500)

    return E_zonal_int

def regridding(E_ori, mask):
    '''
    Regrid data from ORCA grid to geographical grid.
    It is based on the point in cell interpolation.
    Two options are available:
    1. Bilinear Interpolation
    2. Nearest Neighbour Interpolation
    '''
    print "Regrid the data from ORCA to lat-lon!"
    logging.info("Regrid the data from ORCA to lat-lon!")
    E_mask = np.ma.masked_where(mask == 0, E_ori)
    # use Iris lib for interpolation/regridding
    # support NetCDF
    iris.FUTURE.netcdf_promote = True
    # choose interpolation method
    method_int = 2 # ! 1 = bilinear interpolation ! 2 = nearest neghbour interpolation
    if method_int == 1:
        # prepare the cube
        latitude = iris.coords.AuxCoord(gphiv,standard_name='latitude',units='degrees')
        longitude = iris.coords.AuxCoord(glamv,standard_name='longitude',units='degrees')
        cube_ori = iris.cube.Cube(E_mask/1000,long_name='Oceanic Meridional Energy Transport',
                                  var_name='OMET',units='TW',
                                  aux_coords_and_dims=[(latitude,(0,1)),(longitude,(0,1))])
        # choose the coordinate system for Cube (for regrid module)
        coord_sys = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)
        # Feed cube with coordinate system
        cube_ori.coord('latitude').coord_system = coord_sys
        cube_ori.coord('longitude').coord_system = coord_sys
        print cube_ori
        # create grid_cube for regridding, this is a dummy cube with desired grid
        lat_grid = np.linspace(-90, 90, 181)
        lon_grid = np.linspace(-180, 180, 361)
        # interpolate_points = [('latitude', np.linspace(-90, 90, 181)),
        #                       ('longitude', np.linspace(-180, 181, 361))]
        lat_aux = iris.coords.DimCoord(lat_grid, standard_name='latitude',
                                       units='degrees_north', coord_system='GeogCS')
        lon_aux = iris.coords.DimCoord(lon_grid, standard_name='longitude',
                                       units='degrees_east', coord_system='GeogCS')
        dummy_data = np.zeros((len(lat_grid), len(lon_grid)))
        aux_cube = iris.cube.Cube(dummy_data,dim_coords_and_dims=[(lat_aux, 0), (lon_aux, 1)])
        # Feed cube with coordinate system
        aux_cube.coord('latitude').guess_bounds()
        aux_cube.coord('longitude').guess_bounds()
        aux_cube.coord('latitude').coord_system = coord_sys
        aux_cube.coord('longitude').coord_system = coord_sys
        # create a weight matrix for regridding
        weights = np.ones(cube_ori.shape)
        # interpolate from ORCA grid to rectilinear grid through bilinear interpolation
        # The method uses point in cell interpolation and then perform the bilinear interpolation
        # based on distance and weight
        cube_regrid = iris.experimental.regrid.regrid_weighted_curvilinear_to_rectilinear(cube_ori,weights,aux_cube)
        ##################################################################################################
        # Unfortunately, normal iris modules can not handle the curvilinear grid, only the
        #cube_interpolate = iris.analysis.interpolate.linear(cube_ori, interpolate_points)
        #cube_interpolate = iris.cube.Cube.interpolate(cube_ori,interpolate_points,iris.analysis.Linear())
        #cube_interpolate = cube_ori.interpolate(interpolate_points,iris.analysis.Linear())
        #cube_interpolate = iris.analysis.interpolate.regrid(cube_ori, aux_cube, mode = 'linear')
        ###################################################################################################
    else:
        # define the cube for the use of iris package
        latitude = iris.coords.AuxCoord(gphiv,standard_name='latitude',units='degrees')
        longitude = iris.coords.AuxCoord(glamv,standard_name='longitude',units='degrees')
        cube_ori = iris.cube.Cube(E_mask/1000,long_name='Oceanic Meridional Energy Transport',
                            var_name='OMET',units='PW',aux_coords_and_dims=[(latitude,(0,1)),(longitude,(0,1))])
        print cube_ori
        # choose the projection map type
        projection = ccrs.PlateCarree()
        # Transform cube to target projection
        cube_regrid, extent = iris.analysis.cartography.project(cube_ori, projection, nx=360, ny=180)
    # interpolation complete!!
    print cube_regrid
    E_regrid = cube_regrid.data
    x_coord = cube_regrid.coord('longitude').points
    y_coord = cube_regrid.coord('latitude').points

    return cube_regrid, E_regrid, x_coord, y_coord

def visualization(cube_regrid,year):
    print "Visualize the data on PlateCarree map!"
    logging.info("Visualize the data on PlateCarree map!")
    # support NetCDF
    iris.FUTURE.netcdf_promote = True
    print cube_regrid
    fig2 = plt.figure()
    fig2.suptitle('ORCA1 Data Projected to PlateCarree')
    # Set up axes and title
    ax = plt.subplot(projection=ccrs.PlateCarree())
    # Set limits
    ax.set_global()
    # Draw coastlines
    ax.coastlines()
    # set gridlines and ticks
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,linewidth=1,
                 color='gray', alpha=0.5,linestyle='--')
    gl.xlabels_top = False
    gl.xlabel_style = {'size': 11, 'color': 'gray'}
    #gl.xlines = False
    #gl.set_xticks()
    #gl.set_yticks()
    gl.xformatter = LONGITUDE_FORMATTER
    gl.ylabel_style = {'size': 11, 'color': 'gray'}
    #ax.ylabels_left = False
    gl.yformatter = LATITUDE_FORMATTER
    # plot with Iris quickplot pcolormesh
    qplt.pcolormesh(cube_regrid,cmap='coolwarm')
    iplt.show()
    fig2.savefig(output_path + os.sep + 'lat-lon' + os.sep + 'OMET_ORAS4_lat-lon_%d.jpg' % (year),dpi = 500)

    # extract the interpolated values from cube
    #E_interpolation = cube_regrid.data

    #return E_interpolation

def create_netcdf_point (meridional_E_point_pool,output_path):
    print '*******************************************************************'
    print '*********************** create netcdf file ************************'
    print '***********************    OMET on ORCA   *************************'
    print '*******************************************************************'
    logging.info("Start creating netcdf file for total meridional energy transport at each grid point.")
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path + os.sep + 'oras4_model_monthly_orca1_E_point.nc' ,'w',format = 'NETCDF3_64BIT')
    # create dimensions for netcdf data
    year_wrap_dim = data_wrap.createDimension('year',len(period))
    month_wrap_dim = data_wrap.createDimension('month',12)
    lat_wrap_dim = data_wrap.createDimension('j',jj)
    lon_wrap_dim = data_wrap.createDimension('i',ji)
    # create coordinate variables for 3-dimensions
    # 1D
    year_wrap_var = data_wrap.createVariable('year',np.int32,('year',))
    month_wrap_var = data_wrap.createVariable('month',np.int32,('month',))
    # 2D
    lat_wrap_var = data_wrap.createVariable('latitude',np.float32,('j','i'))
    lon_wrap_var = data_wrap.createVariable('longitude',np.float32,('j','i'))
    # 4D
    E_total_wrap_var = data_wrap.createVariable('E',np.float64,('year','month','j','i'))
    # global attributes
    data_wrap.description = 'Monthly mean meridional energy transport on ORCA grid'
    # variable attributes
    lat_wrap_var.units = 'ORCA1_latitude'
    lon_wrap_var.units = 'ORCA1_longitude'
    E_total_wrap_var.units = 'tera watt'

    lat_wrap_var.long_name = 'ORCA1 grid latitude'
    lon_wrap_var.long_name = 'ORCA1 grid longitude'
    E_total_wrap_var.long_name = 'oceanic meridional energy transport'
    # writing data
    year_wrap_var[:] = period
    lat_wrap_var[:] = gphiv
    lon_wrap_var[:] = glamv
    month_wrap_var[:] = np.arange(1,13,1)
    E_total_wrap_var[:] = meridional_E_point_pool
    # close the file
    data_wrap.close()
    print "Create netcdf file successfully"
    logging.info("The generation of netcdf files for the total meridional energy transport on each grid point is complete!!")

def create_netcdf_regrid (meridional_E_point_regrid,output_path):
    print '*******************************************************************'
    print '*********************** create netcdf file ************************'
    print '*********************    OMET on lat-lon   ************************'
    print '*******************************************************************'
    logging.info("Start creating netcdf file for total meridional energy transport at each grid point.")
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path + os.sep + 'oras4_model_monthly_lat-lon_E_point.nc' ,'w',format = 'NETCDF3_64BIT')
    # create dimensions for netcdf data
    year_wrap_dim = data_wrap.createDimension('year',len(period))
    lat_wrap_dim = data_wrap.createDimension('latitude',180)
    lon_wrap_dim = data_wrap.createDimension('longitude',360)
    # create coordinate variables for 3-dimensions
    # 1D
    year_wrap_var = data_wrap.createVariable('year',np.int32,('year',))
    lat_wrap_var = data_wrap.createVariable('latitude',np.float32,('latitude',))
    lon_wrap_var = data_wrap.createVariable('longitude',np.float32,('longitude',))
    # 3D
    E_total_wrap_var = data_wrap.createVariable('E',np.float64,('year','latitude','longitude'))
    # global attributes
    data_wrap.description = 'Monthly mean meridional energy transport interpolated on lat-lon grid'
    # variable attributes
    lat_wrap_var.units = 'degree_north'
    lon_wrap_var.units = 'degree_east'
    E_total_wrap_var.units = 'tera watt'

    lat_wrap_var.long_name = 'latitude'
    lon_wrap_var.long_name = 'longitude'
    E_total_wrap_var.long_name = 'oceanic meridional energy transport'
    # writing data
    year_wrap_var[:] = period
    lat_wrap_var[:] = interpolate_lat
    lon_wrap_var[:] = interpolate_lon
    E_total_wrap_var[:] = meridional_E_point_regrid
    # close the file
    data_wrap.close()
    print "Create netcdf file successfully"
    logging.info("The generation of netcdf files for the total meridional energy transport on each grid point is complete!!")

def create_netcdf_zonal_int (meridional_E_zonal_int_pool,meridional_psi_zonal_glo, meridional_psi_zonal_atl,output_path):
    print '*******************************************************************'
    print '*********************** create netcdf file ************************'
    print '***********************    OMET on ORCA   *************************'
    print '*******************************************************************'
    logging.info("Start creating netcdf file for total meridional energy transport at each grid point.")
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path + os.sep + 'oras4_model_monthly_orca1_E_zonal_int.nc' ,'w',format = 'NETCDF3_64BIT')
    # create dimensions for netcdf data
    year_wrap_dim = data_wrap.createDimension('year',len(period))
    month_wrap_dim = data_wrap.createDimension('month',12)
    lat_wrap_dim = data_wrap.createDimension('latitude_aux',jj)
    lev_wrap_dim = data_wrap.createDimension('lev',level)
    # create coordinate variables for 3-dimensions
    # 1D
    year_wrap_var = data_wrap.createVariable('year',np.int32,('year',))
    month_wrap_var = data_wrap.createVariable('month',np.int32,('month',))
    lat_wrap_var = data_wrap.createVariable('latitude_aux',np.float32,('latitude_aux',))
    lev_wrap_var = data_wrap.createVariable('lev',np.float32,('lev',))
    # 3D
    E_total_wrap_var = data_wrap.createVariable('E',np.float64,('year','month','latitude_aux'))
    # 4D
    psi_glo_wrap_var = data_wrap.createVariable('Psi_glo',np.float64,('year','month','lev','latitude_aux'))
    psi_atl_wrap_var = data_wrap.createVariable('Psi_atl',np.float64,('year','month','lev','latitude_aux'))
    # global attributes
    data_wrap.description = 'Monthly mean zonal integral of meridional energy transport on ORCA grid'
    # variable attributes
    lat_wrap_var.units = 'degree_north'
    E_total_wrap_var.units = 'tera watt'
    lev_wrap_var.units = 'm'
    psi_glo_wrap_var.units = 'Sv'
    psi_atl_wrap_var.units = 'Sv'

    lev_wrap_var.long_name = 'depth'
    lat_wrap_var.long_name = 'auxillary latitude'
    E_total_wrap_var.long_name = 'Oceanic meridional energy transport'
    psi_glo_wrap_var.long_name = 'Meridional overturning stream function of global ocean'
    psi_atl_wrap_var.long_name = 'Meridional overturning stream function of Atlantic ocean'
    # writing data
    year_wrap_var[:] = period
    lat_wrap_var[:] = gphiv[:,96]
    month_wrap_var[:] = np.arange(1,13,1)
    lev_wrap_var[:] = nav_lev
    E_total_wrap_var[:] = meridional_E_zonal_int_pool
    psi_glo_wrap_var[:] = meridional_psi_zonal_glo
    psi_atl_wrap_var[:] = meridional_psi_zonal_atl
    # close the file
    data_wrap.close()
    print "Create netcdf file successfully"
    logging.info("The generation of netcdf files for the total meridional energy transport on each grid point is complete!!")

if __name__=="__main__":
    # create the year index
    period = np.arange(start_year,end_year+1,1)
    index_month = np.arange(12)
    # ORCA1_z42 grid infor (Madec and Imbard 1996)
    ji = 362
    jj = 292
    level = 42
    # extract the mesh_mask and coordinate information
    nav_lat, nav_lon, nav_lev, tmask, vmask, tmaskatl, e1t, e2t, e1v, e2v, gphiv,\
    glamv, mbathy, e3t_0, e3t_ps = var_coordinate(datapath)
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
    # create a data pool to save the OMET for each year and month
    E_pool_point = np.zeros((len(period),12,jj,ji),dtype = float)
    E_pool_zonal_int = np.zeros((len(period),12,jj),dtype = float)
    # create a data pool to save the meridional overturning for each year and month
    psi_pool_zonal_glo = np.zeros((len(period),12,level,jj),dtype = float)
    psi_pool_zonal_atl = np.zeros((len(period),12,level,jj),dtype = float)
    #E_pool_point_regrid = np.zeros((len(period),180,360),dtype = float)
    # save the latitude and longitude for interpolation
    #interpolate_lat = np.zeros(180,dtype = float)
    #interpolate_lon = np.zeros(360,dtype = float)
    # loop for calculation
    for i in period:
        # get the key of each variable
        theta_key, s_key, u_key, v_key = var_key(datapath, i)
        # calculate the stokes stream function and plot
        psi_glo, psi_atl = stream_function(v_key,e1v)
        psi_pool_zonal_glo[i-1958,:,:,:] = psi_glo
        psi_pool_zonal_atl[i-1958,:,:,:] = psi_atl
        # calculate the meridional energy transport in the ocean
        E_point = meridional_energy_transport(theta_key, s_key, u_key, v_key)
        E_pool_point[i-1958,:,:,:] = E_point
        # regridding for visualization
        #cube_regrid, E_regrid, x_coord, y_coord = regridding(E_point_mean, vmask[0,:,:])
        #E_pool_point_regrid[i-1958,:,:] = E_regrid
        #visualization
        #visualization(cube_regrid,i)
        # plot the meridional energy transport in the ocean
        E_zonal_int = zonal_int_plot(E_point,i)
        E_pool_zonal_int[i-1958,:,:] = E_zonal_int
        #if i == start_year:
            #interpolate_lat = y_coord
            #interpolate_lon = x_coord
    # create NetCDF file and save the output
    create_netcdf_point(E_pool_point,output_path)
    #create_netcdf_regrid(E_pool_point_regrid,output_path)
    create_netcdf_zonal_int(E_pool_zonal_int,psi_pool_zonal_glo,psi_pool_zonal_atl,output_path)

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
