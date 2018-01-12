#!/usr/bin/env python

"""
Copyright Netherlands eScience Center

Function        : A statistical look into the temporal and spatial distribution of fields (ERA-Interim)(HPC-cloud customised)
Author          : Yang Liu
Date            : 2018.01.12
Last Update     : 2018.01.12
Description     : The code aims to statistically take a close look into each fields.
                  This could help understand the difference between each datasets, which
                  will explain the deviation in meridional energy transport. Specifically,
                  the script works with dataset ERA-Interim from ECMWF.
Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, sys, matplotlib
variables       : Absolute Temperature              T         [K]
                  Specific Humidity                 q         [kg/kg]
                  Surface Pressure                  ps        [Pa]
                  Zonal Divergent Wind              u         [m/s]
                  Meridional Divergent Wind         v         [m/s]
		          Surface geopotential  	        z         [m2/s2]
Caveat!!        : The dataset is the complete dataset of ERA-Interim from 20N - 90N.
		          Attention should be paid when calculating the meridional grid length (dy)!
                  Direction of Axis:
                  Model Level: TOA to surface
                  Latitude: North to South (90 to 20)
                  Lontitude: West to East (-180 to 180)
                  Time: 00:00 06:00 12:00 18:00 (6 hourly)
"""
import numpy as np
import scipy
import scipy.interpolate
import time as tttt
from netCDF4 import Dataset,num2date
import os
import platform
import sys
import logging
import matplotlib
# Generate images without having a window appear
#matplotlib.use('Agg')
#import matplotlib.pyplot as plt

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
sys.stdout = open('/project/Reanalysis/ERA_Interim/Subdaily/Model/console_statistics.out','w')

# logging level 'DEBUG' 'INFO' 'WARNING' 'ERROR' 'CRITICAL'
#logging.basicConfig(filename = 'F:\DataBase\ERA_Interim\history.log', filemode = 'w',level = logging.DEBUG,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(filename = '/project/Reanalysis/ERA_Interim/Subdaily/Model/history_statistics.log',
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
# the unit is Pa!!!
# Since there are 60 model levels, there are 61 half levels, so it is for A and B values
A = np.array([
      0.0000000000e+000, 2.0000000000e+001, 3.8425338745e+001, 6.3647796631e+001, 9.5636962891e+001,
      1.3448330688e+002, 1.8058435059e+002, 2.3477905273e+002, 2.9849584961e+002, 3.7397192383e+002,
      4.6461816406e+002, 5.7565112305e+002, 7.1321801758e+002, 8.8366040039e+002, 1.0948347168e+003,
      1.3564746094e+003, 1.6806403809e+003, 2.0822739258e+003, 2.5798886719e+003, 3.1964216309e+003,
      3.9602915039e+003, 4.9067070313e+003, 6.0180195313e+003, 7.3066328125e+003, 8.7650546875e+003,
      1.0376125000e+004, 1.2077445313e+004, 1.3775324219e+004, 1.5379804688e+004, 1.6819472656e+004,
      1.8045183594e+004, 1.9027695313e+004, 1.9755109375e+004, 2.0222203125e+004, 2.0429863281e+004,
      2.0384480469e+004, 2.0097402344e+004, 1.9584328125e+004, 1.8864750000e+004, 1.7961359375e+004,
      1.6899468750e+004, 1.5706449219e+004, 1.4411125000e+004, 1.3043218750e+004, 1.1632757813e+004,
      1.0209500000e+004, 8.8023554688e+003, 7.4388046875e+003, 6.1443164063e+003, 4.9417773438e+003,
      3.8509133301e+003, 2.8876965332e+003, 2.0637797852e+003, 1.3859125977e+003, 8.5536181641e+002,
      4.6733349609e+002, 2.1039389038e+002, 6.5889236450e+001, 7.3677425385e+000, 0.0000000000e+000,
      0.0000000000e+000,],dtype=float)
