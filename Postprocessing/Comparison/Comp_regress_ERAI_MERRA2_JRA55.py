#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : Investigate the correlation between AMET (MERRA2,ERA-Interim,JRA55) and all kinds of fields
Author          : Yang Liu
Date            : 2018.03.16
Last Update     : 2018.03.26
Description     : The code aims to dig into the correlation between atmospheric meridional
                  energy transport and all kinds of climatological fields, as well as some
                  climate index.

                  The AMET are computed from the datasets includes MERRA II from NASA,
                  ERA-Interim from ECMWF and JRA55 from JMA.

                  The index of interest include NAO, AO, AMO, PDO, ENSO.

                  The variable fields of insterest include Sea Level Pressure (SLP), Sea
                  Surface Tmperature (SST), Surface Skin Temperature (TS) and Sea
                  Ice Concentration (SIC).

Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, sys, matplotlib
variables       : Meridional Total Energy Transport           E         [Tera-Watt]

Caveat!!        : Spatial and temporal coverage
                  Temporal
                  ERA-Interim 1979 - 2016
                  MERRA2      1980 - 2016
                  JRA55       1979 - 2015
                  Spatial
                  ERA-Interim 20N - 90N
                  MERRA2      20N - 90N
                  JRA55       90S - 90N
"""

import seaborn as sns
import numpy as np
import scipy as sp
from scipy import stats
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
import matplotlib.ticker as mticker
import matplotlib.path as mpath
from mpl_toolkits.basemap import Basemap, cm
import matplotlib.cm as mpl_cm
import cartopy
import cartopy.crs as ccrs
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import iris
import iris.plot as iplt
import iris.quickplot as qplt
import pandas

# switch on the seaborn effect
sns.set()

# calculate the time for the code execution
start_time = tttt.time()

################################   Input zone  ######################################
# specify data path
datapath_ERAI = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ERAI/postprocessing'
datapath_MERRA2 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/MERRA2/postprocessing'
datapath_JRA55 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/JRA55/postprocessing'
# target fields for regression
datapath_ERAI_fields = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ERAI/regression'
datapath_MERRA2_fields = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/MERRA2/regression'
datapath_JRA55_fields = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/JRA55/regression'
# index
datapath_index = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/Climate_index'
# specify output path for the netCDF4 file
output_path = '/home/yang/NLeSC/Computation_Modeling/BlueAction/AMET/Comparison/regress'
####################################################################################
print '****************************************************************************'
print '********************    latitude index of insteret     *********************'
print '****************************************************************************'
# There is a cut to JRA, too
# index of latitude for insteret
# 20N
lat_ERAI_20 = 93
lat_MERRA2_20 = 0
lat_JRA55_20 = 124
# 30N
lat_ERAI_30 = 80
lat_MERRA2_30 = 20
lat_JRA55_30 = 106
# 40N
lat_ERAI_40 = 67
lat_MERRA2_40 = 40
lat_JRA55_40 = 88
# 50N
lat_ERAI_50 = 53
lat_MERRA2_50 = 60
lat_JRA55_50 = 70
# 60N
lat_ERAI_60 = 40
lat_MERRA2_60 = 80
lat_JRA55_60 = 53
# 70N
lat_ERAI_70 = 27
lat_MERRA2_70 = 100
lat_JRA55_70 = 35
# 80N
lat_ERAI_80 = 13
lat_MERRA2_80 = 120
lat_JRA55_80 = 17
# make a dictionary for instereted sections (for process automation)
lat_interest = {}
lat_interest_list = [20,30,40,50,60,70,80]
lat_interest['ERAI'] = [lat_ERAI_20,lat_ERAI_30,lat_ERAI_40,lat_ERAI_50,lat_ERAI_60,lat_ERAI_70,lat_ERAI_80]
lat_interest['MERRA2'] = [lat_MERRA2_20,lat_MERRA2_30,lat_MERRA2_40,lat_MERRA2_50,lat_MERRA2_60,lat_MERRA2_70,lat_MERRA2_80]
lat_interest['JRA55'] = [lat_JRA55_20,lat_JRA55_30,lat_JRA55_40,lat_JRA55_50,lat_JRA55_60,lat_JRA55_70,lat_JRA55_80]
####################################################################################
print '*******************************************************************'
print '*********************** extract variables *************************'
print '*******************************************************************'
dataset_ERAI = Dataset(datapath_ERAI + os.sep + 'model_daily_075_1979_2016_E_zonal_int.nc')
dataset_MERRA2 = Dataset(datapath_MERRA2 + os.sep + 'AMET_MERRA2_model_daily_1980_2016_E_zonal_int.nc')
dataset_JRA55 = Dataset(datapath_JRA55 + os.sep + 'AMET_JRA55_model_daily_1979_2015_E_zonal_int.nc')

dataset_ERAI_fields = Dataset(datapath_ERAI_fields + os.sep + 'surface_ERAI_monthly_regress_1979_2016.nc')
dataset_MERRA2_fields = Dataset(datapath_MERRA2_fields + os.sep + 'surface_MERRA2_monthly_regress_1980_2016.nc')

dataset_ERAI_fields_extra = Dataset(datapath_ERAI_fields + os.sep + 'surface_ERAI_monthly_regress_1979_2016_extra.nc')

dataset_index = Dataset(datapath_index + os.sep + 'index_climate_monthly_regress_1950_2017.nc')

AMET_ERAI = dataset_ERAI.variables['E'][:]/1000 # from Tera Watt to Peta Watt
AMET_MERRA2 = dataset_MERRA2.variables['E'][:]/1000 # from Tera Watt to Peta Watt
AMET_JRA55 = dataset_JRA55.variables['E'][:,:,0:125]/1000 # from Tera Watt to Peta Watt

year_ERAI = dataset_ERAI.variables['year'][:]             # from 1979 to 2016
year_MERRA2 = dataset_MERRA2.variables['year'][:]         # from 1980 to 2016
year_JRA55 = dataset_JRA55.variables['year'][:]           # from 1979 to 2015

latitude_ERAI = dataset_ERAI.variables['latitude'][:]
latitude_MERRA2 = dataset_MERRA2.variables['latitude'][:]
latitude_JRA55 = dataset_JRA55.variables['latitude'][0:125]

SLP_ERAI_series = dataset_ERAI_fields.variables['msl'][:]   # dimension (time, lat, lon)
SLP_MERRA2 = dataset_MERRA2_fields.variables['SLP'][:]      # dimension (year, month, lat, lon)

SST_ERAI_series = dataset_ERAI_fields.variables['sst'][:]
SST_ERAI_mask = np.ma.getmaskarray(SST_ERAI_series[0,:,:])
#SST_MERRA2_ice = dataset_MERRA2_fields.variables['SST_ice'][:]
SST_MERRA2 = dataset_MERRA2_fields.variables['SST_water'][:] # water surface temperature
#SST_MERRA2_water[SST_MERRA2_water>1000] = 0
SST_MERRA2 = np.ma.masked_where(SST_MERRA2>1000,SST_MERRA2)
SST_MERRA2_mask = np.ma.getmaskarray(SST_MERRA2[0,0,:,:])

SIC_ERAI_series = dataset_ERAI_fields.variables['ci'][:]
SIC_ERAI_mask = np.ma.getmaskarray(SIC_ERAI_series[0,:,:])
SIC_MERRA2 = dataset_MERRA2_fields.variables['SIC'][:]
#SIC_MERRA2_mask = np.ma.getmaskarray(SIC_MERRA2[0,0,:,:]) # no mask from array

TS_ERAI = dataset_ERAI_fields_extra.variables['ts'][:]
TS_MERRA2 = dataset_MERRA2_fields.variables['ts'][:]

T2M_ERAI = dataset_ERAI_fields_extra.variables['t2m'][:]
T2M_MERRA2 = dataset_MERRA2_fields.variables['t2m'][:]

latitude_ERAI_fields = dataset_ERAI_fields.variables['latitude'][:]
latitude_MERRA2_fields = dataset_MERRA2_fields.variables['latitude'][:]

longitude_ERAI_fields = dataset_ERAI_fields.variables['longitude'][:]
longitude_MERRA2_fields = dataset_MERRA2_fields.variables['longitude'][:]

year_ERAI_fields = year_ERAI
year_MERRA2_fields = dataset_MERRA2_fields.variables['year'][:]

# index (originally from 1950 to 2017)
# here we just take 1979 to 2016
NAO = dataset_index.variables['NAO'][348:-12]
MEI = dataset_index.variables['MEI'][348:-12]
AO = dataset_index.variables['AO'][348:-12]
AMO = dataset_index.variables['AMO'][348:-12]
PDO = dataset_index.variables['PDO'][348:-12]

print '*******************************************************************'
print '*************************** whitening *****************************'
print '*******************************************************************'
month_ind = np.arange(12)
# climatology of AMET
seansonal_cycle_AMET_ERAI = np.mean(AMET_ERAI,axis=0)
seansonal_cycle_AMET_MERRA2 = np.mean(AMET_MERRA2,axis=0)
seansonal_cycle_AMET_JRA55 = np.mean(AMET_JRA55,axis=0)

AMET_ERAI_white = np.zeros(AMET_ERAI.shape,dtype=float)
AMET_MERRA2_white = np.zeros(AMET_MERRA2.shape,dtype=float)
AMET_JRA55_white = np.zeros(AMET_JRA55.shape,dtype=float)

for i in np.arange(len(year_ERAI)):
    for j in month_ind:
        AMET_ERAI_white[i,j,:] = AMET_ERAI[i,j,:] - seansonal_cycle_AMET_ERAI[j,:]

for i in np.arange(len(year_MERRA2)):
    for j in month_ind:
        AMET_MERRA2_white[i,j,:] = AMET_MERRA2[i,j,:] - seansonal_cycle_AMET_MERRA2[j,:]

for i in np.arange(len(year_JRA55)):
    for j in month_ind:
        AMET_JRA55_white[i,j,:] = AMET_JRA55[i,j,:] - seansonal_cycle_AMET_JRA55[j,:]

# climatology for individual fields
# climatology for Sea Level Pressure
seasonal_cycle_SLP_ERAI = np.zeros((12,len(latitude_ERAI_fields),len(longitude_ERAI_fields))) # from 20N - 90N
SLP_ERAI_white_series = np.zeros(SLP_ERAI_series.shape,dtype=float)
# anomalies
for i in month_ind:
    # calculate the monthly mean (seasonal cycling)
    seasonal_cycle_SLP_ERAI[i,:,:] = np.mean(SLP_ERAI_series[i::12,:,:],axis=0)
    # remove seasonal mean
    SLP_ERAI_white_series[i::12,:,:] = SLP_ERAI_series[i::12,:,:] - seasonal_cycle_SLP_ERAI[i,:,:]

# climatology for Sea Ice Concentration
seasonal_cycle_SIC_ERAI = np.zeros((12,len(latitude_ERAI_fields[:41]),len(longitude_ERAI_fields))) # from 60N - 90N
SIC_ERAI_white_series = np.zeros(SIC_ERAI_series.shape,dtype=float)
# anomalies
for i in month_ind:
    # calculate the monthly mean (seasonal cycling)
    seasonal_cycle_SIC_ERAI[i,:,:] = np.mean(SIC_ERAI_series[i::12,:,:],axis=0)
    # remove seasonal mean
    SIC_ERAI_white_series[i::12,:,:] = SIC_ERAI_series[i::12,:,:] - seasonal_cycle_SIC_ERAI[i,:,:]

seasonal_cycle_SLP_MERRA2 = np.mean(SLP_MERRA2,axis=0)
SLP_MERRA2_white = np.zeros(SLP_MERRA2.shape,dtype=float)
for i in np.arange(len(year_MERRA2_fields)):
    for j in month_ind:
        SLP_MERRA2_white[i,j,:,:] = SLP_MERRA2[i,j,:,:] - seasonal_cycle_SLP_MERRA2[j,:,:]

# climatology for Sea Surface Temperature
seasonal_cycle_SST_ERAI = np.zeros((12,len(latitude_ERAI_fields),len(longitude_ERAI_fields))) # from 20N - 90N
SST_ERAI_white_series = np.zeros(SST_ERAI_series.shape,dtype=float)
# anomalies
for i in month_ind:
    # calculate the monthly mean (seasonal cycling)
    seasonal_cycle_SST_ERAI[i,:,:] = np.mean(SST_ERAI_series[i::12,:,:],axis=0)
    # remove seasonal mean
    SST_ERAI_white_series[i::12,:,:] = SST_ERAI_series[i::12,:,:] - seasonal_cycle_SST_ERAI[i,:,:]

seasonal_cycle_SST_MERRA2 = np.mean(SST_MERRA2,axis=0)
SST_MERRA2_white = np.zeros(SST_MERRA2.shape,dtype=float)
for i in np.arange(len(year_MERRA2_fields)):
    for j in month_ind:
        SST_MERRA2_white[i,j,:,:] = SST_MERRA2[i,j,:,:] - seasonal_cycle_SST_MERRA2[j,:,:]

seasonal_cycle_TS_ERAI = np.mean(TS_ERAI,axis=0)
TS_ERAI_white = np.zeros(TS_ERAI.shape,dtype=float)
for i in np.arange(len(year_ERAI_fields)):
    for j in month_ind:
        TS_ERAI_white[i,j,:,:] = TS_ERAI[i,j,:,:] - seasonal_cycle_TS_ERAI[j,:,:]

seasonal_cycle_TS_MERRA2 = np.mean(TS_MERRA2,axis=0)
TS_MERRA2_white = np.zeros(TS_MERRA2.shape,dtype=float)
for i in np.arange(len(year_MERRA2_fields)):
    for j in month_ind:
        TS_MERRA2_white[i,j,:,:] = TS_MERRA2[i,j,:,:] - seasonal_cycle_TS_MERRA2[j,:,:]

seasonal_cycle_T2M_ERAI = np.mean(T2M_ERAI,axis=0)
T2M_ERAI_white = np.zeros(T2M_ERAI.shape,dtype=float)
for i in np.arange(len(year_ERAI_fields)):
    for j in month_ind:
        T2M_ERAI_white[i,j,:,:] = T2M_ERAI[i,j,:,:] - seasonal_cycle_T2M_ERAI[j,:,:]

seasonal_cycle_T2M_MERRA2 = np.mean(T2M_MERRA2,axis=0)
T2M_MERRA2_white = np.zeros(T2M_MERRA2.shape,dtype=float)
for i in np.arange(len(year_MERRA2_fields)):
    for j in month_ind:
        T2M_MERRA2_white[i,j,:,:] = T2M_MERRA2[i,j,:,:] - seasonal_cycle_T2M_MERRA2[j,:,:]

seasonal_cycle_SIC_MERRA2 = np.mean(SIC_MERRA2,axis=0)
SIC_MERRA2_white = np.zeros(SIC_MERRA2.shape,dtype=float)
for i in np.arange(len(year_MERRA2_fields)):
    for j in month_ind:
        SIC_MERRA2_white[i,j,:,:] = SIC_MERRA2[i,j,:,:] - seasonal_cycle_SIC_MERRA2[j,:,:]
print '*******************************************************************'
print '****************** prepare variables for plot *********************'
print '*******************************************************************'
# dataset with seasonal cycle - time series
AMET_ERAI_series = AMET_ERAI.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI))
AMET_MERRA2_series = AMET_MERRA2.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2))
AMET_JRA55_series = AMET_JRA55.reshape(len(year_JRA55)*len(month_ind),len(latitude_JRA55))
# dataset without seasonal cycle - time series
AMET_ERAI_white_series = AMET_ERAI_white.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI))
AMET_MERRA2_white_series = AMET_MERRA2_white.reshape(len(year_MERRA2)*len(month_ind),len(latitude_MERRA2))
AMET_JRA55_white_series = AMET_JRA55_white.reshape(len(year_JRA55)*len(month_ind),len(latitude_JRA55))
# fields with seasonal cycle - time series
TS_ERAI_series = TS_ERAI.reshape(len(year_ERAI_fields)*len(month_ind),len(latitude_ERAI_fields),len(longitude_ERAI_fields))
T2M_ERAI_series = T2M_ERAI.reshape(len(year_ERAI_fields)*len(month_ind),len(latitude_ERAI_fields),len(longitude_ERAI_fields))

SLP_MERRA2_series = SLP_MERRA2.reshape(len(year_MERRA2_fields)*len(month_ind),len(latitude_MERRA2_fields),len(longitude_MERRA2_fields))
SST_MERRA2_series = SST_MERRA2.reshape(len(year_MERRA2_fields)*len(month_ind),len(latitude_MERRA2_fields),len(longitude_MERRA2_fields))
TS_MERRA2_series = TS_MERRA2.reshape(len(year_MERRA2_fields)*len(month_ind),len(latitude_MERRA2_fields),len(longitude_MERRA2_fields))
T2M_MERRA2_series = T2M_MERRA2.reshape(len(year_MERRA2_fields)*len(month_ind),len(latitude_MERRA2_fields),len(longitude_MERRA2_fields))
SIC_MERRA2_series = SIC_MERRA2.reshape(len(year_MERRA2_fields)*len(month_ind),len(latitude_MERRA2_fields),len(longitude_MERRA2_fields))
# fields without seasonal cycle - time series
TS_ERAI_white_series = TS_ERAI_white.reshape(len(year_ERAI_fields)*len(month_ind),len(latitude_ERAI_fields),len(longitude_ERAI_fields))
T2M_ERAI_white_series = T2M_ERAI_white.reshape(len(year_ERAI_fields)*len(month_ind),len(latitude_ERAI_fields),len(longitude_ERAI_fields))

SLP_MERRA2_white_series = SLP_MERRA2_white.reshape(len(year_MERRA2_fields)*len(month_ind),len(latitude_MERRA2_fields),len(longitude_MERRA2_fields))
SST_MERRA2_white_series = SST_MERRA2_white.reshape(len(year_MERRA2_fields)*len(month_ind),len(latitude_MERRA2_fields),len(longitude_MERRA2_fields))
TS_MERRA2_white_series = TS_MERRA2_white.reshape(len(year_MERRA2_fields)*len(month_ind),len(latitude_MERRA2_fields),len(longitude_MERRA2_fields))
T2M_MERRA2_white_series = T2M_MERRA2_white.reshape(len(year_MERRA2_fields)*len(month_ind),len(latitude_MERRA2_fields),len(longitude_MERRA2_fields))
SIC_MERRA2_white_series = SIC_MERRA2_white.reshape(len(year_MERRA2_fields)*len(month_ind),len(latitude_MERRA2_fields),len(longitude_MERRA2_fields))
print '*******************************************************************'
print '********************** Running mean/sum ***************************'
print '*******************************************************************'
# running mean is calculated on time series
# define the running window for the running mean
#window = 12 # in month
window = 60 # in month
#window = 120 # in month
#window = 180 # in month

# white time series
AMET_ERAI_white_series_running_mean = np.zeros((len(year_ERAI)*len(month_ind)-window+1,len(latitude_ERAI)),dtype=float)
AMET_MERRA2_white_series_running_mean = np.zeros((len(year_MERRA2)*len(month_ind)-window+1,len(latitude_MERRA2)),dtype=float)
AMET_JRA55_white_series_running_mean = np.zeros((len(year_JRA55)*len(month_ind)-window+1,len(latitude_JRA55)),dtype=float)

SLP_ERAI_white_series_running_mean = np.zeros((len(year_ERAI_fields)*len(month_ind)-window+1,len(latitude_ERAI_fields),len(longitude_ERAI_fields)),dtype=float)
SLP_MERRA2_white_series_running_mean = np.zeros((len(year_MERRA2_fields)*len(month_ind)-window+1,len(latitude_MERRA2_fields),len(longitude_MERRA2_fields)),dtype=float)

SST_ERAI_white_series_running_mean = np.zeros((len(year_ERAI_fields)*len(month_ind)-window+1,len(latitude_ERAI_fields),len(longitude_ERAI_fields)),dtype=float)
SST_MERRA2_white_series_running_mean = np.zeros((len(year_MERRA2_fields)*len(month_ind)-window+1,len(latitude_MERRA2_fields),len(longitude_MERRA2_fields)),dtype=float)

TS_ERAI_white_series_running_mean = np.zeros((len(year_ERAI_fields)*len(month_ind)-window+1,len(latitude_ERAI_fields),len(longitude_ERAI_fields)),dtype=float)
TS_MERRA2_white_series_running_mean = np.zeros((len(year_MERRA2_fields)*len(month_ind)-window+1,len(latitude_MERRA2_fields),len(longitude_MERRA2_fields)),dtype=float)

for i in np.arange(len(year_ERAI)*len(month_ind)-window+1):
    AMET_ERAI_white_series_running_mean[i,:] = np.mean(AMET_ERAI_white_series[i:i+window,:],0)

for i in np.arange(len(year_MERRA2)*len(month_ind)-window+1):
    AMET_MERRA2_white_series_running_mean[i,:] = np.mean(AMET_MERRA2_white_series[i:i+window,:],0)

for i in np.arange(len(year_JRA55)*len(month_ind)-window+1):
    AMET_JRA55_white_series_running_mean[i,:] = np.mean(AMET_JRA55_white_series[i:i+window,:],0)

for i in np.arange(len(year_ERAI_fields)*len(month_ind)-window+1):
    SLP_ERAI_white_series_running_mean[i,:,:] = np.mean(SLP_ERAI_white_series[i:i+window,:,:],0)

for i in np.arange(len(year_MERRA2_fields)*len(month_ind)-window+1):
    SLP_MERRA2_white_series_running_mean[i,:,:] = np.mean(SLP_MERRA2_white_series[i:i+window,:,:],0)

for i in np.arange(len(year_ERAI_fields)*len(month_ind)-window+1):
    SST_ERAI_white_series_running_mean[i,:,:] = np.mean(SST_ERAI_white_series[i:i+window,:,:],0)

for i in np.arange(len(year_MERRA2_fields)*len(month_ind)-window+1):
    SST_MERRA2_white_series_running_mean[i,:,:] = np.mean(SST_MERRA2_white_series[i:i+window,:,:],0)

for i in np.arange(len(year_ERAI_fields)*len(month_ind)-window+1):
    TS_ERAI_white_series_running_mean[i,:,:] = np.mean(TS_ERAI_white_series[i:i+window,:,:],0)

for i in np.arange(len(year_MERRA2_fields)*len(month_ind)-window+1):
    TS_MERRA2_white_series_running_mean[i,:,:] = np.mean(TS_MERRA2_white_series[i:i+window,:,:],0)
print '*******************************************************************'
print '**********************     regression     *************************'
print '******************    original and anomalies   ********************'
print '*******************************************************************'

def figure_PlateCarree(cube_fig,title_fig,vmin,vmax,label,ticks,p,longitude_fields,latitude_fields,path):
    # figsize works for the size of the map, not the entire figure
    fig1 = plt.figure()
    fig1.suptitle(title_fig,fontsize = 7,y=0.93)
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_global()
    #ax.set_aspect('auto')
    ax.set_aspect('1.0')
    ax.coastlines()
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,linewidth=1, color='gray', alpha=0.5,linestyle='--')
    gl.xlabels_top = False
    # use of formatter (fixed), only after this the style setup will work
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    # specify label styles
    gl.xlabel_style = {'size': 6, 'color': 'gray'}
    gl.ylabel_style = {'size': 6, 'color': 'gray'}
    # Load a Cynthia Brewer palette.
    #brewer_cmap = mpl_cm.get_cmap('brewer_RdYlBu_11')
    cs = iplt.pcolormesh(cube_fig,cmap='coolwarm',vmin=vmin,vmax=vmax)
    cbar = fig1.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.1,format="%.2f")
    cbar.set_ticks(ticks)
    cbar.set_clim(vmin, vmax)
    cbar.ax.tick_params(labelsize = 6)
    cbar.set_label(label,size = 6)
    # locate the indices of p_value matrix where error p<0.05 (99.5% confident)
    ii, jj = np.where(p<=0.05)
    # get the coordinate on the map (lon,lat) and plot scatter dots
    ax.scatter(longitude_fields[jj],latitude_fields[ii],transform=ccrs.Geodetic(),s=0.1,c='g',alpha=0.3) # alpha bleding factor with map
    # show and save plot
    plt.show()
    fig1.savefig(path,dpi=300)
    plt.close(fig1)

def figure_NorthPolarStereo(cube_fig,title_fig,vmin,vmax,label,ticks,p,longitude_fields,latitude_fields,path):
    # figsize works for the size of the map, not the entire figure
    fig2 = plt.figure()
    fig2.suptitle(title_fig,fontsize = 7,y=0.93)
    ax = plt.axes(projection=ccrs.NorthPolarStereo())
    ax.set_extent([-180,180,60,90],ccrs.PlateCarree()) # East, West, South, Nouth
    ax.set_aspect('1')
    ax.coastlines()
    gl = ax.gridlines(linewidth=1, color='gray', alpha=0.5,linestyle='--')
    theta = np.linspace(0, 2*np.pi, 100)
    center, radius = [0.5, 0.5], 0.5
    verts = np.vstack([np.sin(theta), np.cos(theta)]).T
    circle = mpath.Path(verts * radius + center)
    ax.set_boundary(circle, transform=ax.transAxes)
    cs = iplt.pcolormesh(cube_fig,cmap='coolwarm',vmin=vmin,vmax=vmax)
    cbar = fig2.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.1,format="%.2f")
    cbar.set_ticks(ticks)
    cbar.set_clim(vmin, vmax)
    cbar.ax.tick_params(labelsize = 6)
    cbar.set_label(label,size = 6)
    # locate the indices of p_value matrix where error p<0.05 (99.5% confident)
    ii, jj = np.where(p<=0.05)
    # get the coordinate on the map (lon,lat) and plot scatter dots
    ax.scatter(longitude_fields[jj],latitude_fields[ii],transform=ccrs.Geodetic(),s=0.1,c='g',alpha=0.3) # alpha bleding factor with map
    plt.show()
    fig2.savefig(path,dpi=300)
    plt.close(fig2)

# all the invariants of figures
vmin_SLP_white = -0.30
vmax_SLP_white = 0.30
ticks_SLP_white = [-0.30, -0.25, -0.20, -0.15, -0.10, -0.05, 0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
label_SLP_white = 'Correlation coefficient'

vmin_SLP = -0.60
vmax_SLP = 0.60
ticks_SLP = [-0.60, -0.50, -0.40, -0.30, -0.20, -0.10, 0, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60]
label_SLP = 'Correlation coefficient'

vmin_SST_white = -0.30
vmax_SST_white = 0.30
ticks_SST_white = [-0.30, -0.25, -0.20, -0.15, -0.10, -0.05, 0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
label_SST_white = 'Correlation coefficient'

vmin_SLP_white_lowpass = -0.60
vmax_SLP_white_lowpass = 0.60
ticks_SLP_white_lowpass = [-0.60, -0.50, -0.40, -0.30, -0.20, -0.10, 0, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60]
label_SLP_white_lowpass = 'Correlation coefficient'

vmin_SST_white_lowpass = -0.60
vmax_SST_white_lowpass = 0.60
ticks_SST_white_lowpass = [-0.60, -0.50, -0.40, -0.30, -0.20, -0.10, 0, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60]
label_SST_white_lowpass = 'Correlation coefficient'

vmin_TS_white = -0.30
vmax_TS_white = 0.30
ticks_TS_white = [-0.30, -0.25, -0.20, -0.15, -0.10, -0.05, 0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
label_TS_white = 'Correlation coefficient'

vmin_T2M_white = -0.30
vmax_T2M_white = 0.30
ticks_T2M_white = [-0.30, -0.25, -0.20, -0.15, -0.10, -0.05, 0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
label_T2M_white = 'Correlation coefficient'

vmin_SIC_white = -0.12
vmax_SIC_white = 0.12
ticks_SIC_white = [-0.12, -0.10, -0.08, -0.06, -0.04, -0.02, 0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12]
label_SIC_white = 'Regression coefficient percentage/PW'
#***************************************************************************#
#*****************   regress of ERA Interim SLP fields   *******************#
#*************   on AMET from ERA-Interim MERRA2 and JRA55   ***************#
#***************************************************************************#

# create an array to store the correlation coefficient
slope_ERAI_fields = np.zeros((len(latitude_ERAI_fields),len(longitude_ERAI_fields)),dtype = float)
r_value_ERAI_fields = np.zeros((len(latitude_ERAI_fields),len(longitude_ERAI_fields)),dtype = float)
p_value_ERAI_fields= np.zeros((len(latitude_ERAI_fields),len(longitude_ERAI_fields)),dtype = float)

latitude_ERAI_iris = iris.coords.DimCoord(latitude_ERAI_fields,standard_name='latitude',long_name='latitude',
                             var_name='lat',units='degrees')
longitude_ERAI_iris = iris.coords.DimCoord(longitude_ERAI_fields,standard_name='longitude',long_name='longitude',
                             var_name='lon',units='degrees')
# choose the coordinate system for Cube (for regrid module)
coord_sys = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)

#*****************             SLP anomalies             *******************#

for c in np.arange(len(lat_interest_list)):
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      ERA-Interim      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
    # linear regress SLP on AMET (anomalies)
    # plot correlation coefficient
    for i in np.arange(len(latitude_ERAI_fields)):
        for j in np.arange(len(longitude_ERAI_fields)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope_ERAI_fields[i,j],_,r_value_ERAI_fields[i,j],p_value_ERAI_fields[i,j],_ = stats.linregress(AMET_ERAI_white_series[:,lat_interest['ERAI'][c]],SLP_ERAI_white_series[:,i,j])
    cube_ERAI = iris.cube.Cube(r_value_ERAI_fields,long_name='Correlation coefficient between SLP and AMET',
                               var_name='r',units='1',dim_coords_and_dims=[(latitude_ERAI_iris, 0), (longitude_ERAI_iris, 1)])
    cube_ERAI.coord('latitude').coord_system = coord_sys
    cube_ERAI.coord('longitude').coord_system = coord_sys
    title = 'Regression of SLP Anomaly from ERA-Interim on AMET Anomaly of ERA-Interim across %d N' % (lat_interest_list[c])
    path = os.path.join(output_path,'SLP','AMET_ERAI_fields_ERAI',
                        "Regression_AMET_ERAI_%dN_SLP_ERAI_white_correlation_coef.jpeg" % (lat_interest_list[c]))
    figure_PlateCarree(cube_ERAI,title,vmin_SLP_white,vmax_SLP_white,label_SLP_white,ticks_SLP_white,
                   p_value_ERAI_fields,longitude_ERAI_fields,latitude_ERAI_fields,path)

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      MERRA2      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
    for i in np.arange(len(latitude_ERAI_fields)):
        for j in np.arange(len(longitude_ERAI_fields)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope_ERAI_fields[i,j],_,r_value_ERAI_fields[i,j],p_value_ERAI_fields[i,j],_ = stats.linregress(AMET_MERRA2_white_series[:,lat_interest['MERRA2'][c]],SLP_ERAI_white_series[12:,i,j])
    cube_ERAI = iris.cube.Cube(r_value_ERAI_fields,long_name='Correlation coefficient between SLP and AMET',
                               var_name='r',units='1',dim_coords_and_dims=[(latitude_ERAI_iris, 0), (longitude_ERAI_iris, 1)])
    cube_ERAI.coord('latitude').coord_system = coord_sys
    cube_ERAI.coord('longitude').coord_system = coord_sys
    # suptitle is the title for the figure
    title = 'Regression of SLP Anomaly from ERA-Interim on AMET Anomaly of MERRA2 across %d N' % (lat_interest_list[c])
    path = os.path.join(output_path,'SLP','AMET_MERRA2_fields_ERAI',
                        "Regression_AMET_MERRA2_%dN_SLP_ERAI_white_correlation_coef.jpeg" % (lat_interest_list[c]))
    figure_PlateCarree(cube_ERAI,title,vmin_SLP_white,vmax_SLP_white,label_SLP_white,ticks_SLP_white,
                   p_value_ERAI_fields,longitude_ERAI_fields,latitude_ERAI_fields,path)

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@       JRA55      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
    for i in np.arange(len(latitude_ERAI_fields)):
        for j in np.arange(len(longitude_ERAI_fields)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope_ERAI_fields[i,j],_,r_value_ERAI_fields[i,j],p_value_ERAI_fields[i,j],_ = stats.linregress(AMET_JRA55_white_series[:,lat_interest['JRA55'][c]],SLP_ERAI_white_series[:-12,i,j])
    cube_ERAI = iris.cube.Cube(r_value_ERAI_fields,long_name='Correlation coefficient between SLP and AMET',
                               var_name='r',units='1',dim_coords_and_dims=[(latitude_ERAI_iris, 0), (longitude_ERAI_iris, 1)])
    cube_ERAI.coord('latitude').coord_system = coord_sys
    cube_ERAI.coord('longitude').coord_system = coord_sys

    title = 'Regression of SLP Anomaly from ERA-Interim on AMET Anomaly of JRA55 across %d N' % (lat_interest_list[c])
    path = os.path.join(output_path,'SLP','AMET_JRA55_fields_ERAI',
                        "Regression_AMET_JRA55_%dN_SLP_ERAI_white_correlation_coef.jpeg" % (lat_interest_list[c]))
    figure_PlateCarree(cube_ERAI,title,vmin_SLP_white,vmax_SLP_white,label_SLP_white,ticks_SLP_white,
                   p_value_ERAI_fields,longitude_ERAI_fields,latitude_ERAI_fields,path)

#******************             SLP original             *******************#

for c in np.arange(len(lat_interest_list)):
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      ERA-Interim      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
    # linear regress SLP on AMET
    # plot correlation coefficient
    for i in np.arange(len(latitude_ERAI_fields)):
        for j in np.arange(len(longitude_ERAI_fields)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope_ERAI_fields[i,j],_,r_value_ERAI_fields[i,j],p_value_ERAI_fields[i,j],_ = stats.linregress(AMET_ERAI_series[:,lat_interest['ERAI'][c]],SLP_ERAI_series[:,i,j])
    # figsize works for the size of the map, not the entire figure
    fig4 = plt.figure()
    cube_ERAI = iris.cube.Cube(r_value_ERAI_fields,long_name='Correlation coefficient between SLP and AMET',
                               var_name='r',units='1',dim_coords_and_dims=[(latitude_ERAI_iris, 0), (longitude_ERAI_iris, 1)])
    cube_ERAI.coord('latitude').coord_system = coord_sys
    cube_ERAI.coord('longitude').coord_system = coord_sys
    title = 'Regression of SLP from ERA-Interim on AMET of ERA-Interim across %d N' % (lat_interest_list[c])
    path = os.path.join(output_path,'SLP','AMET_ERAI_fields_ERAI',
                        "Regression_AMET_ERAI_%dN_SLP_ERAI_correlation_coef.jpeg" % (lat_interest_list[c]))
    figure_PlateCarree(cube_ERAI,title,vmin_SLP,vmax_SLP,label_SLP,ticks_SLP,
                   p_value_ERAI_fields,longitude_ERAI_fields,latitude_ERAI_fields,path)

#***************************************************************************#
#*****************      regress of MERRA2 SLP fields     *******************#
#*************   on AMET from ERA-Interim MERRA2 and JRA55   ***************#
#***************************************************************************#
# create an array to store the correlation coefficient
slope_MERRA2_fields = np.zeros((len(latitude_MERRA2_fields),len(longitude_MERRA2_fields)),dtype = float)
r_value_MERRA2_fields = np.zeros((len(latitude_MERRA2_fields),len(longitude_MERRA2_fields)),dtype = float)
p_value_MERRA2_fields= np.zeros((len(latitude_MERRA2_fields),len(longitude_MERRA2_fields)),dtype = float)

latitude_MERRA2_iris = iris.coords.DimCoord(latitude_MERRA2_fields,standard_name='latitude',long_name='latitude',
                             var_name='lat',units='degrees')
longitude_MERRA2_iris = iris.coords.DimCoord(longitude_MERRA2_fields,standard_name='longitude',long_name='longitude',
                             var_name='lon',units='degrees')
# choose the coordinate system for Cube (for regrid module)
coord_sys = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)

#*****************             SLP anomalies             *******************#

for c in np.arange(len(lat_interest_list)):
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      ERA-Interim      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
    # linear regress SLP on AMET (anomalies)
    # plot correlation coefficient
    for i in np.arange(len(latitude_MERRA2_fields)):
        for j in np.arange(len(longitude_MERRA2_fields)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope_MERRA2_fields[i,j],_,r_value_MERRA2_fields[i,j],p_value_MERRA2_fields[i,j],_ = stats.linregress(AMET_ERAI_white_series[12:,lat_interest['ERAI'][c]],SLP_MERRA2_white_series[:,i,j])
    cube_MERRA2 = iris.cube.Cube(r_value_MERRA2_fields,long_name='Correlation coefficient between SLP and AMET',
                               var_name='r',units='1',dim_coords_and_dims=[(latitude_MERRA2_iris, 0), (longitude_MERRA2_iris, 1)])
    cube_MERRA2.coord('latitude').coord_system = coord_sys
    cube_MERRA2.coord('longitude').coord_system = coord_sys
    title = 'Regression of SLP Anomaly from MERRA2 on AMET Anomaly of ERA-Interim across %d N' % (lat_interest_list[c])
    path = os.path.join(output_path,'SLP','AMET_ERAI_fields_MERRA2',
                        "Regression_AMET_ERAI_%dN_SLP_MERRA2_white_correlation_coef.jpeg" % (lat_interest_list[c]))
    figure_PlateCarree(cube_MERRA2,title,vmin_SLP_white,vmax_SLP_white,label_SLP_white,ticks_SLP_white,
                   p_value_MERRA2_fields,longitude_MERRA2_fields,latitude_MERRA2_fields,path)

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      MERRA2      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
    for i in np.arange(len(latitude_MERRA2_fields)):
        for j in np.arange(len(longitude_MERRA2_fields)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope_MERRA2_fields[i,j],_,r_value_MERRA2_fields[i,j],p_value_MERRA2_fields[i,j],_ = stats.linregress(AMET_MERRA2_white_series[:,lat_interest['MERRA2'][c]],SLP_MERRA2_white_series[:,i,j])
    cube_MERRA2 = iris.cube.Cube(r_value_MERRA2_fields,long_name='Correlation coefficient between SLP and AMET',
                               var_name='r',units='1',dim_coords_and_dims=[(latitude_MERRA2_iris, 0), (longitude_MERRA2_iris, 1)])
    cube_MERRA2.coord('latitude').coord_system = coord_sys
    cube_MERRA2.coord('longitude').coord_system = coord_sys
    title = 'Regression of SLP Anomaly from MERRA2 on AMET Anomaly of MERRA2 across %d N' % (lat_interest_list[c])
    path = os.path.join(output_path,'SLP','AMET_MERRA2_fields_MERRA2',
                        "Regression_AMET_MERRA2_%dN_SLP_MERRA2_white_correlation_coef.jpeg" % (lat_interest_list[c]))
    figure_PlateCarree(cube_MERRA2,title,vmin_SLP_white,vmax_SLP_white,label_SLP_white,ticks_SLP_white,
                   p_value_MERRA2_fields,longitude_MERRA2_fields,latitude_MERRA2_fields,path)

#******************             SLP original             *******************#

for c in np.arange(len(lat_interest_list)):
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      MERRA2      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
    for i in np.arange(len(latitude_MERRA2_fields)):
        for j in np.arange(len(longitude_MERRA2_fields)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope_MERRA2_fields[i,j],_,r_value_MERRA2_fields[i,j],p_value_MERRA2_fields[i,j],_ = stats.linregress(AMET_MERRA2_series[:,lat_interest['MERRA2'][c]],SLP_MERRA2_series[:,i,j])
    cube_MERRA2 = iris.cube.Cube(r_value_MERRA2_fields,long_name='Correlation coefficient between SLP and AMET',
                               var_name='r',units='1',dim_coords_and_dims=[(latitude_MERRA2_iris, 0), (longitude_MERRA2_iris, 1)])
    cube_MERRA2.coord('latitude').coord_system = coord_sys
    cube_MERRA2.coord('longitude').coord_system = coord_sys
    # suptitle is the title for the figure
    title = 'Regression of SLP from MERRA2 on AMET of MERRA2 across %d N' % (lat_interest_list[c])
    path = os.path.join(output_path,'SLP','AMET_MERRA2_fields_MERRA2',
                        "Regression_AMET_MERRA2_%dN_SLP_MERRA2_correlation_coef.jpeg" % (lat_interest_list[c]))
    figure_PlateCarree(cube_MERRA2,title,vmin_SLP,vmax_SLP,label_SLP,ticks_SLP,
                   p_value_MERRA2_fields,longitude_MERRA2_fields,latitude_MERRA2_fields,path)

#***************************************************************************#
#*****************   regress of ERA Interim SST fields   *******************#
#*************   on AMET from ERA-Interim MERRA2 and JRA55   ***************#
#***************************************************************************#

# create an array to store the correlation coefficient
slope_ERAI_fields = np.zeros((len(latitude_ERAI_fields),len(longitude_ERAI_fields)),dtype = float)
r_value_ERAI_fields = np.zeros((len(latitude_ERAI_fields),len(longitude_ERAI_fields)),dtype = float)
p_value_ERAI_fields= np.zeros((len(latitude_ERAI_fields),len(longitude_ERAI_fields)),dtype = float)

latitude_ERAI_iris = iris.coords.DimCoord(latitude_ERAI_fields,standard_name='latitude',long_name='latitude',
                             var_name='lat',units='degrees')
longitude_ERAI_iris = iris.coords.DimCoord(longitude_ERAI_fields,standard_name='longitude',long_name='longitude',
                             var_name='lon',units='degrees')
# choose the coordinate system for Cube (for regrid module)
coord_sys = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)

#*****************             SST anomalies             *******************#

for c in np.arange(len(lat_interest_list)):
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      ERA-Interim      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
    # linear regress SST on AMET (anomalies)
    # plot correlation coefficient
    for i in np.arange(len(latitude_ERAI_fields)):
        for j in np.arange(len(longitude_ERAI_fields)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope_ERAI_fields[i,j],_,r_value_ERAI_fields[i,j],p_value_ERAI_fields[i,j],_ = stats.linregress(AMET_ERAI_white_series[:,lat_interest['ERAI'][c]],SST_ERAI_white_series[:,i,j])
    cube_ERAI = iris.cube.Cube(np.ma.masked_where(SST_ERAI_mask,r_value_ERAI_fields),long_name='Correlation coefficient between SST and AMET',
                               var_name='r',units='1',dim_coords_and_dims=[(latitude_ERAI_iris, 0), (longitude_ERAI_iris, 1)])
    cube_ERAI.coord('latitude').coord_system = coord_sys
    cube_ERAI.coord('longitude').coord_system = coord_sys
    title = 'Regression of SST Anomaly from ERA-Interim on AMET Anomaly of ERA-Interim across %d N' % (lat_interest_list[c])
    path = os.path.join(output_path,'SST','AMET_ERAI_fields_ERAI',
                        "Regression_AMET_ERAI_%dN_SST_ERAI_white_correlation_coef.jpeg" % (lat_interest_list[c]))
    figure_PlateCarree(cube_ERAI,title,vmin_SST_white,vmax_SST_white,label_SST_white,ticks_SST_white,
                   p_value_ERAI_fields,longitude_ERAI_fields,latitude_ERAI_fields,path)

#***************************************************************************#
#******************     regress of MERRA2 SST fields     *******************#
#*************   on AMET from ERA-Interim MERRA2 and JRA55   ***************#
#***************************************************************************#

# create an array to store the correlation coefficient
slope_MERRA2_fields = np.zeros((len(latitude_MERRA2_fields),len(longitude_MERRA2_fields)),dtype = float)
r_value_MERRA2_fields = np.zeros((len(latitude_MERRA2_fields),len(longitude_MERRA2_fields)),dtype = float)
p_value_MERRA2_fields= np.zeros((len(latitude_MERRA2_fields),len(longitude_MERRA2_fields)),dtype = float)

latitude_MERRA2_iris = iris.coords.DimCoord(latitude_MERRA2_fields,standard_name='latitude',long_name='latitude',
                             var_name='lat',units='degrees')
longitude_MERRA2_iris = iris.coords.DimCoord(longitude_MERRA2_fields,standard_name='longitude',long_name='longitude',
                             var_name='lon',units='degrees')
# choose the coordinate system for Cube (for regrid module)
coord_sys = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)

#*****************             SST anomalies             *******************#

for c in np.arange(len(lat_interest_list)):
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      MERRA2      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
    for i in np.arange(len(latitude_MERRA2_fields)):
        for j in np.arange(len(longitude_MERRA2_fields)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope_MERRA2_fields[i,j],_,r_value_MERRA2_fields[i,j],p_value_MERRA2_fields[i,j],_ = stats.linregress(AMET_MERRA2_white_series[:,lat_interest['MERRA2'][c]],SST_MERRA2_white_series[:,i,j])
    cube_MERRA2 = iris.cube.Cube(np.ma.masked_where(SST_MERRA2_mask,r_value_MERRA2_fields),long_name='Correlation coefficient between SST and AMET',
                               var_name='r',units='1',dim_coords_and_dims=[(latitude_MERRA2_iris, 0), (longitude_MERRA2_iris, 1)])
    cube_MERRA2.coord('latitude').coord_system = coord_sys
    cube_MERRA2.coord('longitude').coord_system = coord_sys
    title = 'Regression of SST Anomaly from MERRA2 on AMET Anomaly of MERRA2 across %d N' % (lat_interest_list[c])
    path = os.path.join(output_path,'SST','AMET_MERRA2_fields_MERRA2',
                        'Regression_AMET_MERRA2_%dN_SST_MERRA2_white_correlation_coef.jpeg' % (lat_interest_list[c]))
    figure_PlateCarree(cube_MERRA2,title,vmin_SST_white,vmax_SST_white,label_SST_white,ticks_SST_white,
                       p_value_MERRA2_fields,longitude_MERRA2_fields,latitude_MERRA2_fields,path)

print '*******************************************************************'
print '**********************     regression     *************************'
print '**************    anomalies after low pass filter   ***************'
print '*******************************************************************'
#***************************************************************************#
#*****************   regress of ERA Interim SLP fields   *******************#
#*************   on AMET from ERA-Interim MERRA2 and JRA55   ***************#
#*************            both with low pass filter          ***************#
#***************************************************************************#

# create an array to store the correlation coefficient
slope_ERAI_fields = np.zeros((len(latitude_ERAI_fields),len(longitude_ERAI_fields)),dtype = float)
r_value_ERAI_fields = np.zeros((len(latitude_ERAI_fields),len(longitude_ERAI_fields)),dtype = float)
p_value_ERAI_fields= np.zeros((len(latitude_ERAI_fields),len(longitude_ERAI_fields)),dtype = float)

latitude_ERAI_iris = iris.coords.DimCoord(latitude_ERAI_fields,standard_name='latitude',long_name='latitude',
                             var_name='lat',units='degrees')
longitude_ERAI_iris = iris.coords.DimCoord(longitude_ERAI_fields,standard_name='longitude',long_name='longitude',
                             var_name='lon',units='degrees')
# choose the coordinate system for Cube (for regrid module)
coord_sys = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)

#*****************             SLP anomalies             *******************#

for c in np.arange(len(lat_interest_list)):
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      ERA-Interim      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
    # plot correlation coefficient
    for i in np.arange(len(latitude_ERAI_fields)):
        for j in np.arange(len(longitude_ERAI_fields)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope_ERAI_fields[i,j],_,r_value_ERAI_fields[i,j],p_value_ERAI_fields[i,j],_ = stats.linregress(AMET_ERAI_white_series_running_mean[:,lat_interest['ERAI'][c]],SLP_ERAI_white_series_running_mean[:,i,j])
    cube_ERAI = iris.cube.Cube(r_value_ERAI_fields,long_name='Correlation coefficient between SLP and AMET',
                               var_name='r',units='1',dim_coords_and_dims=[(latitude_ERAI_iris, 0), (longitude_ERAI_iris, 1)])
    cube_ERAI.coord('latitude').coord_system = coord_sys
    cube_ERAI.coord('longitude').coord_system = coord_sys
    title = 'Regression of SLP Anomaly from ERA-Interim on AMET Anomaly of ERA-Interim across %d N with a runnming mean of %d months' % (lat_interest_list[c],window)
    path = os.path.join(output_path,'SLP','AMET_ERAI_fields_ERAI',
                        'Regression_AMET_ERAI_%dN_SLP_ERAI_white_lowpass_%dm_correlation_coef.jpeg' % (lat_interest_list[c],window))
    figure_PlateCarree(cube_ERAI,title,vmin_SLP_white_lowpass,vmax_SLP_white_lowpass,label_SLP_white_lowpass,ticks_SLP_white_lowpass,
                       p_value_ERAI_fields,longitude_ERAI_fields,latitude_ERAI_fields,path)


#***************************************************************************#
#*****************      regress of MERRA2 SLP fields     *******************#
#*************   on AMET from ERA-Interim MERRA2 and JRA55   ***************#
#*************            both with low pass filter          ***************#
#***************************************************************************#
# create an array to store the correlation coefficient
slope_MERRA2_fields = np.zeros((len(latitude_MERRA2_fields),len(longitude_MERRA2_fields)),dtype = float)
r_value_MERRA2_fields = np.zeros((len(latitude_MERRA2_fields),len(longitude_MERRA2_fields)),dtype = float)
p_value_MERRA2_fields= np.zeros((len(latitude_MERRA2_fields),len(longitude_MERRA2_fields)),dtype = float)

latitude_MERRA2_iris = iris.coords.DimCoord(latitude_MERRA2_fields,standard_name='latitude',long_name='latitude',
                             var_name='lat',units='degrees')
longitude_MERRA2_iris = iris.coords.DimCoord(longitude_MERRA2_fields,standard_name='longitude',long_name='longitude',
                             var_name='lon',units='degrees')
# choose the coordinate system for Cube (for regrid module)
coord_sys = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)

#*****************             SLP anomalies             *******************#

for c in np.arange(len(lat_interest_list)):
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      MERRA2      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
    for i in np.arange(len(latitude_MERRA2_fields)):
        for j in np.arange(len(longitude_MERRA2_fields)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope_MERRA2_fields[i,j],_,r_value_MERRA2_fields[i,j],p_value_MERRA2_fields[i,j],_ = stats.linregress(AMET_MERRA2_white_series_running_mean[:,lat_interest['MERRA2'][c]],SLP_MERRA2_white_series_running_mean[:,i,j])
    cube_MERRA2 = iris.cube.Cube(r_value_MERRA2_fields,long_name='Correlation coefficient between SLP and AMET',
                               var_name='r',units='1',dim_coords_and_dims=[(latitude_MERRA2_iris, 0), (longitude_MERRA2_iris, 1)])
    cube_MERRA2.coord('latitude').coord_system = coord_sys
    cube_MERRA2.coord('longitude').coord_system = coord_sys
    title = 'Regression of SLP Anomaly from MERRA2 on AMET Anomaly of MERRA2 across %d N with a running mean of %d months' % (lat_interest_list[c],window)
    path = os.path.join(output_path,'SLP','AMET_MERRA2_fields_MERRA2',
                        'Regression_AMET_MERRA2_%dN_SLP_MERRA2_white_lowpass_%dm_correlation_coef.jpeg' % (lat_interest_list[c],window))
    figure_PlateCarree(cube_MERRA2,title,vmin_SLP_white_lowpass,vmax_SLP_white_lowpass,label_SLP_white_lowpass,ticks_SLP_white_lowpass,
                       p_value_MERRA2_fields,longitude_MERRA2_fields,latitude_MERRA2_fields,path)

#***************************************************************************#
#******************      regress of ERAI SST fields      *******************#
#*************   on AMET from ERA-Interim MERRA2 and JRA55   ***************#
#*************            both with low pass filter          ***************#
#***************************************************************************#
# create an array to store the correlation coefficient
slope_ERAI_fields = np.zeros((len(latitude_ERAI_fields),len(longitude_ERAI_fields)),dtype = float)
r_value_ERAI_fields = np.zeros((len(latitude_ERAI_fields),len(longitude_ERAI_fields)),dtype = float)
p_value_ERAI_fields= np.zeros((len(latitude_ERAI_fields),len(longitude_ERAI_fields)),dtype = float)

latitude_ERAI_iris = iris.coords.DimCoord(latitude_ERAI_fields,standard_name='latitude',long_name='latitude',
                             var_name='lat',units='degrees')
longitude_ERAI_iris = iris.coords.DimCoord(longitude_ERAI_fields,standard_name='longitude',long_name='longitude',
                             var_name='lon',units='degrees')
# choose the coordinate system for Cube (for regrid module)
coord_sys = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)

#*****************             SST anomalies             *******************#

for c in np.arange(len(lat_interest_list)):
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      ERA-Interim      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
    # linear regress SST on AMET (anomalies)
    # plot correlation coefficient
    for i in np.arange(len(latitude_ERAI_fields)):
        for j in np.arange(len(longitude_ERAI_fields)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope_ERAI_fields[i,j],_,r_value_ERAI_fields[i,j],p_value_ERAI_fields[i,j],_ = stats.linregress(AMET_ERAI_white_series_running_mean[:,lat_interest['ERAI'][c]],SST_ERAI_white_series_running_mean[:,i,j])
    cube_ERAI = iris.cube.Cube(np.ma.masked_where(SST_ERAI_mask,r_value_ERAI_fields),long_name='Correlation coefficient between SST and AMET',
                               var_name='r',units='1',dim_coords_and_dims=[(latitude_ERAI_iris, 0), (longitude_ERAI_iris, 1)])
    cube_ERAI.coord('latitude').coord_system = coord_sys
    cube_ERAI.coord('longitude').coord_system = coord_sys
    title = 'Regression of SST Anomaly from ERA-Interim on AMET Anomaly of ERA-Interim across %d N with a running mean of %d months' % (lat_interest_list[c],window)
    path = os.path.join(output_path,'SST','AMET_ERAI_fields_ERAI',
                        'Regression_AMET_ERAI_%dN_SST_ERAI_white_lowpass_%dm_correlation_coef.jpeg' % (lat_interest_list[c],window))
    figure_PlateCarree(cube_ERAI,title,vmin_SST_white_lowpass,vmax_SST_white_lowpass,label_SST_white_lowpass,ticks_SST_white_lowpass,
                       p_value_ERAI_fields,longitude_ERAI_fields,latitude_ERAI_fields,path)

#***************************************************************************#
#*****************      regress of MERRA2 SST fields     *******************#
#*************   on AMET from ERA-Interim MERRA2 and JRA55   ***************#
#*************            both with low pass filter          ***************#
#***************************************************************************#
# create an array to store the correlation coefficient
slope_MERRA2_fields = np.zeros((len(latitude_MERRA2_fields),len(longitude_MERRA2_fields)),dtype = float)
r_value_MERRA2_fields = np.zeros((len(latitude_MERRA2_fields),len(longitude_MERRA2_fields)),dtype = float)
p_value_MERRA2_fields= np.zeros((len(latitude_MERRA2_fields),len(longitude_MERRA2_fields)),dtype = float)

latitude_MERRA2_iris = iris.coords.DimCoord(latitude_MERRA2_fields,standard_name='latitude',long_name='latitude',
                             var_name='lat',units='degrees')
longitude_MERRA2_iris = iris.coords.DimCoord(longitude_MERRA2_fields,standard_name='longitude',long_name='longitude',
                             var_name='lon',units='degrees')
# choose the coordinate system for Cube (for regrid module)
coord_sys = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)

#*****************             SST anomalies             *******************#

for c in np.arange(len(lat_interest_list)):
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      MERRA2      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
    for i in np.arange(len(latitude_MERRA2_fields)):
        for j in np.arange(len(longitude_MERRA2_fields)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope_MERRA2_fields[i,j],_,r_value_MERRA2_fields[i,j],p_value_MERRA2_fields[i,j],_ = stats.linregress(AMET_MERRA2_white_series_running_mean[:,lat_interest['MERRA2'][c]],SST_MERRA2_white_series_running_mean[:,i,j])
    # figsize works for the size of the map, not the entire figure
    fig29 = plt.figure()
    cube_MERRA2 = iris.cube.Cube(np.ma.masked_where(SST_MERRA2_mask,r_value_MERRA2_fields),long_name='Correlation coefficient between SST and AMET',
                               var_name='r',units='1',dim_coords_and_dims=[(latitude_MERRA2_iris, 0), (longitude_MERRA2_iris, 1)])
    cube_MERRA2.coord('latitude').coord_system = coord_sys
    cube_MERRA2.coord('longitude').coord_system = coord_sys
    title = 'Regression of SST Anomaly from MERRA2 on AMET Anomaly of MERRA2 across %d N with a running mean of %d months' % (lat_interest_list[c],window)
    path = os.path.join(output_path,'SST','AMET_MERRA2_fields_MERRA2',
                        'Regression_AMET_MERRA2_%dN_SST_MERRA2_white_lowpass_%dm_correlation_coef.jpeg' % (lat_interest_list[c],window))
    figure_PlateCarree(cube_MERRA2,title,vmin_SST_white_lowpass,vmax_SST_white_lowpass,label_SST_white_lowpass,ticks_SST_white_lowpass,
                       p_value_MERRA2_fields,longitude_MERRA2_fields,latitude_MERRA2_fields,path)

#***************************************************************************#
#******************   regress of ERA Interim TS fields   *******************#
#*************   on AMET from ERA-Interim MERRA2 and JRA55   ***************#
#***************************************************************************#
# create an array to store the correlation coefficient
slope_ERAI_fields = np.zeros((len(latitude_ERAI_fields),len(longitude_ERAI_fields)),dtype = float)
r_value_ERAI_fields = np.zeros((len(latitude_ERAI_fields),len(longitude_ERAI_fields)),dtype = float)
p_value_ERAI_fields= np.zeros((len(latitude_ERAI_fields),len(longitude_ERAI_fields)),dtype = float)

latitude_ERAI_iris = iris.coords.DimCoord(latitude_ERAI_fields,standard_name='latitude',long_name='latitude',
                             var_name='lat',units='degrees')
longitude_ERAI_iris = iris.coords.DimCoord(longitude_ERAI_fields,standard_name='longitude',long_name='longitude',
                             var_name='lon',units='degrees')
# choose the coordinate system for Cube (for regrid module)
coord_sys = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)

#*****************             TS anomalies             *******************#

for c in np.arange(len(lat_interest_list)):
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      ERA-Interim      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
    # linear regress SST on AMET (anomalies)
    # plot correlation coefficient
    for i in np.arange(len(latitude_ERAI_fields)):
        for j in np.arange(len(longitude_ERAI_fields)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope_ERAI_fields[i,j],_,r_value_ERAI_fields[i,j],p_value_ERAI_fields[i,j],_ = stats.linregress(AMET_ERAI_white_series[:,lat_interest['ERAI'][c]],TS_ERAI_white_series[:,i,j])
    cube_ERAI = iris.cube.Cube(r_value_ERAI_fields,long_name='Correlation coefficient between TS and AMET',
                               var_name='r',units='1',dim_coords_and_dims=[(latitude_ERAI_iris, 0), (longitude_ERAI_iris, 1)])
    cube_ERAI.coord('latitude').coord_system = coord_sys
    cube_ERAI.coord('longitude').coord_system = coord_sys
    title('Regression of TS Anomaly from ERA-Interim on AMET Anomaly of ERA-Interim across %d N' % (lat_interest_list[c]) ,fontsize = 7,y=0.93)
    path = os.path.join(output_path,'TS','AMET_ERAI_fields_ERAI',
                        'Regression_AMET_ERAI_%dN_TS_ERAI_white_correlation_coef.jpeg' % (lat_interest_list[c],window))
    figure_PlateCarree(cube_ERAI,title,vmin_TS_white,vmax_TS_white,label_TS_white,ticks_TS_white,
                       p_value_ERAI_fields,longitude_ERAI_fields,latitude_ERAI_fields,path)

#***************************************************************************#
#******************     regress of MERRA2 TS fields     ********************#
#*************   on AMET from ERA-Interim MERRA2 and JRA55   ***************#
#***************************************************************************#
# create an array to store the correlation coefficient
slope_MERRA2_fields = np.zeros((len(latitude_MERRA2_fields),len(longitude_MERRA2_fields)),dtype = float)
r_value_MERRA2_fields = np.zeros((len(latitude_MERRA2_fields),len(longitude_MERRA2_fields)),dtype = float)
p_value_MERRA2_fields= np.zeros((len(latitude_MERRA2_fields),len(longitude_MERRA2_fields)),dtype = float)

latitude_MERRA2_iris = iris.coords.DimCoord(latitude_MERRA2_fields,standard_name='latitude',long_name='latitude',
                             var_name='lat',units='degrees')
longitude_MERRA2_iris = iris.coords.DimCoord(longitude_MERRA2_fields,standard_name='longitude',long_name='longitude',
                             var_name='lon',units='degrees')
# choose the coordinate system for Cube (for regrid module)
coord_sys = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)

#*****************             TS anomalies             *******************#

for c in np.arange(len(lat_interest_list)):
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      MERRA2      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
    for i in np.arange(len(latitude_MERRA2_fields)):
        for j in np.arange(len(longitude_MERRA2_fields)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope_MERRA2_fields[i,j],_,r_value_MERRA2_fields[i,j],p_value_MERRA2_fields[i,j],_ = stats.linregress(AMET_MERRA2_white_series[:,lat_interest['MERRA2'][c]],TS_MERRA2_white_series[:,i,j])
    cube_MERRA2 = iris.cube.Cube(r_value_MERRA2_fields,long_name='Correlation coefficient between TS and AMET',
                               var_name='r',units='1',dim_coords_and_dims=[(latitude_MERRA2_iris, 0), (longitude_MERRA2_iris, 1)])
    cube_MERRA2.coord('latitude').coord_system = coord_sys
    cube_MERRA2.coord('longitude').coord_system = coord_sys
    title('Regression of TS Anomaly from MERRA2 on AMET Anomaly of MERRA2 across %d N' % (lat_interest_list[c]) ,fontsize = 7,y=0.93)
    path = os.path.join(output_path,'TS','AMET_MERRA2_fields_MERRA2',
                        'Regression_AMET_MERRA2_%dN_TS_MERRA2_white_correlation_coef.jpeg' % (lat_interest_list[c],window))
    figure_PlateCarree(cube_MERRA2,title,vmin_TS_white,vmax_TS_white,label_TS_white,ticks_TS_white,
                       p_value_MERRA2_fields,longitude_MERRA2_fields,latitude_MERRA2_fields,path)

#***************************************************************************#
#******************   regress of ERA Interim T2M fields   *******************#
#*************   on AMET from ERA-Interim MERRA2 and JRA55   ***************#
#***************************************************************************#
# create an array to store the correlation coefficient
slope_ERAI_fields = np.zeros((len(latitude_ERAI_fields),len(longitude_ERAI_fields)),dtype = float)
r_value_ERAI_fields = np.zeros((len(latitude_ERAI_fields),len(longitude_ERAI_fields)),dtype = float)
p_value_ERAI_fields= np.zeros((len(latitude_ERAI_fields),len(longitude_ERAI_fields)),dtype = float)

latitude_ERAI_iris = iris.coords.DimCoord(latitude_ERAI_fields,standard_name='latitude',long_name='latitude',
                             var_name='lat',units='degrees')
longitude_ERAI_iris = iris.coords.DimCoord(longitude_ERAI_fields,standard_name='longitude',long_name='longitude',
                             var_name='lon',units='degrees')
# choose the coordinate system for Cube (for regrid module)
coord_sys = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)

#*****************             T2M anomalies             *******************#

for c in np.arange(len(lat_interest_list)):
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      ERA-Interim      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
    # linear regress SST on AMET (anomalies)
    # plot correlation coefficient
    for i in np.arange(len(latitude_ERAI_fields)):
        for j in np.arange(len(longitude_ERAI_fields)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope_ERAI_fields[i,j],_,r_value_ERAI_fields[i,j],p_value_ERAI_fields[i,j],_ = stats.linregress(AMET_ERAI_white_series[:,lat_interest['ERAI'][c]],T2M_ERAI_white_series[:,i,j])
    cube_ERAI = iris.cube.Cube(r_value_ERAI_fields,long_name='Correlation coefficient between T2M and AMET',
                               var_name='r',units='1',dim_coords_and_dims=[(latitude_ERAI_iris, 0), (longitude_ERAI_iris, 1)])
    cube_ERAI.coord('latitude').coord_system = coord_sys
    cube_ERAI.coord('longitude').coord_system = coord_sys
    title = 'Regression of T2M Anomaly from ERA-Interim on AMET Anomaly of ERA-Interim across %d N' % (lat_interest_list[c])
    path = os.path.join(output_path,'T2M','AMET_ERAI_fields_ERAI',
                        'Regression_AMET_ERAI_%dN_T2M_ERAI_correlation_coef.jpeg' % (lat_interest_list[c],window))
    figure_PlateCarree(cube_ERAI,title,vmin_T2M_white,vmax_T2M_white,label_T2M_white,ticks_T2M_white,
                       p_value_ERAI_fields,longitude_ERAI_fields,latitude_ERAI_fields,path)

#***************************************************************************#
#******************     regress of MERRA2 T2M fields     ********************#
#*************   on AMET from ERA-Interim MERRA2 and JRA55   ***************#
#***************************************************************************#
# create an array to store the correlation coefficient
slope_MERRA2_fields = np.zeros((len(latitude_MERRA2_fields),len(longitude_MERRA2_fields)),dtype = float)
r_value_MERRA2_fields = np.zeros((len(latitude_MERRA2_fields),len(longitude_MERRA2_fields)),dtype = float)
p_value_MERRA2_fields= np.zeros((len(latitude_MERRA2_fields),len(longitude_MERRA2_fields)),dtype = float)

latitude_MERRA2_iris = iris.coords.DimCoord(latitude_MERRA2_fields,standard_name='latitude',long_name='latitude',
                             var_name='lat',units='degrees')
longitude_MERRA2_iris = iris.coords.DimCoord(longitude_MERRA2_fields,standard_name='longitude',long_name='longitude',
                             var_name='lon',units='degrees')
# choose the coordinate system for Cube (for regrid module)
coord_sys = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)

#*****************             T2M anomalies             *******************#

for c in np.arange(len(lat_interest_list)):
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@      MERRA2      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ #
    for i in np.arange(len(latitude_MERRA2_fields)):
        for j in np.arange(len(longitude_MERRA2_fields)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope_MERRA2_fields[i,j],_,r_value_MERRA2_fields[i,j],p_value_MERRA2_fields[i,j],_ = stats.linregress(AMET_MERRA2_white_series[:,lat_interest['MERRA2'][c]],T2M_MERRA2_white_series[:,i,j])
    cube_MERRA2 = iris.cube.Cube(r_value_MERRA2_fields,long_name='Correlation coefficient between T2M and AMET',
                               var_name='r',units='1',dim_coords_and_dims=[(latitude_MERRA2_iris, 0), (longitude_MERRA2_iris, 1)])
    cube_MERRA2.coord('latitude').coord_system = coord_sys
    cube_MERRA2.coord('longitude').coord_system = coord_sys
    title = 'Regression of T2M Anomaly from MERRA2 on AMET Anomaly of MERRA2 across %d N' % (lat_interest_list[c])
    path = os.path.join(output_path,'T2M','AMET_MERRA2_fields_MERRA2',
                        'Regression_AMET_MERRA2_%dN_T2M_MERRA2_white_correlation_coef.jpeg' % (lat_interest_list[c],window))
    figure_PlateCarree(cube_MERRA2,title,vmin_T2M_white,vmax_T2M_white,label_T2M_white,ticks_T2M_white,
                       p_value_MERRA2_fields,longitude_MERRA2_fields,latitude_MERRA2_fields,path)


print '*******************************************************************'
print '*********************** correlation Index *************************'
print '*******************************************************************'
# create correlation matrix
row_name = ['NAO','AO','MEI','AMO','PDO']
column_name_dataset = ['ERA-Interim','MERRA2','JRA55']
column_name_lat = lat_interest_list

# @@@@@@@@@@@@@@@    comparison between different products   @@@@@@@@@@@@@@@@@ #

# original & white time series
slope = np.zeros((len(column_name_dataset),len(row_name)),dtype=float)
r_value = np.zeros((len(column_name_dataset),len(row_name)),dtype=float)
p_value = np.zeros((len(column_name_dataset),len(row_name)),dtype=float)

# all the index are from 1979 - 2016
#******************             AMET anomaly             *******************#
for i in np.arange(len(column_name_lat)):
    slope[0,0],_,r_value[0,0],p_value[0,0],_ = stats.linregress(AMET_ERAI_white_series[:,lat_interest['ERAI'][i]],NAO)
    slope[1,0],_,r_value[1,0],p_value[1,0],_ = stats.linregress(AMET_MERRA2_white_series[:,lat_interest['MERRA2'][i]],NAO[12:])
    slope[2,0],_,r_value[2,0],p_value[2,0],_ = stats.linregress(AMET_JRA55_white_series[:,lat_interest['JRA55'][i]],NAO[:-12])

    slope[0,1],_,r_value[0,1],p_value[0,1],_ = stats.linregress(AMET_ERAI_white_series[:,lat_interest['ERAI'][i]],AO)
    slope[1,1],_,r_value[1,1],p_value[1,1],_ = stats.linregress(AMET_MERRA2_white_series[:,lat_interest['MERRA2'][i]],AO[12:])
    slope[2,1],_,r_value[2,1],p_value[2,1],_ = stats.linregress(AMET_JRA55_white_series[:,lat_interest['JRA55'][i]],AO[:-12])

    slope[0,2],_,r_value[0,2],p_value[0,2],_ = stats.linregress(AMET_ERAI_white_series[:,lat_interest['ERAI'][i]],MEI)
    slope[1,2],_,r_value[1,2],p_value[1,2],_ = stats.linregress(AMET_MERRA2_white_series[:,lat_interest['MERRA2'][i]],MEI[12:])
    slope[2,2],_,r_value[2,2],p_value[2,2],_ = stats.linregress(AMET_JRA55_white_series[:,lat_interest['JRA55'][i]],MEI[:-12])

    slope[0,3],_,r_value[0,3],p_value[0,3],_ = stats.linregress(AMET_ERAI_white_series[:,lat_interest['ERAI'][i]],AMO)
    slope[1,3],_,r_value[1,3],p_value[1,3],_ = stats.linregress(AMET_MERRA2_white_series[:,lat_interest['MERRA2'][i]],AMO[12:])
    slope[2,3],_,r_value[2,3],p_value[2,3],_ = stats.linregress(AMET_JRA55_white_series[:,lat_interest['JRA55'][i]],AMO[:-12])

    slope[0,4],_,r_value[0,4],p_value[0,4],_ = stats.linregress(AMET_ERAI_white_series[:,lat_interest['ERAI'][i]],PDO)
    slope[1,4],_,r_value[1,4],p_value[1,4],_ = stats.linregress(AMET_MERRA2_white_series[:,lat_interest['MERRA2'][i]],PDO[12:])
    slope[2,4],_,r_value[2,4],p_value[2,4],_ = stats.linregress(AMET_JRA55_white_series[:,lat_interest['JRA55'][i]],PDO[:-12])

    df_correlation = pandas.DataFrame(r_value,column_name_dataset,row_name)
    df_correlation.to_csv(output_path + os.sep + 'Index' + os.sep + 'Comp_AMET_white_%dN_index_correlation_r_matrix.csv' % (column_name_lat[i]),
                          index=True, header=True, decimal='.', float_format='%.3f')
    df_correlation = pandas.DataFrame(p_value,column_name_dataset,row_name)
    df_correlation.to_csv(output_path + os.sep + 'Index' + os.sep + 'Comp_AMET_white_%dN_index_correlation_p_matrix.csv' % (column_name_lat[i]),
                          index=True, header=True, decimal='.', float_format='%.3f')

#******************             AMET original             *******************#
for i in np.arange(len(column_name_lat)):
    slope[0,0],_,r_value[0,0],p_value[0,0],_ = stats.linregress(AMET_ERAI_series[:,lat_interest['ERAI'][i]],NAO)
    slope[1,0],_,r_value[1,0],p_value[1,0],_ = stats.linregress(AMET_MERRA2_series[:,lat_interest['MERRA2'][i]],NAO[12:])
    slope[2,0],_,r_value[2,0],p_value[2,0],_ = stats.linregress(AMET_JRA55_series[:,lat_interest['JRA55'][i]],NAO[:-12])

    slope[0,1],_,r_value[0,1],p_value[0,1],_ = stats.linregress(AMET_ERAI_series[:,lat_interest['ERAI'][i]],AO)
    slope[1,1],_,r_value[1,1],p_value[1,1],_ = stats.linregress(AMET_MERRA2_series[:,lat_interest['MERRA2'][i]],AO[12:])
    slope[2,1],_,r_value[2,1],p_value[2,1],_ = stats.linregress(AMET_JRA55_series[:,lat_interest['JRA55'][i]],AO[:-12])

    slope[0,2],_,r_value[0,2],p_value[0,2],_ = stats.linregress(AMET_ERAI_series[:,lat_interest['ERAI'][i]],MEI)
    slope[1,2],_,r_value[1,2],p_value[1,2],_ = stats.linregress(AMET_MERRA2_series[:,lat_interest['MERRA2'][i]],MEI[12:])
    slope[2,2],_,r_value[2,2],p_value[2,2],_ = stats.linregress(AMET_JRA55_series[:,lat_interest['JRA55'][i]],MEI[:-12])

    slope[0,3],_,r_value[0,3],p_value[0,3],_ = stats.linregress(AMET_ERAI_series[:,lat_interest['ERAI'][i]],AMO)
    slope[1,3],_,r_value[1,3],p_value[1,3],_ = stats.linregress(AMET_MERRA2_series[:,lat_interest['MERRA2'][i]],AMO[12:])
    slope[2,3],_,r_value[2,3],p_value[2,3],_ = stats.linregress(AMET_JRA55_series[:,lat_interest['JRA55'][i]],AMO[:-12])

    slope[0,4],_,r_value[0,4],p_value[0,4],_ = stats.linregress(AMET_ERAI_series[:,lat_interest['ERAI'][i]],PDO)
    slope[1,4],_,r_value[1,4],p_value[1,4],_ = stats.linregress(AMET_MERRA2_series[:,lat_interest['MERRA2'][i]],PDO[12:])
    slope[2,4],_,r_value[2,4],p_value[2,4],_ = stats.linregress(AMET_JRA55_series[:,lat_interest['JRA55'][i]],PDO[:-12])

    df_correlation = pandas.DataFrame(r_value,column_name_dataset,row_name)
    df_correlation.to_csv(output_path + os.sep + 'Index' + os.sep + 'Comp_AMET_%dN_index_correlation_r_matrix.csv' % (column_name_lat[i]),
                          index=True, header=True, decimal='.', float_format='%.3f')
    df_correlation = pandas.DataFrame(p_value,column_name_dataset,row_name)
    df_correlation.to_csv(output_path + os.sep + 'Index' + os.sep + 'Comp_AMET_%dN_index_correlation_p_matrix.csv' % (column_name_lat[i]),
                          index=True, header=True, decimal='.', float_format='%.3f')

# @@@@@@@@@@@@@@@    comparison between different latitudes   @@@@@@@@@@@@@@@@@ #

# @@@@@@@@@@@@@@@    ERA Interim   @@@@@@@@@@@@@@@@@ #

#******************             AMET anomaly             *******************#

# original & white time series
slope = np.zeros((len(column_name_lat),len(row_name)),dtype=float)
r_value = np.zeros((len(column_name_lat),len(row_name)),dtype=float)
p_value = np.zeros((len(column_name_lat),len(row_name)),dtype=float)

for i in np.arange(len(lat_interest_list)):
    slope[i,0],_,r_value[i,0],p_value[i,0],_ = stats.linregress(AMET_ERAI_white_series[:,lat_interest['ERAI'][i]],NAO)
    slope[i,1],_,r_value[i,1],p_value[i,1],_ = stats.linregress(AMET_ERAI_white_series[:,lat_interest['ERAI'][i]],AO)
    slope[i,2],_,r_value[i,2],p_value[i,2],_ = stats.linregress(AMET_ERAI_white_series[:,lat_interest['ERAI'][i]],MEI)
    slope[i,3],_,r_value[i,3],p_value[i,3],_ = stats.linregress(AMET_ERAI_white_series[:,lat_interest['ERAI'][i]],AMO)
    slope[i,4],_,r_value[i,4],p_value[i,4],_ = stats.linregress(AMET_ERAI_white_series[:,lat_interest['ERAI'][i]],PDO)

df_correlation = pandas.DataFrame(r_value,column_name_lat,row_name)
df_correlation.to_csv(output_path + os.sep + 'Index' + os.sep + 'Comp_AMET_ERAI_white_index_correlation_r_matrix.csv',
                      index=True, header=True, decimal='.', float_format='%.3f')
df_correlation = pandas.DataFrame(p_value,column_name_lat,row_name)
df_correlation.to_csv(output_path + os.sep + 'Index' + os.sep + 'Comp_AMET_ERAI_white_index_correlation_p_matrix.csv',
                      index=True, header=True, decimal='.', float_format='%.3f')

#******************             AMET original             *******************#
# original & white time series
slope = np.zeros((len(column_name_lat),len(row_name)),dtype=float)
r_value = np.zeros((len(column_name_lat),len(row_name)),dtype=float)
p_value = np.zeros((len(column_name_lat),len(row_name)),dtype=float)

for i in np.arange(len(lat_interest_list)):
    slope[i,0],_,r_value[i,0],p_value[i,0],_ = stats.linregress(AMET_ERAI_series[:,lat_interest['ERAI'][i]],NAO)
    slope[i,1],_,r_value[i,1],p_value[i,1],_ = stats.linregress(AMET_ERAI_series[:,lat_interest['ERAI'][i]],AO)
    slope[i,2],_,r_value[i,2],p_value[i,2],_ = stats.linregress(AMET_ERAI_series[:,lat_interest['ERAI'][i]],MEI)
    slope[i,3],_,r_value[i,3],p_value[i,3],_ = stats.linregress(AMET_ERAI_series[:,lat_interest['ERAI'][i]],AMO)
    slope[i,4],_,r_value[i,4],p_value[i,4],_ = stats.linregress(AMET_ERAI_series[:,lat_interest['ERAI'][i]],PDO)

df_correlation = pandas.DataFrame(r_value,column_name_lat,row_name)
df_correlation.to_csv(output_path + os.sep + 'Index' + os.sep + 'Comp_AMET_ERAI_index_correlation_r_matrix.csv',
                      index=True, header=True, decimal='.', float_format='%.3f')
df_correlation = pandas.DataFrame(p_value,column_name_lat,row_name)
df_correlation.to_csv(output_path + os.sep + 'Index' + os.sep + 'Comp_AMET_ERAI_index_correlation_p_matrix.csv',
                      index=True, header=True, decimal='.', float_format='%.3f')

# @@@@@@@@@@@@@@@    MERRA2   @@@@@@@@@@@@@@@@@ #

#******************             AMET anomaly             *******************#
# original & white time series
slope = np.zeros((len(column_name_lat),len(row_name)),dtype=float)
r_value = np.zeros((len(column_name_lat),len(row_name)),dtype=float)
p_value = np.zeros((len(column_name_lat),len(row_name)),dtype=float)

for i in np.arange(len(lat_interest_list)):
    slope[i,0],_,r_value[i,0],p_value[i,0],_ = stats.linregress(AMET_MERRA2_white_series[:,lat_interest['MERRA2'][i]],NAO[12:])
    slope[i,1],_,r_value[i,1],p_value[i,1],_ = stats.linregress(AMET_MERRA2_white_series[:,lat_interest['MERRA2'][i]],AO[12:])
    slope[i,2],_,r_value[i,2],p_value[i,2],_ = stats.linregress(AMET_MERRA2_white_series[:,lat_interest['MERRA2'][i]],MEI[12:])
    slope[i,3],_,r_value[i,3],p_value[i,3],_ = stats.linregress(AMET_MERRA2_white_series[:,lat_interest['MERRA2'][i]],AMO[12:])
    slope[i,4],_,r_value[i,4],p_value[i,4],_ = stats.linregress(AMET_MERRA2_white_series[:,lat_interest['MERRA2'][i]],PDO[12:])

df_correlation = pandas.DataFrame(r_value,column_name_lat,row_name)
df_correlation.to_csv(output_path + os.sep + 'Index' + os.sep + 'Comp_AMET_MERRA2_white_index_correlation_r_matrix.csv',
                      index=True, header=True, decimal='.', float_format='%.3f')
df_correlation = pandas.DataFrame(p_value,column_name_lat,row_name)
df_correlation.to_csv(output_path + os.sep + 'Index' + os.sep + 'Comp_AMET_MERRA2_white_index_correlation_p_matrix.csv',
                      index=True, header=True, decimal='.', float_format='%.3f')

#******************             AMET original             *******************#
# original & white time series
slope = np.zeros((len(column_name_lat),len(row_name)),dtype=float)
r_value = np.zeros((len(column_name_lat),len(row_name)),dtype=float)
p_value = np.zeros((len(column_name_lat),len(row_name)),dtype=float)

for i in np.arange(len(lat_interest_list)):
    slope[i,0],_,r_value[i,0],p_value[i,0],_ = stats.linregress(AMET_MERRA2_series[:,lat_interest['MERRA2'][i]],NAO[12:])
    slope[i,1],_,r_value[i,1],p_value[i,1],_ = stats.linregress(AMET_MERRA2_series[:,lat_interest['MERRA2'][i]],AO[12:])
    slope[i,2],_,r_value[i,2],p_value[i,2],_ = stats.linregress(AMET_MERRA2_series[:,lat_interest['MERRA2'][i]],MEI[12:])
    slope[i,3],_,r_value[i,3],p_value[i,3],_ = stats.linregress(AMET_MERRA2_series[:,lat_interest['MERRA2'][i]],AMO[12:])
    slope[i,4],_,r_value[i,4],p_value[i,4],_ = stats.linregress(AMET_MERRA2_series[:,lat_interest['MERRA2'][i]],PDO[12:])

df_correlation = pandas.DataFrame(r_value,column_name_lat,row_name)
df_correlation.to_csv(output_path + os.sep + 'Index' + os.sep + 'Comp_AMET_MERRA2_index_correlation_r_matrix.csv',
                      index=True, header=True, decimal='.', float_format='%.3f')
df_correlation = pandas.DataFrame(p_value,column_name_lat,row_name)
df_correlation.to_csv(output_path + os.sep + 'Index' + os.sep + 'Comp_AMET_MERRA2_index_correlation_p_matrix.csv',
                      index=True, header=True, decimal='.', float_format='%.3f')


#******************             AMET anomaly             *******************#
# original & white time series
slope = np.zeros((len(column_name_lat),len(row_name)),dtype=float)
r_value = np.zeros((len(column_name_lat),len(row_name)),dtype=float)
p_value = np.zeros((len(column_name_lat),len(row_name)),dtype=float)

for i in np.arange(len(lat_interest_list)):
    slope[i,0],_,r_value[i,0],p_value[i,0],_ = stats.linregress(AMET_JRA55_white_series[:,lat_interest['JRA55'][i]],NAO[:-12])
    slope[i,1],_,r_value[i,1],p_value[i,1],_ = stats.linregress(AMET_JRA55_white_series[:,lat_interest['JRA55'][i]],AO[:-12])
    slope[i,2],_,r_value[i,2],p_value[i,2],_ = stats.linregress(AMET_JRA55_white_series[:,lat_interest['JRA55'][i]],MEI[:-12])
    slope[i,3],_,r_value[i,3],p_value[i,3],_ = stats.linregress(AMET_JRA55_white_series[:,lat_interest['JRA55'][i]],AMO[:-12])
    slope[i,4],_,r_value[i,4],p_value[i,4],_ = stats.linregress(AMET_JRA55_white_series[:,lat_interest['JRA55'][i]],PDO[:-12])

df_correlation = pandas.DataFrame(r_value,column_name_lat,row_name)
df_correlation.to_csv(output_path + os.sep + 'Index' + os.sep + 'Comp_AMET_JRA55_white_index_correlation_r_matrix.csv',
                      index=True, header=True, decimal='.', float_format='%.3f')
df_correlation = pandas.DataFrame(p_value,column_name_lat,row_name)
df_correlation.to_csv(output_path + os.sep + 'Index' + os.sep + 'Comp_AMET_JRA55_white_index_correlation_p_matrix.csv',
                      index=True, header=True, decimal='.', float_format='%.3f')

#******************             AMET original             *******************#
# original & white time series
slope = np.zeros((len(column_name_lat),len(row_name)),dtype=float)
r_value = np.zeros((len(column_name_lat),len(row_name)),dtype=float)
p_value = np.zeros((len(column_name_lat),len(row_name)),dtype=float)

for i in np.arange(len(lat_interest_list)):
    slope[i,0],_,r_value[i,0],p_value[i,0],_ = stats.linregress(AMET_JRA55_series[:,lat_interest['JRA55'][i]],NAO[:-12])
    slope[i,1],_,r_value[i,1],p_value[i,1],_ = stats.linregress(AMET_JRA55_series[:,lat_interest['JRA55'][i]],AO[:-12])
    slope[i,2],_,r_value[i,2],p_value[i,2],_ = stats.linregress(AMET_JRA55_series[:,lat_interest['JRA55'][i]],MEI[:-12])
    slope[i,3],_,r_value[i,3],p_value[i,3],_ = stats.linregress(AMET_JRA55_series[:,lat_interest['JRA55'][i]],AMO[:-12])
    slope[i,4],_,r_value[i,4],p_value[i,4],_ = stats.linregress(AMET_JRA55_series[:,lat_interest['JRA55'][i]],PDO[:-12])

df_correlation = pandas.DataFrame(r_value,column_name_lat,row_name)
df_correlation.to_csv(output_path + os.sep + 'Index' + os.sep + 'Comp_AMET_JRA55_index_correlation_r_matrix.csv',
                      index=True, header=True, decimal='.', float_format='%.3f')
df_correlation = pandas.DataFrame(p_value,column_name_lat,row_name)
df_correlation.to_csv(output_path + os.sep + 'Index' + os.sep + 'Comp_AMET_JRA55_index_correlation_p_matrix.csv',
                      index=True, header=True, decimal='.', float_format='%.3f')

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
