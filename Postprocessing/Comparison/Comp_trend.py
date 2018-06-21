#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : Compare the trend of atmosphere and ocean reanalysis datasets
Author          : Yang Liu
Date            : 2018.06.21
Last Update     : 2018.06.21
Description     : The code aims to study the trend of all the variables from both the
                  atmosphere and ocean reanalysis datasets. The atmosphere reanalysis
                  data include ERA-Interim, MERRA2 and JRA55. The ocean reanalysis
                  involve from ORAS4, GLORYS2V3, SODA3. One hindcast from NOC, which
                  is a NEMO ORCA0083 high resolution hindcast, is employed as well.
Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, sys, matplotlib, logging
variables       : Atmospheric Meridional Energy Transport   ERA-Interim     MERRA2       JRA55
                  Oceanic Meridional Energy Transport       ORAS4           GLORYS2V3    SODA3
                  Mass Transport (volum transport)          ORAS4           GLORYS2V3    SODA3
Caveat!!        : Spatial and temporal coverage
                  Atmosphere
                  ERA-Interim 1979 - 2016
                  MERRA2      1980 - 2016
                  JRA55       1979 - 2015
                  Ocean
                  GLORYS2V3   1993 - 2014
                  ORAS4       1958 - 2014
                  SODA3       1980 - 2015
                  NEMO ORCA   1979 - 2012

                  ! In order to compare the trend between different datasets, we must
                  take the same period. In this case, it is from 1993 to 2012.

                  The full dataset of ORAS4 is from 1958. However, a quality report from
                  Magdalena from ECMWF indicates the quality of data for the first
                  two decades are very poor. Hence we use the data from 1979. which
                  is the start of satellite era.
                  The full dataset of ORAS4 is from 1958.

                  Data from 20N - 90N are taken into account!
