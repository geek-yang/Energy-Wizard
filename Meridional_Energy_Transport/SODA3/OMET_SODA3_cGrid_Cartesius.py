#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : Calculate Oceanic Meridional Energy Transport (SODA3) on Cartesius
Author          : Yang Liu
Date            : 2018.01.12
Last Update     : 2018.02.24
Description     : The code aims to calculate the oceanic meridional energy
                  transport based on oceanic reanalysis dataset SODA3 from
                  Maryland University and TAMU. The complete computaiton is accomplished
                  on model level (original MOM5_z50 Arakawa-B grid). All the interpolations
                  are made on the C grid. The procedure is generic and is able
                  to adapt any ocean reanalysis datasets, with some changes.
Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, sys, matplotlib, logging
variables       : Potential Temperature                     Theta
                  Zonal Current Velocity                    u
                  Meridional Current Velocity               v
                  Zonal Grid Spacing Scale Factors          e1
                  Meridional Grid Spacing Scale Factors     e2
                  Land-Sea Mask                             mask
Caveat!!        : The full dataset is from 1980 to 2015.
                  Direction of Axis:
                  Model Level: MOM5 Arakawa-B grid
                  The data is 5 days mean!!!!!!!!!
                  Dimension:
                  Latitude      1070
                  Longitude     1440
                  Depth         50
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
# cpT:  [J / kg C] * [C]     = [J / kgT]
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
sys.stdout = open('/project/Reanalysis/SODA3/console_E.out','w')

# logging level 'DEBUG' 'INFO' 'WARNING' 'ERROR' 'CRITICAL'
#logging.basicConfig(filename = 'F:\DataBase\ORAS4\history.log', filemode = 'w',level = logging.DEBUG,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(filename = '/project/Reanalysis/SODA3/history_E.log',
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
datapath = '/projects/0/blueactn/reanalysis/SODA3/5day'
# path of mask file
datapath_mask = '/projects/0/blueactn/reanalysis/SODA3'
# the input files are 5 days data
# each file has a name with date
# we have to load files for each month seperately, for the sake of monthly mean
# each record for each month is placed in folders by month
# the names are listed in a txt file line by line
# we will load the name from the txt file
datapath_namelist = '/projects/0/blueactn/reanalysis/SODA3/5day'
ff = open(datapath_namelist + os.sep + 'namelist.txt','r')
# can not skip \n
#namelist = ff.readlines()
# remember to skip \n
namelist = ff.read().splitlines()
print namelist
ff.close()

#file_list_in = sys.stdin.readline()
# starting time (year)
#file_name = str(file_list_in)
# Ending time, if only for 1 year, then it should be the same as starting year
#end_year = 2015
# specify output path for the netCDF4 file
output_path = '/home/lwc16308/reanalysis/SODA3/output'
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
    #subbasin_mesh_key = Dataset(datapath+ os.sep + '') #sub-basin from Andreas
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
    zb = mesh_mask_key.variables['zb'][:]                       # Depth of T cell edges (z51)
    # calculate the depth of each layer
    dz = np.zeros(zt.shape)
    dz[0] = zb[0]
    dz[1:] = zb[1:] - zb[:-1]
    # area of T cell - for the computation onamelistf ocean heat content
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
    tmaskatl = tmask
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

    return grid_x_T, grid_y_T, grid_x_C, grid_y_C, x_T, y_T, x_C, y_C, zt, dz, area_T,\
           e1t, e2t, e1c, e2c, tmask, tmaskatl, cmask, mbathy_t, mbathy_c, topo_depth_t, topo_depth_c


