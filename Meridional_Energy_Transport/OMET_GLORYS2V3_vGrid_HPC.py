#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : Calculate Oceanic Meridional Energy Transport(GLORYS2V3) on HPC
Author          : Yang Liu
Date            : 2017.11.7
Last Update     : 2017.11.7
Description     : The code aims to calculate the oceanic meridional energy
                  transport based on oceanic reanalysis dataset GLORYS2V3 from
                  Mercator Ocean. The complete computaiton is accomplished
                  on model level (original ORCA025_z75 grid). All the interpolations
                  are made on the V grid. The procedure is generic and is able
                  to adapt any ocean reanalysis datasets, with some changes.
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
sys.stdout = open('/project/Reanalysis/GLORYS2V3/monthly/console_E.out','w')

# logging level 'DEBUG' 'INFO' 'WARNING' 'ERROR' 'CRITICAL'
#logging.basicConfig(filename = 'F:\DataBase\ORAS4\history.log', filemode = 'w',level = logging.DEBUG,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(filename = '/project/Reanalysis/GLORYS2V3/monthly/history_E.log',
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
    # land-sea mask
    tmask = mesh_mask_key.variables['tmask'][0,:,:,:]
    #umask = mesh_mask_key.variables['umask'][0,:,:,:]
    vmask = mesh_mask_key.variables['vmask'][0,:,:,:]
    # land-sea mask for sub-basin
    tmaskatl = subbasin_mesh_key.variables['tmaskatl'][:,1:-1] # attention that the size is different!
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
    # depth of partial cells
    e3t_ps = mesh_mask_key.variables['e3t_ps'][0,:,:]

    print "Retrieve the ORCA025 coordinate and mask info successfully!"
    logging.info('Finish retrieving the ORCA025 coordinate and mask info')

    return nav_lat, nav_lon, deptht, tmask, vmask, tmaskatl, e1t, e2t, e1v, e2v, gphiv, glamv, mbathy, e3t_0, e3t_ps


def stream_function(uv_key,e1v):
    '''
    This function is used to calculate the mass transport.
    The unit is Sv (1E+6 m3/s)
    '''
    print "Compute the meridional overturning stream function for globle and Atlantic!"
    logging.info('Compute the meridional overturning stream function for globle and Atlantic!')
    #dominant equation for stream function
    # psi = e1v(m) * rho(kg/m3) * v(m/s) * dz(m) = (kg/s)
    # extract variables
    #u = uv_key.variables['vozocrtx'][0,:,:,:]
    v = uv_key.variables['vomecrty'][0,:,:,:]
    # define the stream function psi
    psi_globe = np.zeros((level,jj,ji),dtype=float)
    psi_atlantic = np.zeros((level,jj,ji),dtype=float)
    # expand the grid size matrix e1v to avoid more loops
    e1v_3D = np.repeat(e1v[np.newaxis,:,:],level,0)
    # choose the integration order
    int_order = 1  # 1 - from sea bottom to sea surface 2 from sea surfaca to sea bottom
    if int_order == 1:
        # take the integral from sea botton to the surface
        # global meridional overturning stream function
        for i in (level - np.arange(level) -1 ):
            if i == level -1:
                psi_globe[i,:,:] = e1v_3D[i,:,:] * v[i,:,:] * vmask[i,:,:] * e3t_0[i] +\
                             e1v_3D[i,:,:] * v[i,:,:] * vmask[i,:,:] * e3t_adjust[i,:,:]
            else:
                psi_globe[i,:,:] = e1v_3D[i,:,:] * v[i,:,:] * vmask[i,:,:] * e3t_0[i] + psi_globe[i+1,:,:] +\
                             e1v_3D[i,:,:] * v[i,:,:] * vmask[i,:,:] * e3t_adjust[i,:,:]
        # Atlantic meridional overturning stream function
        for i in (level - np.arange(level) -1 ):
            if i == level -1:
                psi_atlantic[i,:,:] = e1v_3D[i,:,:] * v[i,:,:] * vmask[i,:,:] * tmaskatl * e3t_0[i] +\
                             e1v_3D[i,:,:] * v[i,:,:] * vmask[i,:,:] * tmaskatl * e3t_adjust[i,:,:]
            else:
                psi_atlantic[i,:,:] = e1v_3D[i,:,:] * v[i,:,:] * vmask[i,:,:] * tmaskatl * e3t_0[i] + psi_atlantic[i+1,:,:] +\
                             e1v_3D[i,:,:] * v[i,:,:] * vmask[i,:,:] * tmaskatl * e3t_adjust[i,:,:]
    elif int_order == 2:
        # take the integral from sea surface to the bottom
        for i in np.arange(level):
            if i == 0:
                psi_globe[i,:,:] = e1v_3D[i,:,:] * v[i,:,:] * vmask[i,:,:] * e3t_0[i]
            else:
                psi_globe[i,:,:] = e1v_3D[i,:,:] * v[i,:,:] * vmask[i,:,:] * e3t_0[i] + psi_globe[i-1,:,:]
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
    X , Y = np.meshgrid(gphiv[:,1060],deptht)
    contour_level = np.arange(-40,80,5)
    plt.contour(X,Y,psi_glo_mean,linewidth= 0.2)
    cs = plt.contourf(X,Y,psi_glo_mean,contour_level,linewidth= 0.2,cmap='RdYlGn')
    plt.title('Stokes Stream Function of Global Ocean')
    plt.xlabel("Laitude")
    plt.xticks(np.linspace(-90,90,13))
    plt.ylabel("Ocean Depth")
    cbar = plt.colorbar(orientation='horizontal')
    cbar.set_label('Transport of mass 1E+6 m3/s')
    #invert the y axis
    plt.gca().invert_yaxis()
    plt.show()
    fig0.savefig(output_path + os.sep + "OMET_GLORYS2V3_StreamFunction_Globe.png",dpi=500)

    # plot the Atlantic meridional overturning stream function
    fig1 = plt.figure()
    X , Y = np.meshgrid(gphiv[:,1060],deptht)
    contour_level = np.arange(-40,80,5)
    plt.contour(X,Y,psi_atl_mean,linewidth= 0.2)
    cs = plt.contourf(X,Y,psi_atl_mean,contour_level,linewidth= 0.2,cmap='RdYlGn')
    plt.title('Stokes Stream Function of Atlantic Ocean')
    plt.xlabel("Laitude")
    plt.xticks(np.linspace(-90,90,13))
    plt.ylabel("Ocean Depth")
    cbar = plt.colorbar(orientation='horizontal')
    cbar.set_label('Transport of mass 1E+6 m3/s')
    #invert the y axis
    plt.gca().invert_yaxis()
    plt.show()
    fig1.savefig(output_path + os.sep + "OMET_GLORYS2V3_StreamFunction_Atlantic.png",dpi=500)

    print "Export meridional overturning stream function for globle and Atlantic."
    logging.info('Export the meridional overturning stream function for globle and Atlantic.')

