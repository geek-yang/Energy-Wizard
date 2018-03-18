#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : Investigate the correlation between AMET (MERRA2,ERA-Interim,JRA55) and all kinds of fields
Author          : Yang Liu
Date            : 2018.03.16
Last Update     : 2018.03.18
Description     : The code aims to dig into the correlation between atmospheric meridional
                  energy transport and all kinds of climatological fields, as well as some
                  climate index.

                  The AMET are computed from the datasets includes MERRA II from NASA,
                  ERA-Interim from ECMWF and JRA55 from JMA.

                  The index of interest include NAO, AO, AMO, PDO, ENSO.

                  The variable fields of insterest include Sea Level Pressure (SLP), Sea
                  Surface Tmperature (SST) and Sea Ice Concentration (SIC).

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
import cartopy
import cartopy.crs as ccrs
import matplotlib.ticker as mticker
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import iris
import iris.plot as iplt
import iris.quickplot as qplt

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
dataset_MERRA2_fields = Dataset(datapath_MERRA2_fields + os.sep + 'surface_MERRA2_monthly_regress_1979_2016.nc')

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

SLP_ERAI_series = dataset_ERAI_fields.variables['msl'][:]      # dimension (time, lat, lon)
SLP_MERRA2 = dataset_MERRA2_fields.variables['SLP'][:]  # dimension (year, month, lat, lon)

SST_ERAI_series = dataset_ERAI_fields.variables['sst'][:]
SST_ERAI_mask = np.ma.getmaskarray(SST_ERAI_series[0,:,:])
#SST_MERRA2_ice = dataset_MERRA2_fields.variables['SST_ice'][:]
SST_MERRA2_water = dataset_MERRA2_fields.variables['SST_water'][:]
#SST_MERRA2_water[SST_MERRA2_water>1000] = 0
SST_MERRA2_water = np.ma.masked_where(SST_MERRA2_water>1000,SST_MERRA2_water)
SST_MERRA2_water_mask = np.ma.getmaskarray(SST_MERRA2_water[0,0,:,:])

SIC_ERAI_series = dataset_ERAI_fields.variables['ci'][:]
SIC_ERAI_mask = np.ma.getmaskarray(SIC_ERAI_series[0,:,:])
SIC_MERRA2 = dataset_MERRA2_fields.variables['SIC'][:]
SIC_MERRA2_mask = np.ma.getmaskarray(SIC_MERRA2[0,0,:,:])

latitude_ERAI_fields = dataset_ERAI_fields.variables['latitude'][:]
latitude_MERRA2_fields = dataset_MERRA2_fields.variables['latitude'][:]

longitude_ERAI_fields = dataset_ERAI_fields.variables['longitude'][:]
longitude_MERRA2_fields = dataset_MERRA2_fields.variables['longitude'][:]

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
for i in month_ind:
    # calculate the monthly mean (seasonal cycling)
    seasonal_cycle_SLP_ERAI[i,:,:] = np.mean(SLP_ERAI_series[i::12,:,:],axis=0)
    # remove seasonal mean
    SLP_ERAI_white_series[i::12,:,:] = SLP_ERAI_series[i::12,:,:] - seasonal_cycle_SLP_ERAI[i,:,:]

seasonal_cycle_SLP_MERRA2 = np.mean(SLP_MERRA2,axis=0)
SLP_MERRA2_white = np.zeros(SLP_MERRA2.shape,dtype=float)
for i in np.arange(len(year_MERRA2_fields)):
    for j in month_ind:
        SLP_MERRA2_white[i,j,:,:] = SLP_MERRA2[i,j,:,:] - seasonal_cycle_SLP_MERRA2[j,:,:]
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
SLP_MERRA2_series = SLP_MERRA2_white.reshape(len(year_MERRA2_fields)*len(month_ind),len(latitude_MERRA2_fields),len(longitude_MERRA2_fields))
# fields without seasonal cycle - time series
SLP_MERRA2_white_series = SLP_MERRA2_white.reshape(len(year_MERRA2_fields)*len(month_ind),len(latitude_MERRA2_fields),len(longitude_MERRA2_fields))
print '*******************************************************************'
print '************************** regression *****************************'
print '*******************************************************************'

#*****************   regress of ERA Interim SLP fields   *******************#
#*****************             SLP anomalies             *******************#

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