B = np.array([
      0.0000000000e+000, 0.0000000000e+000, 0.0000000000e+000, 0.0000000000e+000, 0.0000000000e+000,
      0.0000000000e+000, 0.0000000000e+000, 0.0000000000e+000, 0.0000000000e+000, 0.0000000000e+000,
      0.0000000000e+000, 0.0000000000e+000, 0.0000000000e+000, 0.0000000000e+000, 0.0000000000e+000,
      0.0000000000e+000, 0.0000000000e+000, 0.0000000000e+000, 0.0000000000e+000, 0.0000000000e+000,
      0.0000000000e+000, 0.0000000000e+000, 0.0000000000e+000, 0.0000000000e+000, 7.5823496445e-005,
      4.6139489859e-004, 1.8151560798e-003, 5.0811171532e-003, 1.1142909527e-002, 2.0677875727e-002,
      3.4121163189e-002, 5.1690407097e-002, 7.3533833027e-002, 9.9674701691e-002, 1.3002252579e-001,
      1.6438430548e-001, 2.0247590542e-001, 2.4393314123e-001, 2.8832298517e-001, 3.3515489101e-001,
      3.8389211893e-001, 4.3396294117e-001, 4.8477154970e-001, 5.3570991755e-001, 5.8616840839e-001,
      6.3554745913e-001, 6.8326860666e-001, 7.2878581285e-001, 7.7159661055e-001, 8.1125342846e-001,
      8.4737491608e-001, 8.7965691090e-001, 9.0788388252e-001, 9.3194031715e-001, 9.5182150602e-001,
      9.6764522791e-001, 9.7966271639e-001, 9.8827010393e-001, 9.9401944876e-001, 9.9763011932e-001,
      1.0000000000e+000,],dtype=float)

# target pressure level
# the unit is Pa !!!
p_level_interpolate = np.array([100, 200, 300, 500, 700, 1000, 2000, 3000, 5000, 7000,
                                10000, 12500, 15000, 17500, 20000, 22500, 25000, 30000, 35000, 40000,
                                45000, 50000, 55000, 60000, 65000, 70000, 75000, 77500, 80000, 82500,
                                85000, 87500, 90000, 92500, 95000, 97500, 100000],dtype = float)

################################   Input zone  ######################################
# specify data path
#datapath = 'F:\DataBase\ERA_Interim\Subdaily'
datapath = '/project/Reanalysis/ERA_Interim/Subdaily/Model'
# time of the data, which concerns with the name of input
# starting time (year)
start_year = 1979
# Ending time, if only for 1 year, then it should be the same as starting year
end_year = 2016
# specify output path for the netCDF4 file
#output_path = 'F:\DataBase\ERA_Interim\Subdaily'
output_path = '/project/Reanalysis/ERA_Interim/Subdaily/Model/HPC_output/statistics'
# benchmark datasets for basic dimensions
benchmark_path = '/project/Reanalysis/ERA_Interim/Subdaily/Model/era1980/model_daily_075_1980_1_z_lnsp.nc'
benchmark = Dataset(benchmark_path)
####################################################################################

def var_key(datapath, year, month):
    # get the path to each datasets
    print "Start retrieving datasets"
    logging.info("Start retrieving variables T,q,u,v,lnsp,z for from %d (y) - %d (m)" % (year,month))
    datapath_T_q = datapath + os.sep + 'era%d' % (year) + os.sep + 'model_daily_075_%d_%d_T_q.nc' % (year,month)
    datapath_u_v = datapath + os.sep + 'era%d' % (year) + os.sep + 'model_daily_075_%d_%d_u_v.nc' % (year,month)
    datapath_z_lnsp = datapath + os.sep + 'era%d' % (year) + os.sep + 'model_daily_075_%d_%d_z_lnsp.nc' % (year,month)
    # get the variable keys
    T_q_key = Dataset(datapath_T_q)
    u_v_key = Dataset(datapath_u_v)
    z_lnsp_key = Dataset(datapath_z_lnsp)
    print "Retrieving datasets successfully!"
    logging.info("Retrieving variables for from %d (y) - %d (m) successfully!" % (year,month))
    return T_q_key, u_v_key, z_lnsp_key