def meridional_energy_transport(theta_key, uv_key):
    '''
    This function is used to correct the mass budget.
    '''
    # extract variables
    print "Start extracting variables for the quantification of meridional energy transport."
    theta = theta_key.variables['votemper'][0,:,:,:] # the unit of theta is Celsius!
    #u = u_key.variables['vozocrtx'][0,:,:,:]
    v = uv_key.variables['vomecrty'][0,:,:,:]
    print 'Extracting variables successfully!'
    #logging.info("Extracting variables successfully!")
    # calculate the meridional velocity at T grid
    T_vgrid = np.zeros((level,jj,ji),dtype=float)
    # Interpolation of T on V grid through Nearest-Neighbor method
    for i in np.arange(jj):
        if i == jj-1:
            T_vgrid[:,i,:] = theta[:,i,:]
        else:
            T_vgrid[:,i,:] = (theta[:,i,:] + theta[:,i+1,:])/2
    # calculate heat flux at each grid point
    Internal_E_flux = np.zeros((level,jj,ji),dtype=float)
    partial = 1 # switch for the partial cells 1 = include & 0 = exclude
    for i in np.arange(level):
        if partial == 1: # include partial cells
            Internal_E_flux[i,:,:] = constant['rho'] * constant['cp'] * v[i,:,:] *\
                                     T_vgrid[i,:,:] * e1v * e3t_0[i] * vmask[i,:,:] +\
                                     constant['rho'] * constant['cp'] * v[i,:,:] *\
                                     T_vgrid[i,:,:] * e1v * e3t_adjust[i,:,:] * vmask[i,:,:]
        else: # exclude partial cells
            Internal_E_flux[i,:,:] = constant['rho'] * constant['cp'] * v[i,:,:] *\
                                     T_vgrid[i,:,:] * e1v * e3t_0[i] * vmask[i,:,:]
    # take the vertical integral
    Internal_E_int = np.zeros((jj,ji))
    Internal_E_int = np.sum(Internal_E_flux,0)/1e+12
    print '*****************************************************************************'
    print "**** Computation of meridional energy transport in the ocean is finished ****"
    print "************         The result is in tera-watt (1E+12)          ************"
    print '*****************************************************************************'
    return Internal_E_int

def zonal_int_plot(E_point_annual):
    # take the zonal means
    E_zonal_int_mean = np.mean(np.mean(E_point_annual,0)/1000,0)
    fig3 = plt.figure()
    plt.plot(gphiv[:,1060],E_zonal_int_mean)
    plt.xlabel("Latitude")
    plt.ylabel("Meridional Energy Transport (PW)")
    plt.show()
    fig3.savefig(output_path + os.sep + 'OMET_GLORYS2V3_1993_2014.png',dpi = 500)

