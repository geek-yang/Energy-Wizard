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
                  Surface pressure                  ps        [Pa]
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