def calc_geopotential(T_q_key, z_lnsp_key):
    # extract variables
    print "Start extracting variables for the calculation of geopotential on model level."
    T = T_q_key.variables['t'][:]
    q = T_q_key.variables['q'][:]
    lnsp = z_lnsp_key.variables['lnsp'][:]
    z = z_lnsp_key.variables['z'][:]
    # validate time and location info
    time = T_q_key.variables['time'][:]
    date = num2date(time,T_q_key.variables['time'].units)
    print '*******************************************************************'
    print 'The datasets contain information from %s to %s' % (date[0],date[-1])
    print 'There are %d days in this month' % (len(time)/4)
    print 'The coordinates include %d vertical levels' % (len(level))
    print 'The grid employs %d points in latitude, and %d points in longitude' % (len(latitude),len(longitude))
    print '*******************************************************************'
    print 'Extracting variables successfully!'
    logging.info("Extracting variables successfully!")

    print 'Start calculating geopotential on model level'
    # calculate the surface pressure
    # the unit of pressure here is Pa!!!
    sp = np.exp(lnsp)
    # define the half level pressure matrix
    p_half_plus = np.zeros((len(time),len(level),len(latitude),len(longitude)),dtype = float)
    p_half_minus = np.zeros((len(time),len(level),len(latitude),len(longitude)),dtype = float)
    # calculate the index of pressure levels
    index_level = np.arange(len(level))
    # calculate the pressure at each half level
    for i in index_level:
        p_half_plus[:,i,:,:] = A[i+1] + B[i+1] * sp
        p_half_minus[:,i,:,:] = A[i] + B[i] * sp
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
        # reverse the index
        i_inverse = len(level) - 1 - i
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

def field_statistics(T_q_key, z_lnsp_key, u_v_key):
    # extract variables
    print "Start extracting variables for the quantification of meridional energy transport."
    T = T_q_key.variables['t'][:]
    q = T_q_key.variables['q'][:]
    lnsp = z_lnsp_key.variables['lnsp'][:]
    u = u_v_key.variables['u'][:]
    v = u_v_key.variables['v'][:]
    time = T_q_key.variables['time'][:] # for dimension
    print 'Extracting variables successfully!'
    logging.info("Extracting variables successfully!")
    print 'Start calculating statistics of fields on model level'
    # calculate the mean value of surface pressure level
    sp = np.exp(lnsp)
    # calculate dp based on mean value of surface pressure
    dp_level = np.zeros(T.shape,dtype = float)
    # calculate the index of pressure levels
    index_level = np.arange(Dim_level)
    # define the half level pressure matrix
    p_half_plus = np.zeros(T.shape,dtype = float)
    p_half_minus = np.zeros(T.shape,dtype = float)
    # calculate the pressure at each half level
    for i in index_level:
        p_half_plus[:,i,:,:] = A[i+1]*100 + B[i+1] * sp
        p_half_minus[:,i,:,:] = A[i]*100 + B[i] * sp
    # calculate dp
    dp_level = p_half_plus - p_half_minus
    # vertical mean
    T_vert_mean = np.mean(np.sum((T * dp_level),axis=1) / np.sum(dp_level,axis=1),0)
    v_vert_mean = np.mean(np.sum((v * dp_level),axis=1) / np.sum(dp_level,axis=1),0)
    # horizontal mean
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
    # Since the model level is hybrid level. we have to interpolate the fields on
    # pressure level.
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
    # full model level pressure level
    p_level = (p_half_plus + p_half_minus) / 2.0
    # create space for interpolation of fields
    T_pressure_level = np.zeros((len(time),len(p_level_interpolate),len(latitude),len(longitude)),dtype = float)
    v_pressure_level = np.zeros((len(time),len(p_level_interpolate),len(latitude),len(longitude)),dtype = float)
    # interpolate fields on target pressure level
    for i in np.arange(len(time)): # synoptic time
        for j in np.arange(len(latitude)):
            for k in np.arange(len(longitude)):
                ius_T = scipy.interpolate.interp1d(p_level[i,:,j,k], T[i,:,j,k], kind='slinear',bounds_error=False,fill_value=0.0)
                T_pressure_level[i,:,j,k] = ius_T(p_level_interpolate)
                ius_v = scipy.interpolate.interp1d(p_level[i,:,j,k], v[i,:,j,k], kind='slinear',bounds_error=False,fill_value=0.0)
                v_pressure_level[i,:,j,k] = ius_v(p_level_interpolate)
    # take the zonal mean
    T_zonal_mean = np.mean(np.mean(T_pressure_level,axis=3),0)
    v_zonal_mean = np.mean(np.mean(v_pressure_level,axis=3),0)

    print '*****************************************************************************'
    print "************        The statistics of fields is finished          ***********"
    print '*****************************************************************************'
    logging.info("The ststistics of fields on model level is finished!")

    return T_vert_mean, v_vert_mean, T_zonal_mean, v_zonal_mean

