#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : Quantify atmospheric meridional energy transport (JRA55)(Cartesius)
Author          : Yang Liu
Date            : 2017.11.27
Last Update     : 2017.12.18
Description     : The code aims to calculate the atmospheric meridional energy
                  transport based on atmospheric reanalysis dataset JRA 55 from
                  JMA (Japan). The complete procedure includes the calculation of
                  geopotential on model levels, and the mass budget correction.
                  The procedure is generic and is able to adapt any atmospheric
                  reanalysis datasets, with some changes.
Return Value    : GRIB1 data file
Dependencies    : os, time, numpy, netCDF4, sys, matplotlib
variables       : Absolute Temperature              T         [K]
                  Specific Humidity                 q         [kg/kg]
                  Surface pressure                  ps        [Pa]
                  Zonal Divergent Wind              u         [m/s]
                  Meridional Divergent Wind         v         [m/s]
		          Geopotential Height 	            z         [gpm]
Caveat!!	    : The dataset is the complete dataset of MERRA2 from -90N - 90N.
		          Attention should be paid when calculating the meridional grid length (dy)!
                  Direction of Axis:
                  Model Level: TOA to surface
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
# starting time (year)
start_year = 1979
# Ending time, if only for 1 year, then it should be the same as starting year
end_year = 2013
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