def stream_function(soda_key,e1c):
    '''
    This function is used to calculate the mass transport.
    The unit is Sv (1E+6 m3/s)
    '''
    print "Compute the meridional overturning stream function for globle and Atlantic!"
    logging.info('Compute the meridional overturning stream function for globle and Atlantic!')
    #dominant equation for stream function
    # psi = e1c(m) * rho(kg/m3) * v(m/s) * dz(m) = (kg/s)
    # extract variables
    #u = soda_key.variables['u'][0,:,:,:]
    v = soda_key.variables['v'][0,:,:,:]
    # set the filled value to be 0
    #np.ma.set_fill_value(u,0)
    np.ma.set_fill_value(v,0)
    # define the stream function psi
    psi_globe = np.zeros((level,jj,ji),dtype=float)
    psi_atlantic = np.zeros((level,jj,ji),dtype=float)
    # expand the grid size matrix e1c to avoid more loops
    e1c_3D = np.repeat(e1c[np.newaxis,:,:],level,0)
    # choose the integration order
    int_order = 1  # 1 - from sea bottom to sea surface 2 from sea surfaca to sea bottom
    if int_order == 1:
        # take the integral from sea botton to the surface
        # global meridional overturning stream function
        for i in (level - np.arange(level) -1):
            if i == level -1:
                psi_globe[i,:,:] = e1c_3D[i,:,:] * v[i,:,:].filled() * cmask[:] * dz[i] -\
                                   e1c_3D[i,:,:] * v[i,:,:].filled() * cmask[:] * dz_adjust_c[i,:,:]
                # for old version of python to avoid the filling value during summation
                psi_globe[i,:,:] = psi_globe[i,:,:] * cmask[:]
            else:
                psi_globe[i,:,:] = e1c_3D[i,:,:] * v[i,:,:].filled() * cmask[:] * dz[i] + psi_globe[i+1,:,:] -\
                                   e1c_3D[i,:,:] * v[i,:,:].filled() * cmask[:] * dz_adjust_c[i,:,:]
                # for old version of python to avoid the filling value during summation
                psi_globe[i,:,:] = psi_globe[i,:,:] * cmask[:]
        # Atlantic meridional overturning stream function
        for i in (level - np.arange(level) -1 ):
            if i == level -1:
                psi_atlantic[i,:,:] = e1c_3D[i,:,:] * v[i,:,:].filled() * cmask[:] * tmaskatl * dz[i] -\
                                      e1c_3D[i,:,:] * v[i,:,:].filled() * cmask[:] * tmaskatl * dz_adjust_c[i,:,:]
                # for old version of python to avoid the filling value during summation
                psi_atlantic[i,:,:] = psi_atlantic[i,:,:] * tmaskatl * cmask[:]
            else:
                psi_atlantic[i,:,:] = e1c_3D[i,:,:] * v[i,:,:].filled() * cmask[:] * tmaskatl * dz[i] + psi_atlantic[i+1,:,:] -\
                                      e1c_3D[i,:,:] * v[i,:,:].filled() * cmask[:] * tmaskatl * dz_adjust_c[i,:,:]
                # for old version of python to avoid the filling value during summation
                psi_atlantic[i,:,:] = psi_atlantic[i,:,:] * tmaskatl * cmask[:]
    elif int_order == 2:
        # take the integral from sea surface to the bottom
        for i in np.arange(level):
            if i == 0:
                psi_globe[i,:,:] = e1c_3D[i,:,:] * v[i,:,:].filled() * cmask[:] * dz[i] -\
                                   e1c_3D[i,:,:] * v[i,:,:].filled() * cmask[:] * dz_adjust_c[i,:,:]
            else:
                psi_globe[i,:,:] = e1c_3D[i,:,:] * v[i,:,:].filled() * cmask[:] * dz[i] + psi_globe[i+1,:,:] -\
                                   e1c_3D[i,:,:] * v[i,:,:].filled() * cmask[:] * dz_adjust_c[i,:,:]
    # take the zonal integral
    psi_stream_globe = np.sum(psi_globe,2)/1e+6 # the unit is changed to Sv
    psi_stream_atlantic = np.sum(psi_atlantic,2)/1e+6 # the unit is changed to Sv

    print "Compute the meridional overturning stream function for globle and Atlantic successfully!"
    logging.info('Compute the meridional overturning stream function for globle and Atlantic successfully!')

    return psi_stream_globe, psi_stream_atlantic

def visualization_stream_function(psi_glo,psi_atl):
    print "Visualize meridional overturning stream function for globle and Atlantic."
    logging.info('Visualize the meridional overturning stream function for globle and Atlantic.')

    psi_glo_mean = np.mean(np.mean(psi_glo,0),0)
    psi_atl_mean = np.mean(np.mean(psi_atl,0),0)
    # plot the global meridional overturning stream function
    fig0 = plt.figure()
    X , Y = np.meshgrid(grid_y_C,zt)
    #contour_level = np.arange(-40,80,5)
    plt.contour(X,Y,psi_glo_mean,linewidth= 0.2)
    #cs = plt.contourf(X,Y,psi_glo_mean,contour_level,linewidth= 0.2,cmap='RdYlGn')
    plt.title('Stokes Stream Function of Global Ocean')
    plt.xlabel("Laitude")
    plt.xticks(np.linspace(-90,90,13))
    plt.ylabel("Ocean Depth")
    #cbar = plt.colorbar(orientation='horizontal')
    #cbar.set_label('Transport of mass 1E+6 m3/s')
    #invert the y axis
    plt.gca().invert_yaxis()
    plt.show()
    fig0.savefig(output_path + os.sep + "OMET_SODA3_StreamFunction_Globe.png",dpi=500)

    # plot the Atlantic meridional overturning stream function
    fig1 = plt.figure()
    X , Y = np.meshgrid(grid_y_C,zt)
    #contour_level = np.arange(-40,80,5)
    plt.contour(X,Y,psi_atl_mean,linewidth= 0.2)
    #cs = plt.contourf(X,Y,psi_atl_mean,contour_level,linewidth= 0.2,cmap='RdYlGn')
    plt.title('Stokes Stream Function of Atlantic Ocean')
    plt.xlabel("Laitude")
    plt.xticks(np.linspace(-90,90,13))
    plt.ylabel("Ocean Depth")
    #cbar = plt.colorbar(orientation='horizontal')
    #cbar.set_label('Transport of mass 1E+6 m3/s')
    #invert the y axis
    plt.gca().invert_yaxis()
    plt.show()
    fig1.savefig(output_path + os.sep + "OMET_SODA3_StreamFunction_Atlantic.png",dpi=500)

    print "Export meridional overturning stream function for globle and Atlantic."
    logging.info('Export the meridional overturning stream function for globle and Atlantic.')

