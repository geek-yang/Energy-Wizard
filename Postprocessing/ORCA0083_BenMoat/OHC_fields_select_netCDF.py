#!/usr/bin/env python
"""
Copyright Netherlands eScience Center and National Oceanography Center

Function        : Fetch certain fields from full OHC file
Author          : Yang Liu & Ben Moat
License:        : APACHE 2.0
Date            : 2018.04.19
Last Update     : 2018.04.19
Description     : The script aims to fetch the OHC upto certain depth from the full
                  OHC fields. Target depth includes:
                  0 m - 500  m
                  0 m - 1000 m
                  0 m - 2000 m
                  0 m - bottom
Input Files     : OHC_ORCA0083-N06_{year}m{month}
Return Value    : NetCFD4 file
Dependencies    : os, time, numpy, netCDF4, sys, argparse, logging
variables       : Ocean Heat Content        OHC       [J/km2]
Caveat!!        : The data is from 90 deg north to 90 deg south (Globe).
                  It is on ORCA083 grid.
                  The output is based on year, which means a single file contains
                  12 monthly mean of target fields.
"""
import numpy as np
import time as tttt
from netCDF4 import Dataset,num2date
import os
import argparse
import logging

# depth info of ORCA083 (for reference only)
depthw = np.array(([0, 1.023907, 2.10319, 3.251309, 4.485053, 5.825238, 7.297443,
                   8.932686, 10.7679, 12.84599, 15.21527, 17.92792, 21.03757, 24.59599,
                   28.64965, 33.23697, 38.3871, 44.12101, 50.45447, 57.40257, 64.9846,
                   73.2287, 82.17556, 91.88141, 102.4202, 113.8852, 126.3909, 140.074,
                   155.095, 171.6402, 189.9228, 210.1845, 232.697, 257.7629, 285.7158,
                   316.9199, 351.768, 390.6786, 434.0905, 482.4563, 536.2332, 595.8721,
                   661.8052, 734.4321, 814.1057, 901.118, 995.6885, 1097.954, 1207.963,
                   1325.672, 1450.95, 1583.582, 1723.28, 1869.693, 2022.425, 2181.044,
                   2345.101, 2514.137, 2687.699, 2865.347, 3046.659, 3231.24, 3418.723,
                   3608.769, 3801.072, 3995.354, 4191.367, 4388.89, 4587.726, 4787.702,
                   4988.667, 5190.488, 5393.049, 5596.249, 5800]),dtype=float)

