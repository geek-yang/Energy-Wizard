#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : A statistical look into the temporal and spatial distribution of fields (MERRA2)
Author          : Yang Liu
Date            : 2018.01.10
Last Update     : 2018.01.11
Description     : The code aims to statistically take a close look into each fields.
                  This could help understand the difference between each datasets, which
                  will explain the deviation in meridional energy transport. Specifically,
                  the script deals with atmospheric reanalysis dataset MERRA II from NASA.
Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, sys, matplotlib
variables       : Absolute Temperature              T         [K]
                  Specific Humidity                 q         [kg/kg]
                  Surface Pressure                  ps        [Pa]
                  Zonal Divergent Wind              u         [m/s]
                  Meridional Divergent Wind         v         [m/s]
		          Surface geopotential  	        z         [m2/s2]
Caveat!!	    : The dataset is the complete dataset of MERRA2 from 20N - 90N.
		          Attention should be paid when calculating the meridional grid length (dy)!
                  Direction of Axis:
                  Model Level: TOA to surface
                  Latitude: South to Nouth (20 to 90)
                  Lontitude: West to East (-180 to 180)
                  Time: 00:00 03:00 06:00 09:00 12:00 15:00 18:00 21:00 (3 hourly)

                  Mass correction is accmpolished through the correction of barotropic wind:
                  mass residual = surface pressure tendency + divergence of mass flux (u,v) - (E-P)
                  E-P = evaporation - precipitation = moisture tendency - divergence of moisture flux(u,v)
                  Due to the structure of the dataset, the mass budget correction are split into
                  two parts: 1. Quantify tendency terms in month loop
                             2. Quantify divergence terms in day loop
