#!/usr/bin/env python
"""
Copyright Netherlands eScience Center

Function        : Postprocessing meridional energy transport from HPC cloud (GLORYS2V3)
Author          : Yang Liu
Date            : 2017.11.9
Last Update     : 2017.11.9
Description     : The code aims to postprocess the output from the HPC cloud
                  regarding the computation of oceainic meridional energy
                  transport based on oceanic reanalysis dataset GLORYS2V3 from Mercator Ocean.
                  The complete procedure includes data extraction and making plots.

Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, matplotlib
variables       : Meridional Energy Transport               E
                  Land-Sea Mask                             mask
Caveat!!        : The full dataset is from 1992 to 2014. The data coverage is the entire globe.
"""

import numpy as np
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
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import iris
import iris.plot as iplt
import iris.quickplot as qplt

# print the system structure and the path of the kernal
print platform.architecture()
print os.path

# calculate the time for the code execution
start_time = tttt.time()
# switch on the seaborn effect
sns.set()
################################   Input zone  ######################################
# specify data path
datapath = 'F:\DataBase\HPC_out\GLORYS2V3\postprocessing'
# specify output path for the netCDF4 file
output_path = 'F:\DataBase\HPC_out\GLORYS2V3\postprocessing'
Lat_num = 60 # gphiv = 788
# mask path
mask_path = 'F:\DataBase\GLORYS\S2V3\Monthly'
####################################################################################
print '*******************************************************************'
print '*********************** extract variables *************************'
print '*******************************************************************'
# ORCA025_z75 grid infor (Madec and Imbard 1996)
ji = 1440
jj = 1021
level = 75
# zonal integral
dataset = Dataset(datapath + os.sep + 'GLORYS2V3_model_monthly_orca025_E_zonal_int.nc')
# spacial distribution
dataset_point = Dataset(datapath + os.sep + 'GLORYS2V3_model_monthly_orca025_E_point.nc')
# load land-sea mask INFO
dataset_mask = Dataset(mask_path + os.sep + 'G2V3_mesh_mask_myocean.nc')
dataset_mask_atlantic = Dataset(mask_path + os.sep + 'new_maskglo.nc')

for zonal in dataset.variables:
    print dataset.variables['%s' % (zonal)]

for point in dataset_point.variables:
    print dataset_point.variables['%s' % (point)]

# zonal integral
E = dataset.variables['E'][:]
# spacial distribution
E_point = dataset_point.variables['E'][:]

year = dataset.variables['year'][:]
month = dataset.variables['month'][:]
latitude_aux = dataset.variables['latitude_aux'][:]
level = dataset.variables['lev'][:]
latitude = dataset_point.variables['latitude'][:]
longitude = dataset_point.variables['longitude'][:]

# land-sea mask
# surface mask for v grid
vmask = dataset_mask.variables['vmask'][0,0,:,:]
tmaskatl = dataset_mask_atlantic.variables['tmaskatl'][:,1:-1] # attention that the size is different!

print '*******************************************************************'
print '****************** prepare variables for plot *********************'
print '*******************************************************************'
# remove seasonal cycles
# zonal integral
month_ind = np.arange(12)
year_ind = np.arange(len(year))

E_seasonal_cycle = np.mean(E,0)
E_white = np.zeros(E.shape)
for i in month_ind:
    for j in year_ind:
        E_white[j,i,:] = E[j,i,:] - E_seasonal_cycle[i,:]
# spacial distribution
E_point_seasonal_cycle = np.mean(E_point,0)
E_point_white = np.zeros(E_point.shape)
for i in month_ind:
    for j in year_ind:
        E_point_white[j,i,:,:] = E_point[j,i,:,:] - E_point_seasonal_cycle[i,:,:]

# reshape the array into time series
# original signals
series_E = E.reshape(len(year)*len(month),len(latitude_aux))
# whiten signals
series_E_white = E_white.reshape(len(year)*len(month),len(latitude_aux))
series_E_point_white = E_point_white.reshape(len(year)*len(month),jj,ji)