def var_3D_key_retrieve(datapath, year, month, counter_surface):
    '''
    This module extracts the variables for mass correction and the computation of AMET.
    '''
    print '*******************************************************************'
    print '****************** open pygrib files - 3D fields ******************'
    print '*******************************************************************'
    print "Start retrieving datasets %d (y) - %s (m) for 3D variables" % (year,namelist_month[month-1])
    logging.info("Start retrieving 3D variables T,q,u,v,z for from %d (y) - %s (m)" % (year,namelist_month[month-1]))
    # determine how many days are there in a month
    # for the first 10 days
    key_10d_hgt = pygrib.open(datapath + os.sep + 'jra%d' % (year) + os.sep + 'anl_mdl.007_hgt.reg_tl319.%d%s0100_%d%s1018' %(year,namelist_month[month-1],year,namelist_month[month-1]))
    key_10d_tmp = pygrib.open(datapath + os.sep + 'jra%d' % (year) + os.sep + 'anl_mdl.011_tmp.reg_tl319.%d%s0100_%d%s1018' %(year,namelist_month[month-1],year,namelist_month[month-1]))
    key_10d_ugrd = pygrib.open(datapath + os.sep + 'jra%d' % (year) + os.sep + 'anl_mdl.033_ugrd.reg_tl319.%d%s0100_%d%s1018' %(year,namelist_month[month-1],year,namelist_month[month-1]))
    key_10d_vgrd = pygrib.open(datapath + os.sep + 'jra%d' % (year) + os.sep + 'anl_mdl.034_vgrd.reg_tl319.%d%s0100_%d%s1018' %(year,namelist_month[month-1],year,namelist_month[month-1]))
    key_10d_spfh = pygrib.open(datapath + os.sep + 'jra%d' % (year) + os.sep + 'anl_mdl.051_spfh.reg_tl319.%d%s0100_%d%s1018' %(year,namelist_month[month-1],year,namelist_month[month-1]))
    # for the second 10 days
    key_20d_hgt = pygrib.open(datapath + os.sep + 'jra%d' % (year) + os.sep + 'anl_mdl.007_hgt.reg_tl319.%d%s1100_%d%s2018' %(year,namelist_month[month-1],year,namelist_month[month-1]))
    key_20d_tmp = pygrib.open(datapath + os.sep + 'jra%d' % (year) + os.sep + 'anl_mdl.011_tmp.reg_tl319.%d%s1100_%d%s2018' %(year,namelist_month[month-1],year,namelist_month[month-1]))
    key_20d_ugrd = pygrib.open(datapath + os.sep + 'jra%d' % (year) + os.sep + 'anl_mdl.033_ugrd.reg_tl319.%d%s1100_%d%s2018' %(year,namelist_month[month-1],year,namelist_month[month-1]))
    key_20d_vgrd = pygrib.open(datapath + os.sep + 'jra%d' % (year) + os.sep + 'anl_mdl.034_vgrd.reg_tl319.%d%s1100_%d%s2018' %(year,namelist_month[month-1],year,namelist_month[month-1]))
    key_20d_spfh = pygrib.open(datapath + os.sep + 'jra%d' % (year) + os.sep + 'anl_mdl.051_spfh.reg_tl319.%d%s1100_%d%s2018' %(year,namelist_month[month-1],year,namelist_month[month-1]))
    # for the rest of days
    if month in long_month_list:
        last_day = 31
    elif month == 2:
        if year in leap_year_list:
            last_day = 29
        else:
            last_day = 28
    else:
        last_day = 30
    # deal with the changing last day of each month
    key_30d_hgt = pygrib.open(datapath + os.sep + 'jra%d' % (year) + os.sep + 'anl_mdl.007_hgt.reg_tl319.%d%s2100_%d%s%d18' %(year,namelist_month[month-1],year,namelist_month[month-1],last_day))
    key_30d_tmp = pygrib.open(datapath + os.sep + 'jra%d' % (year) + os.sep + 'anl_mdl.011_tmp.reg_tl319.%d%s2100_%d%s%d18' %(year,namelist_month[month-1],year,namelist_month[month-1],last_day))
    key_30d_ugrd = pygrib.open(datapath + os.sep + 'jra%d' % (year) + os.sep + 'anl_mdl.033_ugrd.reg_tl319.%d%s2100_%d%s%d18' %(year,namelist_month[month-1],year,namelist_month[month-1],last_day))
    key_30d_vgrd = pygrib.open(datapath + os.sep + 'jra%d' % (year) + os.sep + 'anl_mdl.034_vgrd.reg_tl319.%d%s2100_%d%s%d18' %(year,namelist_month[month-1],year,namelist_month[month-1],last_day))
    key_30d_spfh = pygrib.open(datapath + os.sep + 'jra%d' % (year) + os.sep + 'anl_mdl.051_spfh.reg_tl319.%d%s2100_%d%s%d18' %(year,namelist_month[month-1],year,namelist_month[month-1],last_day))
    print "Retrieving datasets successfully and return the variable key!"
    logging.info("Retrieving 3D variables for from %d (y) - %s (m) successfully!" % (year,namelist_month[month-1]))
    print '*******************************************************************'
    print '********************** extract target fields **********************'
    print '*******************************************************************'
    print "Extract target fields!"
    logging.info("Extract target fields")
    # reserve space for target fields
    z = np.zeros((last_day*4,60,Dim_latitude,Dim_longitude),dtype = float)
    T = np.zeros((last_day*4,60,Dim_latitude,Dim_longitude),dtype = float)
    u = np.zeros((last_day*4,60,Dim_latitude,Dim_longitude),dtype = float)
    v = np.zeros((last_day*4,60,Dim_latitude,Dim_longitude),dtype = float)
    q = np.zeros((last_day*4,60,Dim_latitude,Dim_longitude),dtype = float)
    sp = np.zeros((last_day*4,Dim_latitude,Dim_longitude),dtype = float)
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
    # the second ten days
    # reset counters
    counter_time = 4*10 # !!! time should not reset!!!
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
    # the second ten days
    # reset counters
    counter_time = 4*20 # !!! time should not reset!!!
    counter_lev = 0
    counter_message = 1
    while (counter_message <= 60*4*10):
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
    key_sp_year = pygrib.open(datapath + os.sep + 'jra_surf' + os.sep + 'anl_surf.001_pres.reg_tl319.%d010100_%d123118' %(year,year))
    counter_message = 1
    while (counter_message <= last_day*4 + counter_surface):
        key_sp = key_sp_year.message(counter_surface + counter_message)
        sp[counter_message-1,:,:] = key_sp.values
        counter_message = counter_message + 1
    # renew the surface counter for next loop (a new month)
    counter_surface = counter_surface + counter_message - 1
    # return all the fields
    return z, T, u, v, q, sp, last_day, counter_surface