"""
import numpy as np
import scipy
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
# from surface to TOA
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

# target pressure level
# the unit is Pa !!!
p_level_interpolate = np.array([100, 200, 300, 500, 700, 1000, 2000, 3000, 5000, 7000,
                                10000, 12500, 15000, 17500, 20000, 22500, 25000, 30000, 35000, 40000,
                                45000, 50000, 55000, 60000, 65000, 70000, 75000, 77500, 80000, 82500,
                                85000, 87500, 90000, 92500, 95000, 97500, 100000],dtype = float)

################################   Input zone  ######################################
#get input from shell
# this aims for running serial program with one node on Cartesius
line_in = sys.stdin.readline()
# specify data path
#datapath = 'F:\DataBase\ERA_Interim\Subdaily'
datapath = '/projects/0/blueactn/reanalysis/MERRA2/subdaily'
# time of the data, which concerns with the name of input
# starting time (year)
start_year = int(line_in)
# Ending time, if only for 1 year, then it should be the same as starting year
end_year = int(line_in)
# specify output path for the netCDF4 file
#output_path = 'F:\DataBase\ERA_Interim\Subdaily'
output_path = '/home/lwc16308/reanalysis/MERRA2/output/statistics'
# benchmark datasets for basic dimensions
benchmark_path = '/projects/0/blueactn/reanalysis/MERRA2/subdaily/merra1980/MERRA2_100.inst3_3d_asm_Nv.19801221.SUB.nc4'
benchmark = Dataset(benchmark_path)
####################################################################################

###############################   stdout and log  ##################################
# calculate the time for the code execution
start_time = tttt.time()

# Redirect all the console output to a file
sys.stdout = open('/home/lwc16308/reanalysis/MERRA2/stdout/console_%d_statistics.out' % (start_year),'w')
# logging level 'DEBUG' 'INFO' 'WARNING' 'ERROR' 'CRITICAL'
logging.basicConfig(filename = '/home/lwc16308/reanalysis/MERRA2/log/history_%d_statistics.log' % (start_year),
                    filemode = 'w', level = logging.DEBUG,
                    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
####################################################################################

def var_key_retrieve(datapath, year, month, day):
    '''
    This module extracts the variables for mass correction and the computation of AMET.
    Due to the strcture of the dataset (MEERA2), the processing unit is daily data.
    '''
    # get the path to each datasets
    print "Start retrieving datasets %d (y) - %s (m) - %s (d)" % (year,namelist_month[month-1],namelist_day[day])
    logging.info("Start retrieving variables T,q,u,v,sp,z for from %d (y) - %s (m) - %s (d) " % (year,namelist_month[month-1],namelist_day[day]))
    if year < 1992:
        datapath_var = datapath + os.sep + 'merra%d' % (year) + os.sep + 'MERRA2_100.inst3_3d_asm_Nv.%d%s%s.SUB.nc4' % (year,namelist_month[month-1],namelist_day[day])
    elif year < 2001:
        datapath_var = datapath + os.sep + 'merra%d' % (year) + os.sep + 'MERRA2_200.inst3_3d_asm_Nv.%d%s%s.SUB.nc4' % (year,namelist_month[month-1],namelist_day[day])
    elif year < 2011:
        datapath_var = datapath + os.sep + 'merra%d' % (year) + os.sep + 'MERRA2_300.inst3_3d_asm_Nv.%d%s%s.SUB.nc4' % (year,namelist_month[month-1],namelist_day[day])
    else:
        datapath_var = datapath + os.sep + 'merra%d' % (year) + os.sep + 'MERRA2_400.inst3_3d_asm_Nv.%d%s%s.SUB.nc4' % (year,namelist_month[month-1],namelist_day[day])
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

def field_statistics(var_key):
    print "Start extracting variables for the statistics of fields on model level."
    ps = var_key.variables['PS'][:]
    v = var_key.variables['V'][:]
    T = var_key.variables['T'][:]
    print 'Extracting variables successfully!'
    logging.info("Extracting variables successfully!")
    # calculate dp based on mean value of surface pressure
    index_level = np.arange(len(level))
    dp_level = np.zeros((len(time),len(level),len(latitude),len(longitude)),dtype = float)
    # define the half level pressure matrix
    p_half_plus = np.zeros((len(time),len(level),len(latitude),len(longitude)),dtype = float)
    p_half_minus = np.zeros((len(time),len(level),len(latitude),len(longitude)),dtype = float)
    # calculate the pressure at each half level
    for i in index_level:
        p_half_plus[:,i,:,:] = A[i+1]*100 + B[i+1] * ps
        p_half_minus[:,i,:,:] = A[i]*100 + B[i] * ps
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

    return T_vert_mean, v_vert_mean, T_zonal_mean, v_zonal_mean

# save output datasets
def create_netcdf_point(T_vert_mean_pool, v_vert_mean_pool, T_zonal_mean_pool, v_zonal_mean_pool, output_path, year):
    print '*******************************************************************'
    print '*********************** create netcdf file*************************'
    print '*******************************************************************'
    logging.info("Start creating netcdf file for statistics of fields at each grid point.")
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path + os.sep + 'AMET_MERRA2_model_daily_%d_statistics_point.nc' % (year),'w',format = 'NETCDF3_64BIT')
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
    # create the 4d variable
    # vertical mean
    T_vert_wrap_var = data_wrap.createVariable('T_vert_mean',np.float64,('month','latitude','longitude'))
    v_vert_wrap_var = data_wrap.createVariable('v_vert_mean',np.float64,('month','latitude','longitude'))
    # zonal mean
    T_zonal_wrap_var = data_wrap.createVariable('T_zonal_mean',np.float64,('month','level','latitude'))
    v_zonal_wrap_var = data_wrap.createVariable('v_zonal_mean',np.float64,('month','level','latitude'))
    # global attributes
    data_wrap.description = 'Monthly mean statistics of fields from MERRA2 subdaily dataset'
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
    Dim_year = len(period)
    Dim_level_interpolate = len(p_level_interpolate)
    # calculate zonal & meridional grid size on earth
    # the earth is taken as a perfect sphere, instead of a ellopsoid
    dx = 2 * np.pi * constant['R'] * np.cos(2 * np.pi * latitude / 360) / len(longitude)
    dy = np.pi * constant['R'] / 361
    ####################################################################
    ###  Create space for stroing intermediate variables and outputs ###
    ####################################################################
    # data pool for vertical mean
    T_vert_mean_pool = np.zeros((Dim_month, Dim_latitude, Dim_longitude),dtype = float)
    v_vert_mean_pool = np.zeros((Dim_month, Dim_latitude, Dim_longitude),dtype = float)
    # data pool for zonal mean
    T_zonal_mean_pool = np.zeros((Dim_month, Dim_level_interpolate, Dim_latitude),dtype = float)
    v_zonal_mean_pool = np.zeros((Dim_month, Dim_level_interpolate, Dim_latitude),dtype = float)
    # Initialize the variable key of the last day of the last month for the computation of tendency terms in mass correction
    year_last = start_year - 1
    if year_last < 1992:
        datapath_last = datapath + os.sep + 'merra%d' % (year_last) + os.sep + 'MERRA2_100.inst3_3d_asm_Nv.%d1231.SUB.nc4' % (year_last)
    elif year_last < 2001:
        datapath_last = datapath + os.sep + 'merra%d' % (year_last) + os.sep + 'MERRA2_200.inst3_3d_asm_Nv.%d1231.SUB.nc4' % (year_last)
    elif year_last < 2011:
        datapath_last = datapath + os.sep + 'merra%d' % (year_last) + os.sep + 'MERRA2_300.inst3_3d_asm_Nv.%d1231.SUB.nc4' % (year_last)
    else:
        datapath_last = datapath + os.sep + 'merra%d' % (year_last) + os.sep + 'MERRA2_400.inst3_3d_asm_Nv.%d1231.SUB.nc4' % (year_last)
    var_last = Dataset(datapath_last)
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
            # days loop
            for k in days:
                # get the key of each variable
                var_key = var_key_retrieve(datapath,i,j,k)
                ####################################################################
                ###  Create space for stroing intermediate variables and outputs ###
                ####################################################################
                # data pool for daily mean of vertical mean
                pool_T_vert_daily = np.zeros((len(days),len(latitude),len(longitude)),dtype=float)
                pool_v_vert_daily = np.zeros((len(days),len(latitude),len(longitude)),dtype=float)
                # data pool for daily mean of zonal mean
                pool_T_zonal_daily = np.zeros((len(days), Dim_level_interpolate,len(latitude)),dtype=float)
                pool_v_zonal_daily = np.zeros((len(days), Dim_level_interpolate,len(latitude)),dtype=float)
                ####################################################################
                ######                       Geopotential                    #######
                ####################################################################
                # calculate the geopotential
                #gz = calc_geopotential(var_key)
                ####################################################################
                ######                   Statistics of fields                #######
                ####################################################################
                # calculate the energy flux terms in meridional energy Transport
                T_vert_mean, v_vert_mean, T_zonal_mean, v_zonal_mean = field_statistics(var_key)
                # save the vertical mean terms to the warehouse
                pool_T_vert_daily[k,:,:] = T_vert_mean
                pool_v_vert_daily[k,:,:] = v_vert_mean
                # save the zonal mean terms to the warehouse
                pool_T_zonal_daily[k,:,:] = T_zonal_mean
                pool_v_zonal_daily[k,:,:] = v_zonal_mean
            ####################################################################
            ######                 take the monthly mean                 #######
            ####################################################################
            # save the vertical mean terms to the warehouse
            T_vert_mean_pool[j-1,:,:] = np.mean(pool_T_vert_daily,0)
            v_vert_mean_pool[j-1,:,:] = np.mean(pool_v_vert_daily,0)
            # save the zonal mean terms to the warehouse
            T_zonal_mean_pool[j-1,:,:] = np.mean(pool_T_zonal_daily,0)
            v_zonal_mean_pool[j-1,:,:] = np.mean(pool_v_zonal_daily,0)
            print '*****************************************************************************'
            print "***             The statistics of all the fields are finished             ***"
            print '*****************************************************************************'
            logging.info("The statistics of all the fields are finished on model level is finished!")
        ####################################################################
        ######                 Data Wrapping (NetCDF)                #######
        ####################################################################
        # save data as netcdf file
        create_netcdf_point(T_vert_mean_pool, v_vert_mean_pool, T_zonal_mean_pool, v_zonal_mean_pool, output_path, i)
    print 'Computation of statistics of fields on model level for MERRA2 is complete!!!'
    print 'The output is in sleep, safe and sound!!!'
    logging.info("The full pipeline of the statistics of fields in the atmosphere is accomplished!")

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
