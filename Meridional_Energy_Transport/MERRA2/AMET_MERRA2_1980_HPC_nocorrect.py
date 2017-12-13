#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : Quantify atmospheric meridional energy transport without mass correction(MERRA2)(HPC-cloud customised)
Author          : Yang Liu
Date            : 2017.10.17
Last Update     : 2017.11.9
Description     : The code aims to calculate the atmospheric meridional energy
                  transport based on atmospheric reanalysis dataset MERRA II
                  from NASA. The complete procedure includes the calculation of
                  geopotential on model levels.
                  The procedure is generic and is able to adapt any atmospheric
                  reanalysis datasets, with some changes.
Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, sys, matplotlib
variables       : Absolute Temperature              T         [K]
                  Specific Humidity                 q         [kg/kg]
                  Surface Pressure                  ps        [Pa]
                  Zonal Divergent Wind              u         [m/s]
                  Meridional Divergent Wind         v         [m/s]
		          Surface geopotential  	        z         [m2/s2]
Caveat!!	: The dataset is a testing dataset containing the globe in 1980.
		  Attention should be paid when calculating the meridional grid length (dy)!
                  Direction of Axis:
              	  Model Level: surface to TOA
                  Latitude: South to Nouth (-90 to 90)
                  Lontitude: West to East (-180 to 180)
                  Time: 00:00 03:00 06:00 09:00 12:00 15:00 18:00 21:00 (3 hourly)