def mass_correction(u,v,q,sp,dp,days):
    print 'Begin the calculation of precipitable water tendency'
    moisture_start = np.sum((q[0,:,:,:] * dp[0,:,:,:]), 0) # start of the current month
    moisture_end = np.sum((q[-1,:,:,:] * dp[-1,:,:,:]), 0) # end of the current month
    # compute the moisture tendency (one day has 86400s)
    moisture_tendency = (moisture_end - moisture_start) / (days*86400) / constant['g']
    print 'The calculation of precipitable water tendency is finished !!'
    print 'Begin the calculation of divergent verically integrated moisture flux.'
    # calculte the mean moisture flux for a certain month
    moisture_flux_u = u * q * dp / constant['g']
    moisture_flux_v = v * q * dp / constant['g']
    # take the vertical integral
    moisture_flux_u_int = np.sum(moisture_flux_u,1)
    moisture_flux_v_int = np.sum(moisture_flux_v,1)
    # calculate the divergence of moisture flux
    div_moisture_flux_u = np.zeros((days,len(latitude),len(longitude)),dtype = float)
    div_moisture_flux_v = np.zeros((days,len(latitude),len(longitude)),dtype = float)
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

    # calculate evaporation minus precipitation
    E_P =  np.zeros((len(latitude),len(longitude)),dtype = float)
    E_P = moisture_tendency + np.mean(div_moisture_flux_u,0) + np.mean(div_moisture_flux_v,0)
    print '*******************************************************************'
    print "******  Computation of E-P on each grid point is finished   *******"
    print '*******************************************************************'
    logging.info("Computation of E-P on each grid point is finished!")

    print 'Begin the calculation of surface pressure tendency'
    sp_tendency = (sp[-1,:,:] - sp[0,:,:]) / (days*86400) / constant['g']
    print 'The calculation of surface pressure tendency is finished !!'
    logging.info("Finish calculating the moisture tendency and surface pressure tendency")
    print "Finish calculating the moisture tendency and surface pressure tendency"

    print 'Begin the calculation of divergent verically integrated mass flux.'
    # calculte the mean mass flux for a certain month
    mass_flux_u = u * dp / constant['g']
    mass_flux_v = v * dp / constant['g']
    # take the vertical integral
    mass_flux_u_int = np.sum(mass_flux_u,1)
    mass_flux_v_int = np.sum(mass_flux_v,1)
    # calculate the divergence of moisture flux
    div_mass_flux_u = np.zeros((days,len(latitude),len(longitude)),dtype = float)
    div_mass_flux_v = np.zeros((days,len(latitude),len(longitude)),dtype = float)
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
    mass_residual = np.zeros((len(latitude),len(longitude)),dtype = float)
    mass_residual = sp_tendency + constant['g'] * (np.mean(div_mass_flux_u,0) + np.mean(div_mass_flux_v,0)) - constant['g'] * E_P
    print '*******************************************************************'
    print "*** Computation of mass residual on each grid point is finished ***"
    print '*******************************************************************'
    logging.info("Computation of mass residual on each grid point is finished!")

    print 'Begin the calculation of barotropic correction wind.'
    # calculate precipitable water
    precipitable_water = q * dp / constant['g']
    # take the vertical integral
    precipitable_water_int = np.sum(precipitable_water,1)
    # calculate barotropic correction wind
    uc = np.zeros((len(latitude),len(longitude)),dtype = float)
    vc = np.zeros((len(latitude),len(longitude)),dtype = float)
    vc = mass_residual * dy / (np.mean(sp,0) - constant['g'] * np.mean(precipitable_water_int,0))
    vc[0,:] = 0 # Modification at polar points
    vc[-1,:] = 0
    for i in np.arange(len(latitude)):
        uc[i,:] = mass_residual[i,:] * dx[i] / (np.mean(sp[:,i,:],0) - constant['g'] * np.mean(precipitable_water_int[:,i,:],0))
    print '********************************************************************************'
    print "*** Computation of barotropic correction wind on each grid point is finished ***"
    print '********************************************************************************'
    logging.info("Computation of barotropic correction wind on each grid point is finished!")

    return uc, vc

