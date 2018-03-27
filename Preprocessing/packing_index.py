#!/usr/bin/env python
"""
Copyright Netherlands eScience Center

Function        : Packing index
Author          : Yang Liu
Date            : 2018.03.18
Last Update     : 2018.03.26
Description     : The code aims to pack climate large scale index.
                  Those index include:
                  NAO (based on CDAS from NOAA)
                  ENSO - ONI (based on CDAS from NOAA)
                  AO (based on CDAS from NOAA)
                  AMO (based on Kaplan SST dataset from NOAA)
                  PDO (based on Kaplan SST dataset from University of Washington)
Return Value    : netCDF
Dependencies    : os, time, numpy, scipy, netCDF4, matplotlib, basemap
variables       : NAO           1950 Jan - 2018 Feb (818 records)
                  http://www.cpc.ncep.noaa.gov/products/precip/CWlink/pna/nao.shtml
                  ENSO - MEI    1950 Jan - 2018 Jan (817 records)
                  https://www.esrl.noaa.gov/psd/enso/mei/table.html
                  ENSO - NINO 3.4 SST   1950 Jan - 2018 Jan (817 records)
                  https://www.esrl.noaa.gov/psd/gcos_wgsp/Timeseries/Nino34/
                  AO            1950 Jan - 2018 Feb (818 records)
                  http://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_ao_index/ao.shtml
                  AMO           1950 Jan - 2018 Feb (818 records)
                  AMO unsmoothed, detrended from the Kaplan SST V2
                  The result is standarised
                  https://www.esrl.noaa.gov/psd/data/timeseries/AMO/
                  PDO           1900 Jan - 2018 Feb (1418 records)
                  This PDO index comes from University of Washington
                  It contains SST data from the following 3 datasets:
                  UKMO Historical SST data set for 1900-81;
                  Reynold's Optimally Interpolated SST (V1) for January 1982-Dec 2001)
                  OI SST Version 2 (V2) beginning January 2002 -
                  http://research.jisao.washington.edu/pdo/PDO.latest

Caveat!!        : These index are given by NCEP/NCAR Reanalysis (CDAS),
                  Kaplan SST V2, UKMO Historical SST dataset,
                  Reynold's Optimally Interpolated SST (V1),
                  OI SST Version 2 (V2)
"""

import numpy as np
import scipy as sp
from scipy import stats
import time as tttt
from netCDF4 import Dataset,num2date
import os
import seaborn as sns
import platform
import logging
#import matplotlib
# Generate images without having a window appear
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, cm

# print the system structure and the path of the kernal
print platform.architecture()
print os.path

# calculate the time for the code execution
start_time = tttt.time()
# switch on the seaborn effect
sns.set()

print '***********************     input     *************************'
output_path = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/Climate_index'
print '***********************     input     *************************'

print '***********************      NAO      *************************'
# *************** NAO - NOAA CSAD ***************** #
# from 1950 Jan to 2018 Feb (818 records)
datapath_NAO_NOAA = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/Climate_index/NAO/NOAA'
NAO_file = open(datapath_NAO_NOAA + os.sep + 'NAO_monthly_NOAA_valueonly.txt', 'r')
NAO_value = NAO_file.read().splitlines() # get a list of values
NAO = np.array(NAO_value,dtype=float) # convert str to float
NAO = NAO[:-2] # take 1950 - 2017
NAO_file.close()

print '***********************      ENSO      *************************'
# *************** ENSO MEI - NOAA CSAD ***************** #
# from 1950 Jan to 2017 Dec (816 records)
datapath_ENSO_NOAA = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/Climate_index/ENSO/NOAA'
MEI_file = open(datapath_ENSO_NOAA + os.sep + 'MEI_monthly_NOAA_valueonly.txt', 'r')
MEI_value = MEI_file.read().split() # get a list of values
MEI = np.array(MEI_value,dtype=float) # convert str to float
MEI_file.close()

print '***********************      ENSO      *************************'
# *************** ENSO NINO 3.4 SST - NOAA CSAD ***************** #
# from 1950 Jan to 2017 Dec (816 records)
datapath_ENSO_NOAA = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/Climate_index/ENSO/NOAA'
NINO_file = open(datapath_ENSO_NOAA + os.sep + 'NINO3.4_monthly_NOAA_valueonly.txt', 'r')
NINO_value = NINO_file.read().split() # get a list of values
NINO = np.array(NINO_value,dtype=float) # convert str to float
NINO_file.close()