def main(start_year, end_year, input_path, output_path):
    '''
    Fetch certain fields and output netCDF files
    '''
    # set a log file
    logging.basicConfig(filename = os.path.join(output_path,'OHC_fetch.log'),
                        filemode = 'w+', level = logging.DEBUG,
                        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    #############################################
    #############     constants    ##############
    #############################################
    # The constants comes from the dimension of ORCA083 grid
    # dimension
    ji = 4322
    jj = 3059
    level = 75
    # namelist of month
    namelist_month = ['01','02','03','04','05','06',
                      '07','08','09','10','11','12']
    # target level
    target_level = [39,46,54,74]
    period = np.arange(start_year,end_year+1,1)
    #############################################
    ###########     Extract data    #############
    ###########     Yield netcdf    #############
    #############################################
    # specify empty space for selected fields
    OHC_500 = np.zeros((12,jj,ji),dtype = float)
    OHC_1000 = np.zeros((12,jj,ji),dtype = float)
    OHC_2000 = np.zeros((12,jj,ji),dtype = float)
    OHC_5800 = np.zeros((12,jj,ji),dtype = float)
    for i in period: # loop of year
        for j in np.arange(12): # loop of month
            # point to the input
            key_input = os.path.join(input_path,'OHC_ORCA0083-N06_{}m{}.nc'.format(i,namelist_month[j]))
            dataset = Dataset(key_input)
            OHC_500[j,:,:] = dataset.variables['voheatc'][0,target_level[0],:,:]
            OHC_1000[j,:,:] = dataset.variables['voheatc'][0,target_level[1],:,:]
            OHC_2000[j,:,:] = dataset.variables['voheatc'][0,target_level[2],:,:]
            OHC_5800[j,:,:] = dataset.variables['voheatc'][0,target_level[3],:,:]
            logging.info('Extract data from the time {} (year) {} (month) successfully!'.format(i,namelist_month[j]))
            #############################################
            ###########     Compress data    ############
            #############################################
            # calculate maximum and minimum of each variable
            #OHC_500_max = np.amax(OHC_500)
            #OHC_500_min = np.amin(OHC_500)
            #OHC_1000_max = np.amax(OHC_1000)
            #OHC_1000_min = np.amin(OHC_1000)
            #OHC_2000_max = np.amax(OHC_2000)
            #OHC_2000_min = np.amin(OHC_2000)
            #OHC_5800_max = np.amax(OHC_5800)
            #OHC_5800_min = np.amin(OHC_5800)
            # specify the number of bits for packing
            #n_int = 64
            # Calculate scale factor and offset for compress data in netcdf
            #scale_factor_500, add_offset_500 = compute_scale_and_offset(OHC_500_max, OHC_500_min, n_int)
            #scale_factor_1000, add_offset_1000 = compute_scale_and_offset(OHC_1000_max, OHC_1000_min, n_int)
            #scale_factor_2000, add_offset_2000 = compute_scale_and_offset(OHC_2000_max, OHC_2000_min, n_int)
            #scale_factor_5800, add_offset_5800 = compute_scale_and_offset(OHC_5800_max, OHC_5800_min, n_int)
        # call the function to output netcdf field
        pack_netcdf(OHC_500, OHC_1000, OHC_2000, OHC_5800, i, output_path, ji, jj)
        #            scale_factor_500, add_offset_500,scale_factor_1000, add_offset_1000,
        #            scale_factor_2000, add_offset_2000, scale_factor_5800, add_offset_5800)
        logging.info('Packing selected fields for  the time {} (year) {} (month) successfully!'.format(i,namelist_month[j]))
    logging.info('The full pipeline is complete!')

# Calculate scale factor and offset for packing data in netcdf
# def compute_scale_and_offset(max_a, min_a, n):
#     # stretch/compress data to the available packed range
#     scale_factor = (max_a - min_a) / (2 ** n - 1)
#     # translate the range to be symmetric about zero
#     add_offset = min_a + 2 ** (n - 1) * scale_factor
#     return (scale_factor, add_offset)

def pack_netcdf(OHC_500, OHC_1000, OHC_2000, OHC_5800, year, output_path, ji, jj):
                #scale_factor_500, add_offset_500,scale_factor_1000, add_offset_1000,
                #scale_factor_2000, add_offset_2000, scale_factor_5800, add_offset_5800
    '''
    save target fields as netcdf files
    '''
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(os.path.join(output_path,'OHC_ORCA0083_select_{}.nc'.format(year)),
                        'w', format = 'NETCDF4')
    # create dimensions for netcdf data
    month_wrap_dim = data_wrap.createDimension('month',12)
    lat_wrap_dim = data_wrap.createDimension('latitude',jj)
    lon_wrap_dim = data_wrap.createDimension('longitude',ji)
    # create coordinate variables for 3-dimensions
    month_wrap_var = data_wrap.createVariable('month',np.int32,('month',))
    lat_wrap_var = data_wrap.createVariable('latitude',np.float32,('latitude',))
    lon_wrap_var = data_wrap.createVariable('longitude',np.float32,('longitude',))
    # create the target 3-d variable
    OHC_500_wrap_var = data_wrap.createVariable('OHC_500',np.float64,('month','latitude','longitude'),zlib=True)
    OHC_1000_wrap_var = data_wrap.createVariable('OHC_1000',np.float64,('month','latitude','longitude'),zlib=True)
    OHC_2000_wrap_var = data_wrap.createVariable('OHC_2000',np.float64,('month','latitude','longitude'),zlib=True)
    OHC_5800_wrap_var = data_wrap.createVariable('OHC_bottom',np.float64,('month','latitude','longitude'),zlib=True)
    # global attributes
    data_wrap.description = 'Monthly mean OHC upto selected depth from NEMO ORCA083 simulation over the entire globe'
    # variable attributes
    OHC_500_wrap_var.units = 'J/km2'
    OHC_1000_wrap_var.units = 'J/km2'
    OHC_2000_wrap_var.units = 'J/km2'
    OHC_5800_wrap_var.units = 'J/km2'

    OHC_500_wrap_var.long_name = 'OHC from surface to 500m'
    OHC_1000_wrap_var.long_name = 'OHC from surface to 1000m'
    OHC_2000_wrap_var.long_name = 'OHC from surface to 2000m'
    OHC_5800_wrap_var.long_name = 'OHC from surface to bottom'

    # apply the scale factor and offset for packing
    #OHC_500_wrap_var.scale_factor = scale_factor_500
    #OHC_500_wrap_var.add_offset = add_offset_500
    #OHC_1000_wrap_var.scale_factor = scale_factor_1000
    #OHC_1000_wrap_var.add_offset = add_offset_1000
    #OHC_2000_wrap_var.scale_factor = scale_factor_2000
    #OHC_2000_wrap_var.add_offset = add_offset_2000
    #OHC_5800_wrap_var.scale_factor = scale_factor_5800
    #OHC_5800_wrap_var.add_offset = add_offset_5800

    # special attributes for time variables
    #time_wrap_var.units = 'hours since 1900-01-01 00:00:0.0'
    #time_wrap_var.calender = 'gregorian'

    # writing data
    month_wrap_var[:] = np.arange(1,13,1)
    lat_wrap_var[:] = np.arange(jj)
    lon_wrap_var[:] = np.arange(ji)

    OHC_500_wrap_var[:] = OHC_500
    OHC_1000_wrap_var[:] = OHC_1000
    OHC_2000_wrap_var[:] = OHC_2000
    OHC_5800_wrap_var[:] = OHC_5800
    # close the file
    data_wrap.close()

# pass argument to the main function
def choice_parser():
    '''
    pass command line arguments
    '''
    # define arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--start',type=int, default=1979,
                        help='starting year of input files',
                        required=False)
    parser.add_argument('-e','--end',type=int, default=2012,
                        help='last year of input files',
                        required=False)
    parser.add_argument('-i','--inpath',type=path_check,
                        help='path to the input file',
                        required=True)
    parser.add_argument('-o','--outpath',type=path_check,
                        help='path to save the output files',
                        required=True)
    #get arguments
    choices = parser.parse_args()
    return choices

# check if the input & output path really exist
def path_check(path):
    '''
    check if the path exists
    '''
    if not os.path.isdir(path):
        message = "{} is not an existing directory!".format(path)
        raise argparse.ArgumentTypeError(message)
    return path

if __name__ == "__main__":
    # calculate the time for the code execution
    start_time = tttt.time()
    # get command line arguments through the function defined above
    args = choice_parser()
    # main function to fetch the certain fields and output netCDF files
    main(args.start,args.end,args.inpath,args.outpath)
    print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