# transpose
# original signals
T_series_E = np.transpose(series_E)
# whiten signals
T_series_E_white = np.transpose(series_E_white)

index = np.arange(1,len(year)*len(month)+1,1)
index_year = np.arange(1992,1992+len(year)+1,1)
axis_ref = np.zeros(len(index))

print '*******************************************************************'
print '*********************** time series plots *************************'
print '*******************************************************************'
# 60 N total meridional energy transport time series
fig1 = plt.figure()
plt.plot(index,T_series_E[788,:]/1000,'b-',label='GLORYS2V3') # lat = 60N
plt.title('Oceanic Meridional Energy Transport time series at %d N (1992-2014)' % (Lat_num))
#plt.legend()
fig1.set_size_inches(12, 5)
plt.xlabel("Time")
plt.xticks(np.linspace(0, 276, 24), index_year)
plt.xticks(rotation=60)
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig1.savefig(output_path + os.sep + 'OMET_GLORYS2V3_%dN_total_time_series_1992_2014.jpg' % (Lat_num), dpi = 500)

print '*******************************************************************'
print '*********************** time series shades ************************'
print '*******************************************************************'

x , y = np.meshgrid(index,latitude_aux[579:])

fig2 = plt.figure()
#plt.contour(x,y,T_series_E/1000, linewidth=0.05, colors='k')
# cmap 'jet' 'RdYlBu' 'coolwarm'
plt.contourf(x,y,T_series_E[579:,:]/1000,cmap='coolwarm') # from 20N-90N
plt.title('Oceanic Meridional Energy Transport time series(1992-2014)' )
fig2.set_size_inches(12, 5)
#add color bar
cbar = plt.colorbar()
cbar.set_label('PW (1E+15W)')
plt.xlabel("Time")
plt.xticks(np.linspace(0, 276, 24), index_year)
plt.xticks(rotation=60)
plt.ylabel("Latitude (Globe)")
plt.show()
fig2.savefig(output_path + os.sep + 'OMET_GLORYS2V3_time_series_1992_2014_shades.jpg', dpi = 500)

print '*******************************************************************'
print '*************************** x-y lines  ****************************'
print '*******************************************************************'

fig3 = plt.figure()
plt.axhline(y=0, color='r',ls='--')
plt.plot(latitude_aux,np.mean(series_E,0)/1000,'b-',label='GLORYS2V3')
plt.title('Oceanic Meridional Energy Transport (1992-2014)' )
#plt.legend()
plt.xlabel("Latitudes")
#plt.xticks()
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig3.savefig(output_path + os.sep + 'OMET_GLORYS2V3_mean_1992_2014.jpg', dpi = 500)

print '*******************************************************************'
print '************************* wind rose plots *************************'
print '*******************************************************************'

angle = np.linspace(0, 2 * np.pi, 13)
# np.repeat
angle_series = np.tile(angle[:-1],23)
month_str = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

# wind rose of time series
fig4 = plt.figure()
plt.axes(polar = True)
plt.plot(angle_series,T_series_E[788,:]/1000,'b--',label='GLORYS2V3')
plt.title('Oceanic Meridional Energy Transport at %d N (1992-2014)' % (Lat_num), y=1.07)
#plt.legend()
#fig10.set_size_inches(14, 4)
#plt.xlabel("Time")
plt.xticks(angle[:-1], month_str)
plt.yticks(np.linspace(0,1,5),color='r',size =12)
#plt.xticks(rotation=60)
#plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig4.savefig(output_path + os.sep + 'OMET_GLORYS2V3_%dN_total_windrose_1992_2014.jpg' % (Lat_num), dpi = 500)

# wind rose of time series after removing seasonal cycles

fig5 = plt.figure()
plt.axes(polar = True)
plt.plot(angle_series,T_series_E_white[788,:]/1000,'b--',label='GLORYS2V3')
plt.title('Oceanic Meridional Energy Transport anomaly at %d N (1992-2014)' % (Lat_num), y=1.07)
#plt.legend()
#fig10.set_size_inches(14, 4)
#plt.xlabel("Time")
plt.xticks(angle[:-1], month_str)
plt.yticks(np.linspace(-0.1,0.1,5),color='r',size =12)
#plt.xticks(rotation=60)
#plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig5.savefig(output_path + os.sep + 'OMET_GLORYS2V3_%dN_total_windrose_white_1992_2014.jpg' % (Lat_num), dpi = 500)

