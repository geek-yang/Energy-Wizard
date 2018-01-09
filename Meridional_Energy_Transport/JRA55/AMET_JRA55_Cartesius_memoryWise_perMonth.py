#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : Quantify atmospheric meridional energy transport (JRA55)(Cartesius,memory wise)
Author          : Yang Liu
Date            : 2017.11.27
Last Update     : 2018.1.3
Description     : The code aims to calculate the atmospheric meridional energy
                  transport based on atmospheric reanalysis dataset JRA 55 from
                  JMA (Japan). The complete procedure includes the calculation of
                  geopotential on model levels, and the mass budget correction.
                  The procedure is generic and is able to adapt any atmospheric
                  reanalysis datasets, with some changes.
                  The script is specifically optimised for small memory.
Return Value    : GRIB1 data file
Dependencies    : os, time, numpy, netCDF4, sys, matplotlib
variables       : Absolute Temperature              T         [K]
                  Specific Humidity                 q         [kg/kg]
                  Surface pressure                  ps        [Pa]
                  Zonal Divergent Wind              u         [m/s]
                  Meridional Divergent Wind         v         [m/s]
		          Geopotential Height 	            z         [gpm]
Caveat!!	: The dataset is the complete dataset of JRA55 from -90N - 90N.
		  Attention should be paid when calculating the meridional grid length (dy)!
                  Direction of Axis:
                  Model Level: surface to TOA
                  Latitude: North to South (90 to -90)
                  Lontitude: West to East (0 to 360)
                  Time: 00:00 06:00 12:00 18:00 (6 hourly)

                  The dataset has 60 hybrid model levels. Starting from level 1 (Surface) to 60 (TOA).
                  Data is saved on reduced gaussian grid with the size of 320 (lat) x 640 (lon)

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
A = np.array([0.00000000E+00, 0.00000000E+00, 0.00000000E+00, 0.00000000E+00, 0.00000000E+00,
              0.00000000E+00, 0.00000000E+00, 0.00000000E+00, 1.33051011E+02, 3.64904149E+02,
              6.34602716E+02, 9.59797167E+02, 1.34768004E+03, 1.79090740E+03, 2.29484169E+03,
              2.84748478E+03, 3.46887149E+03, 4.16295646E+03, 4.89188083E+03, 5.67182424E+03,
              6.47671300E+03, 7.29746989E+03, 8.12215979E+03, 8.91408220E+03, 9.65618191E+03,
              1.03294362E+04, 1.09126384E+04, 1.13696478E+04, 1.16953716E+04, 1.18612531E+04,
              1.18554343E+04, 1.16633554E+04, 1.12854041E+04, 1.07299494E+04, 1.00146151E+04,
              9.16724704E+03, 8.22624491E+03, 7.20156898E+03, 6.08867301E+03, 4.95000000E+03,
              4.00000000E+03, 3.23000000E+03, 2.61000000E+03, 2.10500000E+03, 1.70000000E+03,
              1.37000000E+03, 1.10500000E+03, 8.93000000E+02, 7.20000000E+02, 5.81000000E+02,
              4.69000000E+02, 3.77000000E+02, 3.01000000E+02, 2.37000000E+02, 1.82000000E+02,
              1.36000000E+02, 9.70000000E+01, 6.50000000E+01, 3.90000000E+01, 2.00000000E+01,
              0.00000000E+00],dtype=float)
# reverse A
#A = A[::-1]
B = np.array([1.00000000E+00, 9.97000000E-01, 9.94000000E-01, 9.89000000E-01, 9.82000000E-01,
              9.72000000E-01, 9.60000000E-01, 9.46000000E-01, 9.26669490E-01, 9.04350959E-01,
              8.79653973E-01, 8.51402028E-01, 8.19523200E-01, 7.85090926E-01, 7.48051583E-01,
              7.09525152E-01, 6.68311285E-01, 6.24370435E-01, 5.80081192E-01, 5.34281758E-01,
              4.88232870E-01, 4.42025301E-01, 3.95778402E-01, 3.50859178E-01, 3.07438181E-01,
              2.65705638E-01, 2.25873616E-01, 1.89303522E-01, 1.55046284E-01, 1.24387469E-01,
              9.64456568E-02, 7.23664463E-02, 5.21459594E-02, 3.57005059E-02, 2.28538495E-02,
              1.33275296E-02, 6.73755092E-03, 2.48431020E-03, 1.13269915E-04, 0.00000000E+00,
              0.00000000E+00, 0.00000000E+00, 0.00000000E+00, 0.00000000E+00, 0.00000000E+00,
              0.00000000E+00, 0.00000000E+00, 0.00000000E+00, 0.00000000E+00, 0.00000000E+00,
              0.00000000E+00, 0.00000000E+00, 0.00000000E+00, 0.00000000E+00, 0.00000000E+00,
              0.00000000E+00, 0.00000000E+00, 0.00000000E+00, 0.00000000E+00, 0.00000000E+00,
              0.00000000E+00],dtype=float)
# reverse B
#B = B[::-1]