"""
import numpy as np
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

##########################################################################
###########################   Units vacabulory   #########################

# cpT:  [J / kg K] * [K]     = [J / kg]
# Lvq:  [J / kg] * [kg / kg] = [J / kg]
# gz in [m2 / s2] = [ kg m2 / kg s2 ] = [J / kg]

# multiply by v: [J / kg] * [m / s] => [J m / kg s]
# sum over longitudes [J m / kg s] * [ m ] = [J m2 / kg s]

# integrate over pressure: dp: [Pa] = [N m-2] = [kg m2 s-2 m-2] = [kg s-2]
# [J m2 / kg s] * [Pa] = [J m2 / kg s] * [kg / s2] = [J m2 / s3]
# and factor 1/g: [J m2 / s3] * [s2 /m2] = [J / s] = [Wat]
##########################################################################

# print the system structure and the path of the kernal
print platform.architecture()
print os.path

# calculate the time for the code execution
start_time = tttt.time()

# Redirect all the console output to a file
#sys.stdout = open('F:\DataBase\ERA_Interim\console.out','w')
sys.stdout = open('/project/Reanalysis/MERRA2/Subdaily/Model/console_E.out','w')

# logging level 'DEBUG' 'INFO' 'WARNING' 'ERROR' 'CRITICAL'
#logging.basicConfig(filename = 'F:\DataBase\ERA_Interim\history.log', filemode = 'w',level = logging.DEBUG,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(filename = '/project/Reanalysis/MERRA2/Subdaily/Model/history_E.log',
                    filemode = 'w', level = logging.DEBUG,
                    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# define the constant:
constant ={'g' : 9.80616,      # gravititional acceleration [m / s2]
           'R' : 6371009,      # radius of the earth [m]
           'cp': 1004.64,      # heat capacity of air [J/(Kg*K)]
           'Lv': 2264670,      # Latent heat of vaporization [J/Kg]
           'R_dry' : 286.9,    # gas constant of dry air [J/(kg*K)]
           'R_vap' : 461.5,    # gas constant for water vapour [J/(kg*K)]
            }

# A and B values for the definition of sigma levelist
# Since there are 72 model levels, there are 73 half levels, so it is for A and B values
# the unit of A is hPa!!!!!!!!!!!!
# from surface to TOA
A = np.array([
      0.000000e+00, 4.804826e-02, 6.593752e+00, 1.313480e+01, 1.961311e+01, 2.609201e+01,
      3.257081e+01, 3.898201e+01, 4.533901e+01, 5.169611e+01, 5.805321e+01, 6.436264e+01,
      7.062198e+01, 7.883422e+01, 8.909992e+01, 9.936521e+01, 1.091817e+02, 1.189586e+02,
      1.286959e+02, 1.429100e+02, 1.562600e+02, 1.696090e+02, 1.816190e+02, 1.930970e+02,
      2.032590e+02, 2.121500e+02, 2.187760e+02, 2.238980e+02, 2.243630e+02, 2.168650e+02,
      2.011920e+02, 1.769300e+02, 1.503930e+02, 1.278370e+02, 1.086630e+02, 9.236572e+01,
      7.851231e+01, 6.660341e+01, 5.638791e+01, 4.764391e+01, 4.017541e+01, 3.381001e+01,
      2.836781e+01, 2.373041e+01, 1.979160e+01, 1.645710e+01, 1.364340e+01, 1.127690e+01,
      9.292942e+00, 7.619842e+00, 6.216801e+00, 5.046801e+00, 4.076571e+00, 3.276431e+00,
      2.620211e+00, 2.084970e+00, 1.650790e+00, 1.300510e+00, 1.019440e+00, 7.951341e-01,
      6.167791e-01, 4.758061e-01, 3.650411e-01, 2.785261e-01, 2.113490e-01, 1.594950e-01,
      1.197030e-01, 8.934502e-02, 6.600001e-02, 4.758501e-02, 3.270000e-02, 2.000000e-02,
      1.000000e-02,],dtype=float)
# reverse A
A = A[::-1]
# the unit of B is 1!!!!!!!!!!!!
# from surfac eto TOA
B = np.array([
      1.000000e+00, 9.849520e-01, 9.634060e-01, 9.418650e-01, 9.203870e-01, 8.989080e-01,
      8.774290e-01, 8.560180e-01, 8.346609e-01, 8.133039e-01, 7.919469e-01, 7.706375e-01,
      7.493782e-01, 7.211660e-01, 6.858999e-01, 6.506349e-01, 6.158184e-01, 5.810415e-01,
      5.463042e-01, 4.945902e-01, 4.437402e-01, 3.928911e-01, 3.433811e-01, 2.944031e-01,
      2.467411e-01, 2.003501e-01, 1.562241e-01, 1.136021e-01, 6.372006e-02, 2.801004e-02,
      6.960025e-03, 8.175413e-09, 0.000000e+00, 0.000000e+00, 0.000000e+00, 0.000000e+00,
      0.000000e+00, 0.000000e+00, 0.000000e+00, 0.000000e+00, 0.000000e+00, 0.000000e+00,
      0.000000e+00, 0.000000e+00, 0.000000e+00, 0.000000e+00, 0.000000e+00, 0.000000e+00,
      0.000000e+00, 0.000000e+00, 0.000000e+00, 0.000000e+00, 0.000000e+00, 0.000000e+00,
      0.000000e+00, 0.000000e+00, 0.000000e+00, 0.000000e+00, 0.000000e+00, 0.000000e+00,
      0.000000e+00, 0.000000e+00, 0.000000e+00, 0.000000e+00, 0.000000e+00, 0.000000e+00,
      0.000000e+00, 0.000000e+00, 0.000000e+00, 0.000000e+00, 0.000000e+00, 0.000000e+00,
      0.000000e+00,],dtype=float)
# reverse B
B = B[::-1]

################################   Input zone  ######################################
# specify data path
#datapath = 'F:\DataBase\ERA_Interim\Subdaily'
datapath = '/project/Reanalysis/MERRA2/Subdaily/Model'
# time of the data, which concerns with the name of input
# starting time (year)
start_year = 1980
# Ending time, if only for 1 year, then it should be the same as starting year
end_year = 1980
# specify output path for the netCDF4 file
#output_path = 'F:\DataBase\ERA_Interim\Subdaily'
output_path = '/project/Reanalysis/MERRA2/Subdaily/Model'
# benchmark datasets for basic dimensions
benchmark_path = '/project/Reanalysis/MERRA2/Subdaily/Model/merra1980/MERRA2_100.inst3_3d_asm_Nv.19801221.SUB.nc4'
benchmark = Dataset(benchmark_path)
####################################################################################

def var_key_retrieve(datapath, year, month, day):
    '''
    This module extracts the variables for mass correction and the computation of AMET.
    Due to the strcture of the dataset (MEERA2), the processing unit is daily data.
    '''
    # get the path to each datasets
    print "Start retrieving datasets %d (y) - %s (m) - %s (d)" % (year,namelist_month[month-1],namelist_day[day])
    logging.info("Start retrieving variables T,q,u,v,sp,z for from %d (y) - %s (m) - %s (d) " % (year,namelist_month[month-1],namelist_day[day]))
    datapath_var = datapath + os.sep + 'merra%d' % (year) + os.sep + 'MERRA2_100.inst3_3d_asm_Nv.%d%s%s.SUB.nc4' % (year,namelist_month[month-1],namelist_day[day])
    # get the variable keys
    var_key = Dataset(datapath_var)
    # The shape of each variable is (8,72,361,576)
    print "Retrieving datasets successfully and return the variable key!"
    logging.info("Retrieving variables for from %d (y) - %s (m) - %s (d) successfully!" % (year,namelist_month[month-1],namelist_day[day]))
    return var_key


def calc_geopotential(var_key):
    '''
    This module aims to calculate the geopotential based on surface geopotential.
    The procedure and relevant equations can be found in ECMWF IFS 9220.
    See equation 2.20 - 2.23 .
    '''
    # extract variables
    print "Start extracting variables for the calculation of geopotential on model level."
    T = var_key.variables['T'][:]
    q = var_key.variables['QV'][:]
    ps = var_key.variables['PS'][:]
    z = var_key.variables['PHIS'][:]
    print 'Extracting variables successfully!'
    logging.info("Extracting variables successfully!")
    print 'Start calculating geopotential on model level'
    # calculate the surface pressure
    # the unit of pressure here is Pa!!!
    # define the half level pressure matrix
    p_half_plus = np.zeros((len(time),len(level),len(latitude),len(longitude)),dtype = float)
    p_half_minus = np.zeros((len(time),len(level),len(latitude),len(longitude)),dtype = float)
    # calculate the index of pressure levels
    index_level = np.arange(len(level))
    # calculate the pressure at each half level
    for i in index_level:
        p_half_plus[:,i,:,:] = A[i+1]*100 + B[i+1] * ps
        p_half_minus[:,i,:,:] = A[i]*100 + B[i] * ps
    # calculate full pressure level
    #level_full = (p_half_plus + p_half_minus) / 2
    # compute the moist temperature (virtual temperature)
    Tv = T * (1 + (constant['R_vap'] / constant['R_dry'] - 1) * q)
    # initialize the first half level geopotential
    gz_half = np.zeros((len(time),len(latitude),len(longitude)),dtype =float)
    # initialize the full level geopotential
    gz = np.zeros((len(time),len(level),len(latitude),len(longitude)),dtype = float)
    # Calculate the geopotential at each level
    # The integral should be taken from surface level to the TOA
    for i in index_level:
        # reverse the index to make it from surface to the TOA
        i_inverse = len(level) -1 - i
        # the ln(p_plus/p_minus) is calculated, alpha is defined
        # an exception lies in the TOA
        # see equation 2.23 in ECMWF IFS 9220
        if i_inverse == 0:
            ln_p = np.log(p_half_plus[:,i_inverse,:,:]/10)
            alpha = np.log(2)
        else:
            ln_p = np.log(p_half_plus[:,i_inverse,:,:]/p_half_minus[:,i_inverse,:,:])
            delta_p = p_half_plus[:,i_inverse,:,:] - p_half_minus[:,i_inverse,:,:]
            alpha = 1 - p_half_minus[:,i_inverse,:,:] / delta_p * ln_p
        # calculate the geopotential of the full level (exclude surface geopotential)
        # see equation 2.22 in ECMWF IFS 9220
        gz_full = gz_half + alpha * constant['R_dry'] * Tv[:,i_inverse,:,:]
        # add surface geopotential to the full level
        # see equation 2.21 in ECMWF IFS 9220
        gz[:,i_inverse,:,:] = z + gz_full
        # renew the half level geopotential for next loop step (from p_half_minus level to p_half_plus level)
        # see equation 2.20 in ECMWF IFS 9220
        gz_half = gz_half + ln_p * constant['R_dry'] * Tv[:,i_inverse,:,:]
    print '*******************************************************************'
    print "***Computation of geopotential on each pressure level is finished**"
    print '*******************************************************************'
    logging.info("Computation of geopotential on model level is finished!")

    return gz

def meridional_energy_transport(var_key, gz):
    '''
    This module calculate the energy flux which are the componets of meridional
    energy transport in the atmosphere.
    These include:
    internal energy flux
    latent heat flux
    geoptential heat flux
    kinetic energy flux
    '''
    # extract variables
    print "Start extracting variables for the quantification of meridional energy transport."
    T = var_key.variables['T'][:]
    q = var_key.variables['QV'][:]
    ps = var_key.variables['PS'][:]
    u = var_key.variables['U'][:]
    v = var_key.variables['V'][:]
    print 'Extracting variables successfully!'
    logging.info("Extracting variables successfully!")

    print 'Start calculating meridional energy transport on model level'
    # calculate dp based on mean value of surface pressure
    dp_level = np.zeros((len(time),len(level),len(latitude),len(longitude)),dtype = float)
    # calculate the index of pressure levels
    index_level = np.arange(len(level))
    for i in index_level:
        dp_level[:,i,:,:] = (A[i+1]*100 + B[i+1] * ps) - (A[i]*100 + B[i] * ps)
    # calculate each component of total energy
    # take the vertical integral
    # mass correction component
    # Internal Energy cpT
    internal_flux = constant['cp'] * v * T * dp_level / constant['g']
    internal_flux_int = np.mean(np.sum(internal_flux,1),0)
    # Latent heat Lq
    latent_flux = constant['Lv'] * v * q * dp_level / constant['g']
    latent_flux_int = np.mean(np.sum(latent_flux,1),0)
    # geopotential gz
    geopotential_flux = v * gz * dp_level / constant['g']
    geopotential_flux_int = np.mean(np.sum(geopotential_flux,1),0)
    # kinetic energy
    kinetic_flux = v * 1/2 *(u**2 + v**2) * dp_level / constant['g']
    kinetic_flux_int = np.mean(np.sum(kinetic_flux,1),0)

    print 'Complete calculating meridional energy transport on model level'

    return internal_flux_int, latent_flux_int, geopotential_flux_int, kinetic_flux_int


# make plots
def visualization(E_total,E_internal,E_latent,E_geopotential,E_kinetic,output_path,year):
    print "Start making plots for the total meridional energy transport and each component."
    logging.info("Start making plots for the total meridional energy transport and each component.")
    # calculate monthly mean of total energy transport
    # unit change from tera to peta (from 1E+12 to 1E+15)
    E_total_monthly_mean = np.mean(E_total,0)/1000
    E_internal_monthly_mean = np.mean(E_internal,0)/1000
    E_latent_monthly_mean = np.mean(E_latent,0)/1000
    E_geopotential_monthly_mean = np.mean(E_geopotential,0)/1000
    E_kinetic_monthly_mean = np.mean(E_kinetic,0)/1000
    # Plot the total meridional energy transport against the latitude
    fig1 = plt.figure()
    plt.plot(latitude,E_total_monthly_mean,'b-',label='MERRA2')
    plt.axhline(y=0, color='r',ls='--')
    #plt.hold()
    plt.title('Total Atmospheric Meridional Energy Transport %d' % (year))
    #plt.legend()
    plt.xlabel("Laitude")
    plt.xticks(np.linspace(-90,90,13))
    #plt.yticks(np.linspace(0,6,7))
    plt.ylabel("Meridional Energy Transport (PW)")
    #plt.show()
    fig1.savefig(output_path + os.sep + 'merra%d' % (year) + os.sep + 'output' + os.sep + 'AMET_MERRA2_total_%d.png' % (year), dpi = 400)

    # Plot the meridional internal energy transport against the latitude
    fig2 = plt.figure()
    plt.plot(latitude,E_internal_monthly_mean,'b-',label='MERRA2')
    plt.axhline(y=0, color='r',ls='--')
    #plt.hold()
    plt.title('Atmospheric Meridional Internal Energy Transport %d' % (year))
    #plt.legend()
    plt.xlabel("Laitude")
    plt.xticks(np.linspace(-90,90,13))
    #plt.yticks(np.linspace(0,6,7))
    plt.ylabel("Meridional Energy Transport (PW)")
    #plt.show()
    fig2.savefig(output_path + os.sep + 'merra%d' % (year) + os.sep + 'output' + os.sep + 'AMET_MERRA2_internal_%d.png' % (year), dpi = 400)

    # Plot the meridional latent energy transport against the latitude
    fig3 = plt.figure()
    plt.plot(latitude,E_latent_monthly_mean,'b-',label='MERRA2')
    plt.axhline(y=0, color='r',ls='--')
    #plt.hold()
    plt.title('Atmospheric Meridional Latent Energy Transport %d' % (year))
    #plt.legend()
    plt.xlabel("Laitude")
    plt.xticks(np.linspace(-90,90,13))
    #plt.yticks(np.linspace(0,2,5))
    plt.ylabel("Meridional Energy Transport (PW)")
    #plt.show()
    fig3.savefig(output_path + os.sep + 'merra%d' % (year) + os.sep + 'output' + os.sep + 'AMET_MERRA2_latent_%d.png' % (year), dpi = 400)

    # Plot the meridional geopotential energy transport against the latitude
    fig4 = plt.figure()
    plt.plot(latitude,E_geopotential_monthly_mean,'b-',label='MERRA2')
    plt.axhline(y=0, color='r',ls='--')
    #plt.hold()
    plt.title('Atmospheric Meridional Geopotential Energy Transport %d' % (year))
    #plt.legend()
    plt.xlabel("Laitude")
    plt.xticks(np.linspace(-90,90,13))
    #plt.yticks(np.linspace(-2.5,2.0,10))
    plt.ylabel("Meridional Energy Transport (PW)")
    #plt.show()
    fig4.savefig(output_path + os.sep + 'merra%d' % (year) + os.sep + 'output' + os.sep + 'AMET_MERRA2_geopotential_%d.png' % (year), dpi = 400)

    # Plot the meridional kinetic energy transport against the latitude
    fig5 = plt.figure()
    plt.plot(latitude,E_kinetic_monthly_mean,'b-',label='MERRA2')
    plt.axhline(y=0, color='r',ls='--')
    #plt.hold()
    plt.title('Atmospheric Meridional Kinetic Energy Transport %d' % (year))
    #plt.legend()
    plt.xlabel("Laitude")
    plt.xticks(np.linspace(-90,90,13))
    #plt.yticks(np.linspace(0,0.15,6))
    plt.ylabel("Meridional Energy Transport (PW)")
    #plt.show()
    fig5.savefig(output_path + os.sep + 'merra%d' % (year) + os.sep + 'output' + os.sep + 'AMET_MERRA2_kinetic_%d.png' % (year), dpi = 400)
    logging.info("The generation of plots for the total meridional energy transport and each component is complete!")

# save output datasets
def create_netcdf_point (meridional_E_point_pool,meridional_E_internal_point_pool,
                         meridional_E_latent_point_pool,meridional_E_geopotential_point_pool,
                         meridional_E_kinetic_point_pool,output_path,year):
    print '*******************************************************************'
    print '*********************** create netcdf file*************************'
    print '*******************************************************************'
    logging.info("Start creating netcdf file for total meridional energy transport and each component at each grid point.")
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path+os.sep+'merra%d' % (year) + os.sep + 'output' + os.sep + 'AMET_MERRA2_model_daily_%d_E_point.nc' % (year),'w',format = 'NETCDF3_64BIT')
    # create dimensions for netcdf data
    month_wrap_dim = data_wrap.createDimension('month',Dim_month)
    lat_wrap_dim = data_wrap.createDimension('latitude',Dim_latitude)
    lon_wrap_dim = data_wrap.createDimension('longitude',Dim_longitude)
    # create coordinate variables for 3-dimensions
    month_warp_var = data_wrap.createVariable('month',np.int32,('month',))
    lat_warp_var = data_wrap.createVariable('latitude',np.float32,('latitude',))
    lon_warp_var = data_wrap.createVariable('longitude',np.float32,('longitude',))

    E_total_wrap_var = data_wrap.createVariable('E',np.float64,('month','latitude','longitude'))
    E_internal_wrap_var = data_wrap.createVariable('E_cpT',np.float64,('month','latitude','longitude'))
    E_latent_wrap_var = data_wrap.createVariable('E_Lvq',np.float64,('month','latitude','longitude'))
    E_geopotential_wrap_var = data_wrap.createVariable('E_gz',np.float64,('month','latitude','longitude'))
    E_kinetic_wrap_var = data_wrap.createVariable('E_uv2',np.float64,('month','latitude','longitude'))
    # global attributes
    data_wrap.description = 'Monthly mean meridional energy transport and each component at each grid point'
    # variable attributes
    lat_warp_var.units = 'degree_north'
    lon_warp_var.units = 'degree_east'
    E_total_wrap_var.units = 'tera watt'
    E_internal_wrap_var.units = 'tera watt'
    E_latent_wrap_var.units = 'tera watt'
    E_geopotential_wrap_var.units = 'tera watt'
    E_kinetic_wrap_var.units = 'tera watt'

    E_total_wrap_var.long_name = 'atmospheric meridional energy transport'
    E_internal_wrap_var.long_name = 'atmospheric meridional internal energy transport'
    E_latent_wrap_var.long_name = 'atmospheric meridional latent heat transport'
    E_geopotential_wrap_var.long_name = 'atmospheric meridional geopotential transport'
    E_kinetic_wrap_var.long_name = 'atmospheric meridional kinetic energy transport'
    # writing data
    lat_warp_var[:] = latitude
    lon_warp_var[:] = longitude
    month_warp_var[:] = index_month
    E_total_wrap_var[:] = meridional_E_point_pool
    E_internal_wrap_var[:] = meridional_E_internal_point_pool
    E_latent_wrap_var[:] = meridional_E_latent_point_pool
    E_geopotential_wrap_var[:] = meridional_E_geopotential_point_pool
    E_kinetic_wrap_var[:] = meridional_E_kinetic_point_pool
    # close the file
    data_wrap.close()
    print "Create netcdf file successfully"
    logging.info("The generation of netcdf files for the total meridional energy transport and each component on each grid point is complete!!")

# save output datasets
def create_netcdf_zonal_int (meridional_E_pool, meridional_E_internal_pool, meridional_E_latent_pool,
                             meridional_E_geopotential_pool, meridional_E_kinetic_pool, output_path, year):
    print '*******************************************************************'
    print '*********************** create netcdf file*************************'
    print '*******************************************************************'
    logging.info("Start creating netcdf files for the zonal integral of total meridional energy transport and each component.")
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path+os.sep+'merra%d' % (year) + os.sep + 'output' + os.sep + 'AMET_MERRA2_model_daily_%d_E_zonal_int.nc' % (year),'w',format = 'NETCDF3_64BIT')
    # create dimensions for netcdf data
    month_wrap_dim = data_wrap.createDimension('month',Dim_month)
    lat_wrap_dim = data_wrap.createDimension('latitude',Dim_latitude)
    # create coordinate variables for 3-dimensions
    month_warp_var = data_wrap.createVariable('month',np.int32,('month',))
    lat_warp_var = data_wrap.createVariable('latitude',np.float32,('latitude',))
    # create the actual 3-d variable
    E_total_wrap_var = data_wrap.createVariable('E',np.float64,('month','latitude'))
    E_internal_wrap_var = data_wrap.createVariable('E_cpT',np.float64,('month','latitude'))
    E_latent_wrap_var = data_wrap.createVariable('E_Lvq',np.float64,('month','latitude'))
    E_geopotential_wrap_var = data_wrap.createVariable('E_gz',np.float64,('month','latitude'))
    E_kinetic_wrap_var = data_wrap.createVariable('E_uv2',np.float64,('month','latitude'))
    # global attributes
    data_wrap.description = 'Monthly mean zonal integral of meridional energy transport and each component'
    # variable attributes
    lat_warp_var.units = 'degree_north'
    E_total_wrap_var.units = 'tera watt'
    E_internal_wrap_var.units = 'tera watt'
    E_latent_wrap_var.units = 'tera watt'
    E_geopotential_wrap_var.units = 'tera watt'
    E_kinetic_wrap_var.units = 'tera watt'
    E_total_wrap_var.long_name = 'atmospheric meridional energy transport'
    E_internal_wrap_var.long_name = 'atmospheric meridional internal energy transport'
    E_latent_wrap_var.long_name = 'atmospheric meridional latent heat transport'
    E_geopotential_wrap_var.long_name = 'atmospheric meridional geopotential transport'
    E_kinetic_wrap_var.long_name = 'atmospheric meridional kinetic energy transport'
    # writing data
    lat_warp_var[:] = latitude
    month_warp_var[:] = index_month
    E_total_wrap_var[:] = meridional_E_pool
    E_internal_wrap_var[:] = meridional_E_internal_pool
    E_latent_wrap_var[:] = meridional_E_latent_pool
    E_geopotential_wrap_var[:] = meridional_E_geopotential_pool
    E_kinetic_wrap_var[:] = meridional_E_kinetic_pool
    # close the file
    data_wrap.close()
    print "Create netcdf file successfully"
    logging.info("The generation of netcdf files for the zonal integral of total meridional energy transport and each component is complete!!")

if __name__=="__main__":
    ####################################################################
    ######  Create time namelist matrix for variable extraction  #######
    ####################################################################
    # date and time arrangement
    # namelist of month and days for file manipulation
    namelist_month = ['01','02','03','04','05','06','07','08','09','10','11','12']
    namelist_day = ['01','02','03','04','05','06','07','08','09','10',
                    '11','12','13','14','15','16','17','18','19','20',
                    '21','22','23','24','25','26','27','28','29','30',
                    '31']
    # index of months
    period = np.arange(start_year,end_year+1,1)
    index_month = np.arange(1,13,1)
    index_days_long = np.arange(31)
    index_days_short = np.arange(30)
    index_days_Feb_short = np.arange(28)
    index_days_Feb_long = np.arange(29)
    long_month_list = np.array([1,3,5,7,8,10,12])
    leap_year_list = np.array([1976,1980,1984,1988,1992,1996,2000,2004,2008,2012,2016,2020])
    ####################################################################
    ######       Extract invariant and calculate constants       #######
    ####################################################################
    # get invariant from benchmark file
    time = benchmark.variables['time'][:] # only for measuring length
    level = benchmark.variables['lev'][:]
    latitude = benchmark.variables['lat'][:]
    longitude = benchmark.variables['lon'][:]
    # create dimensions for saving data
    Dim_level = len(level)
    Dim_latitude = len(latitude)
    Dim_longitude = len(longitude)
    Dim_month = len(index_month)
    #Dim_year = len(period)
    # calculate zonal & meridional grid size on earth
    # the earth is taken as a perfect sphere, instead of a ellopsoid
    dx = 2 * np.pi * constant['R'] * np.cos(2 * np.pi * latitude / 360) / len(longitude)
    dy = np.pi * constant['R'] / 361
    ####################################################################
    ###  Create space for stroing intermediate variables and outputs ###
    ####################################################################
    # data pool for zonal integral
    meridional_E_pool = np.zeros((Dim_month,Dim_latitude),dtype = float)
    meridional_E_internal_pool = np.zeros((Dim_month,Dim_latitude),dtype = float)
    meridional_E_latent_pool = np.zeros((Dim_month,Dim_latitude),dtype = float)
    meridional_E_geopotential_pool = np.zeros((Dim_month,Dim_latitude),dtype = float)
    meridional_E_kinetic_pool = np.zeros((Dim_month,Dim_latitude),dtype = float)
    # data pool for grid point values
    meridional_E_point_pool = np.zeros((Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    meridional_E_internal_point_pool = np.zeros((Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    meridional_E_latent_point_pool = np.zeros((Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    meridional_E_geopotential_point_pool = np.zeros((Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    meridional_E_kinetic_point_pool = np.zeros((Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    # loop for calculation
    for i in period:
        for j in index_month:
            # determine how many days are there in a month
            if j in long_month_list:
                days = index_days_long
            elif j == 2:
                if i in leap_year_list:
                    days = index_days_Feb_long
                else:
                    days = index_days_Feb_short
            else:
                days = index_days_short
            ####################################################################
            ###  Create space for stroing intermediate variables and outputs ###
            ####################################################################
            # data pool for meridional energy tansport module
            pool_internal_flux_int = np.zeros((len(days),len(latitude),len(longitude)),dtype=float)
            pool_latent_flux_int = np.zeros((len(days),len(latitude),len(longitude)),dtype=float)
            pool_geopotential_flux_int = np.zeros((len(days),len(latitude),len(longitude)),dtype=float)
            pool_kinetic_flux_int = np.zeros((len(days),len(latitude),len(longitude)),dtype=float)
            # days loop
            for k in days:
                # get the key of each variable
                var_key = var_key_retrieve(datapath,i,j,k)
                ####################################################################
                ######                       Geopotential                    #######
                ####################################################################
                # calculate the geopotential
                gz = calc_geopotential(var_key)
                ####################################################################
                ######               Meridional Energy Transport             #######
                ####################################################################
                # calculate the energy flux terms in meridional energy Transport
                internal_flux_int, latent_flux_int, geopotential_flux_int, kinetic_flux_int = meridional_energy_transport(var_key,gz)
                # save the divergence terms to the warehouse
                pool_internal_flux_int[k,:,:] = internal_flux_int
                pool_latent_flux_int[k,:,:] = latent_flux_int
                pool_geopotential_flux_int[k,:,:] = geopotential_flux_int
                pool_kinetic_flux_int[k,:,:] = kinetic_flux_int
            ####################################################################
            # calculate the total meridional energy transport and each component respectively
            # energy on grid point
            meridional_E_internal_point = np.zeros((len(latitude),len(longitude)),dtype=float)
            meridional_E_latent_point = np.zeros((len(latitude),len(longitude)),dtype=float)
            meridional_E_geopotential_point = np.zeros((len(latitude),len(longitude)),dtype=float)
            meridional_E_kinetic_point = np.zeros((len(latitude),len(longitude)),dtype=float)
            meridional_E_point = np.zeros((len(latitude),len(longitude)),dtype=float)
            for c in np.arange(len(latitude)):
                meridional_E_internal_point[c,:] = np.mean(pool_internal_flux_int[:,c,:],0) * dx[c]/1e+12
                meridional_E_latent_point[c,:] = np.mean(pool_latent_flux_int[:,c,:],0) * dx[c]/1e+12
                meridional_E_geopotential_point[c,:] = np.mean(pool_geopotential_flux_int[:,c,:],0) * dx[c]/1e+12
                meridional_E_kinetic_point[c,:] = np.mean(pool_kinetic_flux_int[:,c,:],0) * dx[c]/1e+12
            # total energy transport
            meridional_E_point = meridional_E_internal_point + meridional_E_latent_point + meridional_E_geopotential_point + meridional_E_kinetic_point
            # zonal integral of energy
            meridional_E_internal = np.sum(meridional_E_internal_point,1)
            meridional_E_latent = np.sum(meridional_E_latent_point,1)
            meridional_E_geopotential = np.sum(meridional_E_geopotential_point,1)
            meridional_E_kinetic = np.sum(meridional_E_kinetic_point,1)
            # total energy transport
            meridional_E = meridional_E_internal + meridional_E_latent + meridional_E_geopotential + meridional_E_kinetic
            print '*****************************************************************************'
            print "***Computation of meridional energy transport in the atmosphere is finished**"
            print "************         The result is in tera-watt (1E+12)          ************"
            print '*****************************************************************************'
            logging.info("Computation of meridional energy transport on model level is finished!")
            ####################################################################
            ######                 Data Wrapping (NetCDF)                #######
            ####################################################################
            # save the total meridional energy and each component to the data pool
            meridional_E_pool[j-1,:] = meridional_E
            meridional_E_internal_pool[j-1,:] = meridional_E_internal
            meridional_E_latent_pool[j-1,:] = meridional_E_latent
            meridional_E_geopotential_pool[j-1,:] = meridional_E_geopotential
            meridional_E_kinetic_pool[j-1,:] = meridional_E_kinetic
            # save the meridional energy on each grid point to the data pool
            meridional_E_point_pool[j-1,:,:] = meridional_E_point
            meridional_E_internal_point_pool[j-1,:,:] = meridional_E_internal_point
            meridional_E_latent_point_pool[j-1,:,:] = meridional_E_latent_point
            meridional_E_geopotential_point_pool[j-1,:,:] = meridional_E_geopotential_point
            meridional_E_kinetic_point_pool[j-1,:,:] = meridional_E_kinetic_point
        # make plots for monthly means
        visualization(meridional_E_pool,meridional_E_internal_pool,meridional_E_latent_pool,
                      meridional_E_geopotential_pool,meridional_E_kinetic_pool,output_path,i)
        # save data as netcdf file
        create_netcdf_zonal_int(meridional_E_pool,meridional_E_internal_pool,
                                meridional_E_latent_pool,meridional_E_geopotential_pool,
                                meridional_E_kinetic_pool,output_path,i)
        create_netcdf_point(meridional_E_point_pool,meridional_E_internal_point_pool,
                            meridional_E_latent_point_pool,meridional_E_geopotential_point_pool,
                            meridional_E_kinetic_point_pool,output_path,i)
    print 'Computation of meridional energy transport on model level for ERA-Interim is complete!!!'
    print 'The output is in sleep, safe and sound!!!'
    logging.info("The full pipeline of the quantification of meridional energy transport in the atmosphere is accomplished!")

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