def meridional_energy_transport(z,T,u,v,q,dp,uc,vc):
    print 'Start calculating meridional energy transport on model level'
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
    internal_flux_int = np.mean(np.sum(internal_flux, 1),0)
    latent_flux_int = np.mean(np.sum(latent_flux, 1),0)
    geopotential_flux_int = np.mean(np.sum(geopotential_flux, 1),0)
    kinetic_flux_int = np.mean(np.sum(kinetic_flux, 1),0)
    # mass correction component
    correction_internal_flux_int = vc * np.mean(np.sum(constant['cp'] * T * dp / constant['g'],1),0)
    correction_latent_flux_int = vc * np.mean(np.sum(constant['Lv'] * q * dp / constant['g'],1),0)
    correction_geopotential_flux_int = vc * np.mean(np.sum(z * dp ,1),0) # * constant['g'] / constant['g']
    correction_kinetic_flux_int = vc * np.mean(np.sum(1/2 *(u**2 + v**2) * dp / constant['g'],1),0)
    # calculate zonal & meridional grid size on earth
    # the earth is taken as a perfect sphere, instead of a ellopsoid
    # strickly make dx at polar to be 0
    dx[0] = 0
    dx[-1] = 0
    # take the corrected energy flux at each grid point!
    meridional_E_internal_point = np.zeros((len(latitude),len(longitude)),dtype=float)
    meridional_E_latent_point = np.zeros((len(latitude),len(longitude)),dtype=float)
    meridional_E_geopotential_point = np.zeros((len(latitude),len(longitude)),dtype=float)
    meridional_E_kinetic_point = np.zeros((len(latitude),len(longitude)),dtype=float)
    meridional_E_point = np.zeros((len(latitude),len(longitude)),dtype=float)
    #!!!!!!!!!!!!!!! The unit is tera-watt (TW) !!!!!!!!!!!!!!!!!!!!!!#
    for i in np.arange(len(latitude)):
        meridional_E_internal_point[i,:] = (internal_flux_int[i,:] - correction_internal_flux_int[i,:]) * dx[i]/1e+12
        meridional_E_latent_point[i,:] = (latent_flux_int[i,:] - correction_latent_flux_int[i,:]) * dx[i]/1e+12
        meridional_E_geopotential_point[i,:] = (geopotential_flux_int[i,:] - correction_geopotential_flux_int[i,:]) * dx[i]/1e+12
        meridional_E_kinetic_point[i,:] = (kinetic_flux_int[i,:] - correction_kinetic_flux_int[i,:]) * dx[i]/1e+12
    meridional_E_point = meridional_E_internal_point + meridional_E_latent_point + meridional_E_geopotential_point + meridional_E_kinetic_point
    # take the zonal integral
    meridional_E_internal = np.zeros(len(latitude),dtype=float)
    meridional_E_latent = np.zeros(len(latitude),dtype=float)
    meridional_E_geopotential = np.zeros(len(latitude),dtype=float)
    meridional_E_kinetic = np.zeros(len(latitude),dtype=float)
    meridional_E = np.zeros(len(latitude),dtype=float)
    for i in np.arange(len(latitude)):
        meridional_E_internal[i] = np.sum(meridional_E_internal_point,1)
        meridional_E_latent[i] = np.sum(meridional_E_latent_point,1)
        meridional_E_geopotential[i] = np.sum(meridional_E_geopotential_point,1)
        meridional_E_kinetic[i] = np.sum(meridional_E_kinetic_point,1)
    # meridional total energy transport
    meridional_E = meridional_E_internal + meridional_E_latent + meridional_E_geopotential + meridional_E_kinetic
    print '*****************************************************************************'
    print "***Computation of meridional energy transport in the atmosphere is finished**"
    print "************         The result is in tera-watt (1E+12)          ************"
    print '*****************************************************************************'
    logging.info("Computation of meridional energy transport on model level is finished!")

    return meridional_E, meridional_E_internal, meridional_E_latent, meridional_E_geopotential, meridional_E_kinetic,\
    meridional_E_point, meridional_E_internal_point, meridional_E_latent_point, meridional_E_geopotential_point, meridional_E_kinetic_point

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
    plt.plot(latitude,E_total_monthly_mean,'b-',label='JRA55')
    plt.axhline(y=0, color='r',ls='--')
    #plt.hold()
    plt.title('Total Atmospheric Meridional Energy Transport %d' % (year))
    #plt.legend()
    plt.xlabel("Laitude")
    plt.xticks(np.linspace(-90,90,13))
    #plt.yticks(np.linspace(0,6,7))
    plt.ylabel("Meridional Energy Transport (PW)")
    #plt.show()
    fig1.savefig(output_path + os.sep + 'pngs' + os.sep + 'AMET_JRA55_total_%d.png' % (year), dpi = 400)

    # Plot the meridional internal energy transport against the latitude
    fig2 = plt.figure()
    plt.plot(latitude,E_internal_monthly_mean,'b-',label='JRA55')
    plt.axhline(y=0, color='r',ls='--')
    #plt.hold()
    plt.title('Atmospheric Meridional Internal Energy Transport %d' % (year))
    #plt.legend()
    plt.xlabel("Laitude")
    plt.xticks(np.linspace(-90,90,13))
    #plt.yticks(np.linspace(0,6,7))
    plt.ylabel("Meridional Energy Transport (PW)")
    #plt.show()
    fig2.savefig(output_path + os.sep + 'pngs' + os.sep + 'AMET_JRA55_internal_%d.png' % (year), dpi = 400)

    # Plot the meridional latent energy transport against the latitude
    fig3 = plt.figure()
    plt.plot(latitude,E_latent_monthly_mean,'b-',label='JRA55')
    plt.axhline(y=0, color='r',ls='--')
    #plt.hold()
    plt.title('Atmospheric Meridional Latent Energy Transport %d' % (year))
    #plt.legend()
    plt.xlabel("Laitude")
    plt.xticks(np.linspace(-90,90,13))
    #plt.yticks(np.linspace(0,2,5))
    plt.ylabel("Meridional Energy Transport (PW)")
    #plt.show()
    fig3.savefig(output_path + os.sep + 'pngs' + os.sep + 'AMET_JRA55_latent_%d.png' % (year), dpi = 400)

    # Plot the meridional geopotential energy transport against the latitude
    fig4 = plt.figure()
    plt.plot(latitude,E_geopotential_monthly_mean,'b-',label='JRA55')
    plt.axhline(y=0, color='r',ls='--')
    #plt.hold()
    plt.title('Atmospheric Meridional Geopotential Energy Transport %d' % (year))
    #plt.legend()
    plt.xlabel("Laitude")
    plt.xticks(np.linspace(-90,90,13))
    #plt.yticks(np.linspace(-2.5,2.0,10))
    plt.ylabel("Meridional Energy Transport (PW)")
    #plt.show()
    fig4.savefig(output_path + os.sep + 'pngs' + os.sep + 'AMET_JRA55_geopotential_%d.png' % (year), dpi = 400)

    # Plot the meridional kinetic energy transport against the latitude
    fig5 = plt.figure()
    plt.plot(latitude,E_kinetic_monthly_mean,'b-',label='JRA55')
    plt.axhline(y=0, color='r',ls='--')
    #plt.hold()
    plt.title('Atmospheric Meridional Kinetic Energy Transport %d' % (year))
    #plt.legend()
    plt.xlabel("Laitude")
    plt.xticks(np.linspace(-90,90,13))
    #plt.yticks(np.linspace(0,0.15,6))
    plt.ylabel("Meridional Energy Transport (PW)")
    #plt.show()
    fig5.savefig(output_path + os.sep + 'pngs' + os.sep + 'AMET_JRA55_kinetic_%d.png' % (year), dpi = 400)
    logging.info("The generation of plots for the total meridional energy transport and each component is complete!")