for c in np.arange(len(lat_interest_list)):
    # linear regress SLP on AMET (anomalies)
    # plot correlation coefficient
    for i in np.arange(len(latitude_ERAI_fields)):
        for j in np.arange(len(longitude_ERAI_fields)):
            # return value: slope, intercept, r_value, p_value, stderr
            slope_ERAI_fields[i,j],_,r_value_ERAI_fields[i,j],p_value_ERAI_fields[i,j],_ = stats.linregress(AMET_ERAI_white_series[:,lat_interest['ERAI'][c]],SLP_ERAI_white_series[:,i,j])
    # figsize works for the size of the map, not the entire figure
    fig1 = plt.figure()
    cube_ERAI = iris.cube.Cube(r_value_ERAI_fields,long_name='Correlation coefficient between SLP and AMET',
                               var_name='r',units='1',dim_coords_and_dims=[(latitude_ERAI_iris, 0), (longitude_ERAI_iris, 1)])
    cube_ERAI.coord('latitude').coord_system = coord_sys
    cube_ERAI.coord('longitude').coord_system = coord_sys
    # suptitle is the title for the figure
    fig1.suptitle('Regression of SLP Anomaly on AMET Anomaly of ERA-Interim across %d N' % (lat_interest_list[c]) ,fontsize = 7,y=0.93)
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_global()
    #ax.set_aspect('auto')
    ax.set_aspect('0.8')
    ax.coastlines()
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,linewidth=1, color='gray', alpha=0.5,linestyle='--')
    gl.xlabels_top = False
    # use of formatter (fixed), only after this the style setup will work
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    # specify label styles
    gl.xlabel_style = {'size': 6, 'color': 'gray'}
    gl.ylabel_style = {'size': 6, 'color': 'gray'}
    cs = iplt.contourf(cube_ERAI,cmap='coolwarm',vmin=-0.25,vmax=0.25)
    cbar = fig1.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.1,format="%.2f")
    cbar.set_ticks([-0.25, -0.20, -0.15, -0.10, -0.05, 0, 0.05, 0.10, 0.15, 0.20, 0.25])
    cbar.ax.tick_params(labelsize = 6)
    cbar.set_label('Correlation coefficient',size = 6)
    # locate the indices of p_value matrix where error p<0.05 (99.5% confident)
    ii, jj = np.where(p_value_ERAI_fields<=0.05)
    # get the coordinate on the map (lon,lat) and plot scatter dots
    ax.scatter(longitude_ERAI_fields[jj],latitude_ERAI_fields[ii],transform=ccrs.Geodetic(),s=0.1,c='g',alpha=0.3) # alpha bleding factor with map
    # show and save plot
    plt.show()
    fig1.savefig(output_path + os.sep + 'SLP' + os.sep + 'AMET_ERAI_fields_ERAI' + os.sep + "Regression_AMET_ERAI_%dN_SLP_ERAI_white_correlation_coef.jpeg" % (lat_interest_list[c]),dpi=300)


    # # setup north polar stereographic basemap
    # # resolution c(crude) l(low) i(intermidiate) h(high) f(full)
    # m = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90,llcrnrlon=0,urcrnrlon=360,resolution='l')
    # # draw coastlines
    # m.drawcoastlines(linewidth=0.25)
    # # fill continents, set lake color same as ocean color.
    # # m.fillcontinents(color='coral',lake_color='aqua')
    # # draw parallels and meridians
    # # label location labels=[west,east,north,south]
    # m.drawparallels(np.arange(-90,91,30),labels=[1,1,0,0],fontsize = 7,linewidth=0.75,color='gray')
    # m.drawmeridians(np.arange(-180,181,60),labels=[0,0,0,1],fontsize = 7,linewidth=0.75,color='gray')
    # # x,y coordinate - lon, lat
    # xx, yy = np.meshgrid(longitude_ERAI_fields,latitude_ERAI_fields)
    # XX, YY = m(xx, yy)
    # # define color range for the contourf
    # color = np.linspace(-0.30,0.30,13) # SLP_white
    # # !!!!!take care about the coordinate of contourf(Longitude, Latitude, data(Lat,Lon))
    # cs = m.contourf(XX,YY,r_value_ERAI_fields,color,cmap='coolwarm') # SLP_white
    # # add color bar
    # cbar = m.colorbar(cs,location="bottom",size='4%',pad="8%",format='%.2f')
    # cbar.ax.tick_params(labelsize=8)
    # cbar.set_label('Correlation Coefficient',fontsize = 8)
    # # fancy layout of maps
    # # label of contour lines on the map
    # #plt.clabel(cs,incline=True, format='%.1f', fontsize=12, colors='k')
    # # draw significance stippling on the map
    # # locate the indices of p_value matrix where error p<0.05 (99.5% confident)
    # ii, jj = np.where(p_value_ERAI_fields<=0.05)
    # # get the coordinate on the map (lon,lat) and plot scatter dots
    # m.scatter(XX[ii,jj],YY[ii,jj],1.5,marker='.',color='g',alpha=0.4, edgecolor='none') # alpha bleding factor with map
    # plt.title('Regression of SLP Anomaly on AMET Anomaly across %d N' % (lat_interest_list[c]),fontsize = 9, y=1.05)
    # plt.show()
    # fig1.savefig(output_path + os.sep + 'SLP' + os.sep + 'AMET_ERAI_fields_ERAI' + os.sep + "Regression_AMET_ERAI_%dN_SLP_ERAI_white_correlation_coef.jpeg" % (lat_interest_list[c]),dpi=400)

#*****************      regress of MERRA2 SLP fields     *******************#
#*****************             SLP anomalies             *******************#

print '*******************************************************************'
print '************************** regression *****************************'
print '*******************************************************************'



print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