print '*******************************************************************'
print '********************** spacial distribution ***********************'
print '*******************************************************************'
# The plot tool is iris
# For each plot, a cube has to been constructed first
# spacial distribution of AMET - mean of 36 years

latitude_cube = iris.coords.AuxCoord(latitude,standard_name='latitude',units='degrees')
longitude_cube = iris.coords.AuxCoord(longitude,standard_name='longitude',units='degrees')
E_point_mean = np.mean(np.mean(E_point,0),0)
E_point_mean_mask = np.ma.masked_where(vmask == 0, E_point_mean)
cube_space_mean = iris.cube.Cube(E_point_mean_mask,long_name='Oceanic Meridional Energy Transport',
                                 var_name='OMET',units='PW',aux_coords_and_dims=[(latitude_cube,(0,1)),(longitude_cube,(0,1))])
projection = ccrs.NorthPolarStereo()
cube_space_mean_regrid, extent = iris.analysis.cartography.project(cube_space_mean, projection, nx=360, ny=180)
E_point_mean_regrid = cube_space_mean_regrid.data
y_coord = cube_space_mean_regrid.coord('projection_y_coordinate').points
x_coord = cube_space_mean_regrid.coord('projection_x_coordinate').points

print cube_space_mean_regrid
# support NetCDF
iris.FUTURE.netcdf_promote = True
fig6 =plt.figure()
fig6.suptitle('Oceanic Meridional Energy Transport in 1993 (GLORYS2V3)')
# Set up axes and title
ax = plt.subplot(projection=ccrs.PlateCarree())
#ax = plt.axes(projection=ccrs.NorthPolarStereo())
# Set limits
#ax.set_global()
ax.set_extent([-180,180,30,90],crs=ccrs.PlateCarree())
# Draw coastlines
ax.coastlines(linewidth=0.25)
# set gridlines and ticks
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,linewidth=1,
                 color='gray', alpha=0.5,linestyle='--')
gl.xlabels_top = False
gl.xlabel_style = {'size': 11, 'color': 'gray'}
#gl.xlines = False
#gl.set_xticks()
#gl.set_yticks()
gl.xformatter = LONGITUDE_FORMATTER
gl.ylabel_style = {'size': 11, 'color': 'gray'}
#ax.ylabels_left = False
gl.yformatter = LATITUDE_FORMATTER
# plot with Iris quickplot pcolormesh
cs = iplt.pcolormesh(cube_space_mean_regrid/1000,cmap='coolwarm',vmin=-0.7,vmax=0.7)
cbar = fig2.colorbar(cs,extend='both',orientation='horizontal',shrink =1.0)
cbar.set_label('PW (1E+15W)')
iplt.show()
fig6.savefig(output_path + os.sep + 'Map_OMET_GLORYS2V3_mean.jpg',dpi = 500)

