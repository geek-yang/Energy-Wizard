#!/usr/bin/env python
'''
Copyright Netherlands eScience Center

Function        : Download reanalysis data ERA-Interim from ECMWF archive
Author          : Yang Liu
Date            : 2019.06.19
Description     : The code aims to download the reanalysis data from ECMWF.
                  It is made for the dataset "ERA-Interim". But it could
                  be used to deal with other datasets from ECMWF as well
                  after small adjustment.
Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, ecmwfapi, logging

Cautious!
Before execute the code, the following steps should be complete:
1. Install ECMWF Key
The key could be retrived through the link, after login: https://api.ecmwf.int/v1/key/
For Windows, the key should be placed at the user folder
2. Install client library
The ecmwfapi python library could be accessed through:
'sudo pip install https://software.ecmwf.int/wiki/download/attachments/56664858/ecmwf-api-client-python.tgz'
'''

import os
import time as tttt
import numpy as np
from ecmwfapi import ECMWFDataServer
import logging
import sys

# record the time for downloading the dataset
start_time = tttt.time()
# redirect the console output to a file
sys.stdout = open('/project/Reanalysis/ERA_Interim/Subdaily/Model/console.out','w')

# logging level 'DEBUG' 'INFO' 'WARNING' 'ERROR' 'CRITICAL'
#logging.basicConfig(filename = 'F:\DataBase\history.log', filemode = 'w', level = logging.DEBUG, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(filename = '/project/Reanalysis/ERA_Interim/Subdaily/Model/history.log', filemode = 'w', level = logging.DEBUG, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# credentials of dataset namelist
levtype = {'model' : 'ml',
           'pressure' : 'pl',}

param = {'u_v' : '131.128/132.128',                            # northerly_easterly
         'T_q' : '130.128/133.128',                            # temperature_humidity
         'z_lnsp' : '129.128/152.128',                         # geopotential_Ln pressure
         'T_q_u_v' : '130.128/131.128/132.128/133.128',}

levelist = {'ml' : "1/2/3/4/5/6/7/8/9/10/11/12/13/14/15/16/17/18/19/20/21/22/23/24/25/26/27/28/29/30/31/32/33/34/35/36/37/38/39/40/41/42/43/44/45/46/47/48/49/50/51/52/53/54/55/56/57/58/59/60",
            'pl' : "1/2/3/5/7/10/20/30/50/70/100/125/150/175/200/225/250/300/350/400/450/500/550/600/650/700/750/775/800/825/850/875/900/925/950/975/1000",
            'ml_s' : "1",}

################################   Input zone  ######################################
# starting time (year)
start_year = 2010
# Ending time, if only for 1 year, then it should be the same as starting year
end_year = 2017
# credentials for the datasets dictionary
levtype_input = 'model'
param_input = 'z_lnsp'
#param_input = 'T_q'
#param_input = 'T_q_u_v'
levelist_input = 'ml_s'
#levelist_input = 'ml'
# specify saving path
sav_path = '/project/Reanalysis/ERA_Interim/Subdaily/Model'
####################################################################################

# This function generate a series of time for downloading dataset
# The unit of downloading dataset is per month

def time_series (start_year,end_year):
    # calculate all the leap years
    leap_year = np.arange(1900,2024,4)
    period = np.arange(start_year,end_year+1,1)
    date_str = {}
    for i in period:
        if i in leap_year:
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

# This function generates the basic namelist dictionary for retrieving datasets
def namelist(param,levelist,levtype,date_info,ind_year,ind_month,ind_param):
    namelist_dict = {# Specify the ERA-Interim data archive. Don't change.
                    "class": "ei",
                    "dataset": "interim",
                    # Specify the date of request data
                    "date" : date_info,
                    "expver": "1",
                    # in 0.75 degrees lat/lon
                    "grid": "N128",
                    # pressure levels (levtype:pl), all available levels (levelist)
                    "levelist": levelist,
                    "levtype": levtype,
                    # all available parameters, for codes see http://apps.ecmwf.int/codes/grib/param-db
                    "param": param,
                    "step" : "0",
                    "stream": "oper",
                    "time" : "00:00:00/06:00:00/12:00:00/18:00:00",
                    # reanalysis (type:an), forecast (type:fc)
                    "type": "an",
                    # optionally restrict area to Europe (in N/W/S/E).
                    #"area": "90/-180/-90/180",
                    # Optionally get output in NetCDF format. However, this does not work with the above request due to overlapping timestamps.
                    # ERA-Interim is natively generated with grib1 !!!
                    "format" : "grib1",
                    # set an output file name
                    "target": sav_path+os.sep+"era%s" % (ind_year)+os.sep+"model_daily_N128_%s_%d_%s.grib" % (ind_year,ind_month,ind_param),}
    return namelist_dict

if __name__=="__main__":
    # generate time series
    date_string = time_series(start_year,end_year)
    # generate month index for loop
    index_month = np.arange(1,13,1)
    for i in date_string:
        for j in index_month:
            # make a history log to monitor the downloading progress
            logging.info('Start Downloading  %d (m) %s (y) variable %s' % (j,i,param_input))
            # download data from ECMWF server
            server = ECMWFDataServer()
            server.retrieve(namelist(param['%s' % (param_input)],levelist['%s' % (levelist_input)],levtype['%s' % (levtype_input)],\
            date_string['%s' % (i)][j-1],i,j,param_input))
            logging.info("Downloading %d (m) %s (y) variable %s successfully" % (j,i,param_input))
            # record the progress in the history file
    logging.info('Finish Downloading in %s minutes' % ((tttt.time() - start_time)/60))

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