def meridional_energy_transport(soda_key):
    '''
    This function is used to correct the mass budget.
    '''
    # extract variables
    print "Start extracting variables for the quantification of meridional energy transport."
    #time = soda_key.variables['time'][:]                            # days since 1980-01-01 00:00:00, the unit is JULIAN
    temp = soda_key.variables['temp'][0,:,:,:]                      # potential temperature, the unit is Celsius!
    #u = soda_key.variables['u'][0,:,:,:]
    v = soda_key.variables['v'][0,:,:,:]
    # net_heating = soda_key.variables['net_heating'][0,:,:,:]      # surface ocean heat flux coming through coupler and mass transfer
    # set the filled value to be 0
    np.ma.set_fill_value(v,0)
    print 'Extracting variables successfully!'
    #logging.info("Extracting variables successfully!")
    # calculate the meridional velocity at T grid
    T_cgrid = np.zeros((level,jj,ji),dtype=float)
    # Interpolation of T on V grid through Nearest-Neighbor method
    for i in np.arange(jj):
        for j in np.arange(ji):
            if i == jj-1:
                if j == ji-1:
                    T_cgrid[:,i,j] = (temp[:,i,j] + temp[:,i,0])/2
                else:
                    T_cgrid[:,i,j] = (temp[:,i,j] + temp[:,i,j+1])/2
            else:
                if j == ji-1:
                    T_cgrid[:,i,j] = ((temp[:,i,j] + temp[:,i+1,j])/2 + (temp[:,i,0] + temp[:,i+1,0])/2)/2
                else:
                    T_cgrid[:,i,j] = ((temp[:,i,j] + temp[:,i+1,j])/2 + (temp[:,i,j+1] + temp[:,i+1,j+1])/2)/2
    # calculate heat flux at each grid point
    Internal_E_flux = np.zeros((level,jj,ji),dtype=float)
    partial = 1 # switch for the partial cells 1 = include & 0 = exclude
    for i in np.arange(level):
        if partial == 1: # include partial cells
            Internal_E_flux[i,:,:] = constant['rho'] * constant['cp'] * v[i,:,:].filled() *\
                                     T_cgrid[i,:,:] * e1c * dz[i] * cmask[:] -\
                                     constant['rho'] * constant['cp'] * v[i,:,:].filled() *\
                                     T_cgrid[i,:,:] * e1c * dz_adjust_c[i,:,:] * cmask[:]
        else: # exclude partial cells
            Internal_E_flux[i,:,:] = constant['rho'] * constant['cp'] * v[i,:,:].filled() *\
                                     T_cgrid[i,:,:] * e1c * dz[i] * cmask[:]
    # take the vertical integral
    Internal_E_int = np.zeros((jj,ji))
    Internal_E_int = np.sum(Internal_E_flux,0) * cmask / 1e+12
    print '*****************************************************************************'
    print "**** Computation of meridional energy transport in the ocean is finished ****"
    print "************         The result is in tera-watt (1E+12)          ************"
    print '*****************************************************************************'
    return Internal_E_int

def zonal_int_plot(E_monthly):
    # take the zonal means
    E_zonal_int_mean = np.mean(E_monthly,0)/1000
    fig3 = plt.figure()
    plt.plot(grid_y_C,E_zonal_int_mean)
    plt.xlabel("Latitude")
    plt.ylabel("Meridional Energy Transport (PW)")
    plt.show()
    fig3.savefig(output_path + os.sep + 'OMET_SODA3_monthly.png',dpi = 500)

