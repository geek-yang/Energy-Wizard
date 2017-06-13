# -*- coding: utf-8 -*-
"""
Copyright Netherlands eScience Center

Function        : Download reanalysis data ERA-Interim from ECMWF archive (single variable / file)
Author          : Yang Liu
Date            : 2017.6.12
Description     : The code aims to download the reanalysis data from ECMWF.
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
import time
import numpy as np
from ecmwfapi import ECMWFDataServer

start_time = time.time()

category = {'T': 'Temperature',
            'q': 'Humidity',   # specific humidity
            'u':'Easterly',    # zonal wind velocity
            'v':'Northerly',    # meridional wind velocity
            'z':'Geopotential', # geopotential on level 1
            'lgsp' : 'LogPressure',   # log surface pressure
            'Ps':'Pressure',       # Surface pressure from surface level
            'Custom' : 'Custom'}   # for arbitary download

###############################   Input zone  ######################################
# select the data category for downloading
sel = category['Custom']
# start year
start_Y = 1980
# end year, if only 1 year, then end year should be the same as start year
end_Y = 1980
####################################################################################

def time_cal (start_y,end_y):
    Leap_Year = np.array([1980,1984,1988,1992,1996,2000,2004,2008,2012,2016])
    year =np.arange(start_y,end_y+1,1)
    date_str = {}
    for i in year:
        if i in Leap_Year:
            date_str['%s' % i] = ["%s-01-01/to/%s-01-31" % (i,i),
                                  "%s-02-01/to/%s-02-29" % (i,i),
                                  "%s-03-01/to/%s-03-31" % (i,i),
                                  "%s-04-01/to/%s-04-30" % (i,i),
                                  "%s-05-01/to/%s-05-31" % (i,i),
                                  "%s-06-01/to/%s-06-30" % (i,i),
                                  "%s-07-01/to/%s-07-31" % (i,i),
                                  "%s-08-01/to/%s-08-31" % (i,i),
                                  "%s-09-01/to/%s-09-30" % (i,i),
                                  "%s-10-01/to/%s-10-31" % (i,i),
                                  "%s-11-01/to/%s-11-30" % (i,i),
                                  "%s-12-01/to/%s-12-31" % (i,i),]
        else:
            date_str['%s' % i] = ["%s-01-01/to/%s-01-31" % (i,i),
                                  "%s-02-01/to/%s-02-28" % (i,i),
                                  "%s-03-01/to/%s-03-31" % (i,i),
                                  "%s-04-01/to/%s-04-30" % (i,i),
                                  "%s-05-01/to/%s-05-31" % (i,i),
                                  "%s-06-01/to/%s-06-30" % (i,i),
                                  "%s-07-01/to/%s-07-31" % (i,i),
                                  "%s-08-01/to/%s-08-31" % (i,i),
                                  "%s-09-01/to/%s-09-30" % (i,i),
                                  "%s-10-01/to/%s-10-31" % (i,i),
                                  "%s-11-01/to/%s-11-30" % (i,i),
                                  "%s-12-01/to/%s-12-31" % (i,i),]
    return date_str

ind_month = np.arange(12)

date_string = time_cal(start_Y,end_Y)

#if __name__ == '__main__':

sav_path = 'F:\DataBase\ERA_Interim\Subdaily\model_daily_075_1980'

if sel == 'Pressure':
    for i in date_string:
        for j in ind_month:
            server = ECMWFDataServer()

            server.retrieve({
                    # Specify the ERA-Interim data archive. Don't change.
                    "class": "ei",
                    "dataset": "interim",
                    # Specify the date of request data
                    "date" : date_string['%s' % i][j],
                    "expver": "1",
                    # in 0.75 degrees lat/lon
                    "grid": "0.75/0.75",
                    # pressure levels (levtype:pl), all available levels (levelist)
                    #"levelist": "1/2/3/4/5/6/7/8/9/10/11/12/13/14/15/16/17/18/19/20/21/22/23/24/25/26/27/28/29/30/31/32/33/34/35/36/37/38/39/40/41/42/43/44/45/46/47/48/49/50/51/52/53/54/55/56/57/58/59/60",
                    "levtype": "sfc",
                    # all available parameters, for codes see http://apps.ecmwf.int/codes/grib/param-db
                    "param": "134.128",
                    "step" : "0",
                    "stream": "oper",
                    "time" : "00:00:00/06:00:00/12:00:00/18:00:00",
                    # reanalysis (type:an), forecast (type:fc)
                    "type": "an",
                    # optionally restrict area to Europe (in N/W/S/E).
                    # "area": "75/-20/10/60",
                    # Optionally get output in NetCDF format. However, this does not work with the above request due to overlapping timestamps.
                    "format" :  "netcdf",
                    # set an output file name
                    "target": sav_path+os.sep+"model_daily_075_%s_%d_Ps.nc" % (i,j+1),
                    })


if sel == 'Temperature':
    for i in date_string:
        for j in ind_month:
            server = ECMWFDataServer()

            server.retrieve({
                    # Specify the ERA-Interim data archive. Don't change.
                    "class": "ei",
                    "dataset": "interim",
                    # Specify the date of request data
                    "date" : date_string['%s' % i][j],
                    "expver": "1",
                    # in 0.75 degrees lat/lon
                    "grid": "0.75/0.75",
                    # pressure levels (levtype:pl), all available levels (levelist)
                    "levelist": "1/2/3/4/5/6/7/8/9/10/11/12/13/14/15/16/17/18/19/20/21/22/23/24/25/26/27/28/29/30/31/32/33/34/35/36/37/38/39/40/41/42/43/44/45/46/47/48/49/50/51/52/53/54/55/56/57/58/59/60",
                    "levtype": "ml",
                    # all available parameters, for codes see http://apps.ecmwf.int/codes/grib/param-db
                    "param": "130.128",
                    "step" : "0",
                    "stream": "oper",
                    "time" : "00:00:00/06:00:00/12:00:00/18:00:00",
                    # reanalysis (type:an), forecast (type:fc)
                    "type": "an",
                    # optionally restrict area to Europe (in N/W/S/E).
                    # "area": "75/-20/10/60",
                    # Optionally get output in NetCDF format. However, this does not work with the above request due to overlapping timestamps.
                    "format" :  "netcdf",
                    # set an output file name
                    "target": sav_path+os.sep+"model_daily_075_%s_%d_T.nc" % (i,j+1),
                    })


if sel == 'Humidity':
    for i in date_string:
        for j in ind_month:
            server = ECMWFDataServer()

            server.retrieve({
                    # Specify the ERA-Interim data archive. Don't change.
                    "class": "ei",
                    "dataset": "interim",
                    # Specify the date of request data
                    "date" : date_string['%s' % i][j],
                    "expver": "1",
                    # in 0.75 degrees lat/lon
                    "grid": "0.75/0.75",
                    # pressure levels (levtype:pl), all available levels (levelist)
                    "levelist": "1/2/3/4/5/6/7/8/9/10/11/12/13/14/15/16/17/18/19/20/21/22/23/24/25/26/27/28/29/30/31/32/33/34/35/36/37/38/39/40/41/42/43/44/45/46/47/48/49/50/51/52/53/54/55/56/57/58/59/60",
                    "levtype": "ml",
                    # all available parameters, for codes see http://apps.ecmwf.int/codes/grib/param-db
                    "param": "133.128",
                    "step" : "0",
                    "stream": "oper",
                    "time" : "00:00:00/06:00:00/12:00:00/18:00:00",
                    # reanalysis (type:an), forecast (type:fc)
                    "type": "an",
                    # optionally restrict area to Europe (in N/W/S/E).
                    # "area": "75/-20/10/60",
                    # Optionally get output in NetCDF format. However, this does not work with the above request due to overlapping timestamps.
                    "format" :  "netcdf",
                    # set an output file name
                    "target": sav_path+os.sep+"model_daily_075_%s_%d_q.nc" % (i,j+1),
                    })

if sel == 'Northerly':
    for i in date_string:
        for j in ind_month:
            server = ECMWFDataServer()

            server.retrieve({
                    # Specify the ERA-Interim data archive. Don't change.
                    "class": "ei",
                    "dataset": "interim",
                    # Specify the date of request data
                    "date" : date_string['%s' % i][j],
                    "expver": "1",
                    # in 0.75 degrees lat/lon
                    "grid": "0.75/0.75",
                    # pressure levels (levtype:pl), all available levels (levelist)
                    "levelist": "1/2/3/4/5/6/7/8/9/10/11/12/13/14/15/16/17/18/19/20/21/22/23/24/25/26/27/28/29/30/31/32/33/34/35/36/37/38/39/40/41/42/43/44/45/46/47/48/49/50/51/52/53/54/55/56/57/58/59/60",
                    "levtype": "ml",
                    # all available parameters, for codes see http://apps.ecmwf.int/codes/grib/param-db
                    "param": "132.128",
                    "step" : "0",
                    "stream": "oper",
                    "time" : "00:00:00/06:00:00/12:00:00/18:00:00",
                    # reanalysis (type:an), forecast (type:fc)
                    "type": "an",
                    # optionally restrict area to Europe (in N/W/S/E).
                    # "area": "75/-20/10/60",
                    # Optionally get output in NetCDF format. However, this does not work with the above request due to overlapping timestamps.
                    "format" :  "netcdf",
                    # set an output file name
                    "target": sav_path+os.sep+"model_daily_075_%s_%d_v.nc" % (i,j+1),
                    })

if sel == 'Easterly':
    for i in date_string:
        for j in ind_month:
            server = ECMWFDataServer()

            server.retrieve({
                    # Specify the ERA-Interim data archive. Don't change.
                    "class": "ei",
                    "dataset": "interim",
                    # Specify the date of request data
                    "date" : date_string['%s' % i][j],
                    "expver": "1",
                    # in 0.75 degrees lat/lon
                    "grid": "0.75/0.75",
                    # pressure levels (levtype:pl), all available levels (levelist)
                    "levelist": "1/2/3/4/5/6/7/8/9/10/11/12/13/14/15/16/17/18/19/20/21/22/23/24/25/26/27/28/29/30/31/32/33/34/35/36/37/38/39/40/41/42/43/44/45/46/47/48/49/50/51/52/53/54/55/56/57/58/59/60",
                    "levtype": "ml",
                    # all available parameters, for codes see http://apps.ecmwf.int/codes/grib/param-db
                    "param": "131.128",
                    "step" : "0",
                    "stream": "oper",
                    "time" : "00:00:00/06:00:00/12:00:00/18:00:00",
                    # reanalysis (type:an), forecast (type:fc)
                    "type": "an",
                    # optionally restrict area to Europe (in N/W/S/E).
                    # "area": "75/-20/10/60",
                    # Optionally get output in NetCDF format. However, this does not work with the above request due to overlapping timestamps.
                    "format" :  "netcdf",
                    # set an output file name
                    "target": sav_path+os.sep+"model_daily_075_%s_%d_u.nc" % (i,j+1),
                    })

if sel == 'Geopotential':
    for i in date_string:
        for j in ind_month:
            server = ECMWFDataServer()

            server.retrieve({
                    # Specify the ERA-Interim data archive. Don't change.
                    "class": "ei",
                    "dataset": "interim",
                    # Specify the date of request data
                    "date" : date_string['%s' % i][j],
                    "expver": "1",
                    # in 0.75 degrees lat/lon
                    "grid": "0.75/0.75",
                    # pressure levels (levtype:pl), all available levels (levelist)
                    "levelist": "1",
                    "levtype": "ml",
                    # all available parameters, for codes see http://apps.ecmwf.int/codes/grib/param-db
                    "param": "129.128",
                    "step" : "0",
                    "stream": "oper",
                    "time" : "00:00:00/06:00:00/12:00:00/18:00:00",
                    # reanalysis (type:an), forecast (type:fc)
                    "type": "an",
                    # optionally restrict area to Europe (in N/W/S/E).
                    # "area": "75/-20/10/60",
                    # Optionally get output in NetCDF format. However, this does not work with the above request due to overlapping timestamps.
                    "format" :  "netcdf",
                    # set an output file name
                    "target": sav_path+os.sep+"model_daily_075_%s_%d_z.nc" % (i,j+1),
                    })

if sel == 'LogPressure':
    for i in date_string:
        for j in ind_month:
            server = ECMWFDataServer()

            server.retrieve({
                    # Specify the ERA-Interim data archive. Don't change.
                    "class": "ei",
                    "dataset": "interim",
                    # Specify the date of request data
                    "date" : date_string['%s' % i][j],
                    "expver": "1",
                    # in 0.75 degrees lat/lon
                    "grid": "0.75/0.75",
                    # pressure levels (levtype:pl), all available levels (levelist)
                    "levelist": "1",
                    "levtype": "ml",
                    # all available parameters, for codes see http://apps.ecmwf.int/codes/grib/param-db
                    "param": "152.128",
                    "step" : "0",
                    "stream": "oper",
                    "time" : "00:00:00/06:00:00/12:00:00/18:00:00",
                    # reanalysis (type:an), forecast (type:fc)
                    "type": "an",
                    # optionally restrict area to Europe (in N/W/S/E).
                    # "area": "75/-20/10/60",
                    # Optionally get output in NetCDF format. However, this does not work with the above request due to overlapping timestamps.
                    "format" :  "netcdf",
                    # set an output file name
                    "target": sav_path+os.sep+"model_daily_075_%s_%d_lgsp.nc" % (i,j+1),
                    })

if sel == 'Custom':
    server = ECMWFDataServer()
    server.retrieve({
            # Specify the ERA-Interim data archive. Don't change.
            "class": "ei",
            "dataset": "interim",
            # Specify the date of request data
             "date" : "1980-12-01/to/1980-12-31",
            "expver": "1",
            # in 0.75 degrees lat/lon
            "grid": "0.75/0.75",
            # pressure levels (levtype:pl), all available levels (levelist)
            "levelist": "1/2/3/4/5/6/7/8/9/10/11/12/13/14/15/16/17/18/19/20/21/22/23/24/25/26/27/28/29/30/31/32/33/34/35/36/37/38/39/40/41/42/43/44/45/46/47/48/49/50/51/52/53/54/55/56/57/58/59/60",
            "levtype": "ml",
            # all available parameters, for codes see http://apps.ecmwf.int/codes/grib/param-db
            "param": "131.128",
            "step" : "0",
            "stream": "oper",
            "time" : "00:00:00/06:00:00/12:00:00/18:00:00",
            # reanalysis (type:an), forecast (type:fc)
            "type": "an",
            # optionally restrict area to Europe (in N/W/S/E).
            # "area": "75/-20/10/60",
            # Optionally get output in NetCDF format. However, this does not work with the above request due to overlapping timestamps.
            "format" :  "netcdf",
            # set an output file name
            "target": 'F:\DataBase\ERA_Interim\Subdaily\model_daily_075_1980\\model_daily_075_1980_12_u',
            })

print("--- %s seconds ---" % (time.time() - start_time))