# save output datasets
def create_netcdf_point (meridional_E_point_pool,meridional_E_internal_point_pool,
                         meridional_E_latent_point_pool,meridional_E_geopotential_point_pool,
                         meridional_E_kinetic_point_pool,uc_point_pool,vc_point_pool,output_path,year):
    print '*******************************************************************'
    print '*********************** create netcdf file*************************'
    print '*******************************************************************'
    logging.info("Start creating netcdf file for total meridional energy transport and each component at each grid point.")
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path + os.sep + 'point' + os.sep + 'AMET_JRA55_model_daily_%d_E_point.nc' % (year),'w',format = 'NETCDF3_64BIT')
    # create dimensions for netcdf data
    month_wrap_dim = data_wrap.createDimension('month',Dim_month)
    lat_wrap_dim = data_wrap.createDimension('latitude',Dim_latitude)
    lon_wrap_dim = data_wrap.createDimension('longitude',Dim_longitude)
    # create coordinate variables for 3-dimensions
    month_wrap_var = data_wrap.createVariable('month',np.int32,('month',))
    lat_warp_var = data_wrap.createVariable('latitude',np.float32,('latitude',))
    lon_warp_var = data_wrap.createVariable('longitude',np.float32,('longitude',))
    # create the actual 3-d variable
    uc_warp_var = data_wrap.createVariable('uc',np.float32,('month','latitude','longitude'))
    vc_warp_var = data_wrap.createVariable('vc',np.float32,('month','latitude','longitude'))

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
    month_wrap_var[:] = index_month
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
                             meridional_E_geopotential_pool, meridional_E_kinetic_pool, output_path, year):
    print '*******************************************************************'
    print '*********************** create netcdf file*************************'
    print '*******************************************************************'
    logging.info("Start creating netcdf files for the zonal integral of total meridional energy transport and each component.")
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path + os.sep + 'zonal_int' + os.sep + 'AMET_JRA55_model_daily_%d_E_zonal_int.nc' % (year),'w',format = 'NETCDF3_64BIT')
    # create dimensions for netcdf data
    month_wrap_dim = data_wrap.createDimension('month',Dim_month)
    lat_wrap_dim = data_wrap.createDimension('latitude',Dim_latitude)
    # create coordinate variables for 3-dimensions
    month_wrap_var = data_wrap.createVariable('month',np.int32,('month',))
    lat_warp_var = data_wrap.createVariable('latitude',np.float32,('latitude',))
    # create the actual 3-d variable
    E_total_wrap_var = data_wrap.createVariable('E',np.float64,('month','latitude',))
    E_internal_wrap_var = data_wrap.createVariable('E_cpT',np.float64,('month','latitude',))
    E_latent_wrap_var = data_wrap.createVariable('E_Lvq',np.float64,('month','latitude',))
    E_geopotential_wrap_var = data_wrap.createVariable('E_gz',np.float64,('month','latitude',))
    E_kinetic_wrap_var = data_wrap.createVariable('E_uv2',np.float64,('month','latitude',))
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
    month_wrap_var[:] = index_month
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
    # loop for calculation
    for i in period:
        # set the message counter for the extraction of surface field
        counter_surface = 0
        for j in index_month:
            # extract 3D variables
            z, T, u, v, q, sp, days, counter_surface = var_3D_key_retrieve(datapath, i, j, counter_surface)
            # calculate delta pressure of each level
            dp = np.zeros((days*4,60,len(latitude),len(longitude)),dtype = float)
            for c in np.arange(60):
                dp[:,c,:,:] = (A[c] + B[c] * sp) - (A[c+1] + B[c+1] * sp) # from surface to the TOA
            ####################################################################
            ######                   Mass Correction                     #######
            ####################################################################
            uc, vc = mass_correction(u,v,q,sp,dp,days)
            ####################################################################
            ######               Meridional Energy Transport             #######
            ####################################################################
            meridional_E, meridional_E_internal, meridional_E_latent, meridional_E_geopotential, meridional_E_kinetic,\
            meridional_E_point, meridional_E_internal_point, meridional_E_latent_point, meridional_E_geopotential_point, meridional_E_kinetic_point\
            = meridional_energy_transport(z,T,u,v,q,dp,uc,vc)
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
    print 'Computation of meridional energy transport on model level for MERRA2 is complete!!!'
    print 'The output is in sleep, safe and sound!!!'
    logging.info("The full pipeline of the quantification of meridional energy transport in the atmosphere is accomplished!")

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
