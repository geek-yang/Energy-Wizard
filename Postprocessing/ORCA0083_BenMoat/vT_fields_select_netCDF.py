#!/usr/bin/env python
"""
Copyright Netherlands eScience Center and National Oceanography Center

Function        : Fetch certain fields from full transport file
Author          : Yang Liu & Ben Moat
License:        : APACHE 2.0
Date            : 2018.04.19
Last Update     : 2018.04.23
Description     : The script aims to take the meridional temperature transport over the
                  entire vertical column from given file, which includes meridional/zonal
                  temperature/salinity transport.
Input Files     : vel_T_ORCA0083-N06_{year}m{month}.nc
Return Value    : NetCFD4 file
Dependencies    : os, time, numpy, netCDF4, sys, argparse, logging
variables       : Temperature Transport        v * T       [DegC m / s]
Caveat!!        : The data is from 0N to 90N (North Hemisphere). It is on ORCA083 grid.
                  The output is based on year, which means a single file contains
                  12 monthly mean of target fields.

                  The input data, which is calculated by CDFTool, has values at masked locations!
                  Thus, we have to replace them with 0.
"""
import numpy as np
import time as tttt
from netCDF4 import Dataset,num2date
import os
import argparse
import logging

##########################################################################
###########################   Units vacabulory   #########################
# cpT:  [J / kg C] * [C]     = [J / kg]
# v*rho cpT dxdz = [m/s] * [J / kg] * [kg/m3] * m * m = [J / s] = [Wat]
##########################################################################

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

# define the constant:
constant ={'g' : 9.80616,      # gravititional acceleration [m / s2]
           'R' : 6371009,      # radius of the earth [m]
           'cp': 3987,         # heat capacity of sea water [J/(Kg*C)]
           'rho': 1027,        # sea water density [Kg/m3]
            }