def create_netcdf_point (meridional_E_point_pool,output_path):
    print '*******************************************************************'
    print '*********************** create netcdf file ************************'
    print '***********************    OMET on MOM    *************************'
    print '*******************************************************************'
    logging.info("Start creating netcdf file for total meridional energy transport at each grid point.")
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path + os.sep + 'SODA3_model_5daily_mom5_E_point.nc' ,'w',format = 'NETCDF3_64BIT')
    # create dimensions for netcdf data
    #year_wrap_dim = data_wrap.createDimension('year',len(period))
    #month_wrap_dim = data_wrap.createDimension('month',12)
    time_wrap_dim = data_wrap.createDimension('time',len(namelist))
    lat_wrap_dim = data_wrap.createDimension('j',jj)
    lon_wrap_dim = data_wrap.createDimension('i',ji)
    # create coordinate variables for 3-dimensions
    # 1D
    #year_wrap_var = data_wrap.createVariable('year',np.int32,('year',))
    #month_wrap_var = data_wrap.createVariable('month',np.int32,('month',))
    time_wrap_var = data_wrap.createVariable('time',np.int32,('time',))
    # 2D
    lat_wrap_var = data_wrap.createVariable('latitude',np.float32,('j','i'))
    lon_wrap_var = data_wrap.createVariable('longitude',np.float32,('j','i'))
    # 4D
    E_total_wrap_var = data_wrap.createVariable('E',np.float64,('time','j','i'))
    # global attributes
    data_wrap.description = '5 daily meridional energy transport on MOM5 grid'
    # variable attributes
    lat_wrap_var.units = 'MOM5_latitude'
    lon_wrap_var.units = 'MOM5_longitude'
    time_wrap_var.units = 'day'
    E_total_wrap_var.units = 'tera watt'

    lat_wrap_var.long_name = 'MOM5 grid latitude'
    lon_wrap_var.long_name = 'MOM5 grid longitude'
    time_wrap_var.long_name = '5 day time'
    E_total_wrap_var.long_name = 'oceanic meridional energy transport'
    # writing data
    #year_wrap_var[:] = period
    lat_wrap_var[:] = y_C
    lon_wrap_var[:] = x_C
    time_wrap_var[:] = np.arange(len(namelist))
    #month_wrap_var[:] = np.arange(1,13,1)
    E_total_wrap_var[:] = meridional_E_point_pool
    # close the file
    data_wrap.close()
    print "Create netcdf file successfully"
    logging.info("The generation of netcdf files for the total meridional energy transport on each grid point is complete!!")

def create_netcdf_zonal_int (meridional_E_zonal_int_pool, meridional_psi_zonal_glo, meridional_psi_zonal_atl,output_path):
    print '*******************************************************************'
    print '*********************** create netcdf file ************************'
    print '***********************    OMET on ORCA   *************************'
    print '*******************************************************************'
    logging.info("Start creating netcdf file for total meridional energy transport at each grid point.")
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path + os.sep + 'SODA3_model_5daily_mom5_E_zonal_int.nc' ,'w',format = 'NETCDF3_64BIT')
    # create dimensions for netcdf data
    #year_wrap_dim = data_wrap.createDimension('year',len(period))
    #month_wrap_dim = data_wrap.createDimension('month',12)
    time_wrap_dim = data_wrap.createDimension('time',len(namelist))
    lat_wrap_dim = data_wrap.createDimension('latitude_aux',jj)
    lev_wrap_dim = data_wrap.createDimension('lev',level)
    # create coordinate variables for 3-dimensions
    # 1D
    #year_wrap_var = data_wrap.createVariable('year',np.int32,('year',))
    #month_wrap_var = data_wrap.createVariable('month',np.int32,('month',))
    time_wrap_var = data_wrap.createVariable('time',np.int32,('time',))
    lat_wrap_var = data_wrap.createVariable('latitude_aux',np.float32,('latitude_aux',))
    lev_wrap_var = data_wrap.createVariable('lev',np.float32,('lev',))
    # 3D
    E_total_wrap_var = data_wrap.createVariable('E',np.float64,('time','latitude_aux'))
    # 4D
    psi_glo_wrap_var = data_wrap.createVariable('Psi_glo',np.float64,('time','lev','latitude_aux'))
    psi_atl_wrap_var = data_wrap.createVariable('Psi_atl',np.float64,('time','lev','latitude_aux'))
    # global attributes
    data_wrap.description = 'Monthly mean zonal integral of meridional energy transport on ORCA grid'
    # variable attributes
    lat_wrap_var.units = 'degree_north'
    E_total_wrap_var.units = 'tera watt'
    lev_wrap_var.units = 'm'
    time_wrap_var.units = 'day'
    psi_glo_wrap_var.units = 'Sv'
    psi_atl_wrap_var.units = 'Sv'

    lev_wrap_var.long_name = 'depth'
    lat_wrap_var.long_name = 'auxillary latitude'
    time_wrap_var.long_name = '5 day time'
    E_total_wrap_var.long_name = 'Oceanic meridional energy transport'
    psi_glo_wrap_var.long_name = 'Meridional overturning stream function of global ocean'
    psi_atl_wrap_var.long_name = 'Meridional overturning stream function of Atlantic ocean'
    # writing data
    #year_wrap_var[:] = period
    lat_wrap_var[:] = y_C
    #month_wrap_var[:] = np.arange(1,13,1)
    lev_wrap_var[:] = zt
    time_wrap_var[:] = np.arange(len(namelist))
    E_total_wrap_var[:] = meridional_E_zonal_int_pool
    psi_glo_wrap_var[:] = meridional_psi_zonal_glo
    psi_atl_wrap_var[:] = meridional_psi_zonal_atl
    # close the file
    data_wrap.close()
    print "Create netcdf file successfully"
    logging.info("The generation of netcdf files for the total meridional energy transport is complete!!")

