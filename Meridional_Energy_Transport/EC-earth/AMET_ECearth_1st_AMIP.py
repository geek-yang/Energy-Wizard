#!~/.pyenv/shims/python
"""
Copyright Netherlands eScience Center
Function        : Quantify atmospheric meridional energy transport from EC-earth (Cartesius)
Author          : Yang Liu
Date            : 2017.12.07
Last Update     : 2017.12.13
Description     : The code aims to calculate the atmospheric meridional energy
                  transport based on the output from EC-Earth simulation.
                  The complete procedure includes the calculation of the mass budget
                  correction and the computation of vertical integral of zonally
                  integrated meridional energy transport.
Return Value    : GRIB1 data file
Dependencies    : os, time, numpy, netCDF4, sys, matplotlib, pygrib
variables       : Absolute Temperature              T         [K]
                  Specific Humidity                 q         [kg/kg]
                  Surface pressure                  sp        [Pa]
                  Zonal Divergent Wind              u         [m/s]
                  Meridional Divergent Wind         v         [m/s]
                  Geopotential                      gz        [m2/s2]
Caveat!!        : The dataset is for the entire globe from -90N - 90N.
                  The model uses TL511 spectral resolution with N256 Gaussian Grid.
                  For postprocessing, the spectral fields will be converted to grid.
                  The spatial resolution of Gaussian grid is 512 (lat) x 1024 (lon)
                  It uses hybrid vertical levels and has 91 vertical levels.
                  The simulation starts from 00:00:00 01-01-1979.
                  The time step in the dataset is 3 hours.
                  00:00 03:00 06:00 09:00 12:00 15:00 18:00 21:00
                  The dataset has 91 hybrid model levels. Starting from level 1 (TOA) to 91 (Surface).
                  Data is saved on reduced gaussian grid with the size of 512 (lat) x 1024(lon)
                  Attention should be paid when calculating the meridional grid length (dy)!
                  Direction of Axis:
                  Model Level: TOA to surface (1 to 91)
                  Latitude: South to Nouth (90 to -90)
                  Lontitude: West to East (0 to 360)
                  Mass correction is accmpolished through the correction of barotropic wind:
                  mass residual = surface pressure tendency + divergence of mass flux (u,v) - (E-P)
                  E-P = evaporation - precipitation = moisture tendency - divergence of moisture flux(u,v)
                  Due to the structure of the dataset, the mass budget correction are split into
                  two parts: 1. Quantify tendency terms in month loop
                             2. Quantify divergence terms in day loop
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
import iris
import pygrib

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
# Since there are 60 model levels, there are 61 half levels, so it is for A and B values
# the unit of A is Pa!!!!!!!!!!!!
# from surface to TOA
A = np.array([0.0, 2.00004, 3.980832, 7.387186, 12.908319, 21.413612, 33.952858,
              51.746601, 76.167656, 108.715561, 150.986023, 204.637451, 271.356506,
              352.824493, 450.685791, 566.519226, 701.813354, 857.945801, 1036.166504,
              1237.585449, 1463.16394, 1713.709595, 1989.87439, 2292.155518, 2620.898438,
              2976.302246, 3358.425781, 3767.196045, 4202.416504, 4663.776367, 5150.859863,
              5663.15625, 6199.839355, 6759.727051, 7341.469727, 7942.92627, 8564.624023,
              9208.305664, 9873.560547, 10558.881836, 11262.484375, 11982.662109, 12713.897461,
              13453.225586,14192.009766, 14922.685547, 15638.053711, 16329.560547,16990.623047,
              17613.28125, 18191.029297, 18716.96875, 19184.544922, 19587.513672, 19919.796875,
              20175.394531, 20348.916016, 20434.158203, 20426.21875, 20319.011719, 20107.03125,
              19785.357422, 19348.775391, 18798.822266, 18141.296875, 17385.595703, 16544.585938,
              15633.566406, 14665.645508, 13653.219727, 12608.383789, 11543.166992, 10471.310547,
              9405.222656, 8356.25293, 7335.164551, 6353.920898, 5422.802734, 4550.21582,
              3743.464355, 3010.146973, 2356.202637, 1784.854614, 1297.656128, 895.193542,
              576.314148, 336.772369, 162.043427, 54.208336, 6.575628, 0.00316, 0.0],dtype=float)
# reverse A
#A = A[::-1]
B = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
              0.0, 0.0, 0.0, 0.0, 0.0, 1.4e-005,
              5.5e-005, 0.000131, 0.000279, 0.000548, 0.001, 0.001701,
              0.002765, 0.004267, 0.006322, 0.009035, 0.012508, 0.01686,
              0.022189, 0.02861, 0.036227, 0.045146, 0.055474, 0.067316,
              0.080777, 0.095964, 0.112979, 0.131935, 0.152934, 0.176091,
              0.20152, 0.229315, 0.259554, 0.291993, 0.326329, 0.362203,
              0.399205, 0.436906, 0.475016, 0.51328, 0.551458, 0.589317,
              0.626559, 0.662934, 0.698224, 0.732224, 0.764679, 0.795385,
              0.824185, 0.85095, 0.875518, 0.897767, 0.917651, 0.935157,
              0.950274, 0.963007, 0.973466, 0.982238, 0.989153, 0.994204, 0.99763, 1.0],dtype=float)
# reverse B
#B = B[::-1]

# calculate the time for the code execution
start_time = tttt.time()

####################################################################################
################################   Input zone  #####################################
datapath = '/projects/0/blueactn/reanalysis/temp/'
# time of the data, which concerns with the name of input
line_in = sys.stdin.readline()
file_name = int(line_in)
# specify output path for the netCDF4 file
output_path = '/home/lwc16308/ecearth_postproc/output'
####################################################################################
###############################   stdout and log  ##################################
# Redirect all the console output to a file
sys.stdout = open('/home/lwc16308/ecearth_postproc/console_E.out')
# logging level 'DEBUG' 'INFO' 'WARNING' 'ERROR' 'CRITICAL'
logging.basicConfig(filename = '/home/lwc16308/ecearth_postproc/history_E.log',
                    filemode = 'w', level = logging.DEBUG,
                    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
####################################################################################
def var_key_retrive(file_time):
    # use pygrib to read the grib files
    print "##########################################################################"
    print "# Due to the characteristic of GRIB file, it is highly efficient to read #"
    print "# messages monotonically! Thus, for the sake of processing time,         #"
    print "#                  PLEASE DON'T RETRIVE BACKWARD!                        #"
    print "##########################################################################"
                                                    #
    print "Start retrieving datasets ICMSHECE and ICMGGECE for the time %d" % (file_time)
    logging.info("Start retrieving variables T,q,u,v,sp,gz for from ICMSHECE and ICMGGECE for the time %d" % (file_time))
    ICMSHECE = pygrib.open(datapath + os.sep + 'ICMSHECE3+%d_sp2gpl' % (file_time))
    ICMGGECE = pygrib.open(datapath + os.sep + 'ICMGGECE3+%d' % (file_time))
    print "Retrieving datasets successfully and return the key!"
    # extract the basic information about the dataset
    num_message_SH = ICMSHECE.messages
    num_message_GG = ICMGGECE.messages
    # number of days in this month
    if file_time == 197901:
        days = (num_message_GG/457+1)/8
    else:
        days = (num_message_GG/457)/8
    # get the first message
    first_message = ICMGGECE.message(1)
    # extract the latitudes and longitudes
    

    print "===================================================="
    print "==============  Output Data Profile  ==============="
    print "There are %d messages included in the spectral field" % (num_message_SH)
    print "There are %d messages included in the Gaussian grid" % (num_message_GG)
    print "There are %d days in this month (%d)" % (days,file_time)
    print "===================================================="
    logging.info("Retrieving variables for %d successfully!" % (file_time))
    return ICMSHECE, ICMGGECE, num_message_SH, num_message_GG, days, latitude



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
    ####################################################################
    ######       Extract invariant and calculate constants       #######
    ####################################################################
    # create dimensions for saving data
    Dim_level = 91
    Dim_latitude = 512
    Dim_longitude = 1024
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
    uc_point_pool = np.zeros((Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    vc_point_pool = np.zeros((Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    meridional_E_point_pool = np.zeros((Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    meridional_E_internal_point_pool = np.zeros((Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    meridional_E_latent_point_pool = np.zeros((Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    meridional_E_geopotential_point_pool = np.zeros((Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    meridional_E_kinetic_point_pool = np.zeros((Dim_month,Dim_latitude,Dim_longitude),dtype = float)
    # Initialize the variable key of the last day of the last month for the computation of tendency terms in mass correction
    year_last = start_year - 1
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
            ####################################################################
            ###  Create space for stroing intermediate variables and outputs ###
            ####################################################################
            # data pool for mass budget correction module
            pool_div_moisture_flux_u = np.zeros((len(days),len(latitude),len(longitude)),dtype=float)
            pool_div_moisture_flux_v = np.zeros((len(days),len(latitude),len(longitude)),dtype=float)
            pool_div_mass_flux_u = np.zeros((len(days),len(latitude),len(longitude)),dtype=float)
            pool_div_mass_flux_v = np.zeros((len(days),len(latitude),len(longitude)),dtype=float)
            pool_precipitable_water = np.zeros((len(days),len(latitude),len(longitude)),dtype=float)
            pool_ps_mean = np.zeros((len(days),len(latitude),len(longitude)),dtype=float)
            # data pool for meridional energy tansport module
            pool_internal_flux_int = np.zeros((len(days),len(latitude),len(longitude)),dtype=float)
            pool_latent_flux_int = np.zeros((len(days),len(latitude),len(longitude)),dtype=float)
            pool_geopotential_flux_int = np.zeros((len(days),len(latitude),len(longitude)),dtype=float)
            pool_kinetic_flux_int = np.zeros((len(days),len(latitude),len(longitude)),dtype=float)
            # data pool for the correction of meridional energy tansport
            pool_heat_flux_int = np.zeros((len(days),len(latitude),len(longitude)),dtype=float)
            pool_vapor_flux_int = np.zeros((len(days),len(latitude),len(longitude)),dtype=float)
            pool_geo_flux_int = np.zeros((len(days),len(latitude),len(longitude)),dtype=float)
            pool_velocity_flux_int = np.zeros((len(days),len(latitude),len(longitude)),dtype=float)
            # days loop
            for k in days:
                # get the key of each variable
                var_key = var_key_retrieve(datapath,i,j,k)
                ####################################################################
                ######                   Mass Correction                     #######
                ####################################################################
                # for the computation of tendency terms in the following function
                if k == days[0]:
                    var_start = var_key
                elif k == days[-1]:
                    var_end = var_key
                # calculate divergence terms and other terms in mass correction
                div_moisture_flux_u, div_moisture_flux_v, div_mass_flux_u, div_mass_flux_v, \
                precipitable_water, ps_mean = mass_correction_divergence(var_key)
                # save the divergence terms to the warehouse
                pool_div_moisture_flux_u[k,:,:] = div_moisture_flux_u
                pool_div_moisture_flux_v[k,:,:] = div_moisture_flux_v
                pool_div_mass_flux_u[k,:,:] = div_mass_flux_u
                pool_div_mass_flux_v[k,:,:] = div_mass_flux_v
                pool_precipitable_water[k,:,:] = precipitable_water
                pool_ps_mean[k,:,:] = ps_mean
                ####################################################################
                ######                       Geopotential                    #######
                ####################################################################
                # calculate the geopotential
                gz = calc_geopotential(var_key)
                ####################################################################
                ######               Meridional Energy Transport             #######
                ####################################################################
                # calculate the energy flux terms in meridional energy Transport
                internal_flux_int, latent_flux_int, geopotential_flux_int, kinetic_flux_int,\
                heat_flux_int, vapor_flux_int, geo_flux_int, velocity_flux_int = meridional_energy_transport(var_key,gz)
                # save the divergence terms to the warehouse
                pool_internal_flux_int[k,:,:] = internal_flux_int
                pool_latent_flux_int[k,:,:] = latent_flux_int
                pool_geopotential_flux_int[k,:,:] = geopotential_flux_int
                pool_kinetic_flux_int[k,:,:] = kinetic_flux_int
                # variables for the correction of each energy component
                pool_heat_flux_int[k,:,:] = heat_flux_int
                pool_vapor_flux_int[k,:,:] = vapor_flux_int
                pool_geo_flux_int[k,:,:] = geo_flux_int
                pool_velocity_flux_int[k,:,:] = velocity_flux_int
            ####################################################################
            ######                   Mass Correction                     #######
            ####################################################################
            # complete the mass correction and calculate the barotropic wind correcter
            # calculate the tendency terms in mass correction
            moisture_tendency, ps_tendency = mass_correction_tendency(datapath,i,j,var_start,var_end,var_last,days)
            # update the variable key of the last day of the last month
            var_last = var_end
            # calculate evaporation minus precipitation
            E_P = moisture_tendency + np.mean(pool_div_moisture_flux_u,0) +np.mean(pool_div_moisture_flux_v,0)
            print '*******************************************************************'
            print "******  Computation of E-P on each grid point is finished   *******"
            print '*******************************************************************'
            logging.info("Computation of E-P on each grid point is finished!")
            # calculate the mass residual
            mass_residual = ps_tendency + constant['g'] * (np.mean(pool_div_mass_flux_u,0) +\
                            np.mean(pool_div_mass_flux_v,0)) - constant['g'] * E_P
            print '*******************************************************************'
            print "*** Computation of mass residual on each grid point is finished ***"
            print '*******************************************************************'
            logging.info("Computation of mass residual on each grid point is finished!")
            # calculate barotropic correction wind
            print 'Begin the calculation of barotropic correction wind.'
            uc = np.zeros((len(latitude),len(longitude)),dtype = float)
            vc = np.zeros((len(latitude),len(longitude)),dtype = float)
            vc = mass_residual * dy / (np.mean(pool_ps_mean,0) - constant['g'] * np.mean(pool_precipitable_water,0))
            # extra modification for points at polor mesh
            #vc[0,:] = 0
            vc[-1,:] = 0
            # Here we should avoid i,j,k as counter since they are used and will still function
            for c in np.arange(len(latitude)):
                uc[c,:] = mass_residual[c,:] * dx[c] / (np.mean(pool_ps_mean[:,c,:],0) - constant['g'] * np.mean(pool_precipitable_water[:,c,:],0))
            print '********************************************************************************'
            print "*** Computation of barotropic correction wind on each grid point is finished ***"
            print '********************************************************************************'
            logging.info("Computation of barotropic correction wind on each grid point is finished!")
            ####################################################################
            ######               Meridional Energy Transport             #######
            ####################################################################
            # calculate the correction terms
            correction_internal_flux_int = vc * np.mean(pool_heat_flux_int,0)
            correction_latent_flux_int = vc * np.mean(pool_vapor_flux_int,0)
            correction_geopotential_flux_int = vc * np.mean(pool_geo_flux_int,0)
            correction_kinetic_flux_int = vc * np.mean(pool_velocity_flux_int,0)
            # calculate the total meridional energy transport and each component respectively
            # energy on grid point
            meridional_E_internal_point = np.zeros((len(latitude),len(longitude)),dtype=float)
            meridional_E_latent_point = np.zeros((len(latitude),len(longitude)),dtype=float)
            meridional_E_geopotential_point = np.zeros((len(latitude),len(longitude)),dtype=float)
            meridional_E_kinetic_point = np.zeros((len(latitude),len(longitude)),dtype=float)
            meridional_E_point = np.zeros((len(latitude),len(longitude)),dtype=float)
            for c in np.arange(len(latitude)):
                meridional_E_internal_point[c,:] = (np.mean(pool_internal_flux_int[:,c,:],0) - correction_internal_flux_int[c,:]) * dx[c]/1e+12
                meridional_E_latent_point[c,:] = (np.mean(pool_latent_flux_int[:,c,:],0) - correction_latent_flux_int[c,:]) * dx[c]/1e+12
                meridional_E_geopotential_point[c,:] = (np.mean(pool_geopotential_flux_int[:,c,:],0) - correction_geopotential_flux_int[c,:]) * dx[c]/1e+12
                meridional_E_kinetic_point[c,:] = (np.mean(pool_kinetic_flux_int[:,c,:],0) - correction_kinetic_flux_int[c,:]) * dx[c]/1e+12
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
            # save uc and vc to the data pool
            uc_point_pool[j-1,:,:] = uc
            vc_point_pool[j-1,:,:] = vc
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
                            meridional_E_kinetic_point_pool,uc_point_pool,vc_point_pool,output_path,i)
    print 'Computation of meridional energy transport on model level for ERA-Interim is complete!!!'
    print 'The output is in sleep, safe and sound!!!'
    logging.info("The full pipeline of the quantification of meridional energy transport in the atmosphere is accomplished!")