print '***********************      AO      *************************'
# *************** AO - NOAA CSAD ***************** #
# from 1950 Jan to 2018 Feb (818 records)
datapath_AO_NOAA = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/Climate_index/AO/NOAA'
AO_file = open(datapath_AO_NOAA + os.sep + 'AO_monthly_NOAA_valueonly.txt', 'r')
AO_value = AO_file.read().split() # get a list of values
AO = np.array(AO_value,dtype=float) # convert str to float
AO = AO[:-2] # take 1950 - 2017
AO_file.close()

print '***********************      AMO      *************************'
# *************** AO - NOAA CSAD ***************** #
# from 1950 Jan to 2017 Dec (816 records)
datapath_AMO_NOAA = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/Climate_index/AMO/NOAA'
AMO_file = open(datapath_AMO_NOAA + os.sep + 'AMO_monthly_NOAA_valueonly.txt', 'r')
AMO_value = AMO_file.read().split() # get a list of values
AMO = np.array(AMO_value,dtype=float) # convert str to float
AMO = AMO[24:] # take 1950 - 2017
AMO_file.close()

print '***********************      PDO      *************************'
# *************** AO - NOAA CSAD ***************** #
# from 1900 Jan to 2017 Dec (1416 records)
datapath_PDO_UM = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/Climate_index/PDO/UM'
PDO_file = open(datapath_PDO_UM + os.sep + 'PDO_monthly_UW_valueonly.txt', 'r')
PDO_value = PDO_file.read().split() # get a list of values
PDO = np.array(PDO_value,dtype=float) # convert str to float
PDO = PDO[600:] # take 1950 - 2017
PDO_file.close()


# save output datasets
# we only pack our timeseries from 1979 to 2016
def create_netcdf_point (NAO,MEI,NINO,AO,AMO,PDO,period,output_path):
    series = len(period) * 12
    print '*******************************************************************'
    print '*********************** create netcdf file*************************'
    print '*******************************************************************'
    logging.info("Start creating netcdf file for climate index from 1950 to 2017.")
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(output_path + os.sep + 'index_climate_monthly_regress_1950_2017.nc','w',format = 'NETCDF3_64BIT')
    # create dimensions for netcdf data
    year_wrap_dim = data_wrap.createDimension('year', len(period))
    Timeseries = data_wrap.createDimension('series', series)
    # create coordinate variables for 3-dimensions
    year_wrap_var = data_wrap.createVariable('year',np.int32,('year',))
    # create the actual 3-d variable
    NAO_wrap_var = data_wrap.createVariable('NAO',np.float64,('series',))
    MEI_wrap_var = data_wrap.createVariable('MEI',np.float64,('series',))
    NINO_wrap_var = data_wrap.createVariable('NINO',np.float64,('series',))
    AO_wrap_var = data_wrap.createVariable('AO',np.float64,('series',))
    AMO_wrap_var = data_wrap.createVariable('AMO',np.float64,('series',))
    PDO_wrap_var = data_wrap.createVariable('PDO',np.float64,('series',))

    # global attributes
    data_wrap.description = 'Monthly climate index time series'
    # variable attributes

    NAO_wrap_var.units = '1'
    MEI_wrap_var.units = '1'
    NINO_wrap_var.units = '1'
    AO_wrap_var.units = '1'
    AMO_wrap_var.units = '1'
    PDO_wrap_var.units = '1'

    NAO_wrap_var.long_name = 'North Atlantic Oscillation Index'
    MEI_wrap_var.long_name = 'Multivariate ENSO Index'
    NINO_wrap_var.long_name = 'EI NINO 3.4 SST Index'
    AO_wrap_var.long_name = 'Atlantic Oscillation Index'
    AMO_wrap_var.long_name = 'Atlantic Multidecadal Oscillation Index'
    PDO_wrap_var.long_name = 'Pacific Decadal Oscillation Index'

    # writing data
    year_wrap_var[:] = period

    NAO_wrap_var[:] = NAO
    MEI_wrap_var[:] = MEI
    NINO_wrap_var[:] = NINO
    AO_wrap_var[:] = AO
    AMO_wrap_var[:] = AMO
    PDO_wrap_var[:] = PDO

    # close the file
    data_wrap.close()
    print "Create netcdf file successfully"
    logging.info("The generation of netcdf files for the climate index is complete!!")

if __name__=="__main__":
    # create time dimension for saving the fields
    period = np.arange(1950,2018,1) # take 1950 - 2017
    # create netCDF file
    create_netcdf_point(NAO,MEI,NINO,AO,AMO,PDO,period,output_path)