def main(start_year, end_year, input_path, output_path, grid_path):
    '''
    Fetch certain fields and output netCDF files
    '''
    # set a log file
    logging.basicConfig(filename = os.path.join(output_path,'vel_T_fetch.log'),
                        filemode = 'w+', level = logging.DEBUG,
                        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    #############################################
    #############     constants    ##############
    #############################################
    # The constants comes from the dimension of ORCA083 grid
    # dimension
    ji = 4322
    jj = 3059
    jj_NH = 1565 # north hemisphere only
    level = 75
    # namelist of month
    namelist_month = ['01','02','03','04','05','06',
                      '07','08','09','10','11','12']
    # target level
    period = np.arange(start_year,end_year+1,1)
    #############################################
    ###########     Extract data    #############
    ###########     Yield netcdf    #############
    #############################################
    # create space to store the final results
    pool_vT_vert_int = np.zeros((12,jj_NH,ji),dtype=float)
    pool_vT_zonal_int = np.zeros((12,level,jj_NH),dtype=float)
    # grid infomation
    key_grid_zgr = os.path.join(grid_path,'mesh_zgr.nc')
    key_grid_hgr = os.path.join(grid_path,'mesh_hgr.nc')
    dataset_zgr = Dataset(key_grid_zgr)
    dataset_hgr = Dataset(key_grid_hgr)
    # height and width of cells
    e3v_0 = dataset_zgr.variables['e3v_0'][0,:,1494:,:]
    e1v = dataset_hgr.variables['e1v'][0,1494:,:]
    # v grid
    gphiv = dataset_hgr.variables['gphiv'][0,1494:,:]
    glamv = dataset_hgr.variables['glamv'][0,1494:,:]
    glamv = np.ma.array(glamv,keep_mask=False) # remove the mask
    nav_lev = dataset_zgr.variables['nav_lev'][:]

    for i in period: # loop of year
        for j in np.arange(12): # loop of month
            # point to the input
            key_input = os.path.join(input_path,'vel_T_ORCA0083-N06_{}m{}.nc'.format(i,namelist_month[j]))
            dataset = Dataset(key_input)
            vT = dataset.variables['vomevt'][0,:,1494:,:]
            #np.ma.set_fill_value(vT,0)
            mask = np.ma.getmask(vT)
            # replace wrong value at masked locations with 0
            vT[mask==True] = 0
            # create space for operation
            vT_operate = np.zeros(vT.shape)
            for k in np.arange(level):
                vT_operate[k,:,:] = constant['rho'] * constant['cp'] * vT[k,:,:] * e3v_0[k,:,:] * e1v
                #np.ma.masked_where(mask,vT_operate)
                # compute zonal integral and vertical integral
                vT_vert_int = np.sum(vT_operate,0)/1E+12 # change the unit to tera-watt
                vT_zonal_int = np.sum(vT_operate,2)/1E+12
            logging.info('Extract data from the time {} (year) {} (month) successfully!'.format(i,namelist_month[j]))
            pool_vT_vert_int[j,:,:] = vT_vert_int
            pool_vT_zonal_int[j,:,:] = vT_zonal_int
        # reverse the mask and change to int in the saving list
        mask_sav = mask[0,:,:] == False
        # call the function to output netcdf field
        pack_netcdf(pool_vT_vert_int, pool_vT_zonal_int, gphiv, glamv, nav_lev, mask_sav,
                    i, output_path, ji, jj_NH, level)
        logging.info('Packing selected fields for the time {} (year) successfully!'.format(i))
    logging.info('The full pipeline is complete!')

def pack_netcdf(vT_vert_int, vT_zonal_int, gphiv, glamv, nav_lev, mask,
                year, output_path, ji, jj, level):
    '''
    save target fields as netcdf files
    '''
    # wrap the datasets into netcdf file
    # 'NETCDF3_CLASSIC', 'NETCDF3_64BIT', 'NETCDF4_CLASSIC', and 'NETCDF4'
    data_wrap = Dataset(os.path.join(output_path,'vel_T_ORCA0083_select_{}.nc'.format(year)),
                        'w', format = 'NETCDF4')
    # create dimensions for netcdf data
    month_wrap_dim = data_wrap.createDimension('month',12)
    lat_wrap_dim = data_wrap.createDimension('latitude',jj)
    lon_wrap_dim = data_wrap.createDimension('longitude',ji)
    lev_wrap_dim = data_wrap.createDimension('level',level)
    # create coordinate variables for 3-dimensions
    month_wrap_var = data_wrap.createVariable('month',np.int32,('month',))
    gphiv_wrap_var = data_wrap.createVariable('gphiv',np.float32,('latitude','longitude'))
    glamv_wrap_var = data_wrap.createVariable('glamv',np.float32,('latitude','longitude'))
    lev_wrap_var = data_wrap.createVariable('lev',np.float32,('level',))
    mask_wrap_var = data_wrap.createVariable('mask',np.int8,('latitude','longitude'))
    # create the target 3-d variable
    vT_vert_int_wrap_var = data_wrap.createVariable('vT_vert',np.float64,('month','latitude','longitude'),zlib=True)
    vT_zonal_int_wrap_var = data_wrap.createVariable('vT_zonal',np.float64,('month','level','latitude'),zlib=True)
    # global attributes
    data_wrap.description = 'Monthly mean temperature transport from NEMO ORCA083 simulation in the North Hemisphere'
    # variable attributes
    vT_vert_int_wrap_var.units = 'Tera Watt'
    vT_zonal_int_wrap_var.units = 'Tera Watt'
    lev_wrap_var.units = 'm'

    vT_vert_int_wrap_var.long_name = 'Vertical integral of temperature transport'
    vT_zonal_int_wrap_var.long_name = 'Zonal integral of temperature transport'
    gphiv_wrap_var.long_name = 'Latitude of V grid'
    glamv_wrap_var.long_name = 'Longitude of V grid'
    lev_wrap_var.long_name = 'Depth'

    # special attributes for time variables
    #time_wrap_var.units = 'hours since 1900-01-01 00:00:0.0'
    #time_wrap_var.calender = 'gregorian'

    # writing data
    month_wrap_var[:] = np.arange(1,13,1)
    gphiv_wrap_var[:] = gphiv
    glamv_wrap_var[:] = glamv
    lev_wrap_var[:] = nav_lev
    mask_wrap_var[:] = mask

    vT_vert_int_wrap_var[:] = vT_vert_int
    vT_zonal_int_wrap_var[:] = vT_zonal_int

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
    parser.add_argument('-g','--gridpath',type=path_check,
                        help='path to the grid files mesh_zgr and mesh_hgr',
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
    main(args.start, args.end, args.inpath, args.outpath, args.gridpath)
    print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