# calculate the time for the code execution
start_time = tttt.time()
####################################################################################
################################   Input zone  #####################################
datapath = '/projects/0/blueactn/reanalysis/JRA55/subdaily'
# time of the data, which concerns with the name of input
line_in = sys.stdin.readline()
input_year = int(line_in)
# starting time (year)
start_year = input_year
# Ending time, if only for 1 year, then it should be the same as starting year
end_year = input_year
# specify output path for the netCDF4 file
output_path = '/home/lwc16308/reanalysis/JRA55/output'
####################################################################################
# ==============================  Initial test   ==================================
# benchmark datasets for basic dimensions
benchmark_path = '/projects/0/blueactn/reanalysis/JRA55/subdaily'
benchmark_grbs = pygrib.open(datapath + os.sep + 'jra2000' + os.sep + 'anl_mdl.011_tmp.reg_tl319.2000010100_2000011018')
benchmark_key = benchmark_grbs.message(1)
lats, lons = benchmark_key.latlons()
latitude = lats[:,0]
longitude = lons[0,:]
benchmark_grbs.close()
# =================================================================================
###############################   stdout and log  ##################################
# Redirect all the console output to a file
sys.stdout = open(output_path + os.sep + 'console_E.out','w')
# logging level 'DEBUG' 'INFO' 'WARNING' 'ERROR' 'CRITICAL'
logging.basicConfig(filename = output_path + os.sep + 'history_E.log',
                    filemode = 'w', level = logging.DEBUG,
                    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
####################################################################################

def var_3D_key_retrieve(datapath, year, month, days, counter_surface, rounds):
    '''
    This module extracts the variables for mass correction and the computation of AMET.
    '''
    print '*******************************************************************'
    print '****************** open pygrib files - 3D fields ******************'
    print '*******************************************************************'
    print "Start retrieving datasets %d (y) - %s (m) for 3D variables" % (year,namelist_month[month-1])
    logging.info("Start retrieving 3D variables T,q,u,v,z for from %d (y) - %s (m)" % (year,namelist_month[month-1]))
    # get the base message counter for surface pressure
    counter_accumulate = counter_surface - 1
    if rounds == 0:
        # for the first 10 days
        key_10d_hgt = pygrib.open(datapath + os.sep + 'jra%d' % (year) + os.sep + 'anl_mdl.007_hgt.reg_tl319.%d%s0100_%d%s1018' %(year,namelist_month[month-1],year,namelist_month[month-1]))
        key_10d_tmp = pygrib.open(datapath + os.sep + 'jra%d' % (year) + os.sep + 'anl_mdl.011_tmp.reg_tl319.%d%s0100_%d%s1018' %(year,namelist_month[month-1],year,namelist_month[month-1]))
        key_10d_ugrd = pygrib.open(datapath + os.sep + 'jra%d' % (year) + os.sep + 'anl_mdl.033_ugrd.reg_tl319.%d%s0100_%d%s1018' %(year,namelist_month[month-1],year,namelist_month[month-1]))
        key_10d_vgrd = pygrib.open(datapath + os.sep + 'jra%d' % (year) + os.sep + 'anl_mdl.034_vgrd.reg_tl319.%d%s0100_%d%s1018' %(year,namelist_month[month-1],year,namelist_month[month-1]))
        key_10d_spfh = pygrib.open(datapath + os.sep + 'jra%d' % (year) + os.sep + 'anl_mdl.051_spfh.reg_tl319.%d%s0100_%d%s1018' %(year,namelist_month[month-1],year,namelist_month[month-1]))
        key_sp_year = pygrib.open(datapath + os.sep + 'jra_surf' + os.sep + 'anl_surf.001_pres.reg_tl319.%d010100_%d123118' %(year,year))
        print "Retrieving datasets successfully and return the variable key (1-10)!"
        logging.info("Retrieving 3D variables from %d (y) - %s (m) successfully (1-10)!" % (year,namelist_month[month-1]))
        print '*******************************************************************'
        print '********************** extract target fields **********************'
        print '*******************************************************************'
        print "Extract target fields!"
        logging.info("Extract target fields")
        z = np.zeros((40,60,Dim_latitude,Dim_longitude),dtype = float)
        T = np.zeros((40,60,Dim_latitude,Dim_longitude),dtype = float)
        u = np.zeros((40,60,Dim_latitude,Dim_longitude),dtype = float)
        v = np.zeros((40,60,Dim_latitude,Dim_longitude),dtype = float)
        q = np.zeros((40,60,Dim_latitude,Dim_longitude),dtype = float)
        sp = np.zeros((40,Dim_latitude,Dim_longitude),dtype = float)
        # get the target fields
        # the first ten days
        # reset counters
        counter_time = 0
        counter_lev = 0
        counter_message = 1
        while (counter_message <= 60*4*10):
            # take the key
            key_z = key_10d_hgt.message(counter_message)
            key_T = key_10d_tmp.message(counter_message)
            key_u = key_10d_ugrd.message(counter_message)
            key_v = key_10d_vgrd.message(counter_message)
            key_q = key_10d_spfh.message(counter_message)
            # 60 levels (0-59)
            if counter_lev == 60:
                counter_lev = 0
                counter_time = counter_time + 1
            # take the values
            z[counter_time,counter_lev,:,:] = key_z.values
            T[counter_time,counter_lev,:,:] = key_T.values
            u[counter_time,counter_lev,:,:] = key_u.values
            v[counter_time,counter_lev,:,:] = key_v.values
            q[counter_time,counter_lev,:,:] = key_q.values
            # push the counter
            counter_lev = counter_lev + 1
            counter_message = counter_message + 1
        # for surface pressure
        counter_time = 0
        while (counter_surface <= counter_accumulate + 10*4):
            key_sp = key_sp_year.message(counter_surface)
            sp[counter_time,:,:] = key_sp.values
            counter_time = counter_time + 1
            counter_surface = counter_surface + 1
        # close all the grib files
        key_10d_hgt.close()
        key_10d_tmp.close()
        key_10d_ugrd.close()
        key_10d_vgrd.close()
        key_10d_spfh.close()
        key_sp_year.close()

    # for the second 10 days
    elif rounds == 1:
        key_20d_hgt = pygrib.open(datapath + os.sep + 'jra%d' % (year) + os.sep + 'anl_mdl.007_hgt.reg_tl319.%d%s1100_%d%s2018' %(year,namelist_month[month-1],year,namelist_month[month-1]))
        key_20d_tmp = pygrib.open(datapath + os.sep + 'jra%d' % (year) + os.sep + 'anl_mdl.011_tmp.reg_tl319.%d%s1100_%d%s2018' %(year,namelist_month[month-1],year,namelist_month[month-1]))
        key_20d_ugrd = pygrib.open(datapath + os.sep + 'jra%d' % (year) + os.sep + 'anl_mdl.033_ugrd.reg_tl319.%d%s1100_%d%s2018' %(year,namelist_month[month-1],year,namelist_month[month-1]))
        key_20d_vgrd = pygrib.open(datapath + os.sep + 'jra%d' % (year) + os.sep + 'anl_mdl.034_vgrd.reg_tl319.%d%s1100_%d%s2018' %(year,namelist_month[month-1],year,namelist_month[month-1]))
        key_20d_spfh = pygrib.open(datapath + os.sep + 'jra%d' % (year) + os.sep + 'anl_mdl.051_spfh.reg_tl319.%d%s1100_%d%s2018' %(year,namelist_month[month-1],year,namelist_month[month-1]))
        key_sp_year = pygrib.open(datapath + os.sep + 'jra_surf' + os.sep + 'anl_surf.001_pres.reg_tl319.%d010100_%d123118' %(year,year))
        print "Retrieving datasets successfully and return the variable key (10-20)!"
        logging.info("Retrieving 3D variables from %d (y) - %s (m) successfully (10-20)!" % (year,namelist_month[month-1]))
        print '*******************************************************************'
        print '********************** extract target fields **********************'
        print '*******************************************************************'
        print "Extract target fields!"
        logging.info("Extract target fields")
        z = np.zeros((40,60,Dim_latitude,Dim_longitude),dtype = float)
        T = np.zeros((40,60,Dim_latitude,Dim_longitude),dtype = float)
        u = np.zeros((40,60,Dim_latitude,Dim_longitude),dtype = float)
        v = np.zeros((40,60,Dim_latitude,Dim_longitude),dtype = float)
        q = np.zeros((40,60,Dim_latitude,Dim_longitude),dtype = float)
        sp = np.zeros((40,Dim_latitude,Dim_longitude),dtype = float)
        # the second ten days
        # reset counters
        counter_time = 0
        counter_lev = 0
        counter_message = 1
        while (counter_message <= 60*4*10):
            # take the key
            key_z = key_20d_hgt.message(counter_message)
            key_T = key_20d_tmp.message(counter_message)
            key_u = key_20d_ugrd.message(counter_message)
            key_v = key_20d_vgrd.message(counter_message)
            key_q = key_20d_spfh.message(counter_message)
            # 60 levels (0-59)
            if counter_lev == 60:
                counter_lev = 0
                counter_time = counter_time + 1
            # take the values
            z[counter_time,counter_lev,:,:] = key_z.values
            T[counter_time,counter_lev,:,:] = key_T.values
            u[counter_time,counter_lev,:,:] = key_u.values
            v[counter_time,counter_lev,:,:] = key_v.values
            q[counter_time,counter_lev,:,:] = key_q.values
            # push the counter
            counter_lev = counter_lev + 1
            counter_message = counter_message + 1
        # for surface pressure
        counter_time = 0
        while (counter_surface <= counter_accumulate + 10*4):
            key_sp = key_sp_year.message(counter_surface)
            sp[counter_time,:,:] = key_sp.values
            counter_time = counter_time + 1
            counter_surface = counter_surface + 1
        # close all the grib files
        key_20d_hgt.close()
        key_20d_tmp.close()
        key_20d_ugrd.close()
        key_20d_vgrd.close()
        key_20d_spfh.close()
        key_sp_year.close()

    # for the rest of days
    else:
        # deal with the changing last day of each month
        key_30d_hgt = pygrib.open(datapath + os.sep + 'jra%d' % (year) + os.sep + 'anl_mdl.007_hgt.reg_tl319.%d%s2100_%d%s%d18' %(year,namelist_month[month-1],year,namelist_month[month-1],days))
        key_30d_tmp = pygrib.open(datapath + os.sep + 'jra%d' % (year) + os.sep + 'anl_mdl.011_tmp.reg_tl319.%d%s2100_%d%s%d18' %(year,namelist_month[month-1],year,namelist_month[month-1],days))
        key_30d_ugrd = pygrib.open(datapath + os.sep + 'jra%d' % (year) + os.sep + 'anl_mdl.033_ugrd.reg_tl319.%d%s2100_%d%s%d18' %(year,namelist_month[month-1],year,namelist_month[month-1],days))
        key_30d_vgrd = pygrib.open(datapath + os.sep + 'jra%d' % (year) + os.sep + 'anl_mdl.034_vgrd.reg_tl319.%d%s2100_%d%s%d18' %(year,namelist_month[month-1],year,namelist_month[month-1],days))
        key_30d_spfh = pygrib.open(datapath + os.sep + 'jra%d' % (year) + os.sep + 'anl_mdl.051_spfh.reg_tl319.%d%s2100_%d%s%d18' %(year,namelist_month[month-1],year,namelist_month[month-1],days))
        key_sp_year = pygrib.open(datapath + os.sep + 'jra_surf' + os.sep + 'anl_surf.001_pres.reg_tl319.%d010100_%d123118' %(year,year))
        print "Retrieving datasets successfully and return the variable key (20-end)!"
        logging.info("Retrieving 3D variables from %d (y) - %s (m) successfully (20-end)!" % (year,namelist_month[month-1]))
        print '*******************************************************************'
        print '********************** extract target fields **********************'
        print '*******************************************************************'
        print "Extract target fields!"
        logging.info("Extract target fields")
        # reserve space for target fields
        z = np.zeros(((days-20)*4,60,Dim_latitude,Dim_longitude),dtype = float)
        T = np.zeros(((days-20)*4,60,Dim_latitude,Dim_longitude),dtype = float)
        u = np.zeros(((days-20)*4,60,Dim_latitude,Dim_longitude),dtype = float)
        v = np.zeros(((days-20)*4,60,Dim_latitude,Dim_longitude),dtype = float)
        q = np.zeros(((days-20)*4,60,Dim_latitude,Dim_longitude),dtype = float)
        sp = np.zeros(((days-20)*4,Dim_latitude,Dim_longitude),dtype = float)
        # the rest of days
        # reset counters
        counter_time = 0
        counter_lev = 0
        counter_message = 1
        while (counter_message <= 60*4*(days-20)):
            # take the key
            key_z = key_30d_hgt.message(counter_message)
            key_T = key_30d_tmp.message(counter_message)
            key_u = key_30d_ugrd.message(counter_message)
            key_v = key_30d_vgrd.message(counter_message)
            key_q = key_30d_spfh.message(counter_message)
            # 60 levels (0-59)
            if counter_lev == 60:
                counter_lev = 0
                counter_time = counter_time + 1
                # take the values
            z[counter_time,counter_lev,:,:] = key_z.values
            T[counter_time,counter_lev,:,:] = key_T.values
            u[counter_time,counter_lev,:,:] = key_u.values
            v[counter_time,counter_lev,:,:] = key_v.values
            q[counter_time,counter_lev,:,:] = key_q.values
            # push the counter
            counter_lev = counter_lev + 1
            counter_message = counter_message + 1
        # for surface pressure
        counter_time = 0
        while (counter_surface <= counter_accumulate + (days-20)*4):
            key_sp = key_sp_year.message(counter_surface)
            sp[counter_time,:,:] = key_sp.values
            counter_time = counter_time + 1
            counter_surface = counter_surface + 1
        # close all the grib files
        key_30d_hgt.close()
        key_30d_tmp.close()
        key_30d_ugrd.close()
        key_30d_vgrd.close()
        key_30d_spfh.close()
        key_sp_year.close()

    # return all the fields
    return z, T, u, v, q, sp, counter_surface

def mass_correction_divergence(u,v,q,dp):
    print 'Begin the calculation of divergent verically integrated moisture flux.'
    logging.info("Begin the calculation of divergent verically integrated moisture flux.")
    # calculte the mean moisture flux for a certain month
    moisture_flux_u = u * q * dp / constant['g']
    moisture_flux_v = v * q * dp / constant['g']
    # take the vertical integral
    moisture_flux_u_int = np.sum(moisture_flux_u,1)
    moisture_flux_v_int = np.sum(moisture_flux_v,1)
    del moisture_flux_u, moisture_flux_v
    # calculate the divergence of moisture flux
    div_moisture_flux_u = np.zeros(moisture_flux_u_int.shape,dtype = float)
    div_moisture_flux_v = np.zeros(moisture_flux_v_int.shape,dtype = float)
    ######################## Attnention to the coordinate and symbol #######################
    # zonal moisture flux divergence
    for i in np.arange(len(latitude)):
        for j in np.arange(len(longitude)):
            # the longitude could be from 0 to 360 or -180 to 180, but the index remains the same
            if j == 0:
                div_moisture_flux_u[:,i,j] = (moisture_flux_u_int[:,i,j+1] - moisture_flux_u_int[:,i,-1]) / (2 * dx[i])
            elif j == (len(longitude)-1) :
                div_moisture_flux_u[:,i,j] = (moisture_flux_u_int[:,i,0] - moisture_flux_u_int[:,i,j-1]) / (2 * dx[i])
            else:
                div_moisture_flux_u[:,i,j] = (moisture_flux_u_int[:,i,j+1] - moisture_flux_u_int[:,i,j-1]) / (2 * dx[i])
    # meridional moisture flux divergence
    for i in np.arange(len(latitude)):
        if i == 0:
            div_moisture_flux_v[:,i,:] = -(moisture_flux_v_int[:,i+1,:] - moisture_flux_v_int[:,i,:]) / (2 * dy)
        elif i == (len(latitude)-1):
            div_moisture_flux_v[:,i,:] = -(moisture_flux_v_int[:,i,:] - moisture_flux_v_int[:,i-1,:]) / (2 * dy)
        else:
            div_moisture_flux_v[:,i,:] = -(moisture_flux_v_int[:,i+1,:] - moisture_flux_v_int[:,i-1,:]) / (2 * dy)
    print 'The calculation of divergent verically integrated moisture flux is finished !!'

    print 'Begin the calculation of divergent verically integrated mass flux.'
    logging.info("Begin the calculation of divergent verically integrated mass flux.")
    # calculte the mean mass flux for a certain month
    mass_flux_u = u * dp / constant['g']
    # take the vertical integral
    mass_flux_v = v * dp / constant['g']
    # take the vertical integral
    mass_flux_u_int = np.sum(mass_flux_u,1)
    mass_flux_v_int = np.sum(mass_flux_v,1)
    # save memory
    del mass_flux_u, mass_flux_v
    # calculate the divergence of moisture flux
    div_mass_flux_u = np.zeros(mass_flux_u_int.shape,dtype = float)
    div_mass_flux_v = np.zeros(mass_flux_v_int.shape,dtype = float)
    # zonal mass flux divergence
    # zonal moisture flux divergence
    for i in np.arange(len(latitude)):
        for j in np.arange(len(longitude)):
            # the longitude could be from 0 to 360 or -180 to 180, but the index remains the same
            if j == 0:
                div_mass_flux_u[:,i,j] = (mass_flux_u_int[:,i,j+1] - mass_flux_u_int[:,i,-1]) / (2 * dx[i])
            elif j == (len(longitude)-1) :
                div_mass_flux_u[:,i,j] = (mass_flux_u_int[:,i,0] - mass_flux_u_int[:,i,j-1]) / (2 * dx[i])
            else:
                div_mass_flux_u[:,i,j] = (mass_flux_u_int[:,i,j+1] - mass_flux_u_int[:,i,j-1]) / (2 * dx[i])
    # meridional mass flux divergence
    for i in np.arange(len(latitude)):
        if i == 0:
            div_mass_flux_v[:,i,:] = -(mass_flux_v_int[:,i+1,:] - mass_flux_v_int[:,i,:]) / (2 * dy)
        elif i == (len(latitude)-1):
            div_mass_flux_v[:,i,:] = -(mass_flux_v_int[:,i,:] - mass_flux_v_int[:,i-1,:]) / (2 * dy)
        else:
            div_mass_flux_v[:,i,:] = -(mass_flux_v_int[:,i+1,:] - mass_flux_v_int[:,i-1,:]) / (2 * dy)
    print 'The calculation of divergent verically integrated mass flux is finished !!'

    print 'Calculate precipitable water!!'
    logging.info("Calculate precipitable water.")
    # calculate precipitable water
    precipitable_water = q * dp / constant['g']
    # take the vertical integral
    precipitable_water_int = np.sum(precipitable_water,1)

    return div_moisture_flux_u, div_moisture_flux_v, div_mass_flux_u, div_mass_flux_v, precipitable_water_int

def meridional_energy_transport_divergence(z,T,u,v,q,dp):
    print 'Start calculating meridional energy transport on model level'
    logging.info("Start calculating meridional energy transport on model level.")
    # calculate each component of total energy
    # Internal Energy cpT
    internal_flux = constant['cp'] * v * T * dp / constant['g']
    # Latent heat Lq
    latent_flux = constant['Lv'] * v * q * dp / constant['g']
    # geopotential
    geopotential_flux = v * z * dp # * constant['g'] / constant['g']
    # kinetic energy
    kinetic_flux = v * 1/2 *(u**2 + v**2) * dp / constant['g']
    # take the vertical integral and monthly mean
    internal_flux_int = np.sum(internal_flux, 1)
    latent_flux_int = np.sum(latent_flux, 1)
    geopotential_flux_int = np.sum(geopotential_flux, 1)
    kinetic_flux_int = np.sum(kinetic_flux, 1)
    # save memory
    del internal_flux, latent_flux, geopotential_flux, kinetic_flux
    # mass correction component
    heat_flux_int = np.sum(constant['cp'] * T * dp / constant['g'],1)
    vapor_flux_int = np.sum(constant['Lv'] * q * dp / constant['g'],1)
    geo_flux_int = np.sum(z * dp,1) # * constant['g'] / constant['g']
    velocity_flux_int = np.sum(1/2 *(u**2 + v**2) * dp / constant['g'],1)

    return internal_flux_int, latent_flux_int, geopotential_flux_int, kinetic_flux_int, \
           heat_flux_int, vapor_flux_int, geo_flux_int, velocity_flux_int

# make plots
def visualization(E_total,E_internal,E_latent,E_geopotential,E_kinetic,output_path,year,month):
    print "Start making plots for the total meridional energy transport and each component."
    logging.info("Start making plots for the total meridional energy transport and each component.")
    # calculate monthly mean of total energy transport
    # unit change from tera to peta (from 1E+12 to 1E+15)
    E_total_monthly_mean = E_total/1000
    E_internal_monthly_mean = E_internal/1000
    E_latent_monthly_mean = E_latent/1000
    E_geopotential_monthly_mean = E_geopotential/1000
    E_kinetic_monthly_mean = E_kinetic/1000
    # Plot the total meridional energy transport against the latitude
    fig1 = plt.figure()
    plt.plot(latitude,E_total_monthly_mean,'b-',label='JRA55')
    plt.axhline(y=0, color='r',ls='--')
    #plt.hold()
    plt.title('Total Atmospheric Meridional Energy Transport %d%s' % (year,namelist_month[month-1]))
    #plt.legend()
    plt.xlabel("Laitude")
    plt.xticks(np.linspace(-90,90,13))
    #plt.yticks(np.linspace(0,6,7))
    plt.ylabel("Meridional Energy Transport (PW)")
    #plt.show()
    fig1.savefig(output_path + os.sep + 'pngs' + os.sep + 'AMET_JRA55_total_%d%s.png' % (year,namelist_month[month-1]), dpi = 400)
    plt.close(fig1)

    # Plot the meridional internal energy transport against the latitude
    fig2 = plt.figure()
    plt.plot(latitude,E_internal_monthly_mean,'b-',label='JRA55')
    plt.axhline(y=0, color='r',ls='--')
    #plt.hold()
    plt.title('Atmospheric Meridional Internal Energy Transport %d%s' % (year,namelist_month[month-1]))
    #plt.legend()
    plt.xlabel("Laitude")
    plt.xticks(np.linspace(-90,90,13))
    #plt.yticks(np.linspace(0,6,7))
    plt.ylabel("Meridional Energy Transport (PW)")
    #plt.show()
    fig2.savefig(output_path + os.sep + 'pngs' + os.sep + 'AMET_JRA55_internal_%d%s.png' % (year,namelist_month[month-1]), dpi = 400)
    plt.close(fig2)

    # Plot the meridional latent energy transport against the latitude
    fig3 = plt.figure()
    plt.plot(latitude,E_latent_monthly_mean,'b-',label='JRA55')
    plt.axhline(y=0, color='r',ls='--')
    #plt.hold()
    plt.title('Atmospheric Meridional Latent Energy Transport %d%s' % (year,namelist_month[month-1]))
    #plt.legend()
    plt.xlabel("Laitude")
    plt.xticks(np.linspace(-90,90,13))
    #plt.yticks(np.linspace(0,2,5))
    plt.ylabel("Meridional Energy Transport (PW)")
    #plt.show()
    fig3.savefig(output_path + os.sep + 'pngs' + os.sep + 'AMET_JRA55_latent_%d%s.png' % (year,namelist_month[month-1]), dpi = 400)
    plt.close(fig3)

    # Plot the meridional geopotential energy transport against the latitude
    fig4 = plt.figure()
    plt.plot(latitude,E_geopotential_monthly_mean,'b-',label='JRA55')
    plt.axhline(y=0, color='r',ls='--')
    #plt.hold()
    plt.title('Atmospheric Meridional Geopotential Energy Transport %d%s' % (year,namelist_month[month-1]))
    #plt.legend()
    plt.xlabel("Laitude")
    plt.xticks(np.linspace(-90,90,13))
    #plt.yticks(np.linspace(-2.5,2.0,10))
    plt.ylabel("Meridional Energy Transport (PW)")
    #plt.show()
    fig4.savefig(output_path + os.sep + 'pngs' + os.sep + 'AMET_JRA55_geopotential_%d%s.png' % (year,namelist_month[month-1]), dpi = 400)
    plt.close(fig4)

    # Plot the meridional kinetic energy transport against the latitude
    fig5 = plt.figure()
    plt.plot(latitude,E_kinetic_monthly_mean,'b-',label='JRA55')
    plt.axhline(y=0, color='r',ls='--')
    #plt.hold()
    plt.title('Atmospheric Meridional Kinetic Energy Transport %d%s' % (year,namelist_month[month-1]))
    #plt.legend()
    plt.xlabel("Laitude")
    plt.xticks(np.linspace(-90,90,13))
    #plt.yticks(np.linspace(0,0.15,6))
    plt.ylabel("Meridional Energy Transport (PW)")
    #plt.show()
    fig5.savefig(output_path + os.sep + 'pngs' + os.sep + 'AMET_JRA55_kinetic_%d%s.png' % (year,namelist_month[month-1]), dpi = 400)
    logging.info("The generation of plots for the total meridional energy transport and each component is complete!")
    plt.close(fig5)

# save output datasets
def create_netcdf_point (meridional_E_point_pool,meridional_E_internal_point_pool,
                         meridional_E_latent_point_pool,meridional_E_geopotential_point_pool,
                         meridional_E_kinetic_point_pool,uc_point_pool,vc_point_pool,output_path,year,month):
    print '*******************************************************************'
    print '*********************** create netcdf file*************************'
    print '*******************************************************************'
    logging.info("Start creating netcdf file for total meridional energy transport and each component at each grid point.")
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path + os.sep + 'point' + os.sep + 'AMET_JRA55_model_daily_%d%s_E_point.nc' % (year,namelist_month[month-1]),'w',format = 'NETCDF3_64BIT')
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
                             meridional_E_geopotential_pool, meridional_E_kinetic_pool, output_path, year, month):
    print '*******************************************************************'
    print '*********************** create netcdf file*************************'
    print '*******************************************************************'
    logging.info("Start creating netcdf files for the zonal integral of total meridional energy transport and each component.")
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path + os.sep + 'zonal_int' + os.sep + 'AMET_JRA55_model_daily_%d%s_E_zonal_int.nc' % (year,namelist_month[month-1]),'w',format = 'NETCDF3_64BIT')
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
    ######  Create time namelist matrix for variable extraction  #######
    ####################################################################
    # date and time arrangement
    # namelist of month and days for file manipulation
    namelist_month = ['01','02','03','04','05','06','07','08','09','10','11','12']
    # index of months
    period = np.arange(start_year,end_year+1,1)
    index_month = np.arange(1,13,1)
    long_month_list = np.array([1,3,5,7,8,10,12])
    leap_year_list = np.array([1976,1980,1984,1988,1992,1996,2000,2004,2008,2012,2016,2020])
    ####################################################################
    ######       Extract invariant and calculate constants       #######
    ####################################################################
    # create dimensions for saving data
    Dim_level = 60
    Dim_latitude = len(latitude)
    Dim_longitude = len(longitude)
    Dim_month = len(index_month)
    #Dim_year = len(period)
    # calculate zonal & meridional grid size on earth
    # the earth is taken as a perfect sphere, instead of a ellopsoid
    dx = 2 * np.pi * constant['R'] * np.cos(2 * np.pi * latitude / 360) / len(longitude)
    dy = np.pi * constant['R'] / (len(latitude)-1)
    ####################################################################
    ###  Create space for stroing intermediate variables and outputs ###
    ####################################################################
    # data pool for zonal integral
    meridional_E_pool = np.zeros(Dim_latitude,dtype = float)
    meridional_E_internal_pool = np.zeros(Dim_latitude,dtype = float)
    meridional_E_latent_pool = np.zeros(Dim_latitude,dtype = float)
    meridional_E_geopotential_pool = np.zeros(Dim_latitude,dtype = float)
    meridional_E_kinetic_pool = np.zeros(Dim_latitude,dtype = float)
    # data pool for grid point values
    uc_point_pool = np.zeros((Dim_latitude,Dim_longitude),dtype = float)
    vc_point_pool = np.zeros((Dim_latitude,Dim_longitude),dtype = float)
    meridional_E_point_pool = np.zeros((Dim_latitude,Dim_longitude),dtype = float)
    meridional_E_internal_point_pool = np.zeros((Dim_latitude,Dim_longitude),dtype = float)
    meridional_E_latent_point_pool = np.zeros((Dim_latitude,Dim_longitude),dtype = float)
    meridional_E_geopotential_point_pool = np.zeros((Dim_latitude,Dim_longitude),dtype = float)
    meridional_E_kinetic_point_pool = np.zeros((Dim_latitude,Dim_longitude),dtype = float)
    # loop for calculation
    for i in period:
        # set the message counter for the extraction of surface field
        counter_surface = 1
        for j in index_month:
            rounds = 0 # for the optimization of memory
            #dx = dx_benchmark
	    #dy = dy_benchmark
            # determine how many days are there in a month
            if j in long_month_list:
                days = 31
            elif j == 2:
                if i in leap_year_list:
                    days = 29
                else:
                    days = 28
            else:
                days = 30
            ####################################################################
            ###  Create space for stroing intermediate variables and outputs ###
            ####################################################################
            # data pool for mass budget correction module
            pool_div_moisture_flux_u = np.zeros((days*4,len(latitude),len(longitude)),dtype=float)
            pool_div_moisture_flux_v = np.zeros((days*4,len(latitude),len(longitude)),dtype=float)
            pool_div_mass_flux_u = np.zeros((days*4,len(latitude),len(longitude)),dtype=float)
            pool_div_mass_flux_v = np.zeros((days*4,len(latitude),len(longitude)),dtype=float)
            pool_precipitable_water = np.zeros((days*4,len(latitude),len(longitude)),dtype=float)
            pool_ps_mean = np.zeros((days*4,len(latitude),len(longitude)),dtype=float)
            # data pool for meridional energy tansport module
            pool_internal_flux_int = np.zeros((days*4,len(latitude),len(longitude)),dtype=float)
            pool_latent_flux_int = np.zeros((days*4,len(latitude),len(longitude)),dtype=float)
            pool_geopotential_flux_int = np.zeros((days*4,len(latitude),len(longitude)),dtype=float)
            pool_kinetic_flux_int = np.zeros((days*4,len(latitude),len(longitude)),dtype=float)
            # data pool for the correction of meridional energy tansport
            pool_heat_flux_int = np.zeros((days*4,len(latitude),len(longitude)),dtype=float)
            pool_vapor_flux_int = np.zeros((days*4,len(latitude),len(longitude)),dtype=float)
            pool_geo_flux_int = np.zeros((days*4,len(latitude),len(longitude)),dtype=float)
            pool_velocity_flux_int = np.zeros((days*4,len(latitude),len(longitude)),dtype=float)
            for k in np.arange(3): # devide into 3 rounds
                # extract 3D variables
                z, T, u, v, q, sp, counter_surface = var_3D_key_retrieve(datapath, i, j, days, counter_surface,k)
                # calculate delta pressure of each level
                dp = np.zeros(T.shape,dtype = float)
                for c in np.arange(60):
                    dp[:,c,:,:] = (A[c] + B[c] * sp) - (A[c+1] + B[c+1] * sp) # from surface to the TOA
                ####################################################################
                ######                Mass Correction Divergence             #######
                ####################################################################
                # for the computation of divergence terms
                div_moisture_flux_u, div_moisture_flux_v, div_mass_flux_u, div_mass_flux_v, \
                precipitable_water_int = mass_correction_divergence(u,v,q,dp)
                # save output to temporary storage
                if k == 0:
                    q_start = q[0,:,:,:]
                    sp_start = sp[0,:,:]
                    dp_start = dp[0,:,:,:]
                    pool_div_moisture_flux_u[:40,:,:] = div_moisture_flux_u
                    pool_div_moisture_flux_v[:40,:,:] = div_moisture_flux_v
                    pool_div_mass_flux_u[:40,:,:] = div_mass_flux_u
                    pool_div_mass_flux_v[:40,:,:] = div_mass_flux_v
                    pool_precipitable_water[:40,:,:] = precipitable_water_int
                    pool_ps_mean[:40,:,:] = sp
                elif k == 1:
                    pool_div_moisture_flux_u[40:80,:,:] = div_moisture_flux_u
                    pool_div_moisture_flux_v[40:80,:,:] = div_moisture_flux_v
                    pool_div_mass_flux_u[40:80,:,:] = div_mass_flux_u
                    pool_div_mass_flux_v[40:80,:,:] = div_mass_flux_v
                    pool_precipitable_water[40:80,:,:] = precipitable_water_int
                    pool_ps_mean[40:80,:,:] = sp
                else:
                    q_end = q[-1,:,:,:]
                    sp_end = sp[-1,:,:]
                    dp_end = dp[-1,:,:,:]
                    pool_div_moisture_flux_u[80:,:,:] = div_moisture_flux_u
                    pool_div_moisture_flux_v[80:,:,:] = div_moisture_flux_v
                    pool_div_mass_flux_u[80:,:,:] = div_mass_flux_u
                    pool_div_mass_flux_v[80:,:,:] = div_mass_flux_v
                    pool_precipitable_water[80:,:,:] = precipitable_water_int
                    pool_ps_mean[80:,:,:] = sp
                ####################################################################
                ######               Meridional Energy Transport             #######
                ####################################################################
                internal_flux_int, latent_flux_int, geopotential_flux_int, kinetic_flux_int,\
                heat_flux_int, vapor_flux_int, geo_flux_int, velocity_flux_int,\
                = meridional_energy_transport_divergence(z,T,u,v,q,dp)
                if k == 0:
                    pool_internal_flux_int[:40,:,:] = internal_flux_int
                    pool_latent_flux_int[:40,:,:] = latent_flux_int
                    pool_geopotential_flux_int[:40,:,:] = geopotential_flux_int
                    pool_kinetic_flux_int[:40,:,:] = kinetic_flux_int
                    pool_heat_flux_int[:40,:,:] = heat_flux_int
                    pool_vapor_flux_int[:40,:,:] = vapor_flux_int
                    pool_geo_flux_int[:40,:,:] = geo_flux_int
                    pool_velocity_flux_int[:40,:,:] = velocity_flux_int
                elif k == 1:
                    pool_internal_flux_int[40:80,:,:] = internal_flux_int
                    pool_latent_flux_int[40:80,:,:] = latent_flux_int
                    pool_geopotential_flux_int[40:80,:,:] = geopotential_flux_int
                    pool_kinetic_flux_int[40:80,:,:] = kinetic_flux_int
                    pool_heat_flux_int[40:80,:,:] = heat_flux_int
                    pool_vapor_flux_int[40:80,:,:] = vapor_flux_int
                    pool_geo_flux_int[40:80,:,:] = geo_flux_int
                    pool_velocity_flux_int[40:80,:,:] = velocity_flux_int
                else:
                    pool_internal_flux_int[80:,:,:] = internal_flux_int
                    pool_latent_flux_int[80:,:,:] = latent_flux_int
                    pool_geopotential_flux_int[80:,:,:] = geopotential_flux_int
                    pool_kinetic_flux_int[80:,:,:] = kinetic_flux_int
                    pool_heat_flux_int[80:,:,:] = heat_flux_int
                    pool_vapor_flux_int[80:,:,:] = vapor_flux_int
                    pool_geo_flux_int[80:,:,:] = geo_flux_int
                    pool_velocity_flux_int[80:,:,:] = velocity_flux_int
            ####################################################################
            ######                     Mass Correction                   #######
            ####################################################################
            # save memory
	    del z, T, u, v, q
            print 'Begin the calulation of precipitable water tendency'
            moisture_start = np.sum((q_start * dp_start), 0) # start of the current month
            moisture_end = np.sum((q_end * dp_end), 0) # end of the current month
            # compute the moisture tendency (one day has 86400s)
            moisture_tendency = (moisture_end - moisture_start) / (days*86400) / constant['g']
            print 'The calculation of precipitable water tendency is finished !!'
            # calculate evaporation minus precipitation
            E_P =  np.zeros((len(latitude),len(longitude)),dtype = float)
            E_P = moisture_tendency + np.mean(pool_div_moisture_flux_u,0) + np.mean(pool_div_moisture_flux_v,0)
            print '*******************************************************************'
            print "******  Computation of E-P on each grid point is finished   *******"
            print '*******************************************************************'
            logging.info("Computation of E-P on each grid point is finished!")
            print 'Begin the calculation of surface pressure tendency'
            sp_tendency = (sp_end - sp_start) / (days*86400) / constant['g']
            print 'The calculation of surface pressure tendency is finished !!'
            logging.info("Finish calculating the moisture tendency and surface pressure tendency")
            print "Finish calculating the moisture tendency and surface pressure tendency"
            mass_residual = np.zeros((len(latitude),len(longitude)),dtype = float)
            mass_residual = sp_tendency + constant['g'] * (np.mean(pool_div_mass_flux_u,0) + np.mean(pool_div_mass_flux_v,0)) - constant['g'] * E_P
            print '*******************************************************************'
            print "*** Computation of mass residual on each grid point is finished ***"
            print '*******************************************************************'
            logging.info("Computation of mass residual on each grid point is finished!")

            print 'Begin the calculation of barotropic correction wind.'
            # calculate barotropic correction wind
            uc = np.zeros((len(latitude),len(longitude)),dtype = float)
            vc = np.zeros((len(latitude),len(longitude)),dtype = float)
            vc = mass_residual * dy / (np.mean(pool_ps_mean,0) - constant['g'] * np.mean(pool_precipitable_water,0))
            vc[0,:] = 0 # Modification at polar points
            vc[-1,:] = 0
            for c in np.arange(len(latitude)):
                uc[c,:] = mass_residual[c,:] * dx[c] / (np.mean(pool_ps_mean[:,c,:],0) - constant['g'] * np.mean(pool_precipitable_water[:,c,:],0))
            print '********************************************************************************'
            print "*** Computation of barotropic correction wind on each grid point is finished ***"
            print '********************************************************************************'
            logging.info("Computation of barotropic correction wind on each grid point is finished!")
            ####################################################################
            ######               Meridional Energy Transport             #######
            ####################################################################
            # calculate zonal & meridional grid size on earth
            # the earth is taken as a perfect sphere, instead of a ellopsoid
            # strickly make dx at polar to be 0
            #dx[0] = 0
            #dx[-1] = 0
            # mass correction component
            correction_internal_flux_int = vc * np.mean(pool_heat_flux_int,0)
            correction_latent_flux_int = vc * np.mean(pool_vapor_flux_int,0)
            correction_geopotential_flux_int = vc * np.mean(pool_geo_flux_int,0)
            correction_kinetic_flux_int = vc * np.mean(pool_velocity_flux_int,0)
            # take the corrected energy flux at each grid point!
            meridional_E_internal_point = np.zeros((len(latitude),len(longitude)),dtype=float)
            meridional_E_latent_point = np.zeros((len(latitude),len(longitude)),dtype=float)
            meridional_E_geopotential_point = np.zeros((len(latitude),len(longitude)),dtype=float)
            meridional_E_kinetic_point = np.zeros((len(latitude),len(longitude)),dtype=float)
            meridional_E_point = np.zeros((len(latitude),len(longitude)),dtype=float)
            #!!!!!!!!!!!!!!! The unit is tera-watt (TW) !!!!!!!!!!!!!!!!!!!!!!#
            for c in np.arange(len(latitude)):
                meridional_E_internal_point[c,:] = (np.mean(pool_internal_flux_int[:,c,:],0) - correction_internal_flux_int[c,:]) * dx[c]/1e+12
                meridional_E_latent_point[c,:] = (np.mean(pool_latent_flux_int[:,c,:],0) - correction_latent_flux_int[c,:]) * dx[c]/1e+12
                meridional_E_geopotential_point[c,:] = (np.mean(pool_geopotential_flux_int[:,c,:],0) - correction_geopotential_flux_int[c,:]) * dx[c]/1e+12
                meridional_E_kinetic_point[c,:] = (np.mean(pool_kinetic_flux_int[:,c,:],0) - correction_kinetic_flux_int[c,:]) * dx[c]/1e+12
            meridional_E_point = meridional_E_internal_point + meridional_E_latent_point + meridional_E_geopotential_point + meridional_E_kinetic_point
            # take the zonal integral
            meridional_E_internal = np.zeros(len(latitude),dtype=float)
            meridional_E_latent = np.zeros(len(latitude),dtype=float)
            meridional_E_geopotential = np.zeros(len(latitude),dtype=float)
            meridional_E_kinetic = np.zeros(len(latitude),dtype=float)
            meridional_E = np.zeros(len(latitude),dtype=float)
           
	    meridional_E_internal = np.sum(meridional_E_internal_point,1)
            meridional_E_latent = np.sum(meridional_E_latent_point,1)
            meridional_E_geopotential = np.sum(meridional_E_geopotential_point,1)
            meridional_E_kinetic = np.sum(meridional_E_kinetic_point,1)
            # meridional total energy transport
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
            # make plots for monthly means
            visualization(meridional_E_pool,meridional_E_internal_pool,meridional_E_latent_pool,
                          meridional_E_geopotential_pool,meridional_E_kinetic_pool,output_path,i,j)
            # save data as netcdf file
            create_netcdf_zonal_int(meridional_E_pool,meridional_E_internal_pool,
                                    meridional_E_latent_pool,meridional_E_geopotential_pool,
                                    meridional_E_kinetic_pool,output_path,i,j)
            create_netcdf_point(meridional_E_point_pool,meridional_E_internal_point_pool,
                                meridional_E_latent_point_pool,meridional_E_geopotential_point_pool,
                                meridional_E_kinetic_point_pool,uc_point_pool,vc_point_pool,output_path,i,j)
    print 'Computation of meridional energy transport on model level for JRA55 is complete!!!'
    print 'The output is in sleep, safe and sound!!!'
    logging.info("The full pipeline of the quantification of meridional energy transport in the atmosphere is accomplished!")

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