# fig17 =plt.figure()
# # setup north polar stereographic basemap
# # resolution c(crude) l(low) i(intermidiate) h(high) f(full)
# # lon_0 is at 6 o'clock
# m = Basemap(projection='npstere',boundinglat=30,round=True,lon_0=0,resolution='l')
# # draw coastlines
# m.drawcoastlines()
# # fill continents, set lake color same as ocean color.
# # m.fillcontinents(color='coral',lake_color='aqua')
# # draw parallels and meridians
# # location labels=[left,right,top,bottom]
# m.drawparallels(np.arange(30,91,30),fontsize = 7)
# m.drawmeridians(np.arange(0,360,30),labels=[1,1,1,1],fontsize = 7)
# # x,y coordinate - lon, lat
# xx, yy = np.meshgrid(x_coord,y_coord[90:])
# XX, YY = m(xx, yy)
# # define color range for the contourf
# color = np.linspace(-1,1,11)
# # !!!!!take care about the coordinate of contourf(Longitude, Latitude, data(Lat,Lon))
# cs = m.contourf(XX,YY,E_point_mean_regrid[90:,:]/1000,color,cmap='coolwarm')
# # add color bar
# cbar = m.colorbar(cs,location="bottom",size='4%',pad="8%",format='%.1f')
# cbar.ax.tick_params(labelsize=8)
# cbar.set_label('Peta Watt',fontsize = 8)
# plt.title('Mean Meridional Energy Transport (1979-2014)',fontsize = 9, y=1.05)
# plt.show()
# fig17.savefig(output_path + os.sep + "Map_OMET_ORAS4_mean.jpeg",dpi=500)
#
# # spacial distribution of AMET - trend of the anomaly of 36 years
# # calculate trend
# # create an array to store the slope coefficient and residual
# a = np.zeros((jj,ji),dtype = float)
# b = np.zeros((jj,ji),dtype = float)
# # the least square fit equation is y = ax + b
# # np.lstsq solves the equation ax=b, a & b are the input
# # thus the input file should be reformed for the function
# # we can rewrite the line y = Ap, with A = [x,1] and p = [[a],[b]]
# A = np.vstack([index,np.ones(len(index))]).T
# # start the least square fitting
# for i in np.arange(jj):
#     for j in np.arange(ji):
#         # return value: coefficient matrix a and b, where a is the slope
#         a[i,j], b[i,j] = np.linalg.lstsq(A,series_E_point_white[:,i,j]/1000)[0]
#
# E_point_trend_mask = np.ma.masked_where(vmask == 0, a)
# cube_trend = iris.cube.Cube(E_point_trend_mask,long_name='Trend of Oceanic Meridional Energy Transport Anomaly',
#                             var_name='OMET',units='PW',aux_coords_and_dims=[(latitude_cube,(0,1)),(longitude_cube,(0,1))])
# projection = ccrs.NorthPolarStereo()
# cube_trend_regrid, extent = iris.analysis.cartography.project(cube_trend, projection, nx=360, ny=180)
# a_trend_regrid = cube_trend_regrid.data
# #y_coord = cube_space_mean_regrid.coord('projection_y_coordinate').points
# #x_coord = cube_space_mean_regrid.coord('projection_x_coordinate').points
#
# fig18 = plt.figure()
# # setup north polar stereographic basemap
# # resolution c(crude) l(low) i(intermidiate) h(high) f(full)
# # lon_0 is at 6 o'clock
# m = Basemap(projection='npstere',boundinglat=30,round=True,lon_0=0,resolution='l')
# # draw coastlines
# m.drawcoastlines()
# # fill continents, set lake color same as ocean color.
# # m.fillcontinents(color='coral',lake_color='aqua')
# # draw parallels and meridians
# # location labels=[left,right,top,bottom]
# m.drawparallels(np.arange(30,91,30),fontsize = 7)
# m.drawmeridians(np.arange(0,360,30),labels=[1,1,1,1],fontsize = 7)
# # x,y coordinate - lon, lat
# xx, yy = np.meshgrid(x_coord,y_coord[90:])
# XX, YY = m(xx, yy)
# # define color range for the contourf
# color = np.linspace(-0.1,0.1,11)
# # !!!!!take care about the coordinate of contourf(Longitude, Latitude, data(Lat,Lon))
# cs = m.contourf(XX,YY,a_trend_regrid[90:,:]*12*10,color,cmap='coolwarm')
# # add color bar
# cbar = m.colorbar(cs,location="bottom",size='4%',pad="8%",format='%.2f')
# cbar.ax.tick_params(labelsize=8)
# cbar.set_label('PW/decade',fontsize = 8)
# plt.title('Trend of OMET anomaly (1979-2014)',fontsize = 9, y=1.05)
# plt.show()
# fig18.savefig(output_path + os.sep + "Map_OMET_ORAS4_anomaly_trend.jpeg",dpi=500)

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
