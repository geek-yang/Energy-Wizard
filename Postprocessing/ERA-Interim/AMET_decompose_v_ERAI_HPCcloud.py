#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : Quantify stationary and transient eddy from atmospheric meridional energy transport (ERA-Interim)(HPC-cloud customised)
Author          : Yang Liu
Date            : 2018.05.02
Last Update     : 2018.05.30
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
sys.stdout = open('/project/Reanalysis/ERA_Interim/Subdaily/Model/console_E-decompose.out','w+')

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
#datapath = 'F:\DataBase\ERA_Interim\Subdaily'
datapath = '/project/Reanalysis/ERA_Interim/Subdaily/Model'
# mass correction baratropic wind
uc_vc_datapath = '/project/Reanalysis/ERA_Interim/Subdaily/Model/HPC_Output/point'
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
    Dim_level = len(benchmark.variables['level'][:])
    Dim_latitude = len(benchmark.variables['latitude'][:])
    Dim_longitude = len(benchmark.variables['longitude'][:])
    Dim_month = len(index_month)
    Dim_period = len(period)
    #latitude = benchmark.variables['latitude'][:]
    #longitude = benchmark.variables['longitude'][:]
    #Dim_time = len(benchmark.variables['time'][:])
    # a list of the index of starting day in each month
    month_day_length = [31,28,31,30,31,30,31,31,30,31,30,31]
    month_day_index = [0,31,59,90,120,151,181,212,243,273,304,334]
    # create variables
    v_temporal_mean = np.zeros((365,len(lev_target),Dim_latitude,Dim_longitude),dtype=float) #! we ignore the last day of February for the leap year
    v_spatial_mean = np.zeros((Dim_period,365,len(lev_target),Dim_latitude),dtype=float) #! we ignore the last day of February for the leap year
    return period, index_month, Dim_level, Dim_latitude, Dim_longitude, Dim_month, Dim_period,\
           month_day_length, month_day_index, v_temporal_sum, v_spatial_mean

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
    v_daily = np.zeros((len(time)/4,len(lev_target),len(latitude),len(longitude)),dtype=float)
    for i in np.arange(len(time)/4):
        v_daily[i,:,:,:] = np.mean(v[i:i+4,:,:,:],0)
    if days == 29:
        v_out = v_daily[:-1,:,:,:]
    else:
        v_out = v_daily

    print 'Extracting variables successfully!'
    logging.info("Extracting variables successfully!")

    return v_out

# make plots
def visualization(E_total,E_internal,E_latent,E_geopotential,E_kinetic,output_path,year):
    print "Start making plots for the total meridional energy transport and each component."
    logging.info("Start making plots for the total meridional energy transport and each component.")
    # calculate monthly mean of total energy transport
    # unit change from tera to peta (from 1E+12 to 1E+15)

    # take latitude data from benchmark variable
    Lat = benchmark.variables['latitude'][:]

    # Plot the total meridional energy transport against the latitude
    fig1 = plt.figure()
    plt.plot(Lat,E_total_monthly_mean,'b-',label='ECMWF')
    plt.axhline(y=0, color='r',ls='--')
    #plt.hold()
    plt.title('Total Atmospheric Meridional Energy Transport %d' % (year))
    #plt.legend()
    plt.xlabel("Laitude")
    plt.xticks(np.linspace(30,90,13))
    plt.yticks(np.linspace(0,6,7))
    plt.ylabel("Meridional Energy Transport (PW)")
    #plt.show()
    fig1.savefig(output_path + os.sep + 'era%d' % (year) + os.sep + 'Meridional_Energy_total_%d.png' % (year), dpi = 400)

    # Plot the meridional internal energy transport against the latitude
    fig2 = plt.figure()
    plt.plot(Lat,E_internal_monthly_mean,'b-',label='ECMWF')
    plt.axhline(y=0, color='r',ls='--')
    #plt.hold()
    plt.title('Atmospheric Meridional Internal Energy Transport %d' % (year))
    #plt.legend()
    plt.xlabel("Laitude")
    plt.xticks(np.linspace(30,90,13))
    plt.yticks(np.linspace(0,6,7))
    plt.ylabel("Meridional Energy Transport (PW)")
    #plt.show()
    fig2.savefig(output_path + os.sep + 'era%d' % (year) + os.sep + 'Meridional_Energy_internal_%d.png' % (year), dpi = 400)

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

# pass argument to the main function
def choice_parser():
    '''
    pass command line arguments
    '''
    # define arguments
    parser = argparse.ArgumentParser(description="Choose the function")
    parser.add_argument('--mean', action = 'store_true',
                        help='function switch for calculating the temporal & spatial mean')
    #get arguments
    choices = parser.parse_args()
    return choices

# save output datasets

if __name__=="__main__":
    # calculate the time for the code execution
    start_time = tttt.time()
    # initialization
    period, index_month, Dim_level, Dim_latitude, Dim_longitude, Dim_month, Dim_period,\
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
    else:
        print '*******************************************************************'
        print '**********  calculate the stationary and transient eddy  **********'
        print '*******************************************************************'

    print 'The full pipeline of the decomposition of meridional energy transport in the atmosphere is accomplished!'
    logging.info("The full pipeline of the decomposition of meridional energy transport in the atmosphere is accomplished!")
    print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