"""
import numpy as np
import seaborn as sns
#import scipy as sp
import time as tttt
from netCDF4 import Dataset,num2date
import os
import platform
import sys
import logging
import matplotlib
# generate images without having a window appear
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
#from scipy.interpolate import InterpolatedUnivariateSpline
import scipy
from mpl_toolkits.basemap import Basemap, cm
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import iris
import iris.plot as iplt
import iris.quickplot as qplt

# print the system structure and the path of the kernal
print platform.architecture()
print os.path

# switch on the seaborn effect
sns.set()
sns.set_style("ticks")
sns.despine()

# calculate the time for the code execution
start_time = tttt.time()

################################   Input zone  ######################################
print '****************************************************************************'
print '*****************************   path   *************************************'
print '****************************************************************************'

# specify data path
datapath_ERAI = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ERAI'
datapath_MERRA2 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/MERRA2'
datapath_JRA55 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/JRA55'

datapath_ORAS4 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ORAS4'
datapath_GLORYS2V3 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/GLORYS2V3'
datapath_SODA3 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/SODA3'
datapath_NEMO = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ORCA012_BenMoat'
# specify output path for the netCDF4 file
output_path = '/home/yang/NLeSC/Computation_Modeling/BlueAction/Bjerknes/AMET_OMET/trend'

print '****************************************************************************'
print '********************    latitude index of insteret     *********************'
print '****************************************************************************'
# There is a cut to JRA, too
# index of latitude for insteret
# 20N
lat_ERAI_20 = 93
lat_MERRA2_20 = 0
lat_JRA55_20 = 124

lat_ORAS4_20 = 181
lat_GLORYS2V3_20 = 579
lat_SODA3_20 = 569
# after a cut to 20-90 N
lat_ORAS4_20_cut = 1
lat_GLORYS2V3_20_cut = 0
lat_SODA3_20_cut = 0

# 30N
lat_ERAI_30 = 80
lat_MERRA2_30 = 20
lat_JRA55_30 = 106

lat_ORAS4_30 = 192
lat_GLORYS2V3_30 = 623
lat_SODA3_30 = 613
# after a cut to 20-90 N
lat_ORAS4_30_cut = 12
lat_GLORYS2V3_30_cut = 44
lat_SODA3_30_cut = 44

# 40N
lat_ERAI_40 = 67
lat_MERRA2_40 = 40
lat_JRA55_40 = 88

lat_ORAS4_40 = 204
lat_GLORYS2V3_40 = 672
lat_SODA3_40 = 662
# after a cut to 20-90 N
lat_ORAS4_40_cut = 24
lat_GLORYS2V3_40_cut = 93
lat_SODA3_40_cut = 93

# 50N
lat_ERAI_50 = 53
lat_MERRA2_50 = 60
lat_JRA55_50 = 70

lat_ORAS4_50 = 218
lat_GLORYS2V3_50 = 726
lat_SODA3_50 = 719
# after a cut to 20-90 N
lat_ORAS4_50_cut = 38
lat_GLORYS2V3_50_cut = 147
lat_SODA3_50_cut = 150

# 60N
lat_ERAI_60 = 40
lat_MERRA2_60 = 80
lat_JRA55_60 = 53

lat_ORAS4_60 = 233
lat_GLORYS2V3_60 = 788
lat_SODA3_60 = 789
# after a cut to 20-90 N
lat_ORAS4_60_cut = 53
lat_GLORYS2V3_60_cut = 209
lat_SODA3_60_cut = 220

# 70N
lat_ERAI_70 = 27
lat_MERRA2_70 = 100
lat_JRA55_70 = 35

lat_ORAS4_70 = 250
lat_GLORYS2V3_70 = 857
lat_SODA3_70 = 880
# after a cut to 20-90 N
lat_ORAS4_70_cut = 70
lat_GLORYS2V3_70_cut = 278
lat_SODA3_70_cut = 311

# 80N
lat_ERAI_80 = 13
lat_MERRA2_80 = 120
lat_JRA55_80 = 17

lat_ORAS4_80 = 269
lat_GLORYS2V3_80 = 932
lat_SODA3_80 = 974
# after a cut to 20-90 N
lat_ORAS4_80_cut = 89
lat_GLORYS2V3_80_cut = 353
lat_SODA3_80_cut = 405

# make a dictionary for instereted sections (for process automation)
lat_interest = {}
lat_interest_list = [20,30,40,50,60,70,80]
lat_interest['ERAI'] = [lat_ERAI_20,lat_ERAI_30,lat_ERAI_40,lat_ERAI_50,lat_ERAI_60,lat_ERAI_70,lat_ERAI_80]
lat_interest['MERRA2'] = [lat_MERRA2_20,lat_MERRA2_30,lat_MERRA2_40,lat_MERRA2_50,lat_MERRA2_60,lat_MERRA2_70,lat_MERRA2_80]
lat_interest['JRA55'] = [lat_JRA55_20,lat_JRA55_30,lat_JRA55_40,lat_JRA55_50,lat_JRA55_60,lat_JRA55_70,lat_JRA55_80]
# after cut
lat_interest['ORAS4'] = [lat_ORAS4_20_cut,lat_ORAS4_30_cut,lat_ORAS4_40_cut,lat_ORAS4_50_cut,lat_ORAS4_60_cut,lat_ORAS4_70_cut,lat_ORAS4_80_cut]
lat_interest['GLORYS2V3'] = [lat_GLORYS2V3_20_cut,lat_GLORYS2V3_30_cut,lat_GLORYS2V3_40_cut,lat_GLORYS2V3_50_cut,lat_GLORYS2V3_60_cut,lat_GLORYS2V3_70_cut,lat_GLORYS2V3_80_cut]
lat_interest['SODA3'] = [lat_SODA3_20_cut,lat_SODA3_30_cut,lat_SODA3_40_cut,lat_SODA3_50_cut,lat_SODA3_60_cut,lat_SODA3_70_cut,lat_SODA3_80_cut]
# mask path
#mask_path = 'F:\DataBase\ORAS\ORAS4\Monthly\Model'
####################################################################################
print '*******************************************************************'
print '*********************** extract variables *************************'
print '*******************************************************************'
# # ORCA1_z42 grid infor (Madec and Imbard 1996)
# ji_1 = 362
# jj_1 = 292
# level_1 = 42
#
# # ORCA025_z75 grid infor (Madec and Imbard 1996)
# ji_025 = 1440
# jj_025 = 1021
# level_025 = 75

# # MOM5_z50 grid info
# ji_5 = 1440
# jj_5 = 1070
# level_5 = 50

dataset_AMET_ERAI = Dataset(os.path.join(datapath_ERAI,'postprocessing', 'model_daily_075_1979_2016_E_zonal_int.nc'))
dataset_AMET_MERRA2 = Dataset(os.path.join(datapath_MERRA2,'postprocessing','AMET_MERRA2_model_daily_1980_2016_E_zonal_int.nc'))
dataset_AMET_JRA55 = Dataset(os.path.join(datapath_JRA55,'postprocessing','AMET_JRA55_model_daily_1979_2015_E_zonal_int.nc'))

dataset_OMET_GLORYS2V3 = Dataset(os.path.join(datapath_GLORYS2V3,'postprocessing','GLORYS2V3_model_monthly_orca025_E_point.nc'))
dataset_OMET_ORAS4 = Dataset(os.path.join(datapath_ORAS4,'postprocessing','oras4_model_monthly_orca1_E_point.nc'))
dataset_OMET_SODA3 = Dataset(os.path.join(datapath_SODA3,'postprocessing','OMET_SODA3_model_5daily_1980_2015_E_point.nc'))

dataset_OHC_GLORYS2V3 = Dataset(os.path.join(datapath_GLORYS2V3,'statistics','GLORYS2V3_model_monthly_orca025_OHC_point.nc'))
dataset_OHC_ORAS4 = Dataset(os.path.join(datapath_ORAS4,'statistics','oras4_model_monthly_orca1_OHC_point.nc'))
dataset_OHC_SODA3 = Dataset(os.path.join(datapath_SODA3,'statistics','OMET_SODA3_model_5daily_1980_2015_OHC.nc'))

dataset_psi_GLORYS2V3 = Dataset(os.path.join(datapath_GLORYS2V3,'statistics','GLORYS2V3_model_monthly_orca025_psi_point.nc'))
dataset_psi_ORAS4 = Dataset(os.path.join(datapath_ORAS4,'statistics','oras4_model_monthly_orca1_psi_point.nc'))
dataset_psi_SODA3 = Dataset(os.path.join(datapath_SODA3,'statistics','OMET_SODA3_model_5daily_1980_2015_psi.nc'))

dataset_mask_ORAS4 = Dataset(os.path.join(datapath_ORAS4,'basinmask_050308_UKMO.nc'))
dataset_mask_GLORYS2V3 = Dataset(os.path.join(datapath_GLORYS2V3,'new_maskglo.nc'))
dataset_mask_SODA3 = Dataset(os.path.join(datapath_SODA3,'topog.nc'))
# year
year_ERAI = dataset_AMET_ERAI.variables['year'][14:-4]        # from 1979 to 2016
year_MERRA2 = dataset_AMET_MERRA2.variables['year'][13:-4]    # from 1980 to 2016
year_JRA55 = dataset_AMET_JRA55.variables['year'][14:-3]      # from 1979 to 2015
#year
year_ORAS4 = dataset_OMET_ORAS4.variables['year'][35:-2]      # from 1979 to 2014
year_GLORYS2V3 = dataset_OMET_GLORYS2V3.variables['year'][:-2]# from 1993 to 2014
year_SODA3 = dataset_OMET_SODA3.variables['year'][13:-3]      # from 1980 to 2015

latitude_ERAI = dataset_AMET_ERAI.variables['latitude'][:]
latitude_MERRA2 = dataset_AMET_MERRA2.variables['latitude'][:]
latitude_JRA55 = dataset_AMET_JRA55.variables['latitude'][0:125]
# latitude
latitude_GLORYS2V3 = dataset_OHC_GLORYS2V3.variables['latitude_aux'][579:]
latitude_ORAS4 = dataset_OHC_ORAS4.variables['latitude_aux'][180:]
latitude_SODA3 = dataset_OHC_SODA3.variables['latitude_aux'][569:]

print '*******************************************************************'
print '******************         extract AMET         *******************'
print '*******************************************************************'
# total AMET
AMET_E_ERAI = dataset_AMET_ERAI.variables['E'][14:-4,:,:]/1000 # from Tera Watt to Peta Watt
AMET_E_MERRA2 = dataset_AMET_MERRA2.variables['E'][13:-4,:,:]/1000 # from Tera Watt to Peta Watt
AMET_E_JRA55 = dataset_AMET_JRA55.variables['E'][14:-3,:,0:125]/1000 # from Tera Watt to Peta Watt
# internal energy
AMET_E_cpT_ERAI = dataset_AMET_ERAI.variables['E_cpT'][14:-4,:,:]/1000
AMET_E_cpT_MERRA2 = dataset_AMET_MERRA2.variables['E_cpT'][13:-4,:,:]/1000
AMET_E_cpT_JRA55 = dataset_AMET_JRA55.variables['E_cpT'][14:-3,:,0:125]/1000
# latent heat
AMET_E_Lvq_ERAI = dataset_AMET_ERAI.variables['E_Lvq'][14:-4,:,:]/1000
AMET_E_Lvq_MERRA2 = dataset_AMET_MERRA2.variables['E_Lvq'][13:-4,:,:]/1000
AMET_E_Lvq_JRA55 = dataset_AMET_JRA55.variables['E_Lvq'][14:-3,:,0:125]/1000
# geopotential
AMET_E_gz_ERAI = dataset_AMET_ERAI.variables['E_gz'][14:-4,:,:]/1000
AMET_E_gz_MERRA2 = dataset_AMET_MERRA2.variables['E_gz'][13:-4,:,:]/1000
AMET_E_gz_JRA55 = dataset_AMET_JRA55.variables['E_gz'][14:-3,:,0:125]/1000
# kinetic energy
AMET_E_uv2_ERAI = dataset_AMET_ERAI.variables['E_uv2'][14:-4,:,:]/1000
AMET_E_uv2_MERRA2 = dataset_AMET_MERRA2.variables['E_uv2'][13:-4,:,:]/1000
AMET_E_uv2_JRA55 = dataset_AMET_JRA55.variables['E_uv2'][14:-3,:,0:125]/1000

print '*******************************************************************'
print '******************          make masks          *******************'
print '*******************************************************************'
# Atlantic
tmaskatl_ORAS4 = dataset_mask_ORAS4.variables['tmaskatl'][:]
tmaskatl_GLORYS2V3 = dataset_mask_GLORYS2V3.variables['tmaskatl'][:,1:-1] # attention that the size is different!
tmask_SODA3 = dataset_mask_SODA3.variables['wet'][:]

lat_ORAS4 = dataset_OMET_ORAS4.variables['latitude'][:]
lat_SODA3 = dataset_psi_SODA3.variables['y_C'][:]

# small correction to the ORAS4 atlantic mask
tmaskatl_ORAS4[lat_ORAS4>70] = 0
# calculate the atlantic land sea mask
tmaskatl_SODA3 = np.zeros(tmask_SODA3.shape,dtype=int)
tmaskatl_SODA3[:] = tmask_SODA3
tmaskatl_SODA3[0:225,:] = 0 # boundary south
tmaskatl_SODA3[:,0:727] = 0 # boundary west
tmaskatl_SODA3[:,1200:] = 0 # boundary east
tmaskatl_SODA3[lat_SODA3>70] = 0 # boundary north
# correction Mediterranean
tmaskatl_SODA3[614:680,1100:1240] = 0
tmaskatl_SODA3[660:720,1140:1280] = 0
# correction Pacific
tmaskatl_SODA3[225:522,759:839] = 0
tmaskatl_SODA3[225:545,670:780] = 0
tmaskatl_SODA3[225:560,670:759] = 0
print '*******************************************************************'
print '******************         extract AMET         *******************'
print '*******************************************************************'
OMET_glo_GLORYS2V3_point = dataset_OMET_GLORYS2V3.variables['E'][:-2,:,579:,:]/1000 # from Tera Watt to Peta Watt # start from 1993
OMET_glo_ORAS4_point = dataset_OMET_ORAS4.variables['E'][35:-2,:,180:,:]/1000 # from Tera Watt to Peta Watt # start from 1979
OMET_glo_SODA3_point = dataset_OMET_SODA3.variables['E'][13:-3,:,569:,:]/1000 # from Tera Watt to Peta Watt # start from 1979

OMET_glo_GLORYS2V3 = np.sum(OMET_glo_GLORYS2V3_point,3)/1000 # from Tera Watt to Peta Watt # start from 1993
OMET_glo_ORAS4 = np.sum(OMET_glo_ORAS4_point,3)/1000 # from Tera Watt to Peta Watt # start from 1979
OMET_glo_SODA3 = np.sum(OMET_glo_SODA3_point,3)/1000 # from Tera Watt to Peta Watt # start from 1979
# prepare mask for atlantic
tmaskatl_GLORYS2V3_3D = np.repeat(tmaskatl_GLORYS2V3[np.newaxis,579:,:],12,0)
tmaskatl_ORAS4_3D = np.repeat(tmaskatl_ORAS4[np.newaxis,180:,:],12,0)
tmaskatl_SODA3_3D = np.repeat(tmaskatl_SODA3[np.newaxis,569:,:],12,0)

tmaskatl_GLORYS2V3_4D = np.repeat(tmaskatl_GLORYS2V3_3D[np.newaxis,:,:],len(year_GLORYS2V3),0)
tmaskatl_ORAS4_4D = np.repeat(tmaskatl_ORAS4_3D[np.newaxis,:,:],len(year_ORAS4),0)
tmaskatl_SODA3_4D = np.repeat(tmaskatl_SODA3_3D[np.newaxis,:,:],len(year_SODA3),0)

OMET_atl_GLORYS2V3 = np.sum(OMET_glo_GLORYS2V3_point * tmaskatl_GLORYS2V3_4D,3)/1000 # from Tera Watt to Peta Watt # start from 1993
OMET_atl_ORAS4 = np.sum(OMET_glo_ORAS4_point * tmaskatl_ORAS4_4D,3)/1000 # from Tera Watt to Peta Watt # start from 1979
OMET_atl_SODA3 = np.sum(OMET_glo_SODA3_point * tmaskatl_SODA3_4D,3)/1000 # from Tera Watt to Peta Watt # start from 1979

del OMET_glo_GLORYS2V3_point
del OMET_glo_ORAS4_point
del OMET_glo_SODA3_point

OHC_glo_vert_ORAS4 = np.sum(dataset_OHC_ORAS4.variables['OHC_glo_vert'][35:-2,:,180:,:],3)/1E+10        # start from 1979
OHC_glo_vert_GLORYS2V3 = np.sum(dataset_OHC_GLORYS2V3.variables['OHC_glo_vert'][:-2,:,579:,:],3)/1E+10  # start from 1993
OHC_glo_vert_SODA3 = np.sum(dataset_OHC_SODA3.variables['OHC_glo_vert'][13:-3,:,569:,:],3)/1E+10        # start from 1980

OHC_atl_vert_ORAS4 = np.sum(dataset_OHC_ORAS4.variables['OHC_atl_vert'][35:-2,:,180:,:],3)/1E+10        # start from 1979
OHC_atl_vert_GLORYS2V3 = np.sum(dataset_OHC_GLORYS2V3.variables['OHC_atl_vert'][:-2,:,579:,:],3)/1E+10  # start from 1993
OHC_atl_vert_SODA3 = np.sum(dataset_OHC_SODA3.variables['OHC_atl_vert'][13:-3,:,569:,:],3)/1E+10        # start from 1980

psi_glo_vert_ORAS4 = np.sum(dataset_psi_ORAS4.variables['psi_glo_vert'][35:-2,:,180:,:],3)/1E+10        # start from 1979
psi_glo_vert_GLORYS2V3 = np.sum(dataset_psi_GLORYS2V3.variables['psi_glo_vert'][:-2,:,579:,:],3)/1E+10  # start from 1993
psi_glo_vert_SODA3 = np.sum(dataset_psi_SODA3.variables['psi_glo_vert'][13:-3,:,569:,:],3)/1E+10        # start from 1980

psi_atl_vert_ORAS4 = np.sum(dataset_psi_ORAS4.variables['psi_atl_vert'][35:-2,:,180:,:],3)/1E+10        # start from 1979
psi_atl_vert_GLORYS2V3 = np.sum(dataset_psi_GLORYS2V3.variables['psi_atl_vert'][:-2,:,579:,:],3)/1E+10  # start from 1993
psi_atl_vert_SODA3 = np.sum(dataset_psi_SODA3.variables['psi_atl_vert'][13:-3,:,569:,:],3)/1E+10        # start from 1980
print '*******************************************************************'
print '********************   whitening atmosphere   *********************'
print '*******************************************************************'
# remove the seasonal cycling of AMET
month_ind = np.arange(12)
# dimension of AMET[year,month]
# total energy transport
AMET_E_ERAI_seansonal_cycle = np.mean(AMET_E_ERAI,axis=0)
AMET_E_ERAI_white = np.zeros(AMET_E_ERAI.shape,dtype=float)
for i in np.arange(len(year_ERAI)):
    for j in month_ind:
        AMET_E_ERAI_white[i,j,:] = AMET_E_ERAI[i,j,:] - AMET_E_ERAI_seansonal_cycle[j,:]

AMET_E_MERRA2_seansonal_cycle = np.mean(AMET_E_MERRA2,axis=0)
AMET_E_MERRA2_white = np.zeros(AMET_E_MERRA2.shape,dtype=float)
for i in np.arange(len(year_MERRA2)):
    for j in month_ind:
        AMET_E_MERRA2_white[i,j,:] = AMET_E_MERRA2[i,j,:] - AMET_E_MERRA2_seansonal_cycle[j,:]

AMET_E_JRA55_seansonal_cycle = np.mean(AMET_E_JRA55,axis=0)
AMET_E_JRA55_white = np.zeros(AMET_E_JRA55.shape,dtype=float)
for i in np.arange(len(year_JRA55)):
    for j in month_ind:
        AMET_E_JRA55_white[i,j,:] = AMET_E_JRA55[i,j,:] - AMET_E_JRA55_seansonal_cycle[j,:]

# internal energy
AMET_E_cpT_ERAI_seansonal_cycle = np.mean(AMET_E_cpT_ERAI,axis=0)
AMET_E_cpT_ERAI_white = np.zeros(AMET_E_cpT_ERAI.shape,dtype=float)
for i in np.arange(len(year_ERAI)):
    for j in month_ind:
        AMET_E_cpT_ERAI_white[i,j,:] = AMET_E_cpT_ERAI[i,j,:] - AMET_E_cpT_ERAI_seansonal_cycle[j,:]

AMET_E_cpT_MERRA2_seansonal_cycle = np.mean(AMET_E_cpT_MERRA2,axis=0)
AMET_E_cpT_MERRA2_white = np.zeros(AMET_E_cpT_MERRA2.shape,dtype=float)
for i in np.arange(len(year_MERRA2)):
    for j in month_ind:
        AMET_E_cpT_MERRA2_white[i,j,:] = AMET_E_cpT_MERRA2[i,j,:] - AMET_E_cpT_MERRA2_seansonal_cycle[j,:]

AMET_E_cpT_JRA55_seansonal_cycle = np.mean(AMET_E_cpT_JRA55,axis=0)
AMET_E_cpT_JRA55_white = np.zeros(AMET_E_cpT_JRA55.shape,dtype=float)
for i in np.arange(len(year_JRA55)):
    for j in month_ind:
        AMET_E_cpT_JRA55_white[i,j,:] = AMET_E_cpT_JRA55[i,j,:] - AMET_E_cpT_JRA55_seansonal_cycle[j,:]

# latent heat
AMET_E_Lvq_ERAI_seansonal_cycle = np.mean(AMET_E_Lvq_ERAI,axis=0)
AMET_E_Lvq_ERAI_white = np.zeros(AMET_E_Lvq_ERAI.shape,dtype=float)
for i in np.arange(len(year_ERAI)):
    for j in month_ind:
        AMET_E_Lvq_ERAI_white[i,j,:] = AMET_E_Lvq_ERAI[i,j,:] - AMET_E_Lvq_ERAI_seansonal_cycle[j,:]

AMET_E_Lvq_MERRA2_seansonal_cycle = np.mean(AMET_E_Lvq_MERRA2,axis=0)
AMET_E_Lvq_MERRA2_white = np.zeros(AMET_E_Lvq_MERRA2.shape,dtype=float)
for i in np.arange(len(year_MERRA2)):
    for j in month_ind:
        AMET_E_Lvq_MERRA2_white[i,j,:] = AMET_E_Lvq_MERRA2[i,j,:] - AMET_E_Lvq_MERRA2_seansonal_cycle[j,:]

AMET_E_Lvq_JRA55_seansonal_cycle = np.mean(AMET_E_Lvq_JRA55,axis=0)
AMET_E_Lvq_JRA55_white = np.zeros(AMET_E_Lvq_JRA55.shape,dtype=float)
for i in np.arange(len(year_JRA55)):
    for j in month_ind:
        AMET_E_Lvq_JRA55_white[i,j,:] = AMET_E_Lvq_JRA55[i,j,:] - AMET_E_Lvq_JRA55_seansonal_cycle[j,:]

# geopotential
AMET_E_gz_ERAI_seansonal_cycle = np.mean(AMET_E_gz_ERAI,axis=0)
AMET_E_gz_ERAI_white = np.zeros(AMET_E_gz_ERAI.shape,dtype=float)
for i in np.arange(len(year_ERAI)):
    for j in month_ind:
        AMET_E_gz_ERAI_white[i,j,:] = AMET_E_gz_ERAI[i,j,:] - AMET_E_gz_ERAI_seansonal_cycle[j,:]

AMET_E_gz_MERRA2_seansonal_cycle = np.mean(AMET_E_gz_MERRA2,axis=0)
AMET_E_gz_MERRA2_white = np.zeros(AMET_E_gz_MERRA2.shape,dtype=float)
for i in np.arange(len(year_MERRA2)):
    for j in month_ind:
        AMET_E_gz_MERRA2_white[i,j,:] = AMET_E_gz_MERRA2[i,j,:] - AMET_E_gz_MERRA2_seansonal_cycle[j,:]

AMET_E_gz_JRA55_seansonal_cycle = np.mean(AMET_E_gz_JRA55,axis=0)
AMET_E_gz_JRA55_white = np.zeros(AMET_E_gz_JRA55.shape,dtype=float)
for i in np.arange(len(year_JRA55)):
    for j in month_ind:
        AMET_E_gz_JRA55_white[i,j,:] = AMET_E_gz_JRA55[i,j,:] - AMET_E_gz_JRA55_seansonal_cycle[j,:]

# kinetic energy
AMET_E_uv2_ERAI_seansonal_cycle = np.mean(AMET_E_uv2_ERAI,axis=0)
AMET_E_uv2_ERAI_white = np.zeros(AMET_E_uv2_ERAI.shape,dtype=float)
for i in np.arange(len(year_ERAI)):
    for j in month_ind:
        AMET_E_uv2_ERAI_white[i,j,:] = AMET_E_uv2_ERAI[i,j,:] - AMET_E_uv2_ERAI_seansonal_cycle[j,:]

AMET_E_uv2_MERRA2_seansonal_cycle = np.mean(AMET_E_uv2_MERRA2,axis=0)
AMET_E_uv2_MERRA2_white = np.zeros(AMET_E_uv2_MERRA2.shape,dtype=float)
for i in np.arange(len(year_MERRA2)):
    for j in month_ind:
        AMET_E_uv2_MERRA2_white[i,j,:] = AMET_E_uv2_MERRA2[i,j,:] - AMET_E_uv2_MERRA2_seansonal_cycle[j,:]

AMET_E_uv2_JRA55_seansonal_cycle = np.mean(AMET_E_uv2_JRA55,axis=0)
AMET_E_uv2_JRA55_white = np.zeros(AMET_E_uv2_JRA55.shape,dtype=float)
for i in np.arange(len(year_JRA55)):
    for j in month_ind:
        AMET_E_uv2_JRA55_white[i,j,:] = AMET_E_uv2_JRA55[i,j,:] - AMET_E_uv2_JRA55_seansonal_cycle[j,:]
print '*******************************************************************'
print '*************^*******     whitening ocean     *********************'
print '*******************************************************************'
# seasonal cycle of OHC for the globe
seansonal_cycle_OMET_glo_ORAS4 = np.mean(OMET_glo_ORAS4,axis=0)
seansonal_cycle_OMET_glo_GLORYS2V3 = np.mean(OMET_glo_GLORYS2V3,axis=0)
seansonal_cycle_OMET_glo_SODA3 = np.mean(OMET_glo_SODA3,axis=0)

seansonal_cycle_OMET_atl_ORAS4 = np.mean(OMET_atl_ORAS4,axis=0)
seansonal_cycle_OMET_atl_GLORYS2V3 = np.mean(OMET_atl_GLORYS2V3,axis=0)
seansonal_cycle_OMET_atl_SODA3 = np.mean(OMET_atl_SODA3,axis=0)

seansonal_cycle_OHC_glo_vert_ORAS4 = np.mean(OHC_glo_vert_ORAS4,axis=0)
seansonal_cycle_OHC_glo_vert_GLORYS2V3 = np.mean(OHC_glo_vert_GLORYS2V3,axis=0)
seansonal_cycle_OHC_glo_vert_SODA3 = np.mean(OHC_glo_vert_SODA3,axis=0)

seansonal_cycle_OHC_atl_vert_ORAS4 = np.mean(OHC_atl_vert_ORAS4,axis=0)
seansonal_cycle_OHC_atl_vert_GLORYS2V3 = np.mean(OHC_atl_vert_GLORYS2V3,axis=0)
seansonal_cycle_OHC_atl_vert_SODA3 = np.mean(OHC_atl_vert_SODA3,axis=0)

seansonal_cycle_psi_glo_vert_ORAS4 = np.mean(psi_glo_vert_ORAS4,axis=0)
seansonal_cycle_psi_glo_vert_GLORYS2V3 = np.mean(psi_glo_vert_GLORYS2V3,axis=0)
seansonal_cycle_psi_glo_vert_SODA3 = np.mean(psi_glo_vert_SODA3,axis=0)

seansonal_cycle_psi_atl_vert_ORAS4 = np.mean(psi_atl_vert_ORAS4,axis=0)
seansonal_cycle_psi_atl_vert_GLORYS2V3 = np.mean(psi_atl_vert_GLORYS2V3,axis=0)
seansonal_cycle_psi_atl_vert_SODA3 = np.mean(psi_atl_vert_SODA3,axis=0)

OMET_glo_ORAS4_white = np.zeros(OMET_glo_ORAS4.shape,dtype=float)
OMET_glo_GLORYS2V3_white = np.zeros(OMET_glo_GLORYS2V3.shape,dtype=float)
OMET_glo_SODA3_white = np.zeros(OMET_glo_SODA3.shape,dtype=float)

OMET_atl_ORAS4_white = np.zeros(OMET_atl_ORAS4.shape,dtype=float)
OMET_atl_GLORYS2V3_white = np.zeros(OMET_atl_GLORYS2V3.shape,dtype=float)
OMET_atl_SODA3_white = np.zeros(OMET_atl_SODA3.shape,dtype=float)

OHC_glo_vert_ORAS4_white = np.zeros(OHC_glo_vert_ORAS4.shape,dtype=float)
OHC_glo_vert_GLORYS2V3_white = np.zeros(OHC_glo_vert_GLORYS2V3.shape,dtype=float)
OHC_glo_vert_SODA3_white = np.zeros(OHC_glo_vert_SODA3.shape,dtype=float)

OHC_atl_vert_ORAS4_white = np.zeros(OHC_atl_vert_ORAS4.shape,dtype=float)
OHC_atl_vert_GLORYS2V3_white = np.zeros(OHC_atl_vert_GLORYS2V3.shape,dtype=float)
OHC_atl_vert_SODA3_white = np.zeros(OHC_atl_vert_SODA3.shape,dtype=float)

psi_glo_vert_ORAS4_white = np.zeros(psi_glo_vert_ORAS4.shape,dtype=float)
psi_glo_vert_GLORYS2V3_white = np.zeros(psi_glo_vert_GLORYS2V3.shape,dtype=float)
psi_glo_vert_SODA3_white = np.zeros(psi_glo_vert_SODA3.shape,dtype=float)

psi_atl_vert_ORAS4_white = np.zeros(psi_atl_vert_ORAS4.shape,dtype=float)
psi_atl_vert_GLORYS2V3_white = np.zeros(psi_atl_vert_GLORYS2V3.shape,dtype=float)
psi_atl_vert_SODA3_white = np.zeros(psi_atl_vert_SODA3.shape,dtype=float)

for i in np.arange(len(year_ORAS4)):
    for j in month_ind:
        OMET_glo_ORAS4_white[i,j,:] = OMET_glo_ORAS4[i,j,:] - seansonal_cycle_OMET_glo_ORAS4[j,:]
        OMET_atl_ORAS4_white[i,j,:] = OMET_atl_ORAS4[i,j,:] - seansonal_cycle_OMET_atl_ORAS4[j,:]
        OHC_glo_vert_ORAS4_white[i,j,:] = OHC_glo_vert_ORAS4[i,j,:] - seansonal_cycle_OHC_glo_vert_ORAS4[j,:]
        OHC_atl_vert_ORAS4_white[i,j,:] = OHC_atl_vert_ORAS4[i,j,:] - seansonal_cycle_OHC_atl_vert_ORAS4[j,:]
        psi_glo_vert_ORAS4_white[i,j,:] = psi_glo_vert_ORAS4[i,j,:] - seansonal_cycle_psi_glo_vert_ORAS4[j,:]
        psi_atl_vert_ORAS4_white[i,j,:] = psi_atl_vert_ORAS4[i,j,:] - seansonal_cycle_psi_atl_vert_ORAS4[j,:]

for i in np.arange(len(year_GLORYS2V3)):
    for j in month_ind:
        OMET_glo_GLORYS2V3_white[i,j,:] = OMET_glo_GLORYS2V3[i,j,:] - seansonal_cycle_OMET_glo_GLORYS2V3[j,:]
        OMET_atl_GLORYS2V3_white[i,j,:] = OMET_atl_GLORYS2V3[i,j,:] - seansonal_cycle_OMET_atl_GLORYS2V3[j,:]
        OHC_glo_vert_GLORYS2V3_white[i,j,:] = OHC_glo_vert_GLORYS2V3[i,j,:] - seansonal_cycle_OHC_glo_vert_GLORYS2V3[j,:]
        OHC_atl_vert_GLORYS2V3_white[i,j,:] = OHC_atl_vert_GLORYS2V3[i,j,:] - seansonal_cycle_OHC_atl_vert_GLORYS2V3[j,:]
        psi_glo_vert_GLORYS2V3_white[i,j,:] = psi_glo_vert_GLORYS2V3[i,j,:] - seansonal_cycle_psi_glo_vert_GLORYS2V3[j,:]
        psi_atl_vert_GLORYS2V3_white[i,j,:] = psi_atl_vert_GLORYS2V3[i,j,:] - seansonal_cycle_psi_atl_vert_GLORYS2V3[j,:]

for i in np.arange(len(year_SODA3)):
    for j in month_ind:
        OMET_glo_SODA3_white[i,j,:] = OMET_glo_SODA3[i,j,:] - seansonal_cycle_OMET_glo_SODA3[j,:]
        OMET_atl_SODA3_white[i,j,:] = OMET_atl_SODA3[i,j,:] - seansonal_cycle_OMET_atl_SODA3[j,:]
        OHC_glo_vert_SODA3_white[i,j,:] = OHC_glo_vert_SODA3[i,j,:] - seansonal_cycle_OHC_glo_vert_SODA3[j,:]
        OHC_atl_vert_SODA3_white[i,j,:] = OHC_atl_vert_SODA3[i,j,:] - seansonal_cycle_OHC_atl_vert_SODA3[j,:]
        psi_glo_vert_SODA3_white[i,j,:] = psi_glo_vert_SODA3[i,j,:] - seansonal_cycle_psi_glo_vert_SODA3[j,:]
        psi_atl_vert_SODA3_white[i,j,:] = psi_atl_vert_SODA3[i,j,:] - seansonal_cycle_psi_atl_vert_SODA3[j,:]

print '*******************************************************************'
print '***************    prepare variables atmosphere   *****************'
print '*******************************************************************'
# take the time series of original signal
# total energy transport
# AMET_E_ERAI_series = AMET_E_ERAI.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI))
# AMET_E_MERRA2_series = AMET_E_MERRA2.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2))
# AMET_E_JRA55_series = AMET_E_JRA55.reshape(len(year_JRA55)*len(month_ind),len(latitude_JRA55))
# # internal energy
# AMET_E_cpT_ERAI_series = AMET_E_cpT_ERAI.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI))
# AMET_E_cpT_MERRA2_series = AMET_E_cpT_MERRA2.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2))
# AMET_E_cpT_JRA55_series = AMET_E_cpT_JRA55.reshape(len(year_JRA55)*len(month_ind),len(latitude_JRA55))
# # latent heat
# AMET_E_Lvq_ERAI_series = AMET_E_Lvq_ERAI.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI))
# AMET_E_Lvq_MERRA2_series = AMET_E_Lvq_MERRA2.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2))
# AMET_E_Lvq_JRA55_series = AMET_E_Lvq_JRA55.reshape(len(year_JRA55)*len(month_ind),len(latitude_JRA55))
# # geopotential
# AMET_E_gz_ERAI_series = AMET_E_gz_ERAI.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI))
# AMET_E_gz_MERRA2_series = AMET_E_gz_MERRA2.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2))
# AMET_E_gz_JRA55_series = AMET_E_gz_JRA55.reshape(len(year_JRA55)*len(month_ind),len(latitude_JRA55))
# # kinetic energy
# AMET_E_uv2_ERAI_series = AMET_E_uv2_ERAI.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI))
# AMET_E_uv2_MERRA2_series = AMET_E_uv2_MERRA2.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2))
# AMET_E_uv2_JRA55_series = AMET_E_uv2_JRA55.reshape(len(year_JRA55)*len(month_ind),len(latitude_JRA55))

# take the time series of anomalies
AMET_E_ERAI_white_series = AMET_E_ERAI_white.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI))
AMET_E_MERRA2_white_series = AMET_E_MERRA2_white.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2))
AMET_E_JRA55_white_series = AMET_E_JRA55_white.reshape(len(year_JRA55)*len(month_ind),len(latitude_JRA55))
# internal energy
AMET_E_cpT_ERAI_white_series = AMET_E_cpT_ERAI_white.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI))
AMET_E_cpT_MERRA2_white_series = AMET_E_cpT_MERRA2_white.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2))
AMET_E_cpT_JRA55_white_series = AMET_E_cpT_JRA55_white.reshape(len(year_JRA55)*len(month_ind),len(latitude_JRA55))
# latent heat
AMET_E_Lvq_ERAI_white_series = AMET_E_Lvq_ERAI_white.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI))
AMET_E_Lvq_MERRA2_white_series = AMET_E_Lvq_MERRA2_white.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2))
AMET_E_Lvq_JRA55_white_series = AMET_E_Lvq_JRA55_white.reshape(len(year_JRA55)*len(month_ind),len(latitude_JRA55))
# geopotential
AMET_E_gz_ERAI_white_series = AMET_E_gz_ERAI_white.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI))
AMET_E_gz_MERRA2_white_series = AMET_E_gz_MERRA2_white.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2))
AMET_E_gz_JRA55_white_series = AMET_E_gz_JRA55_white.reshape(len(year_JRA55)*len(month_ind),len(latitude_JRA55))
# kinetic energy
AMET_E_uv2_ERAI_white_series = AMET_E_uv2_ERAI_white.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI))
AMET_E_uv2_MERRA2_white_series = AMET_E_uv2_MERRA2_white.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2))
AMET_E_uv2_JRA55_white_series = AMET_E_uv2_JRA55_white.reshape(len(year_JRA55)*len(month_ind),len(latitude_JRA55))
print '*******************************************************************'
print '***************      prepare variables ocean      *****************'
print '*******************************************************************'
# OMET_ORAS4_series = OMET_ORAS4.reshape(len(year_ORAS4)*len(month_ind),len(latitude_ORAS4))
# OMET_GLORYS2V3_series = OMET_GLORYS2V3.reshape(len(year_GLORYS2V3)*len(month_ind),len(latitude_GLORYS2V3))
# OMET_SODA3_series = OMET_SODA3.reshape(len(year_SODA3)*len(month_ind),len(latitude_SODA3))
# dataset without seasonal cycle - time series
OMET_glo_ORAS4_white_series = OMET_glo_ORAS4_white.reshape(len(year_ORAS4)*len(month_ind),len(latitude_ORAS4))
OMET_glo_GLORYS2V3_white_series = OMET_glo_GLORYS2V3_white.reshape(len(year_GLORYS2V3)*len(month_ind),len(latitude_GLORYS2V3))
OMET_glo_SODA3_white_series = OMET_glo_SODA3_white.reshape(len(year_SODA3)*len(month_ind),len(latitude_SODA3))

OMET_atl_ORAS4_white_series = OMET_atl_ORAS4_white.reshape(len(year_ORAS4)*len(month_ind),len(latitude_ORAS4))
OMET_atl_GLORYS2V3_white_series = OMET_atl_GLORYS2V3_white.reshape(len(year_GLORYS2V3)*len(month_ind),len(latitude_GLORYS2V3))
OMET_atl_SODA3_white_series = OMET_atl_SODA3_white.reshape(len(year_SODA3)*len(month_ind),len(latitude_SODA3))

# dataset with seasonal cycle - time series
# OHC_glo_vert_ORAS4_series = OHC_glo_vert_ORAS4.reshape(len(year_ORAS4)*len(month_ind),len(latitude_ORAS4))
# OHC_glo_vert_GLORYS2V3_series = OHC_glo_vert_GLORYS2V3.reshape(len(year_GLORYS2V3)*len(month_ind),len(latitude_GLORYS2V3))
# OHC_glo_vert_SODA3_series = OHC_glo_vert_SODA3.reshape(len(year_SODA3)*len(month_ind),len(latitude_SODA3))
# dataset without seasonal cycle - time series
OHC_glo_vert_ORAS4_white_series = OHC_glo_vert_ORAS4_white.reshape(len(year_ORAS4)*len(month_ind),len(latitude_ORAS4))
OHC_glo_vert_GLORYS2V3_white_series = OHC_glo_vert_GLORYS2V3_white.reshape(len(year_GLORYS2V3)*len(month_ind),len(latitude_GLORYS2V3))
OHC_glo_vert_SODA3_white_series = OHC_glo_vert_SODA3_white.reshape(len(year_SODA3)*len(month_ind),len(latitude_SODA3))

OHC_atl_vert_ORAS4_white_series = OHC_atl_vert_ORAS4_white.reshape(len(year_ORAS4)*len(month_ind),len(latitude_ORAS4))
OHC_atl_vert_GLORYS2V3_white_series = OHC_atl_vert_GLORYS2V3_white.reshape(len(year_GLORYS2V3)*len(month_ind),len(latitude_GLORYS2V3))
OHC_atl_vert_SODA3_white_series = OHC_atl_vert_SODA3_white.reshape(len(year_SODA3)*len(month_ind),len(latitude_SODA3))

# dataset without seasonal cycle - time series
psi_glo_vert_ORAS4_white_series = psi_glo_vert_ORAS4_white.reshape(len(year_ORAS4)*len(month_ind),len(latitude_ORAS4))
psi_glo_vert_GLORYS2V3_white_series = psi_glo_vert_GLORYS2V3_white.reshape(len(year_GLORYS2V3)*len(month_ind),len(latitude_GLORYS2V3))
psi_glo_vert_SODA3_white_series = psi_glo_vert_SODA3_white.reshape(len(year_SODA3)*len(month_ind),len(latitude_SODA3))

psi_atl_vert_ORAS4_white_series = psi_atl_vert_ORAS4_white.reshape(len(year_ORAS4)*len(month_ind),len(latitude_ORAS4))
psi_atl_vert_GLORYS2V3_white_series = psi_atl_vert_GLORYS2V3_white.reshape(len(year_GLORYS2V3)*len(month_ind),len(latitude_GLORYS2V3))
psi_atl_vert_SODA3_white_series = psi_atl_vert_SODA3_white.reshape(len(year_SODA3)*len(month_ind),len(latitude_SODA3))

print '*******************************************************************'
print '******************    trend at each latitude    *******************'
print '*******************************************************************'
counter_ERAI = np.arange(len(year_ERAI)*len(month_ind))
counter_MERRA2 = np.arange(len(year_MERRA2)*len(month_ind))
counter_JRA55 = np.arange(len(year_JRA55)*len(month_ind))
counter_ORAS4 = np.arange(len(year_ORAS4)*len(month_ind))
counter_GLORYS2V3 = np.arange(len(year_GLORYS2V3)*len(month_ind))
counter_SODA3 = np.arange(len(year_SODA3)*len(month_ind))
# Trend of total energy transport
# the calculation of trend are based on target climatolory after removing seasonal cycles
# trend of OMET at each lat
# create an array to store the slope coefficient and residual
a_ERAI = np.zeros((len(latitude_ERAI)),dtype = float)
b_ERAI = np.zeros((len(latitude_ERAI)),dtype = float)
# the least square fit equation is y = ax + b
# np.lstsq solves the equation ax=b, a & b are the input
# thus the input file should be reformed for the function
# we can rewrite the line y = Ap, with A = [x,1] and p = [[a],[b]]
A_ERAI = np.vstack([counter_ERAI,np.ones(len(counter_ERAI))]).T
# start the least square fitting
for i in np.arange(len(latitude_ERAI)):
        # return value: coefficient matrix a and b, where a is the slope
        a_ERAI[i], b_ERAI[i] = np.linalg.lstsq(A_ERAI,AMET_E_ERAI_white_series[:,i])[0]

a_MERRA2 = np.zeros((len(latitude_MERRA2)),dtype = float)
b_MERRA2 = np.zeros((len(latitude_MERRA2)),dtype = float)
A_MERRA2 = np.vstack([counter_MERRA2,np.ones(len(counter_MERRA2))]).T
for i in np.arange(len(latitude_MERRA2)):
        a_MERRA2[i], b_MERRA2[i] = np.linalg.lstsq(A_MERRA2,AMET_E_MERRA2_white_series[:,i])[0]

a_JRA55 = np.zeros((len(latitude_JRA55)),dtype = float)
b_JRA55 = np.zeros((len(latitude_JRA55)),dtype = float)
A_JRA55 = np.vstack([counter_JRA55,np.ones(len(counter_JRA55))]).T
for i in np.arange(len(latitude_JRA55)):
        a_JRA55[i], b_JRA55[i] = np.linalg.lstsq(A_JRA55,AMET_E_JRA55_white_series[:,i])[0]

# trend of AMET anomalies at each latitude
fig1 = plt.figure()
fig1.set_size_inches(8, 6)
plt.axhline(y=0, color='k',ls='-')
plt.plot(latitude_ERAI,a_ERAI*12,'b-',label='ERAI')
plt.plot(latitude_MERRA2,a_MERRA2*12,'r-',label='MERRA2')
plt.plot(latitude_JRA55,a_JRA55*12,'g-',label='JRA55')
plt.title('Trend of AMET anomalies from 20N to 90N (1993-2012)' )
plt.legend(frameon=True, loc=3, prop={'size': 14})
plt.xlabel("Latitudes",fontsize = 16)
plt.xticks(fontsize = 16)
plt.ylabel("Meridional Energy Transport (PW/year)",fontsize = 16)
plt.yticks(fontsize=16)
plt.show()
fig1.savefig(output_path + os.sep + 'Comp_AMET_E_white_trend.jpg', dpi = 400)

# Trend of latent energy transport
for i in np.arange(len(latitude_ERAI)):
        a_ERAI[i], b_ERAI[i] = np.linalg.lstsq(A_ERAI,AMET_E_Lvq_ERAI_white_series[:,i])[0]
for i in np.arange(len(latitude_MERRA2)):
        a_MERRA2[i], b_MERRA2[i] = np.linalg.lstsq(A_MERRA2,AMET_E_Lvq_MERRA2_white_series[:,i])[0]
for i in np.arange(len(latitude_JRA55)):
        a_JRA55[i], b_JRA55[i] = np.linalg.lstsq(A_JRA55,AMET_E_Lvq_JRA55_white_series[:,i])[0]

fig2 = plt.figure()
fig2.set_size_inches(8, 6)
plt.axhline(y=0, color='k',ls='-')
plt.plot(latitude_ERAI,a_ERAI*12,'b-',label='ERAI')
plt.plot(latitude_MERRA2,a_MERRA2*12,'r-',label='MERRA2')
plt.plot(latitude_JRA55,a_JRA55*12,'g-',label='JRA55')
plt.title('Trend of latent heat transport anomalies from 20N to 90N (1993-2012)')
plt.legend(frameon=True, loc=3, prop={'size': 14})
plt.xlabel("Latitudes",fontsize = 16)
plt.xticks(fontsize = 16)
plt.ylabel("Meridional Energy Transport (PW/year)",fontsize = 16)
plt.yticks(fontsize=16)
plt.show()
fig2.savefig(output_path + os.sep + 'Comp_AMET_E_Lvq_white_trend.jpg', dpi = 400)

# Trend of temperature transport
for i in np.arange(len(latitude_ERAI)):
        a_ERAI[i], b_ERAI[i] = np.linalg.lstsq(A_ERAI,AMET_E_cpT_ERAI_white_series[:,i])[0]
for i in np.arange(len(latitude_MERRA2)):
        a_MERRA2[i], b_MERRA2[i] = np.linalg.lstsq(A_MERRA2,AMET_E_cpT_MERRA2_white_series[:,i])[0]
for i in np.arange(len(latitude_JRA55)):
        a_JRA55[i], b_JRA55[i] = np.linalg.lstsq(A_JRA55,AMET_E_cpT_JRA55_white_series[:,i])[0]

fig3 = plt.figure()
fig3.set_size_inches(8, 6)
plt.axhline(y=0, color='k',ls='-')
plt.plot(latitude_ERAI,a_ERAI*12,'b-',label='ERAI')
plt.plot(latitude_MERRA2,a_MERRA2*12,'r-',label='MERRA2')
plt.plot(latitude_JRA55,a_JRA55*12,'g-',label='JRA55')
plt.title('Trend of temperature transport anomalies from 20N to 90N (1993-2012)')
plt.legend(frameon=True, loc=3, prop={'size': 14})
plt.xlabel("Latitudes",fontsize = 16)
plt.xticks(fontsize = 16)
plt.ylabel("Meridional Energy Transport (PW/year)",fontsize = 16)
plt.yticks(fontsize=16)
plt.show()
fig3.savefig(output_path + os.sep + 'Comp_AMET_E_cpT_white_trend.jpg', dpi = 400)

a_ORAS4 = np.zeros((len(latitude_ORAS4)),dtype = float)
b_ORAS4 = np.zeros((len(latitude_ORAS4)),dtype = float)
A_ORAS4 = np.vstack([counter_ORAS4,np.ones(len(counter_ORAS4))]).T

a_GLORYS2V3 = np.zeros((len(latitude_GLORYS2V3)),dtype = float)
b_GLORYS2V3 = np.zeros((len(latitude_GLORYS2V3)),dtype = float)
A_GLORYS2V3 = np.vstack([counter_GLORYS2V3,np.ones(len(counter_GLORYS2V3))]).T

a_SODA3 = np.zeros((len(latitude_SODA3)),dtype = float)
b_SODA3 = np.zeros((len(latitude_SODA3)),dtype = float)
A_SODA3 = np.vstack([counter_SODA3,np.ones(len(counter_SODA3))]).T

# Trend of OMET in the entire globe
for i in np.arange(len(latitude_ORAS4)):
        a_ORAS4[i], b_ORAS4[i] = np.linalg.lstsq(A_ORAS4,OMET_glo_ORAS4_white_series[:,i])[0]
for i in np.arange(len(latitude_GLORYS2V3)):
        a_GLORYS2V3[i], b_GLORYS2V3[i] = np.linalg.lstsq(A_GLORYS2V3,OMET_glo_GLORYS2V3_white_series[:,i])[0]
for i in np.arange(len(latitude_SODA3)):
        a_SODA3[i], b_SODA3[i] = np.linalg.lstsq(A_SODA3,OMET_glo_SODA3_white_series[:,i])[0]

fig4 = plt.figure()
fig4.set_size_inches(8, 6)
plt.axhline(y=0, color='k',ls='-')
plt.plot(latitude_ORAS4,a_ORAS4*12,'b-',label='ORAS4')
plt.plot(latitude_GLORYS2V3,a_GLORYS2V3*12,'r-',label='GLORYS2V3')
plt.plot(latitude_SODA3,a_SODA3*12,'g-',label='SODA3')
plt.title('Trend of global OMET anomalies from 20N to 90N (1993-2012)')
plt.legend(frameon=True, loc=3, prop={'size': 14})
plt.xlabel("Latitudes",fontsize = 16)
plt.xticks(fontsize = 16)
plt.ylabel("Meridional Energy Transport (PW/year)",fontsize = 16)
plt.yticks(fontsize=16)
plt.show()
fig4.savefig(output_path + os.sep + 'Comp_OMET_glo_white_trend.jpg', dpi = 400)

# Trend of OMET in the atlantic
for i in np.arange(len(latitude_ORAS4)):
        a_ORAS4[i], b_ORAS4[i] = np.linalg.lstsq(A_ORAS4,OMET_atl_ORAS4_white_series[:,i])[0]
for i in np.arange(len(latitude_GLORYS2V3)):
        a_GLORYS2V3[i], b_GLORYS2V3[i] = np.linalg.lstsq(A_GLORYS2V3,OMET_atl_GLORYS2V3_white_series[:,i])[0]
for i in np.arange(len(latitude_SODA3)):
        a_SODA3[i], b_SODA3[i] = np.linalg.lstsq(A_SODA3,OMET_atl_SODA3_white_series[:,i])[0]

fig5 = plt.figure()
fig5.set_size_inches(8, 6)
plt.axhline(y=0, color='k',ls='-')
plt.plot(latitude_ORAS4,a_ORAS4*12,'b-',label='ORAS4')
plt.plot(latitude_GLORYS2V3,a_GLORYS2V3*12,'r-',label='GLORYS2V3')
plt.plot(latitude_SODA3,a_SODA3*12,'g-',label='SODA3')
plt.title('Trend of Atlantic OMET anomalies from 20N to 90N (1993-2012)')
plt.legend(frameon=True, loc=3, prop={'size': 14})
plt.xlabel("Latitudes",fontsize = 16)
plt.xticks(fontsize = 16)
plt.ylabel("Meridional Energy Transport (PW/year)",fontsize = 16)
plt.yticks(fontsize=16)
plt.show()
fig5.savefig(output_path + os.sep + 'Comp_OMET_atl_white_trend.jpg', dpi = 400)

# Trend of OHC in the entire globe
for i in np.arange(len(latitude_ORAS4)):
        a_ORAS4[i], b_ORAS4[i] = np.linalg.lstsq(A_ORAS4,OHC_glo_vert_ORAS4_white_series[:,i])[0]
for i in np.arange(len(latitude_GLORYS2V3)):
        a_GLORYS2V3[i], b_GLORYS2V3[i] = np.linalg.lstsq(A_GLORYS2V3,OHC_glo_vert_GLORYS2V3_white_series[:,i])[0]
for i in np.arange(len(latitude_SODA3)):
        a_SODA3[i], b_SODA3[i] = np.linalg.lstsq(A_SODA3,OHC_glo_vert_SODA3_white_series[:,i])[0]

fig6 = plt.figure()
fig6.set_size_inches(8, 6)
plt.axhline(y=0, color='k',ls='-')
plt.plot(latitude_ORAS4,a_ORAS4*12,'b-',label='ORAS4')
plt.plot(latitude_GLORYS2V3,a_GLORYS2V3*12,'r-',label='GLORYS2V3')
plt.plot(latitude_SODA3,a_SODA3*12,'g-',label='SODA3')
plt.title('Trend of global OHC anomalies from 20N to 90N (1993-2012)')
plt.legend(frameon=True, loc=3, prop={'size': 14})
plt.xlabel("Latitudes",fontsize = 16)
plt.xticks(fontsize = 16)
plt.ylabel("Meridional Energy Transport (1E+22 Joule/year)",fontsize = 16)
plt.yticks(fontsize=16)
plt.show()
fig6.savefig(output_path + os.sep + 'Comp_OHC_glo_white_trend.jpg', dpi = 400)

# Trend of OHC in the atlantic
for i in np.arange(len(latitude_ORAS4)):
        a_ORAS4[i], b_ORAS4[i] = np.linalg.lstsq(A_ORAS4,OHC_atl_vert_ORAS4_white_series[:,i])[0]
for i in np.arange(len(latitude_GLORYS2V3)):
        a_GLORYS2V3[i], b_GLORYS2V3[i] = np.linalg.lstsq(A_GLORYS2V3,OHC_atl_vert_GLORYS2V3_white_series[:,i])[0]
for i in np.arange(len(latitude_SODA3)):
        a_SODA3[i], b_SODA3[i] = np.linalg.lstsq(A_SODA3,OHC_atl_vert_SODA3_white_series[:,i])[0]

fig7 = plt.figure()
fig7.set_size_inches(8, 6)
plt.axhline(y=0, color='k',ls='-')
plt.plot(latitude_ORAS4,a_ORAS4*12,'b-',label='ORAS4')
plt.plot(latitude_GLORYS2V3,a_GLORYS2V3*12,'r-',label='GLORYS2V3')
plt.plot(latitude_SODA3,a_SODA3*12,'g-',label='SODA3')
plt.title('Trend of Atlantic OHC anomalies from 20N to 90N (1993-2012)')
plt.legend(frameon=True, loc=3, prop={'size': 14})
plt.xlabel("Latitudes",fontsize = 16)
plt.xticks(fontsize = 16)
plt.ylabel("Meridional Energy Transport (1E+22 Joule/year)",fontsize = 16)
plt.yticks(fontsize=16)
plt.show()
fig7.savefig(output_path + os.sep + 'Comp_OHC_atl_white_trend.jpg', dpi = 400)

# Trend of psi in the entire globe
for i in np.arange(len(latitude_ORAS4)):
        a_ORAS4[i], b_ORAS4[i] = np.linalg.lstsq(A_ORAS4,psi_glo_vert_ORAS4_white_series[:,i])[0]
for i in np.arange(len(latitude_GLORYS2V3)):
        a_GLORYS2V3[i], b_GLORYS2V3[i] = np.linalg.lstsq(A_GLORYS2V3,psi_glo_vert_GLORYS2V3_white_series[:,i])[0]
for i in np.arange(len(latitude_SODA3)):
        a_SODA3[i], b_SODA3[i] = np.linalg.lstsq(A_SODA3,psi_glo_vert_SODA3_white_series[:,i])[0]

fig8 = plt.figure()
fig8.set_size_inches(8, 6)
plt.axhline(y=0, color='k',ls='-')
plt.plot(latitude_ORAS4,a_ORAS4*12,'b-',label='ORAS4')
plt.plot(latitude_GLORYS2V3,a_GLORYS2V3*12,'r-',label='GLORYS2V3')
plt.plot(latitude_SODA3,a_SODA3*12,'g-',label='SODA3')
plt.title('Trend of global mass transport anomalies from 20N to 90N (1993-2012)')
plt.legend(frameon=True, loc=3, prop={'size': 14})
plt.xlabel("Latitudes",fontsize = 16)
plt.xticks(fontsize = 16)
plt.ylabel("Meridional Energy Transport (Sv/year)",fontsize = 16)
plt.yticks(fontsize=16)
plt.show()
fig8.savefig(output_path + os.sep + 'Comp_psi_glo_white_trend.jpg', dpi = 400)


# Trend of psi in the atlantic
for i in np.arange(len(latitude_ORAS4)):
        a_ORAS4[i], b_ORAS4[i] = np.linalg.lstsq(A_ORAS4,psi_atl_vert_ORAS4_white_series[:,i])[0]
for i in np.arange(len(latitude_GLORYS2V3)):
        a_GLORYS2V3[i], b_GLORYS2V3[i] = np.linalg.lstsq(A_GLORYS2V3,psi_atl_vert_GLORYS2V3_white_series[:,i])[0]
for i in np.arange(len(latitude_SODA3)):
        a_SODA3[i], b_SODA3[i] = np.linalg.lstsq(A_SODA3,psi_atl_vert_SODA3_white_series[:,i])[0]

fig9 = plt.figure()
fig9.set_size_inches(8, 6)
plt.axhline(y=0, color='k',ls='-')
plt.plot(latitude_ORAS4,a_ORAS4*12,'b-',label='ORAS4')
plt.plot(latitude_GLORYS2V3,a_GLORYS2V3*12,'r-',label='GLORYS2V3')
plt.plot(latitude_SODA3,a_SODA3*12,'g-',label='SODA3')
plt.title('Trend of Atlantic mass transport anomalies from 20N to 90N (1993-2012)')
plt.legend(frameon=True, loc=3, prop={'size': 14})
plt.xlabel("Latitudes",fontsize = 16)
plt.xticks(fontsize = 16)
plt.ylabel("Meridional Energy Transport (Sv/year)",fontsize = 16)
plt.yticks(fontsize=16)
plt.show()
fig9.savefig(output_path + os.sep + 'Comp_psi_atl_white_trend.jpg', dpi = 400)

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