# save output datasets
def create_netcdf_point(T_vert_mean_pool, v_vert_mean_pool, T_zonal_mean_pool, v_zonal_mean_pool, output_path, year):
    print '*******************************************************************'
    print '*********************** create netcdf file*************************'
    print '*******************************************************************'
    logging.info("Start creating netcdf file for total meridional energy transport and each component at each grid point.")
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path + os.sep + 'AMET_ERAI_model_daily_%d_statistics_point.nc' % (year),'w',format = 'NETCDF3_64BIT')
    # create dimensions for netcdf data
    month_wrap_dim = data_wrap.createDimension('month',Dim_month)
    lat_wrap_dim = data_wrap.createDimension('latitude',Dim_latitude)
    lon_wrap_dim = data_wrap.createDimension('longitude',Dim_longitude)
    lev_wrap_dim = data_wrap.createDimension('level',Dim_level_interpolate)
    # create coordinate variables for 3-dimensions
    month_wrap_var = data_wrap.createVariable('month',np.int32,('month',))
    lat_wrap_var = data_wrap.createVariable('latitude',np.float32,('latitude',))
    lon_wrap_var = data_wrap.createVariable('longitude',np.float32,('longitude',))
    lev_wrap_var = data_wrap.createVariable('level',np.int32,('level',))
    # create the actual 3-d variable
    # vertical mean
    T_vert_wrap_var = data_wrap.createVariable('T_vert_mean',np.float64,('month','latitude','longitude'))
    v_vert_wrap_var = data_wrap.createVariable('v_vert_mean',np.float64,('month','latitude','longitude'))
    # zonal mean
    T_zonal_wrap_var = data_wrap.createVariable('T_zonal_mean',np.float64,('month','level','latitude'))
    v_zonal_wrap_var = data_wrap.createVariable('v_zonal_mean',np.float64,('month','level','latitude'))
    # global attributes
    data_wrap.description = 'Monthly mean statistics of fields from ERA-Interim subdaily dataset'
    # variable attributes
    lat_wrap_var.units = 'degree_north'
    lon_wrap_var.units = 'degree_east'
    lev_wrap_var.units = 'hPa'

    T_vert_wrap_var.units = 'Kelvin'
    v_vert_wrap_var.units = 'm/s'

    T_zonal_wrap_var.units = 'Kelvin'
    v_zonal_wrap_var.units = 'm/s'

    T_vert_wrap_var.long_name = 'vertical mean of temperature'
    v_vert_wrap_var.long_name = 'vertical mean of meridional velocity'

    T_zonal_wrap_var.long_name = 'zonal mean of temperature'
    v_zonal_wrap_var.long_name = 'zonal mean of meridional velocity'
    # writing data
    lat_wrap_var[:] = latitude
    lon_wrap_var[:] = longitude
    month_wrap_var[:] = index_month
    lev_wrap_var[:] = p_level_interpolate / 100 # change the unit to helipasca

    T_vert_wrap_var[:] = T_vert_mean_pool
    v_vert_wrap_var[:] = v_vert_mean_pool

    T_zonal_wrap_var[:] = T_zonal_mean_pool
    v_zonal_wrap_var[:] = v_zonal_mean_pool
    # close the file
    data_wrap.close()
    print "Create netcdf file successfully"
    logging.info("The generation of netcdf files for the total meridional energy transport and each component on each grid point is complete!!")