if __name__=="__main__":
    print '*******************************************************************'
    print '******  Prepare all the constants and auxillary variables   *******'
    print '*******************************************************************'
    # create the year index
    #period = np.arange(start_year,end_year+1,1)
    namelist_month = ['01','02','03','04','05','06','07','08','09','10','11','12']
    #index_month = np.arange(12)
    #index_filename = len(namelist)
    # ORCA1_z42 info (Madec and Imbard 1996)
    ji = 1440
    jj = 1070
    level = 50
    # extract the mesh_mask and coordinate information
    grid_x_T, grid_y_T, grid_x_C, grid_y_C, x_T, y_T, x_C, y_C, zt, dz, area_T, e1t,\
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
                dz_adjust_t[counter_t,i,j] = np.sum(zt[0:counter_t]) - topo_depth_t[i,j]    # python start with 0, so i-1
            if mbathy_c[i,j] != 0:
                counter_c = int(mbathy_c[i,j] - 1)
                dz_adjust_c[counter_c,i,j] = np.sum(zt[0:counter_c]) - topo_depth_c[i,j]    # python start with 0, so i-1
    ####################################################################
    ###  Create space for stroing intermediate variables and outputs ###
    ####################################################################
    #create a data pool to save the OMET for each year and month
    E_pool_point = np.zeros((len(namelist),jj,ji),dtype = float)
    E_pool_zonal_int = np.zeros((len(namelist),jj),dtype = float)
    #E_pool_point_regrid = np.zeros((len(period),900,1440),dtype = float)
    # Meridional overturning stream function
    psi_pool_zonal_glo = np.zeros((len(namelist),level,jj),dtype = float) # for Globe
    psi_pool_zonal_atl = np.zeros((len(namelist),level,jj),dtype = float) # for Atlantic
    # loop for calculation
    for i in np.arange(len(namelist)):
        ####################################################################
        #########################  Extract variables #######################
        ####################################################################
        # get the key of each variable
        soda_key = var_key(datapath, namelist[i])
        ####################################################################
        ########  Calculate meridional overturning stream function #########
        ####################################################################
        # calculate the stokes stream function and plot
        psi_glo, psi_atl = stream_function(soda_key,e1c)
        psi_pool_zonal_glo[i,:,:] = psi_glo
        psi_pool_zonal_atl[i,:,:] = psi_atl
        ####################################################################
        ##############  Calculate meridional energy transport ##############
        ####################################################################
        # calculate the meridional energy transport in the ocean
        E_point = meridional_energy_transport(soda_key)
        E_pool_point[i,:,:] = E_point
        E_pool_zonal_int[i,:] = np.sum(E_point,1)
        # plot the stream function
        #visualization_stream_function(psi_pool_zonal_glo,psi_pool_zonal_atl)
        # create NetCDF file and save the output
    # plot the zonal int of all time
    zonal_int_plot(E_pool_zonal_int)
    create_netcdf_point(E_pool_point,output_path)
    create_netcdf_zonal_int(E_pool_zonal_int,psi_pool_zonal_glo,psi_pool_zonal_atl,output_path)

    print 'Computation of meridional energy transport on MOM5 grid for SODA3 is complete!!!'
    print 'The output is in sleep, safe and sound!!!'
    logging.info("The full pipeline of the quantification of meridional energy transport in the ocean is accomplished!")

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