def create_netcdf_point (meridional_E_point_pool,output_path):
    print '*******************************************************************'
    print '*********************** create netcdf file ************************'
    print '***********************    OMET on ORCA   *************************'
    print '*******************************************************************'
    logging.info("Start creating netcdf file for total meridional energy transport at each grid point.")
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path + os.sep + 'GLORYS2V3_model_monthly_orca025_E_point.nc' ,'w',format = 'NETCDF3_64BIT')
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
    lat_wrap_var.units = 'ORCA025_latitude'
    lon_wrap_var.units = 'ORCA025_longitude'
    E_total_wrap_var.units = 'tera watt'
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

def create_netcdf_zonal_int (meridional_E_zonal_int_pool, meridional_psi_zonal_glo, meridional_psi_zonal_atl,output_path):
    print '*******************************************************************'
    print '*********************** create netcdf file ************************'
    print '***********************    OMET on ORCA   *************************'
    print '*******************************************************************'
    logging.info("Start creating netcdf file for total meridional energy transport at each grid point.")
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path + os.sep + 'GLORYS2V3_model_monthly_orca025_E_zonal_int.nc' ,'w',format = 'NETCDF3_64BIT')
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
    E_total_wrap_var.long_name = 'oceanic meridional energy transport'
    psi_glo_wrap_var.units = 'Sv'
    psi_glo_wrap_var.long_name = 'Meridional overturning stream function of global ocean'
    psi_atl_wrap_var.units = 'Sv'
    psi_atl_wrap_var.long_name = 'Meridional overturning stream function of Atlantic ocean'
    # writing data
    year_wrap_var[:] = period
    lat_wrap_var[:] = gphiv[:,1060]
    month_wrap_var[:] = np.arange(1,13,1)
    lev_wrap_var[:] = deptht
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
    period = np.arange(start_year,end_year+1,1)
    namelist_month = ['01','02','03','04','05','06','07','08','09','10','11','12']
    index_month = np.arange(12)
    # ORCA1_z42 info (Madec and Imbard 1996)
    ji = 1440
    jj = 1021
    level = 75
    # extract the mesh_mask and coordinate information
    nav_lat, nav_lon, deptht, tmask, vmask, tmaskatl, e1t, e2t, e1v, e2v, gphiv,\
    glamv, mbathy, e3t_0, e3t_ps = var_coordinate(datapath)
    print '*******************************************************************'
    print '*******************  Partial cells correction   *******************'
    print '*******************************************************************'
    # construct partial depth matrix
    # include the partial cell to the layers above, due to the presence of variabels (t,u,v)
    e3t_adjust = np.zeros((level,jj,ji),dtype = float)
    for i in np.arange(1,level,1):
        for j in np.arange(jj):
            for k in np.arange(ji):
                if i == mbathy[j,k]:
                    e3t_adjust[i-1,j,k] = e3t_ps[j,k]
    ####################################################################
    ###  Create space for stroing intermediate variables and outputs ###
    ####################################################################
    #create a data pool to save the OMET for each year and month
    E_pool_point = np.zeros((len(period),12,jj,ji),dtype = float)
    E_pool_zonal_int = np.zeros((len(period),12,jj),dtype = float)
    #E_pool_point_regrid = np.zeros((len(period),900,1440),dtype = float)
    # Meridional overturning stream function
    psi_pool_zonal_glo = np.zeros((len(period),12,level,jj),dtype = float) # for Globe
    psi_pool_zonal_atl = np.zeros((len(period),12,level,jj),dtype = float) # for Atlantic
    # loop for calculation
    for i in period:
        for j in index_month:
            ####################################################################
            #########################  Extract variables #######################
            ####################################################################
            # get the key of each variable
            theta_key, uv_key = var_key(datapath, i, j)
            ####################################################################
            ########  Calculate meridional overturning stream function #########
            ####################################################################
            # calculate the stokes stream function and plot
            psi_glo, psi_atl = stream_function(uv_key,e1v)
            psi_pool_zonal_glo[i-1993,j,:,:] = psi_glo
            psi_pool_zonal_atl[i-1993,j,:,:] = psi_atl
            ####################################################################
            ##############  Calculate meridional energy transport ##############
            ####################################################################
            # calculate the meridional energy transport in the ocean
            E_point = meridional_energy_transport(theta_key, uv_key)
            E_pool_point[i-1993,j,:,:] = E_point
            E_pool_zonal_int[i-1993,j,:] = np.sum(E_point,1)
    # plot the zonal int of all time
    zonal_int_plot(E_pool_zonal_int)
    # plot the stream function
    visualization_stream_function(psi_pool_zonal_glo,psi_pool_zonal_atl)
    # create NetCDF file and save the output
    create_netcdf_point(E_pool_point,output_path)
    create_netcdf_zonal_int(E_pool_zonal_int,psi_pool_zonal_glo,psi_pool_zonal_atl,output_path)

    print 'Computation of meridional energy transport on ORCA grid for GLORYS2V3 is complete!!!'
    print 'The output is in sleep, safe and sound!!!'
    logging.info("The full pipeline of the quantification of meridional energy transport in the ocean is accomplished!")

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
