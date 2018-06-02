#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : Quantify stationary and transient eddy from atmospheric meridional energy transport (ERA-Interim)(HPC-cloud customised)
Author          : Yang Liu
Date            : 2018.05.02
Last Update     : 2018.06.02
Description     : The code aims to calculate the time and space dependent components
                  of atmospheric meridional energy transport based on atmospheric
                  reanalysis dataset ERA-Interim from ECMWF. The complete procedure
                  includes the calculation of geopotential on model levels, and the
                  decomposition of standing & transient eddies. The mass budget correction
                  is applied here. Much attention should be paid that we have to use daily
                  mean since the decomposition takes place at subdaily level could introduce
                  non-meaningful oscillation due to daily cycling.

                  The procedure is generic and is able to adapt any atmospheric
                  reanalysis datasets, with some changes.

                  Referring to the book "Physics of Climate", the concept of decomposition
                  of circulation is given with full details. As a consequence, the meridional
                  energy transport can be decomposed into 4 parts:
                  @@@   A = [/overbar{A}] + /ovrebar{A*} + [A]' + A'*   @@@
                  [/overbar{A}]:    energy transport by steady mean circulation
                  /ovrebar{A*}:     energy transport by stationary eddy
                  [A]':             energy transport by transient eddy
                  A'*:              energy transport by instantaneous and asymmetric part

                  An example is given at page 277, in terms of transport of moisture.
                  Here we will focus on three components of total meridional energy
                  transport:
                  @@@   [/overbar{vT}] = [/overbar{v}] x [/overbar{T}] + [/overbar{v}* x /overbar{T}*] + [/overbar{v'T'}]   @@@
                  [/overbar{v}] x [/overbar{T}]:    energy transport by steady mean circulation
                  [/overbar{v}* x /overbar{T}*]:    energy transport by stationary eddy
                  [/overbar{v'T'}]:                 energy transport by transient eddy

                  Due to a time dependent surface pressure, we will take the vertical
                  integral first and then decompose the total energy transport. Hence,
                  we actually harness the equation of single variable. Thus, we will calculate
                  all the 4 components.

Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, sys, matplotlib
variables       : Absolute Temperature              T
                  Specific Humidity                 q
                  Logarithmic Surface Pressure      lnsp
                  Zonal Divergent Wind              u
                  Meridional Divergent Wind         v
		          Surface geopotential  	        z
Caveat!!	    : The dataset is from 20 deg north to 90 deg north (Northern Hemisphere).
		          Attention should be paid when calculating the meridional grid length (dy)!
