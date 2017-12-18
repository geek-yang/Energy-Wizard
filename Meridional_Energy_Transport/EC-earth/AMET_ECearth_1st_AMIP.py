#!~/.pyenv/shims/python
"""
Copyright Netherlands eScience Center
Function        : Quantify atmospheric meridional energy transport from EC-earth (Cartesius)
Author          : Yang Liu
Date            : 2017.12.07
Last Update     : 2017.12.18
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
		          Geopotential 	                    gz        [m2/s2]
Caveat!!	    : The dataset is for the entire globe from -90N - 90N.
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
#import iris
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
sys.stdout = open('/home/lwc16308/ecearth_postproc/console_E.out','w')
# logging level 'DEBUG' 'INFO' 'WARNING' 'ERROR' 'CRITICAL'
logging.basicConfig(filename = '/home/lwc16308/ecearth_postproc/history_E.log',
                    filemode = 'w', level = logging.DEBUG,
                    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
####################################################################################

###############################   Initial test  ##################################
# create the output file for the complete message
# grbs = pygrib.open(datapath + os.sep + 'ICMSHECE3+%d_sp2gpl' % (file_time))
# namelist = open('/home/lwc16308/ecearth_postproc/message_list.txt','w')
# namelist.write('%s\n' % 'Message List of GRIB file')
# # enumerate the message
# for messenger in grbs:
#     namelist.write('%s\n' % (messenger))
# namelist.close()
####################################################################################

def var_key_retrive(file_time):
    # use pygrib to read the grib files
    print "##########################################################################"
    print "# Due to the characteristic of GRIB file, it is highly efficient to read #"
    print "# messages monotonically! Thus, for the sake of processing time,         #"
    print "#                  PLEASE DON'T RETRIVE BACKWARD!                        #"
    print "##########################################################################"

    print "Start retrieving datasets ICMSHECE and ICMGGECE for the time %d" % (file_time)
    logging.info("Start retrieving variables T,q,u,v,sp,gz for from ICMSHECE and ICMGGECE for the time %d" % (file_time))
    ICMSHECE = pygrib.open(datapath + os.sep + 'ICMSHECE3+%d_sp2gpl' % (file_time))
    ICMGGECE = pygrib.open(datapath + os.sep + 'ICMGGECE3+%d_gp' % (file_time))
    print "Retrieving datasets successfully and return the key!"
    # extract the basic information about the dataset
    num_message_SH = ICMSHECE.messages
    num_message_GG = ICMGGECE.messages
    # number of days in this month
    days = (num_message_GG/136+1)/8 # no 00:00:00 at each year
    # number of records
    num_record = num_message_GG/136
    # get the first message
    first_message = ICMGGECE.message(1)
    # extract the latitudes and longitudes
    lats, lons = first_message.latlons()
    latitude = lats[:,0]
    longitude = lons[0,:]
    print "===================================================="
    print "==============  Output Data Profile  ==============="
    print "There are %d messages included in the spectral field" % (num_message_SH)
    print "There are %d messages included in the Gaussian grid" % (num_message_GG)
    print "There are %d days in this month (%d)" % (days,file_time)
    print "===================================================="
    logging.info("Retrieving variables for %d successfully!" % (file_time))
    return ICMSHECE, ICMGGECE, num_message_SH, num_message_GG, num_record, days, latitude, longitude

# make plots
def visualization(E_total,E_internal,E_latent,E_geopotential,E_kinetic,output_path,filename):
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
    plt.plot(latitude,E_total_monthly_mean,'b-',label='EC-earth')
    plt.axhline(y=0, color='r',ls='--')
    #plt.hold()
    plt.title('Total Atmospheric Meridional Energy Transport %d' % (filename))
    #plt.legend()
    plt.xlabel("Laitude")
    plt.xticks(np.linspace(-90,90,13))
    #plt.yticks(np.linspace(0,6,7))
    plt.ylabel("Meridional Energy Transport (PW)")
    #plt.show()
    fig1.savefig(output_path + os.sep + 'pngs' + os.sep + 'AMET_EC-earth_total_%d.png' % (filename), dpi = 400)

    # Plot the meridional internal energy transport against the latitude
    fig2 = plt.figure()
    plt.plot(latitude,E_internal_monthly_mean,'b-',label='EC-earth')
    plt.axhline(y=0, color='r',ls='--')
    #plt.hold()
    plt.title('Atmospheric Meridional Internal Energy Transport %d' % (filename))
    #plt.legend()
    plt.xlabel("Laitude")
    plt.xticks(np.linspace(-90,90,13))
    #plt.yticks(np.linspace(0,6,7))
    plt.ylabel("Meridional Energy Transport (PW)")
    #plt.show()
    fig2.savefig(output_path + os.sep + 'pngs' + os.sep + 'AMET_EC-earth_internal_%d.png' % (filename), dpi = 400)

    # Plot the meridional latent energy transport against the latitude
    fig3 = plt.figure()
    plt.plot(latitude,E_latent_monthly_mean,'b-',label='EC-earth')
    plt.axhline(y=0, color='r',ls='--')
    #plt.hold()
    plt.title('Atmospheric Meridional Latent Energy Transport %d' % (filename))
    #plt.legend()
    plt.xlabel("Laitude")
    plt.xticks(np.linspace(-90,90,13))
    #plt.yticks(np.linspace(0,2,5))
    plt.ylabel("Meridional Energy Transport (PW)")
    #plt.show()
    fig3.savefig(output_path + os.sep + 'pngs' + os.sep + 'AMET_EC-earth_latent_%d.png' % (filename), dpi = 400)

    # Plot the meridional geopotential energy transport against the latitude
    fig4 = plt.figure()
    plt.plot(latitude,E_geopotential_monthly_mean,'b-',label='EC-earth')
    plt.axhline(y=0, color='r',ls='--')
    #plt.hold()
    plt.title('Atmospheric Meridional Geopotential Energy Transport %d' % (filename))
    #plt.legend()
    plt.xlabel("Laitude")
    plt.xticks(np.linspace(-90,90,13))
    #plt.yticks(np.linspace(-2.5,2.0,10))
    plt.ylabel("Meridional Energy Transport (PW)")
    #plt.show()
    fig4.savefig(output_path + os.sep + 'pngs' + os.sep + 'AMET_EC-earth_geopotential_%d.png' % (filename), dpi = 400)

    # Plot the meridional kinetic energy transport against the latitude
    fig5 = plt.figure()
    plt.plot(latitude,E_kinetic_monthly_mean,'b-',label='EC-earth')
    plt.axhline(y=0, color='r',ls='--')
    #plt.hold()
    plt.title('Atmospheric Meridional Kinetic Energy Transport %d' % (filename))
    #plt.legend()
    plt.xlabel("Laitude")
    plt.xticks(np.linspace(-90,90,13))
    #plt.yticks(np.linspace(0,0.15,6))
    plt.ylabel("Meridional Energy Transport (PW)")
    #plt.show()
    fig5.savefig(output_path + os.sep + 'pngs' + os.sep + 'AMET_EC-earth_kinetic_%d.png' % (filename), dpi = 400)
    logging.info("The generation of plots for the total meridional energy transport and each component is complete!")

# save output datasets
def create_netcdf_point (meridional_E_point_pool,meridional_E_internal_point_pool,
                         meridional_E_latent_point_pool,meridional_E_geopotential_point_pool,
                         meridional_E_kinetic_point_pool,uc_point_pool,vc_point_pool,output_path,filename):
    print '*******************************************************************'
    print '*********************** create netcdf file*************************'
    print '*******************************************************************'
    logging.info("Start creating netcdf file for total meridional energy transport and each component at each grid point.")
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path + os.sep + 'point' + os.sep + 'AMET_EC-earth_model_daily_%d_E_point.nc' % (filename),'w',format = 'NETCDF3_64BIT')
    # create dimensions for netcdf data
    lat_wrap_dim = data_wrap.createDimension('latitude',Dim_latitude)
    lon_wrap_dim = data_wrap.createDimension('longitude',Dim_longitude)
    # create coordinate variables for 3-dimensions
    lat_warp_var = data_wrap.createVariable('latitude',np.float32,('latitude',))
    lon_warp_var = data_wrap.createVariable('longitude',np.float32,('longitude',))
    # create the actual 3-d variable
    uc_warp_var = data_wrap.createVariable('uc',np.float32,('latitude','longitude'))
    vc_warp_var = data_wrap.createVariable('vc',np.float32,('latitude','longitude'))

    E_total_wrap_var = data_wrap.createVariable('E',np.float64,('latitude','longitude'))
    E_internal_wrap_var = data_wrap.createVariable('E_cpT',np.float64,('latitude','longitude'))
    E_latent_wrap_var = data_wrap.createVariable('E_Lvq',np.float64,('latitude','longitude'))
    E_geopotential_wrap_var = data_wrap.createVariable('E_gz',np.float64,('latitude','longitude'))
    E_kinetic_wrap_var = data_wrap.createVariable('E_uv2',np.float64,('latitude','longitude'))
    # global attributes
    data_wrap.description = 'Monthly mean meridional energy transport and each component at each grid point'
    # variable attributes
    lat_warp_var.units = 'degree_north'
    lon_warp_var.units = 'degree_east'
    uc_warp_var.units = 'm/s'
    vc_warp_var.units = 'm/s'
    E_total_wrap_var.units = 'tera watt'
    E_internal_wrap_var.units = 'tera watt'
    E_latent_wrap_var.units = 'tera watt'
    E_geopotential_wrap_var.units = 'tera watt'
    E_kinetic_wrap_var.units = 'tera watt'

    uc_warp_var.long_name = 'zonal barotropic correction wind'
    vc_warp_var.long_name = 'meridional barotropic correction wind'
    E_total_wrap_var.long_name = 'atmospheric meridional energy transport'
    E_internal_wrap_var.long_name = 'atmospheric meridional internal energy transport'
    E_latent_wrap_var.long_name = 'atmospheric meridional latent heat transport'
    E_geopotential_wrap_var.long_name = 'atmospheric meridional geopotential transport'
    E_kinetic_wrap_var.long_name = 'atmospheric meridional kinetic energy transport'
    # writing data
    lat_warp_var[:] = latitude
    lon_warp_var[:] = longitude
    uc_warp_var[:] = uc_point_pool
    vc_warp_var[:] = vc_point_pool
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
                             meridional_E_geopotential_pool, meridional_E_kinetic_pool, output_path, filename):
    print '*******************************************************************'
    print '*********************** create netcdf file*************************'
    print '*******************************************************************'
    logging.info("Start creating netcdf files for the zonal integral of total meridional energy transport and each component.")
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path + os.sep + 'zonal_int' + os.sep + 'AMET_EC-earth_model_daily_%d_E_zonal_int.nc' % (filename),'w',format = 'NETCDF3_64BIT')
    # create dimensions for netcdf data
    lat_wrap_dim = data_wrap.createDimension('latitude',Dim_latitude)
    # create coordinate variables for 3-dimensions
    lat_warp_var = data_wrap.createVariable('latitude',np.float32,('latitude',))
    # create the actual 3-d variable
    E_total_wrap_var = data_wrap.createVariable('E',np.float64,('latitude',))
    E_internal_wrap_var = data_wrap.createVariable('E_cpT',np.float64,('latitude',))
    E_latent_wrap_var = data_wrap.createVariable('E_Lvq',np.float64,('latitude',))
    E_geopotential_wrap_var = data_wrap.createVariable('E_gz',np.float64,('latitude',))
    E_kinetic_wrap_var = data_wrap.createVariable('E_uv2',np.float64,('latitude',))
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
    ######  use pygrib.open to get the key from ec-earth outputs  ######
    ####################################################################
    ICMSHECE, ICMGGECE, num_message_SH, num_message_GG, num_record, days, latitude, longitude = var_key_retrive(file_name)
    ####################################################################
    ######       Extract invariant and calculate constants       #######
    ####################################################################
    # create dimensions for saving data
    Dim_level = 91
    Dim_latitude = 512
    Dim_longitude = 1024
    # number of messages for one record
    num_SH_per = 457
    num_GG_per = 136
    # calculate zonal & meridional grid size on earth
    # the earth is taken as a perfect sphere, instead of a ellopsoid
    dx = 2 * np.pi * constant['R'] * np.cos(2 * np.pi * latitude / 360) / len(longitude)
    dy = np.pi * constant['R'] / (len(latitude)-1)
    ####################################################################
    ###  Create space for stroing intermediate variables and outputs ###
    ####################################################################
    # for climatological variables
    u = np.zeros((Dim_level,len(latitude),len(longitude)),dtype=float)
    v = np.zeros((Dim_level,len(latitude),len(longitude)),dtype=float)
    T = np.zeros((Dim_level,len(latitude),len(longitude)),dtype=float)
    gz = np.zeros((Dim_level,len(latitude),len(longitude)),dtype=float)
    sp = np.zeros((len(latitude),len(longitude)),dtype=float)
    q = np.zeros((Dim_level,len(latitude),len(longitude)),dtype=float)
    # for vertical integral
    dp = np.zeros((Dim_level,len(latitude),len(longitude)),dtype=float)
    # for tendency terms
    q_start = np.zeros((Dim_level,len(latitude),len(longitude)),dtype=float)
    q_end = np.zeros((Dim_level,len(latitude),len(longitude)),dtype=float)
    sp_start = np.zeros((len(latitude),len(longitude)),dtype=float)
    sp_end = np.zeros((len(latitude),len(longitude)),dtype=float)
    dp_start = np.zeros((Dim_level,len(latitude),len(longitude)),dtype=float)
    dp_end = np.zeros((Dim_level,len(latitude),len(longitude)),dtype=float)
    # data pool for grid point values
    uc_point_pool = np.zeros((Dim_latitude,Dim_longitude),dtype = float)
    vc_point_pool = np.zeros((Dim_latitude,Dim_longitude),dtype = float)
    meridional_E_point_pool = np.zeros((Dim_latitude,Dim_longitude),dtype = float)
    meridional_E_internal_point_pool = np.zeros((Dim_latitude,Dim_longitude),dtype = float)
    meridional_E_latent_point_pool = np.zeros((Dim_latitude,Dim_longitude),dtype = float)
    meridional_E_geopotential_point_pool = np.zeros((Dim_latitude,Dim_longitude),dtype = float)
    meridional_E_kinetic_point_pool = np.zeros((Dim_latitude,Dim_longitude),dtype = float)
    # data pool for zonal integral
    meridional_E_pool = np.zeros((Dim_latitude),dtype = float)
    meridional_E_internal_pool = np.zeros((Dim_latitude),dtype = float)
    meridional_E_latent_pool = np.zeros((Dim_latitude),dtype = float)
    meridional_E_geopotential_pool = np.zeros((Dim_latitude),dtype = float)
    meridional_E_kinetic_pool = np.zeros((Dim_latitude),dtype = float)
    ####################################################################
    ####  Create space for stroing temporary variables and outputs  ####
    ####################################################################
    # data pool for mass budget correction module
    pool_div_moisture_flux_u = np.zeros((num_record,Dim_latitude,Dim_longitude),dtype=float)
    pool_div_moisture_flux_v = np.zeros((num_record,Dim_latitude,Dim_longitude),dtype=float)
    pool_div_mass_flux_u = np.zeros((num_record,Dim_latitude,Dim_longitude),dtype=float)
    pool_div_mass_flux_v = np.zeros((num_record,Dim_latitude,Dim_longitude),dtype=float)
    pool_precipitable_water = np.zeros((num_record,Dim_latitude,Dim_longitude),dtype=float)
    pool_sp = np.zeros((num_record,Dim_latitude,Dim_longitude),dtype=float)
    # data pool for meridional energy tansport module
    pool_internal_flux_int = np.zeros((num_record,Dim_latitude,Dim_longitude),dtype=float)
    pool_latent_flux_int = np.zeros((num_record,Dim_latitude,Dim_longitude),dtype=float)
    pool_geopotential_flux_int = np.zeros((num_record,Dim_latitude,Dim_longitude),dtype=float)
    pool_kinetic_flux_int = np.zeros((num_record,Dim_latitude,Dim_longitude),dtype=float)
    # data pool for the correction of meridional energy tansport
    pool_heat_flux_int = np.zeros((num_record,Dim_latitude,Dim_longitude),dtype=float)
    pool_vapor_flux_int = np.zeros((num_record,Dim_latitude,Dim_longitude),dtype=float)
    pool_geo_flux_int = np.zeros((num_record,Dim_latitude,Dim_longitude),dtype=float)
    pool_velocity_flux_int = np.zeros((num_record,Dim_latitude,Dim_longitude),dtype=float)
    ###############################################################################
    ###  extract variables and calculate the vertical integrated zonal integral ###
    ###############################################################################
    # create a message iterator
    index_SH = 2
    index_GG = 35 # the first message is already read
    for i in np.arange(num_record):
        ################################################################
        ######       Get all the variables - spectral field      #######
        ################################################################
        # for the variables on the spectral fields
        while (index_SH <= (92+i*num_SH_per)):
            key_u = ICMSHECE.message(index_SH)
            u[index_SH-2-i*num_SH_per,:,:] = key_u.values
            index_SH = index_SH + 1
        while (index_SH <= (183+i*num_SH_per)):
            key_v = ICMSHECE.message(index_SH)
            v[index_SH-93-i*num_SH_per,:,:] = key_v.values
            index_SH = index_SH + 1
        while (index_SH <= (274+i*num_SH_per)):
            key_T = ICMSHECE.message(index_SH)
            T[index_SH-184-i*num_SH_per,:,:] = key_T.values
            index_SH = index_SH + 1
        while (index_SH <= (365+i*num_SH_per)):
            key_gz = ICMSHECE.message(index_SH)
            gz[index_SH-275-i*num_SH_per,:,:] = key_gz.values
            index_SH = index_SH + 1
        # jump the vertical velocity, now index_SH is 366 + i x 475
        index_SH = index_SH + 91
        # jump the lograithm of surface pressure (2 records)
        index_SH = index_SH + 2
        print "Retrieving datasets on the spectral fields successfully for the %d record!" % (i+1)
        logging.info("Retrieving variables on the spectral fields for the %d record successfully!" % (i+1))
        ############################################################
        ######       Get all the fields - Gaussian grid      #######
        ############################################################
        while (index_GG <= (125+i*num_GG_per)):
            key_q = ICMGGECE.message(index_GG)
            q[index_GG-35-i*num_GG_per,:,:] = key_q.values
            index_GG = index_GG + 1
        key_sp = ICMGGECE.message(index_GG)
        sp = key_sp.values
        # jump the other variables that are not relevant
        index_GG = index_GG + 45
        print "Retrieving datasets on the Gaussian grid successfully for the %d record!" % (i+1)
        logging.info("Retrieving variables on the Gaussian grid for the %d record successfully!" % (i+1))
        ############################################################
        ######    for the computation of tendency terms      #######
        ############################################################
        if i==0:
            q_start = q
            sp_start = sp
        elif i==(num_record-1):
            q_end = q
            sp_end = sp
        ############################################################
        ######       calculate flux (vertical integral)      #######
        ######           meridional energy transport         #######
        ############################################################
        # use matrix A and B to calculate dp based on half pressure level
        index_level = np.arange(Dim_level)
        for j in index_level:
            dp[j,:,:] = (A[j+1] + B[j+1] * sp) - (A[j] + B[j] * sp)
        # calculate each component of total energy
        # take the vertical integral
        # variables for correction
        # Internal Energy cpT
        internal_flux = constant['cp'] * v * T * dp / constant['g']
        internal_flux_int = np.sum(internal_flux,0)
        # Latent heat Lq
        latent_flux = constant['Lv'] * v * q * dp / constant['g']
        latent_flux_int = np.sum(latent_flux,0)
        # geopotential gz
        geopotential_flux = v * gz * dp / constant['g']
        geopotential_flux_int = np.sum(geopotential_flux,0)
        # kinetic energy
        kinetic_flux = v * 1/2 *(u**2 + v**2) * dp / constant['g']
        kinetic_flux_int = np.sum(kinetic_flux,0)
        # variables for correction
        # for the correction of Internal Energy cpT
        heat_flux = constant['cp'] * T * dp / constant['g']
        heat_flux_int = np.sum(heat_flux,0)
        # for the correction of Latent Heat flux Lq
        vapor_flux = constant['Lv'] * q* dp / constant['g']
        vapor_flux_int = np.sum(vapor_flux,0)
        # for the correction of Geopotential flux gz
        geo_flux = gz * dp / constant['g']
        geo_flux_int = np.sum(geo_flux,0)
        # for the correction of Kinetic Energy flux u2
        velocity_flux = 1/2 *(u**2 + v**2) * dp / constant['g']
        velocity_flux_int = np.sum(velocity_flux,0)
        print 'Complete calculating meridional energy transport on model level'
        # save the divergence terms to the warehouse
        pool_internal_flux_int[i,:,:] = internal_flux_int
        pool_latent_flux_int[i,:,:] = latent_flux_int
        pool_geopotential_flux_int[i,:,:] = geopotential_flux_int
        pool_kinetic_flux_int[i,:,:] = kinetic_flux_int
        # variables for the correction of each energy component
        pool_heat_flux_int[i,:,:] = heat_flux_int
        pool_vapor_flux_int[i,:,:] = vapor_flux_int
        pool_geo_flux_int[i,:,:] = geo_flux_int
        pool_velocity_flux_int[i,:,:] = velocity_flux_int
        ############################################################
        ######       calculate flux (vertical integral)      #######
        ######             mass budget correction            #######
        ############################################################
        print 'Begin the calculation of divergent verically integrated moisture flux.'
        # calculte the mean moisture flux for a certain month
        moisture_flux_u = u * q * dp / constant['g']
        moisture_flux_v = v * q * dp / constant['g']
        # take the vertical integral
        moisture_flux_u_int = np.sum(moisture_flux_u,0)
        moisture_flux_v_int = np.sum(moisture_flux_v,0)
        # save memory
        #del moisture_flux_u, moisture_flux_v
        # calculate the divergence of moisture flux
        div_moisture_flux_u = np.zeros((Dim_latitude,Dim_longitude),dtype = float)
        div_moisture_flux_v = np.zeros((Dim_latitude,Dim_longitude),dtype = float)
        ######################## Attnention to the coordinate and symbol #######################
        # zonal moisture flux divergence
        for j in np.arange(Dim_latitude):
            for k in np.arange(Dim_longitude):
                # the longitude could be from 0 to 360 or -180 to 180, but the index remains the same
                if k == 0:
                    div_moisture_flux_u[j,k] = (moisture_flux_u_int[j,k+1] - moisture_flux_u_int[j,-1]) / (2 * dx[j])
                elif k == (Dim_longitude-1) :
                    div_moisture_flux_u[j,k] = (moisture_flux_u_int[j,0] - moisture_flux_u_int[j,k-1]) / (2 * dx[j])
                else:
                    div_moisture_flux_u[j,k] = (moisture_flux_u_int[j,k+1] - moisture_flux_u_int[j,k-1]) / (2 * dx[j])
        # meridional moisture flux divergence
        # the latitude is from 90N to -90S
        for j in np.arange(Dim_latitude):
            if j == 0:
                div_moisture_flux_v[j,:] = -(moisture_flux_v_int[j+1,:] - moisture_flux_v_int[j,:]) / (2 * dy)
            elif j == (Dim_latitude-1):
                div_moisture_flux_v[j,:] = -(moisture_flux_v_int[j,:] - moisture_flux_v_int[j-1,:]) / (2 * dy)
            else:
                div_moisture_flux_v[j,:] = -(moisture_flux_v_int[j+1,:] - moisture_flux_v_int[j-1,:]) / (2 * dy)
        print 'The calculation of divergent verically integrated moisture flux is finished !!'
        # save the divergence terms to the warehouse
        pool_div_moisture_flux_u[i,:,:] = div_moisture_flux_u
        pool_div_moisture_flux_v[i,:,:] = div_moisture_flux_v
        ########################################################################
        print 'Begin the calculation of divergent verically integrated mass flux.'
        # calculate the mass flux
        mass_flux_u = u * dp / constant['g']
        mass_flux_v = v * dp / constant['g']
        # take the vertical integral
        mass_flux_u_int = np.sum(mass_flux_u,0)
        mass_flux_v_int = np.sum(mass_flux_v,0)
        # calculate the divergence of moisture flux
        div_mass_flux_u = np.zeros((Dim_latitude,Dim_longitude),dtype = float)
        div_mass_flux_v = np.zeros((Dim_latitude,Dim_longitude),dtype = float)
        # zonal mass flux divergence
        for j in np.arange(Dim_latitude):
            for k in np.arange(Dim_longitude):
                # the longitude could be from 0 to 360 or -180 to 180, but the index remains the same
                if k == 0:
                    div_mass_flux_u[j,k] = (mass_flux_u_int[j,k+1] - mass_flux_u_int[j,-1]) / (2 * dx[j])
                elif k == (Dim_longitude-1) :
                    div_mass_flux_u[j,k] = (mass_flux_u_int[j,0] - mass_flux_u_int[j,k-1]) / (2 * dx[j])
                else:
                    div_mass_flux_u[j,k] = (mass_flux_u_int[j,k+1] - mass_flux_u_int[j,k-1]) / (2 * dx[j])
        # meridional mass flux divergence
        for j in np.arange(Dim_latitude):
            if j == 0:
                div_mass_flux_v[j,:] = -(mass_flux_v_int[j+1,:] - mass_flux_v_int[j,:]) / (2 * dy)
            elif j == (Dim_latitude-1):
                div_mass_flux_v[j,:] = -(mass_flux_v_int[j,:] - mass_flux_v_int[j-1,:]) / (2 * dy)
            else:
                div_mass_flux_v[j,:] = -(mass_flux_v_int[j+1,:] - mass_flux_v_int[j-1,:]) / (2 * dy)
        print 'The calculation of divergent verically integrated mass flux is finished !!'
        # save the divergence terms to the warehouse
        pool_div_mass_flux_u[i,:,:] = div_mass_flux_u
        pool_div_mass_flux_v[i,:,:] = div_mass_flux_v
        ########################################################################
        # calculate precipitable water
        precipitable_water = q * dp / constant['g']
        precipitable_water_int = np.sum(precipitable_water,0)
        pool_precipitable_water[i,:,:] = precipitable_water_int
        # surface pressure for further mean comp
        pool_sp[i,:,:] = sp
    print "====================================================================="
    print " The extraction of variables and the computation of terms are done!! "
    print "====================================================================="
    # now we can close the grib files
    ICMSHECE.close()
    ICMGGECE.close()
    ############################################################
    ###########            mass correction           ###########
    ############################################################
    # calculate tendency terms
    # use matrix A and B to calculate dp based on half pressure level
    for j in index_level:
        dp_start[j,:,:] = (A[j+1] + B[j+1] * sp_start) - (A[j] + B[j] * sp_start)
        dp_end[j,:,:] = (A[j+1] + B[j+1] * sp_end) - (A[j] + B[j] * sp_end)
    print 'Begin the calculation of precipitable water tendency'
    moisture_start = np.sum((q_start * dp_start), 0) # start of the current month
    moisture_end = np.sum((q_end * dp_end), 0) # end of the current month
    # compute the moisture tendency (one day has 86400s)
    moisture_tendency = (moisture_end - moisture_start) / (days*86400) / constant['g']
    print 'The calculation of precipitable water tendency is finished !!'
    print 'Begin the calculation of surface pressure tendency'
    sp_tendency = (sp_end - sp_start) / (days*86400) / constant['g']
    print 'The calculation of surface pressure tendency is finished !!'
    logging.info("Finish calculating the moisture tendency and surface pressure tendency")
    print "Finish calculating the moisture tendency and surface pressure tendency"
    # calculate the bartropic correction wind velocity
    E_P = moisture_tendency + np.mean(pool_div_moisture_flux_u,0) +np.mean(pool_div_moisture_flux_v,0)
    print '*******************************************************************'
    print "******  Computation of E-P on each grid point is finished   *******"
    print '*******************************************************************'
    logging.info("Computation of E-P on each grid point is finished!")
    # calculate the mass residual
    mass_residual = sp_tendency + constant['g'] * (np.mean(pool_div_mass_flux_u,0) +\
                    np.mean(pool_div_mass_flux_v,0)) - constant['g'] * E_P
    print '*******************************************************************'
    print "*** Computation of mass residual on each grid point is finished ***"
    print '*******************************************************************'
    logging.info("Computation of mass residual on each grid point is finished!")
    # calculate barotropic correction wind
    print 'Begin the calculation of barotropic correction wind.'
    uc = np.zeros((Dim_latitude,Dim_longitude),dtype = float)
    vc = np.zeros((Dim_latitude,Dim_longitude),dtype = float)
    vc = mass_residual * dy / (np.mean(pool_sp,0) - constant['g'] * np.mean(pool_precipitable_water,0))
    # extra modification for points at polor mesh
    vc[0,:] = 0
    vc[-1,:] = 0
    for c in np.arange(Dim_latitude):
        uc[c,:] = mass_residual[c,:] * dx[c] / (np.mean(pool_sp[:,c,:],0) - constant['g'] * np.mean(pool_precipitable_water[:,c,:],0))
    print '********************************************************************************'
    print "*** Computation of barotropic correction wind on each grid point is finished ***"
    print '********************************************************************************'
    logging.info("Computation of barotropic correction wind on each grid point is finished!")
    ####################################################################
    ##########           Meridional Energy Transport          ##########
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
    for c in np.arange(Dim_latitude):
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
    #######              Final Data Wrapping (NetCDF)            #######
    ####################################################################
    # save the total meridional energy and each component to the data pool
    meridional_E_pool = meridional_E
    meridional_E_internal_pool = meridional_E_internal
    meridional_E_latent_pool = meridional_E_latent
    meridional_E_geopotential_pool = meridional_E_geopotential
    meridional_E_kinetic_pool = meridional_E_kinetic
    # save uc and vc to the data pool
    uc_point_pool = uc
    vc_point_pool = vc
    # save the meridional energy on each grid point to the data pool
    meridional_E_point_pool = meridional_E_point
    meridional_E_internal_point_pool = meridional_E_internal_point
    meridional_E_latent_point_pool = meridional_E_latent_point
    meridional_E_geopotential_point_pool = meridional_E_geopotential_point
    meridional_E_kinetic_point_pool = meridional_E_kinetic_point
    ####################################################################
    # make plots for monthly means
    visualization(meridional_E_pool,meridional_E_internal_pool,meridional_E_latent_pool,
                  meridional_E_geopotential_pool,meridional_E_kinetic_pool,output_path,file_name)
    # save data as netcdf file
    create_netcdf_zonal_int(meridional_E_pool,meridional_E_internal_pool,
                            meridional_E_latent_pool,meridional_E_geopotential_pool,
                            meridional_E_kinetic_pool,output_path,file_name)
    create_netcdf_point(meridional_E_point_pool,meridional_E_internal_point_pool,
                        meridional_E_latent_point_pool,meridional_E_geopotential_point_pool,
                        meridional_E_kinetic_point_pool,uc_point_pool,vc_point_pool,output_path,file_name)
    print 'Computation of meridional energy transport on model level for ERA-Interim is complete!!!'
    print 'The output is in sleep, safe and sound!!!'
    logging.info("The full pipeline of the quantification of meridional energy transport in the atmosphere is accomplished!")

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