if __name__=="__main__":
    # create the month index
    period = np.arange(start_year,end_year+1,1)
    index_month = np.arange(1,13,1)
    # take benchmark variables
    level = benchmark.variables['level'][:]
    latitude = benchmark.variables['latitude'][:]
    longitude = benchmark.variables['longitude'][:]
    # create dimensions for saving data
    Dim_level = len(level)
    Dim_latitude = len(latitude)
    Dim_longitude = len(longitude)
    Dim_month = len(index_month)
    #Dim_year = len(period)
    Dim_level_interpolate = len(p_level_interpolate)
    # calculate zonal & meridional grid size on earth
    # the earth is taken as a perfect sphere, instead of a ellopsoid
    dx = 2 * np.pi * constant['R'] * np.cos(2 * np.pi * latitude / 360) / len(longitude)
    dy = np.pi * constant['R'] / 240
    ####################################################################
    ###  Create space for stroing intermediate variables and outputs ###
    ####################################################################
    # data pool for vertical mean
    T_vert_mean_pool = np.zeros((Dim_month, Dim_latitude, Dim_longitude),dtype = float)
    v_vert_mean_pool = np.zeros((Dim_month, Dim_latitude, Dim_longitude),dtype = float)
    # data pool for zonal mean
    T_zonal_mean_pool = np.zeros((Dim_month, Dim_level_interpolate, Dim_latitude),dtype = float)
    v_zonal_mean_pool = np.zeros((Dim_month, Dim_level_interpolate, Dim_latitude),dtype = float)
    # data pool for grid point values
    # loop for calculation
    for i in period:
        for j in index_month:
            # get the key of each variable
            T_q_key, u_v_key, z_lnsp_key = var_key(datapath,i,j)
            ####################################################################
            ######                       Geopotential                    #######
            ####################################################################
            #gz = calc_geopotential(T_q_key, z_lnsp_key)
            ####################################################################
            ######                   Statistics of fields                #######
            ####################################################################
            T_vert_mean, v_vert_mean, T_zonal_mean, v_zonal_mean = field_statistics(T_q_key, z_lnsp_key, u_v_key)
            # save the total meridional energy and each component to the data pool
            # save the vertical mean terms to the warehouse
            T_vert_mean_pool[j-1,:,:] = T_vert_mean
            v_vert_mean_pool[j-1,:,:] = v_vert_mean
            # save the zonal mean terms to the warehouse
            T_zonal_mean_pool[j-1,:,:] = T_zonal_mean
            v_zonal_mean_pool[j-1,:,:] = v_zonal_mean
        # save data as netcdf file
        create_netcdf_point(T_vert_mean_pool, v_vert_mean_pool, T_zonal_mean_pool, v_zonal_mean_pool, output_path, i)
    print 'Computation of meridional energy transport on model level for ERA-Interim is complete!!!'
    print 'The output is in sleep, safe and sound!!!'
    logging.info("The full pipeline of the quantification of meridional energy transport in the atmosphere is accomplished!")

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