"""
import numpy as np
import time as tttt
from netCDF4 import Dataset,num2date
import os
import platform
import sys
import logging
import matplotlib
import argparse
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

# Redirect all the console output to a file
#sys.stdout = open('F:\DataBase\ERA_Interim\console.out','w')
sys.stdout = open('/project/Reanalysis/ERA_Interim/Subdaily/Model/console_E_decompose.out','w+')

# logging level 'DEBUG' 'INFO' 'WARNING' 'ERROR' 'CRITICAL'
#logging.basicConfig(filename = 'F:\DataBase\ERA_Interim\history.log', filemode = 'w',level = logging.DEBUG,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(filename = '/project/Reanalysis/ERA_Interim/Subdaily/Model/history_E_decompose.log',
                    filemode = 'w+', level = logging.DEBUG,
                    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# define the constant:
constant ={'g' : 9.80616,      # gravititional acceleration [m / s2]
           'R' : 6371009,      # radius of the earth [m]
           'cp': 1004.64,      # heat capacity of air [J/(Kg*K)]
           'Lv': 2264670,      # Latent heat of vaporization [J/Kg]
           'R_dry' : 286.9,    # gas constant of dry air [J/(kg*K)]
           'R_vap' : 461.5,    # gas constant for water vapour [J/(kg*K)]
           'Ps_ref' : 101300,  # reference surface pressure [Pa]    # to determine certain pressure levels on hybrid grid
            }

# A and B values for the definition of sigma levelist
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

################################   Input zone  ######################################
# specify data path
datapath = '/project/Reanalysis/ERA_Interim/Subdaily/Model'
# mass correction baratropic wind
uc_vc_datapath = '/project/Reanalysis/ERA_Interim/Subdaily/Model/HPC_Output/point'
# temporal and spatial mean of fields
mean_datapath = '/project/Reanalysis/ERA_Interim/Subdaily/Model/HPC_Output/eddy/v'
# time of the data, which concerns with the name of input
# starting time (year)
start_year = 1979
# Ending time, if only for 1 year, then it should be the same as starting year
end_year = 2016
# specify output path for the netCDF4 file
#output_path = 'F:\DataBase\ERA_Interim\Subdaily'
output_path = '/project/Reanalysis/ERA_Interim/Subdaily/Model/HPC_Output/eddy/v'
# benchmark datasets for basic dimensions
benchmark_path = '/project/Reanalysis/ERA_Interim/Subdaily/Model/era1980/model_daily_075_1980_1_z_lnsp.nc'
benchmark = Dataset(benchmark_path)
# levels of interest
# [200hPa,500hPa,850hPa]
lev_target = [29,39,49] # on native hybrid grid - half level
####################################################################################

def var_key(datapath, year, month):
    # get the path to each datasets
    print "Start retrieving datasets"
    logging.info("Start retrieving variables T,q,u,v,lnsp,z for from %d (y) - %d (m)" % (year,month))
    datapath_u_v = datapath + os.sep + 'era%d' % (year) + os.sep + 'model_daily_075_%d_%d_u_v.nc' % (year,month)
    # get the variable keys
    u_v_key = Dataset(datapath_u_v)
    print "Retrieving datasets successfully!"
    logging.info("Retrieving variables for from %d (y) - %d (m) successfully!" % (year,month))
    return u_v_key

def initialization(benchmark):
    print "Prepare for the main work!"
    # create the month index
    period = np.arange(start_year,end_year+1,1)
    index_month = np.arange(1,13,1)
    # create dimensions for saving data
    #Dim_level = len(benchmark.variables['level'][:])
    Dim_latitude = len(benchmark.variables['latitude'][:])
    Dim_longitude = len(benchmark.variables['longitude'][:])
    Dim_month = len(index_month)
    Dim_period = len(period)
    #latitude = benchmark.variables['latitude'][:]
    #longitude = benchmark.variables['longitude'][:]
    #Dim_time = len(benchmark.variables['time'][:])
    # a list of the index of starting day in each month
    month_day_length = [31,28,31,30,31,30,31,31,30,31,30,31] #! we ignore the last day of February for the leap year
    month_day_index = [0,31,59,90,120,151,181,212,243,273,304,334]
    # create variables
    v_temporal_sum = np.zeros((365,len(lev_target),Dim_latitude,Dim_longitude),dtype=float) #! we ignore the last day of February for the leap year
    v_spatial_mean = np.zeros((Dim_period,365,len(lev_target),Dim_latitude),dtype=float) #! we ignore the last day of February for the leap year
    return period, index_month, Dim_latitude, Dim_longitude, Dim_month, Dim_period,\
           month_day_length, month_day_index, v_temporal_sum, v_spatial_mean

def initialization_eddy(mean_datapath):
    print "Grab temporal and spatial mean for the following computation of eddies!"
    datapath_temporal_spatial_mean = os.path.join(mean_datapath,'model_daily_075_v_mean_point.nc')
    mean_key = Dataset(datapath_temporal_spatial_mean)
    # Here we only use the temporal mean, for the spatial mean we will take it dynamically
    # during the calculation of eddies, for the sake of memory usage.
    v_temporal_mean = mean_key.variables['v_temporal_mean']
    # create space for eddies
    v_2_transient_pool = np.zeros((Dim_period,Dim_month,len(lev_target),Dim_latitude,Dim_longitude),dtype=float)
    v_2_standing_pool = np.zeros((Dim_period,Dim_month,len(lev_target),Dim_latitude,Dim_longitude),dtype=float)
    v_2_transient_mean_pool = np.zeros((Dim_period,Dim_month,len(lev_target),Dim_latitude),dtype=float)
    v_2_stationary_mean_pool = np.zeros((Dim_period,Dim_month,len(lev_target),Dim_latitude,Dim_longitude),dtype=float)
    # create space for overall momentum
    v_2_overall_pool = np.zeros((Dim_period,Dim_month,len(lev_target),Dim_latitude,Dim_longitude),dtype=float)
    # create space for deviations
    #v_prime_pool = np.zeros((Dim_period,Dim_month,len(lev_target),Dim_latitude,Dim_longitude),dtype=float)
    #v_star_pool = np.zeros((Dim_period,Dim_month,len(lev_target),Dim_latitude,Dim_longitude),dtype=float)
    # calculate mean meridional circulation
    v_2_steady_mean_zonal_mean = np.mean(v_temporal_mean,3)
    v_2_steady_mean_monthly_zonal_mean = np.zeros((12,len(lev_target),Dim_latitude),dtype=float)
    for i in np.arange(Dim_month):
        v_2_steady_mean_monthly_zonal_mean[i,:,:] = np.mean(v_2_steady_mean_zonal_mean[month_day_index[i-1]:month_day_index[i-1]+month_day_length[i-1],:,:],0)
    v_2_steady_mean = v_2_steady_mean_monthly_zonal_mean * v_2_steady_mean_monthly_zonal_mean

    return v_temporal_mean, v_2_transient_pool, v_2_standing_pool, v_2_transient_mean_pool,\
           v_2_stationary_mean_pool, v_2_overall_pool, v_2_steady_mean

def pick_v(u_v_key):
    # validate time and location info
    time = u_v_key.variables['time'][:]
    level = u_v_key.variables['level'][:]
    latitude = u_v_key.variables['latitude'][:]
    longitude = u_v_key.variables['longitude'][:]
    date = num2date(time,u_v_key.variables['time'].units)
    days = len(time)/4
    print '*******************************************************************'
    print 'The datasets contain information from %s to %s' % (date[0],date[-1])
    print 'There are %d days in this month' % (len(time)/4)
    print 'The coordinates include %d vertical levels' % (len(level))
    print 'The grid employs %d points in latitude, and %d points in longitude' % (len(latitude),len(longitude))
    print '*******************************************************************'
    # extract variables
    print "Start extracting velocity for the calculation of mean over time and space."
    # extract data at certain levels
    v = np.zeros((len(time),len(lev_target),len(latitude),len(longitude)),dtype=float)
    v[:,0,:,:] = u_v_key.variables['v'][:,29,:,:] # 200hPa
    v[:,1,:,:] = u_v_key.variables['v'][:,39,:,:] # 500hPa
    v[:,2,:,:] = u_v_key.variables['v'][:,49,:,:] # 850hPa
    # daily mean
    # first we reshape the array
    v_expand = v.reshape(len(time)/4,4,len(lev_target),len(latitude),len(longitude))
    # Then we take daily mean
    v_daily = np.mean(v_expand,1)
    if days == 29:
        v_out = v_daily[:-1,:,:,:]
    else:
        v_out = v_daily
    print 'Extracting variables successfully!'
    logging.info("Extracting variables successfully!")

    return v_out

def compute_eddy(v_temporal_mean_select, v):
    '''
    We follow the method given by Peixoto and Oort, 1983.
    The equation is listed on page 61-63.
    equation 4.6 and 4.10
    The example is given on page 288.
    Here we take our naming convention for different eddies.
    For the details, please visit "Transient & Standing eddy"
    in notes.
    '''
    # shape of v[days,target_levels,lat,lon]
    logging.info("Calculate eddies!")
    # calculate transient eddies
    ################# transient eddy ###################
    print "Calculate transient eddies!"
    v_prime = v - v_temporal_mean_select
    v_2_transient = v_prime * v_prime
    # monthly mean
    # shape[target_levels,lat,lon]
    v_2_transient_monthly_mean = np.mean(v_2_transient,0)
    ####################################################
    # calculate transient mean eddies
    ############### transient mean eddy ################
    print "Calculate transient mean eddies!"
    v_prime_zonal_mean = np.mean(v,3) - np.mean(v_temporal_mean_select,3)
    v_2_transient_mean = v_prime_zonal_mean * v_prime_zonal_mean
    # monthly mean
    # shape[target_levels,lat]
    v_2_transient_mean_monthly_mean = np.mean(v_2_transient_mean,0)
    ####################################################
    # Calculate standing eddies
    ################## standing eddy ###################
    print "Calculate standing eddies!"
    v_star = np.zeros(v.shape,dtype=float)
    v_zonal_mean = np.mean(v,3)
    v_zonal_mean_enlarge = np.repeat(v_zonal_mean[:,:,:,np.newaxis],Dim_longitude,3)
    v_star = v - v_zonal_mean_enlarge
    v_2_standing = v_star * v_star
    # monthly mean
    # shape[target_levels,lat,lon]
    v_2_standing_monthly_mean = np.mean(v_2_standing,0)
    ####################################################
    # Calculate stationary mean eddies
    ##############  stationary mean eddy ###############
    print "Calculate stationary mean eddies!"
    v_monthly_mean = np.mean(v,0)
    v_monthly_zonal_mean = np.mean(v_monthly_mean,2)
    v_monthly_zonal_mean_enlarge = np.repeat(v_monthly_zonal_mean[:,:,np.newaxis],Dim_longitude,2)
    v_star_monthly_zonal_mean = v_monthly_mean - v_monthly_zonal_mean_enlarge
    # monthly mean
    # shape[target_levels,lat,lon]
    v_2_stationary_mean_monthly_mean = v_star_monthly_zonal_mean * v_star_monthly_zonal_mean
    ####################################################
    # calculate the overall momentum transport
    ##############   overall transport   ###############
    print "Calculate overall momentum transport!"
    v_2_overall = v * v
    # monthly mean
    # shape[target_levels,lat,lon]
    v_2_overall_monthly_mean = np.mean(v_2_overall,0)
    ####################################################
    logging.info("Finish the computation of eddies!")

    return v_2_transient_monthly_mean, v_2_transient_mean_monthly_mean,\
           v_2_standing_monthly_mean, v_2_stationary_mean_monthly_mean,\
           v_2_overall_monthly_mean

# make plots
def visualization(v2_overall,v2_transient,v2_transient_mean,v2_standing,
                  v2_stationary_mean,v2_steady_mean,output_path):
    print "Start making plot for the meridional momentum transport by each component."
    logging.info("Start making plot for the meridional momentum transport by each component.")
    # calculate annual mean of momentum transport
    v2_overall_average = np.mean(np.mean(np.mean(v2_overall,4),1),0)
    v2_transient_average = np.mean(np.mean(np.mean(v2_transient,4),1),0)
    v2_transient_mean_average = np.mean(np.mean(v2_transient_mean,1),0)
    v2_standing_average = np.mean(np.mean(np.mean(v2_standing,4),1),0)
    v2_stationary_mean_average = np.mean(np.mean(np.mean(v2_stationary_mean,4),1),0)
    v2_steady_mean_average = np.mean(v2_steady_mean,0)
    # take latitude data from benchmark variable
    Lat = benchmark.variables['latitude'][:]
    # Plot the total meridional energy transport against the latitude
    level_plot = [200,500,850]
    for i in np.arange(len(lev_target)):
        fig1 = plt.figure()
        plt.axhline(y=0, color='k',ls='--')
        plt.plot(Lat,v2_overall_average[i,:],'y-',linewidth = 2.0, label='Overall')
        plt.plot(Lat,v2_steady_mean_average[i,:],'g-',linewidth = 2.0, label='Steady Mean')
        plt.plot(Lat,v2_transient_average[i,:],'r-',linewidth = 2.0, label='Transient')
        plt.plot(Lat,v2_transient_mean_average[i,:],'m-',linewidth = 2.0, label='Transient Mean')
        plt.plot(Lat,v2_standing_average[i,:],'b-',linewidth = 2.0, label='Standing')
        plt.plot(Lat,v2_stationary_mean_average[i,:],'c-',linewidth = 2.0, label='Stationary Mean')
        #plt.hold()
        plt.title('Meridional Momentum Transport by different components at %dhPa' % (level_plot[i]))
        plt.legend()
        plt.xlabel("Laitude")
        plt.xticks(np.linspace(20,90,15))
        #plt.yticks(np.linspace(0,6,7))
        plt.ylabel("Meridional Momentum Transport (m2/s2)")
        #plt.show()
        fig1.savefig(output_path + os.sep + 'Meridional_Momentum_Transport_lev_%dhPa_overall.png' % (level_plot[i]), dpi = 400)
        plt.close(fig1)

# save output datasets
def create_netcdf_point_mean (v_temporal_mean,v_spatial_mean,output_path):
    print '*******************************************************************'
    print '*********************** create netcdf file*************************'
    print '*******************************************************************'
    logging.info("Start creating netcdf file for temporal and spatial mean of velocity at each grid point.")
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(os.path.join(output_path,'model_daily_075_v_mean_point.nc'),'w',format = 'NETCDF4')
    # create dimensions for netcdf data
    year_wrap_dim = data_wrap.createDimension('year',Dim_period)
    day_wrap_dim = data_wrap.createDimension('day',365)
    lev_wrap_dim = data_wrap.createDimension('level',len(lev_target))
    lat_wrap_dim = data_wrap.createDimension('latitude',Dim_latitude)
    lon_wrap_dim = data_wrap.createDimension('longitude',Dim_longitude)
    # create coordinate variables for 1-dimensions
    year_wrap_var = data_wrap.createVariable('year',np.int32,('year',))
    day_wrap_var = data_wrap.createVariable('day',np.int32,('day',))
    lev_wrap_var = data_wrap.createVariable('level',np.int32,('level',))
    lat_wrap_var = data_wrap.createVariable('latitude',np.float32,('latitude',))
    lon_wrap_var = data_wrap.createVariable('longitude',np.float32,('longitude',))
    # create the actual 4-d variable
    v_temporal_mean_wrap_var = data_wrap.createVariable('v_temporal_mean',np.float64,('day','level','latitude','longitude'),zlib=True)
    v_spatial_mean_wrap_var = data_wrap.createVariable('v_spatial_mean',np.float64,('year','day','level','latitude'),zlib=True)
    # global attributes
    data_wrap.description = 'Daily temporal and spatial mean of velocity at each grid point'
    # variable attributes
    lat_wrap_var.units = 'degree_north'
    lon_wrap_var.units = 'degree_east'
    lev_wrap_var.units = 'hPa'
    v_temporal_mean_wrap_var.units = 'm/s'
    v_spatial_mean_wrap_var.units = 'm/s'

    lat_wrap_var.long_name = 'Latitude'
    lon_wrap_var.long_name = 'Longitude'
    lev_wrap_var.long_name = 'Pressure level'
    v_temporal_mean_wrap_var.long_name = 'Temporal mean of meridional wind velocity'
    v_spatial_mean_wrap_var.long_name = 'Zonal mean of meridional wind velocity'

    # writing data
    year_wrap_var[:] = period
    day_wrap_var[:] = np.arange(1,366,1)
    lev_wrap_var[:] = [200,500,850]
    lat_wrap_var[:] = benchmark.variables['latitude'][:]
    lon_wrap_var[:] = benchmark.variables['longitude'][:]
    v_temporal_mean_wrap_var[:] = v_temporal_mean
    v_spatial_mean_wrap_var[:] = v_spatial_mean

    # close the file
    data_wrap.close()
    print "Create netcdf file successfully"
    logging.info("The generation of netcdf files for the temporal and spatial mean of velocity on each grid point is complete!!")

def create_netcdf_point_eddy(v2_overall,v2_transient,v2_transient_mean,v2_standing,
                             v2_stationary_mean,v2_steady_mean,output_path):
    # take the zonal mean
    v2_overall_zonal = np.mean(v2_overall,4)
    v2_transient_zonal = np.mean(v2_transient,4)
    # v2_transient_mean is zonal mean already
    v2_standing_zonal = np.mean(v2_standing,4)
    v2_stationary_mean_zonal = np.mean(v2_stationary_mean,4)
    # create netCDF
    print '*******************************************************************'
    print '*********************** create netcdf file*************************'
    print '*******************************************************************'
    logging.info("Start creating netcdf file for stationary and transient eddies at each grid point.")
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(os.path.join(output_path,'model_daily_075_v2_eddies_point.nc'),'w',format = 'NETCDF4')
    # create dimensions for netcdf data
    year_wrap_dim = data_wrap.createDimension('year',Dim_period)
    month_wrap_dim = data_wrap.createDimension('month',Dim_month)
    lev_wrap_dim = data_wrap.createDimension('level',len(lev_target))
    lat_wrap_dim = data_wrap.createDimension('latitude',Dim_latitude)
    lon_wrap_dim = data_wrap.createDimension('longitude',Dim_longitude)
    # create coordinate variables for 1-dimensions
    year_wrap_var = data_wrap.createVariable('year',np.int32,('year',))
    month_wrap_var = data_wrap.createVariable('month',np.int32,('month',))
    lev_wrap_var = data_wrap.createVariable('level',np.int32,('level',))
    lat_wrap_var = data_wrap.createVariable('latitude',np.float32,('latitude',))
    lon_wrap_var = data_wrap.createVariable('longitude',np.float32,('longitude',))
    # create the 5-d variable
    v2_overall_wrap_var = data_wrap.createVariable('v2_overall',np.float64,('year','month','level','latitude','longitude'),zlib=True)
    v2_transient_wrap_var = data_wrap.createVariable('v2_transient',np.float64,('year','month','level','latitude','longitude'),zlib=True)
    v2_standing_wrap_var = data_wrap.createVariable('v2_standing',np.float64,('year','month','level','latitude','longitude'),zlib=True)
    v2_stationary_mean_wrap_var = data_wrap.createVariable('v2_stationary_mean',np.float64,('year','month','level','latitude','longitude'),zlib=True)
    # create the 4d variable
    v2_overall_zonal_wrap_var = data_wrap.createVariable('v2_overall_zonal',np.float64,('year','month','level','latitude'),zlib=True)
    v2_transient_zonal_wrap_var = data_wrap.createVariable('v2_transient_zonal',np.float64,('year','month','level','latitude'),zlib=True)
    v2_transient_mean_wrap_var = data_wrap.createVariable('v2_transient_mean',np.float64,('year','month','level','latitude'),zlib=True)
    v2_standing_zonal_wrap_var = data_wrap.createVariable('v2_standing_zonal',np.float64,('year','month','level','latitude'),zlib=True)
    v2_stationary_mean_zonal_wrap_var = data_wrap.createVariable('v2_stationary_mean_zonal',np.float64,('year','month','level','latitude'),zlib=True)
    # create the 2d variable
    v2_steady_mean_wrap_var = data_wrap.createVariable('v2_steady_mean',np.float64,('month','level','latitude'),zlib=True)
    # global attributes
    data_wrap.description = 'Monthly stationary and transient eddies at each grid point'
    # variable attributes
    lat_wrap_var.units = 'degree_north'
    lon_wrap_var.units = 'degree_east'
    lev_wrap_var.units = 'hPa'
    v2_overall_wrap_var.units = 'm2/s2'
    v2_transient_wrap_var.units = 'm2/s2'
    v2_standing_wrap_var.units = 'm2/s2'
    v2_stationary_mean_wrap_var.units = 'm2/s2'
    v2_overall_zonal_wrap_var.units = 'm2/s2'
    v2_transient_zonal_wrap_var.units = 'm2/s2'
    v2_transient_mean_wrap_var.units = 'm2/s2'
    v2_standing_zonal_wrap_var.units = 'm2/s2'
    v2_stationary_mean_zonal_wrap_var.units = 'm2/s2'
    v2_steady_mean_wrap_var.units = 'm2/s2'

    lat_wrap_var.long_name = 'Latitude'
    lon_wrap_var.long_name = 'Longitude'
    lev_wrap_var.long_name = 'Pressure level'
    v2_overall_wrap_var.long_name = 'Northward transport of momentum by all motions'
    v2_transient_wrap_var.long_name = 'Northward transport of momentum by transient eddy'
    v2_standing_wrap_var.long_name = 'Northward transport of momentum by standing eddy'
    v2_stationary_mean_wrap_var.long_name = 'Northward transport of momentum by stationary mean eddy'
    v2_overall_zonal_wrap_var.long_name = 'Zonal mean of northward transport of momentum by all motions'
    v2_transient_zonal_wrap_var.long_name = 'Zonal mean of northward transport of momentum by transient eddy'
    v2_transient_mean_wrap_var.long_name = 'Northward transport of momentum by transient mean eddy'
    v2_standing_zonal_wrap_var.long_name = 'Zonal mean of northward transport of momentum by standing eddy'
    v2_stationary_mean_zonal_wrap_var.long_name = 'Zonal mean of northward transport of momentum by stationary mean eddy'
    v2_steady_mean_wrap_var.long_name = 'Northward transport of momentum by steady mean meridional circulation'

    # writing data
    year_wrap_var[:] = period
    month_wrap_var[:] = index_month
    lev_wrap_var[:] = [200,500,850]
    lat_wrap_var[:] = benchmark.variables['latitude'][:]
    lon_wrap_var[:] = benchmark.variables['longitude'][:]
    v2_overall_wrap_var[:] = v2_overall
    v2_transient_wrap_var[:] = v2_transient
    v2_standing_wrap_var[:] = v2_standing
    v2_stationary_mean_wrap_var[:] = v2_stationary_mean
    v2_overall_zonal_wrap_var[:] = v2_overall_zonal
    v2_transient_zonal_wrap_var[:] = v2_transient_zonal
    v2_transient_mean_wrap_var[:] = v2_transient_mean
    v2_standing_zonal_wrap_var[:] = v2_standing_zonal
    v2_stationary_mean_zonal_wrap_var[:] = v2_stationary_mean_zonal
    v2_steady_mean_wrap_var[:] = v2_steady_mean

# pass argument to the main function
def choice_parser():
    '''
    pass command line arguments
    '''
    # define arguments
    parser = argparse.ArgumentParser(description="Choose the function")
    parser.add_argument('--mean', action = 'store_true',
                        help='function switch for calculating the temporal & spatial mean')
    parser.add_argument('--eddy', action = 'store_true',
                        help='function switch for calculating the stationary & transient eddy')
    #get arguments
    choices = parser.parse_args()
    return choices

# save output datasets

if __name__=="__main__":
    # calculate the time for the code execution
    start_time = tttt.time()
    # initialization
    period, index_month, Dim_latitude, Dim_longitude, Dim_month, Dim_period,\
    month_day_length, month_day_index, v_temporal_sum, v_spatial_mean = initialization(benchmark)
    # get command line arguments and decide the function of this script
    args = choice_parser()
    if args.mean:
        print '*******************************************************************'
        print '************  calculate the temporal and spatial mean  ************'
        print '*******************************************************************'
        for i in period:
            for j in index_month:
                # get the key of each variable
                u_v_key = var_key(datapath,i,j)
                # take the daily mean of target fields at certain levels
                v = pick_v(u_v_key)
                # add daily field to the summation operator
                v_temporal_sum[month_day_index[j-1]:month_day_index[j-1]+month_day_length[j-1],:,:,:] = \
                v_temporal_sum[month_day_index[j-1]:month_day_index[j-1]+month_day_length[j-1],:,:,:] + v
                # calculate the zonal (spatial) mean
                v_spatial_mean[i-start_year,month_day_index[j-1]:month_day_index[j-1]+month_day_length[j-1],:,:] = \
                np.mean(v,3)
        # calculate the temporal mean
        v_temporal_mean = v_temporal_sum / Dim_period
        # create netcdf file for the output
        create_netcdf_point_mean(v_temporal_mean,v_spatial_mean,output_path)
    elif args.eddy:
        del v_temporal_sum, v_spatial_mean
        print '*******************************************************************'
        print '**********  calculate the stationary and transient eddy  **********'
        print '*******************************************************************'
        # Initialization
        # Grab temporal & spatial mean
        # The mean meridional circulation is calculated here
        v_temporal_mean, v_2_transient_pool, v_2_standing_pool, v_2_transient_mean_pool,\
        v_2_stationary_mean_pool, v_2_overall_pool, v_2_steady_mean = initialization_eddy(mean_datapath)
        for i in period:
            for j in index_month:
                # get the key of each variable
                u_v_key = var_key(datapath,i,j)
                # take the daily mean of target fields at certain levels
                v = pick_v(u_v_key)
                v_temporal_mean_select = v_temporal_mean[month_day_index[j-1]:month_day_index[j-1]+month_day_length[j-1],:,:,:]
                v_2_transient, v_2_transient_mean, v_2_standing, v_2_stationary_mean,\
                v_2_overall = compute_eddy(v_temporal_mean_select, v)
                # save output to the data pool for netCDF
                v_2_overall_pool[i-start_year,j-1,:,:,:] = v_2_overall
                v_2_transient_pool[i-start_year,j-1,:,:,:] = v_2_transient
                v_2_transient_mean_pool[i-start_year,j-1,:,:] = v_2_transient_mean
                v_2_standing_pool[i-start_year,j-1,:,:,:] = v_2_standing
                v_2_stationary_mean_pool[i-start_year,j-1,:,:,:] = v_2_stationary_mean
        create_netcdf_point_eddy(v_2_overall_pool,v_2_transient_pool,v_2_transient_mean_pool,
                                 v_2_standing_pool,v_2_stationary_mean_pool,v_2_steady_mean,output_path)
        visualization(v_2_overall_pool,v_2_transient_pool,v_2_transient_mean_pool,
                      v_2_standing_pool,v_2_stationary_mean_pool,v_2_steady_mean,output_path)
    else:
        print 'Please specify the function of the code!'
    print 'The full pipeline of the decomposition of meridional energy transport in the atmosphere is accomplished!'
    logging.info("The full pipeline of the decomposition of meridional energy transport in the atmosphere is accomplished!")
    print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
