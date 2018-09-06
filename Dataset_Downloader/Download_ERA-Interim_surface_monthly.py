#!/usr/bin/env python
"""
Copyright Netherlands eScience Center

Function        : Download reanalysis data ERA-Interim from ECMWF archive
Author          : Yang Liu
Date            : 2018.03.15
Last update     : 2018.03.24
Description     : The code aims to download the reanalysis data from ECMWF.
                  The script is specified on surface and pressure level data.
                  Those data are used for analysis and diagnostic, rather than
                  the calculation of meridional energy transport.

                  The surface variables is from 1979 - 2016.
                  The pressure level variables are from 1994 - 1998 (5 years)

                  It is made for the dataset "ERA-Interim". But it could
                  be used to deal with other datasets from ECMWF as well
                  after small adjustment. This code is used to download single
                  variable for each independent file. Due to the request and queue
                  nature of MARS, the waiting time could be longer than combining
                  several variables for each file.
Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, ecmwfapi

Cautious!
Before execute the code, the following steps should be complete:
1. Install ECMWF Key
The key could be retrived through the link, after login: https://api.ecmwf.int/v1/key/
For Windows, the key should be placed at the user folder (for instance, C:\Users\ESLT0068\.ecmwfapirc)
2. Install client library
The ecmwfapi python library could be accessed through:
'sudo pip install https://software.ecmwf.int/wiki/download/attachments/56664858/ecmwf-api-client-python.tgz'

"""

# cpT:  [J / kg K] * [K]     = [J / kg]
# Lvq:  [J / kg] * [kg / kg] = [J / kg]
# gz in [m2 / s2] = [ kg m2 / kg s2 ] = [J / kg]

# multiply by v: [J / kg] * [m / s] => [J m / kg s]
# sum over longitudes [J m / kg s] * [ m ] = [J m2 / kg s]

# integrate over pressure: dp: [Pa] = [N m-2] = [kg m2 s-2 m-2] = [kg s-2]
# [J m2 / kg s] * [Pa] = [J m2 / kg s] * [kg / s2] = [J m2 / s3]
# and factor 1/g: [J m2 / s3] * [s2 /m2] = [J / s] = [Wat]

import os
import time as tttt
import numpy as np
from ecmwfapi import ECMWFDataServer

start_time = tttt.time()

###############################   Input zone  ######################################
# select the data category for downloading
# start year
start_year = 1979
# end year, if only 1 year, then end year should be the same as start year
end_year = 2016
# save path
sav_path = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ERAI/regression'
####################################################################################
year = np.arange(start_year,end_year+1,1)
month = np.arange(12)
print '*******************************************************************'
print '***********************   surface level   *************************'
print '*******************************************************************'
#surface
for i in year:
    server = ECMWFDataServer()
    server.retrieve({
                # Specify the ERA-Interim data archive. Don't change.
                "class": "ei",
                "dataset": "interim",
                # Specify the date of request data
                "date" : "%d0101/%d0201/%d0301/%d0401/%d0501/%d0601/%d0701/%d0801/%d0901/%d1001/%d1101/%d1201" % (i,i,i,i,i,i,i,i,i,i,i,i),
                "expver": "1",
                # in 0.75 degrees lat/lon
                "grid": "0.75/0.75",
                # pressure levels (levtype:pl), all available levels (levelist)
                #"levelist": "1",
                "levtype": "sfc",
                # all available parameters, for codes see http://apps.ecmwf.int/codes/grib/param-db
                "param": "167.128/235.128",
                "stream": "moda",
                # reanalysis (type:an), forecast (type:fc)
                "type": "an",
                # optionally restrict area to Europe (in N/W/S/E).
                # "area": "75/-20/10/60",
                # Optionally get output in NetCDF format. However, this does not work with the above request due to overlapping timestamps.
                "format" :  "netcdf",
                # set an output file name
                "target": sav_path + os.sep + 'surface'  +os.sep + "surface_monthly_075_%d_t2m_ts.nc" % (i),
                })

# pressure level
print '*******************************************************************'
print '***********************   pressure level  *************************'
print '*******************************************************************'
# diagnostic levels
# for i in year:
#     filename = "pressure_monthly_075_%d_200_500_850.nc" % (i)
#     server = ECMWFDataServer()
#     server.retrieve({
#         "class": "ei",
#         "dataset": "interim",
#         "date": "%d0101/%d0201/%d0301/%d0401/%d0501/%d0601/%d0701/%d0801/%d0901/%d1001/%d1101/%d1201" % (i,i,i,i,i,i,i,i,i,i,i,i),
#         "expver": "1",
#         "grid": "0.75/0.75",
#         "levelist": "200/500/850",
#         "levtype": "pl",
#         "param": "129.128/130.128/131.128/132.128/133.128",
#         "stream": "moda",
#         "type": "an",
#         "format" :  "netcdf",
#         "target": sav_path + os.sep + filename,
#     })

# full pressure levels


print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
