#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : Land-sea mask for different oceans and seas on ORCA1, ORCA025 and MOM5 grid
Author          : Yang Liu
Date            : 2018.02.09
Last Update     : 2018.02.11
Description     : The code aims to plot land sea mask for all the oceans and seas
                  on original ORCA1, ORCA025 and MOM5 grid. This info is very useful
                  for the study on compensation for over certain areas between ocean
                  and atmosphere.
Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, sys, matplotlib, logging
variables       : Scaler and Vector coordinate of Arakawa C Grid
                  T and C Cell coordinate of MOM 5 Grid
                  Zonal Grid Spacing Scale Factors          e1
                  Meridional Grid Spacing Scale Factors     e2
                  Land-Sea Mask                             mask
Caveat!!        : MOM5 Grid
                  Direction of Axis: from south to north, west to east
                  Model Level: MOM5 Arakawa-B grid
                  Dimension:
                  Latitude      1070
                  Longitude     1440
                  Depth         50

                  ORCA1 Grid
                  Direction of Axis: from south to north, west to east
                  Model Level: MOM5 Arakawa-C grid
                  Dimension:
                  Latitude      362
                  Longitude     292
                  Depth         42

                  ORCA025 Grid
                  Direction of Axis: from south to north, west to east
                  Model Level: MOM5 Arakawa-C grid
                  Dimension:
                  Latitude      1021
                  Longitude     1440
                  Depth         75

                  The mask might have filled value of 1E+20 (in order to maintain
                  the size of the netCDF file and make full use of the storage). When
                  take the mean of intergral, this could result in abnormal large results.
                  With an aim to avoid this problem, it is important to re-set the filled
                  value to be 0 and then take the array with filled value during calculation.
                  (use "masked_array.filled()")
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
# package for plot
import matplotlib
# generate images without having a window appear
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.path as mpath
from mpl_toolkits.basemap import Basemap, cm
import cartopy
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
# calculate the time for the code execution
start_time = tttt.time()

################################   Input zone  ######################################
mask_ORAS4 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ORAS4'
mask_GLORYS2V3 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/GLORYS2V3'
mask_SODA3 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/SODA3'
# specify output path
output_path = '/home/yang/NLeSC/Computation_Modeling/BlueAction/Oceanography/mask_sea_ocean'
####################################################################################
print '*******************************************************************'
print '*********************** extract variables *************************'
print '*******************************************************************'
# land-sea mask
mesh_mask_ORAS4 = Dataset(mask_ORAS4 + os.sep + 'mesh_mask.nc')
mesh_mask_GLORYS2V3 = Dataset(mask_GLORYS2V3 + os.sep + 'G2V3_mesh_mask_myocean.nc')
mesh_mask_SODA3 = Dataset(mask_SODA3 + os.sep + 'topog.nc')
# individual sea/ocean mask
ocean_mask_ORAS4 = Dataset(mask_ORAS4 + os.sep + 'basinmask_050308_UKMO.nc')
ocean_mask_GLORYS2V3 = Dataset(mask_GLORYS2V3 + os.sep + 'new_maskglo.nc')

# lat and lon of T grid
lat_ORAS4 =  mesh_mask_ORAS4.variables['nav_lat'][:]
lat_GLORYS2V3 =  mesh_mask_GLORYS2V3.variables['nav_lat'][:]
lat_SODA3 =  mesh_mask_SODA3.variables['y_T'][:]

lon_ORAS4 =  mesh_mask_ORAS4.variables['nav_lon'][:]
lon_GLORYS2V3 =  mesh_mask_GLORYS2V3.variables['nav_lon'][:]
lon_SODA3 =  mesh_mask_SODA3.variables['x_T'][:]
# Caveat!! The original range of longitude is -280 - +80
# change it to the range -180 - +180
# the new value is only useful for determination of ocean/sea mask
# DO NOT USE IT FOR PLOT
aux_lon_SODA3 = lon_SODA3
aux_lon_SODA3[aux_lon_SODA3<-180] = aux_lon_SODA3[aux_lon_SODA3<-180] + 360

# tmask
tmask_ORAS4 = mesh_mask_ORAS4.variables['tmask'][0,0,:,:]
tmask_GLORYS2V3 = mesh_mask_GLORYS2V3.variables['tmask'][0,0,:,:]
tmask_SODA3 = mesh_mask_SODA3.variables['wet'][:]
# sea/ocean mask
# Atlantic
tmaskatl_ORAS4 = ocean_mask_ORAS4.variables['tmaskatl'][:]
tmaskatl_GLORYS2V3 = ocean_mask_GLORYS2V3.variables['tmaskatl'][:,1:-1] # attention that the size is different!

print '*******************************************************************'
print '************************** maps factory ***************************'
print '*******************************************************************'
print 'The visualization of AMET and OMET are complete with Iris and Cartopy.'

# support NetCDF
iris.FUTURE.netcdf_promote = True

print '*******************************************************************'
print '**************************** Atlantic *****************************'
print '*******************************************************************'

# here we apply nearest neighbour interpolation
print '========================  ORAS4  ========================'
# define the cube for the use of iris package
latitude_ORAS4 = iris.coords.AuxCoord(lat_ORAS4,standard_name='latitude',units='degrees')
longitude_ORAS4 = iris.coords.AuxCoord(lon_ORAS4,standard_name='longitude',units='degrees')
cube_ORAS4_atlantic = iris.cube.Cube(tmaskatl_ORAS4,long_name='Atlantic land sea mask', var_name='mask',
                            units='1',aux_coords_and_dims=[(latitude_ORAS4,(0,1)),(longitude_ORAS4,(0,1))])
#print cube_ORAS4
# Transform cube to target projection
cube_ORAS4_atlantic_regrid, extent = iris.analysis.cartography.project(cube_ORAS4_atlantic, ccrs.PlateCarree(), nx=720, ny=360)
# interpolation complete!!
print cube_ORAS4_atlantic_regrid

# plot
fig1 = plt.figure(figsize=(12,6))
fig1.suptitle('Atlantic land sea mask of ORCA1',fontsize = 12,y=0.93)

# Set up axes
ax = plt.axes(projection=ccrs.PlateCarree())

# Set limits
ax.set_global()
#ax.set_extent([-180,180,90,90],ccrs.PlateCarree()) # East, West, South, Nouth

# adjust map by data coverage (function from matplotlib)
# could make the map an ellipse
#ax.set_aspect('auto')
ax.set_aspect('1')

# Draw coastlines
ax.coastlines()

# set gridlines and ticks
# options of crs and draw_labels only work for PlateCarree() and Mercator()
gl = ax.gridlines(draw_labels=True, linewidth=1, color='gray', alpha=0.5,linestyle='--')
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
#cs = iplt.pcolormesh(cube_ORAS4_atlantic_regrid,cmap='coolwarm',vmin=0,vmax=1)
cs = iplt.pcolormesh(cube_ORAS4_atlantic_regrid,cmap='RdYlBu',vmin=0,vmax=1)
cbar = fig1.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.05)
cbar.set_label('sea-land')

# show and save plot
iplt.show()
fig1.savefig(output_path + os.sep + 'atlantic_mask_ORAS4.jpg',dpi = 500)

print '========================  GLORYS2V3  ========================'
# define the cube for the use of iris package
latitude_GLORYS2V3 = iris.coords.AuxCoord(lat_GLORYS2V3,standard_name='latitude',units='degrees')
longitude_GLORYS2V3 = iris.coords.AuxCoord(lon_GLORYS2V3,standard_name='longitude',units='degrees')
cube_GLORYS2V3_atlantic = iris.cube.Cube(tmaskatl_GLORYS2V3,long_name='Atlantic land sea mask', var_name='mask',
                            units='1',aux_coords_and_dims=[(latitude_GLORYS2V3,(0,1)),(longitude_GLORYS2V3,(0,1))])
#print cube_ORAS4
# Transform cube to target projection
cube_GLORYS2V3_atlantic_regrid, extent = iris.analysis.cartography.project(cube_GLORYS2V3_atlantic, ccrs.PlateCarree(), nx=1440, ny=900)
# interpolation complete!!
print cube_GLORYS2V3_atlantic_regrid

# plot
fig2 = plt.figure(figsize=(12,6))
fig2.suptitle('Atlantic land sea mask of ORCA025',fontsize = 12,y=0.93)

# Set up axes
ax = plt.axes(projection=ccrs.PlateCarree())

# Set limits
ax.set_global()
#ax.set_extent([-180,180,90,90],ccrs.PlateCarree()) # East, West, South, Nouth

# adjust map by data coverage (function from matplotlib)
# could make the map an ellipse
#ax.set_aspect('auto')
ax.set_aspect('1')

# Draw coastlines
ax.coastlines()

# set gridlines and ticks
# options of crs and draw_labels only work for PlateCarree() and Mercator()
gl = ax.gridlines(draw_labels=True, linewidth=1, color='gray', alpha=0.5,linestyle='--')
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
#cs = iplt.pcolormesh(cube_GLORYS2V3_atlantic_regrid,cmap='coolwarm',vmin=0,vmax=1)
cs = iplt.pcolormesh(cube_GLORYS2V3_atlantic_regrid,cmap='RdYlBu',vmin=0,vmax=1)
cbar = fig2.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.05)
cbar.set_label('sea-land')

# show and save plot
iplt.show()
fig2.savefig(output_path + os.sep + 'atlantic_mask_GLORYS2V3.jpg',dpi = 500)

print '========================  SODA3  ========================'
# calculate the atlantic land sea mask
tmaskatl_SODA3 = tmask_SODA3
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

# define the cube for the use of iris package
latitude_SODA3 = iris.coords.AuxCoord(lat_SODA3,standard_name='latitude',units='degrees')
longitude_SODA3 = iris.coords.AuxCoord(lon_SODA3,standard_name='longitude',units='degrees')
cube_SODA3_atlantic = iris.cube.Cube(tmaskatl_SODA3,long_name='Atlantic land sea mask', var_name='mask',
                            units='1',aux_coords_and_dims=[(latitude_SODA3,(0,1)),(longitude_SODA3,(0,1))])
#print cube_ORAS4
# Transform cube to target projection
cube_SODA3_atlantic_regrid, extent = iris.analysis.cartography.project(cube_SODA3_atlantic, ccrs.PlateCarree(), nx=1440, ny=900)
# interpolation complete!!
print cube_SODA3_atlantic_regrid

# plot
fig3 = plt.figure(figsize=(12,6))
fig3.suptitle('Atlantic land sea mask of MOM5',fontsize = 12,y=0.93)

# Set up axes
ax = plt.axes(projection=ccrs.PlateCarree())

# Set limits
ax.set_global()
#ax.set_extent([-180,180,90,90],ccrs.PlateCarree()) # East, West, South, Nouth

# adjust map by data coverage (function from matplotlib)
# could make the map an ellipse
#ax.set_aspect('auto')
ax.set_aspect('1')

# Draw coastlines
ax.coastlines()

# set gridlines and ticks
# options of crs and draw_labels only work for PlateCarree() and Mercator()
gl = ax.gridlines(draw_labels=True, linewidth=1, color='gray', alpha=0.5,linestyle='--')
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
#cs = iplt.pcolormesh(cube_GLORYS2V3_atlantic_regrid,cmap='coolwarm',vmin=0,vmax=1)
cs = iplt.pcolormesh(cube_SODA3_atlantic_regrid,cmap='RdYlBu',vmin=0,vmax=1)
cbar = fig3.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.05)
cbar.set_label('sea-land')

# show and save plot
iplt.show()
fig3.savefig(output_path + os.sep + 'atlantic_mask_SODA3.jpg',dpi = 500)

print '*******************************************************************'
print '***************************** Globe *******************************'
print '*******************************************************************'
# here we apply nearest neighbour interpolation
print '========================  ORAS4  ========================'
# define the cube for the use of iris package
latitude_ORAS4 = iris.coords.AuxCoord(lat_ORAS4,standard_name='latitude',units='degrees')
longitude_ORAS4 = iris.coords.AuxCoord(lon_ORAS4,standard_name='longitude',units='degrees')
cube_ORAS4_globe = iris.cube.Cube(tmask_ORAS4,long_name='Global land sea mask', var_name='mask',
                                  units='1',aux_coords_and_dims=[(latitude_ORAS4,(0,1)),(longitude_ORAS4,(0,1))])
#print cube_ORAS4
# Transform cube to target projection
cube_ORAS4_globe_regrid, extent = iris.analysis.cartography.project(cube_ORAS4_globe, ccrs.PlateCarree(), nx=720, ny=360)
# interpolation complete!!
print cube_ORAS4_globe_regrid

# plot
fig97 = plt.figure(figsize=(12,6))
fig97.suptitle('Global land sea mask of ORCA1',fontsize = 12,y=0.93)

# Set up axes
ax = plt.axes(projection=ccrs.PlateCarree())

# Set limits
ax.set_global()
#ax.set_extent([-180,180,90,90],ccrs.PlateCarree()) # East, West, South, Nouth

# adjust map by data coverage (function from matplotlib)
# could make the map an ellipse
#ax.set_aspect('auto')
ax.set_aspect('1')

# Draw coastlines
ax.coastlines()

# set gridlines and ticks
# options of crs and draw_labels only work for PlateCarree() and Mercator()
gl = ax.gridlines(draw_labels=True, linewidth=1, color='gray', alpha=0.5,linestyle='--')
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
#cs = iplt.pcolormesh(cube_ORAS4_globe_regrid,cmap='coolwarm',vmin=0,vmax=1)
cs = iplt.pcolormesh(cube_ORAS4_globe_regrid,cmap='RdYlBu',vmin=0,vmax=1)
cbar = fig97.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.05)
cbar.set_label('sea-land')

# show and save plot
iplt.show()
fig97.savefig(output_path + os.sep + 'globe_mask_ORAS4.jpg',dpi = 500)

print '========================  GLORYS2V3  ========================'
# define the cube for the use of iris package
latitude_GLORYS2V3 = iris.coords.AuxCoord(lat_GLORYS2V3,standard_name='latitude',units='degrees')
longitude_GLORYS2V3 = iris.coords.AuxCoord(lon_GLORYS2V3,standard_name='longitude',units='degrees')
cube_GLORYS2V3_globe = iris.cube.Cube(tmask_GLORYS2V3,long_name='Global land sea mask', var_name='mask',
                            units='1',aux_coords_and_dims=[(latitude_GLORYS2V3,(0,1)),(longitude_GLORYS2V3,(0,1))])
#print cube_ORAS4
# Transform cube to target projection
cube_GLORYS2V3_globe_regrid, extent = iris.analysis.cartography.project(cube_GLORYS2V3_globe, ccrs.PlateCarree(), nx=1440, ny=900)
# interpolation complete!!
print cube_GLORYS2V3_globe_regrid

# plot
fig98 = plt.figure(figsize=(12,6))
fig98.suptitle('Global land sea mask of ORCA025',fontsize = 12,y=0.93)

# Set up axes
ax = plt.axes(projection=ccrs.PlateCarree())

# Set limits
ax.set_global()
#ax.set_extent([-180,180,90,90],ccrs.PlateCarree()) # East, West, South, Nouth

# adjust map by data coverage (function from matplotlib)
# could make the map an ellipse
#ax.set_aspect('auto')
ax.set_aspect('1')

# Draw coastlines
ax.coastlines()

# set gridlines and ticks
# options of crs and draw_labels only work for PlateCarree() and Mercator()
gl = ax.gridlines(draw_labels=True, linewidth=1, color='gray', alpha=0.5,linestyle='--')
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
#cs = iplt.pcolormesh(cube_GLORYS2V3_globe_regrid,cmap='coolwarm',vmin=0,vmax=1)
cs = iplt.pcolormesh(cube_GLORYS2V3_globe_regrid,cmap='RdYlBu',vmin=0,vmax=1)
cbar = fig98.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.05)
cbar.set_label('sea-land')

# show and save plot
iplt.show()
fig98.savefig(output_path + os.sep + 'globe_mask_GLORYS2V3.jpg',dpi = 500)

print '========================  SODA3  ========================'
# define the cube for the use of iris package
latitude_SODA3 = iris.coords.AuxCoord(lat_SODA3,standard_name='latitude',units='degrees')
longitude_SODA3 = iris.coords.AuxCoord(lon_SODA3,standard_name='longitude',units='degrees')
cube_SODA3_globe = iris.cube.Cube(tmask_SODA3,long_name='Global land sea mask', var_name='mask',
                            units='1',aux_coords_and_dims=[(latitude_SODA3,(0,1)),(longitude_SODA3,(0,1))])
#print cube_ORAS4
# Transform cube to target projection
cube_SODA3_globe_regrid, extent = iris.analysis.cartography.project(cube_SODA3_globe, ccrs.PlateCarree(), nx=1440, ny=900)
# interpolation complete!!
print cube_SODA3_globe_regrid

# plot
fig99 = plt.figure(figsize=(12,6))
fig99.suptitle('Global land sea mask of MOM5',fontsize = 12,y=0.93)

# Set up axes
ax = plt.axes(projection=ccrs.PlateCarree())

# Set limits
ax.set_global()
#ax.set_extent([-180,180,90,90],ccrs.PlateCarree()) # East, West, South, Nouth

# adjust map by data coverage (function from matplotlib)
# could make the map an ellipse
#ax.set_aspect('auto')
ax.set_aspect('1')

# Draw coastlines
ax.coastlines()

# set gridlines and ticks
# options of crs and draw_labels only work for PlateCarree() and Mercator()
gl = ax.gridlines(draw_labels=True, linewidth=1, color='gray', alpha=0.5,linestyle='--')
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
#cs = iplt.pcolormesh(cube_GLORYS2V3_globe_regrid,cmap='coolwarm',vmin=0,vmax=1)
cs = iplt.pcolormesh(cube_SODA3_globe_regrid,cmap='RdYlBu',vmin=0,vmax=1)
cbar = fig99.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.05)
cbar.set_label('sea-land')

# show and save plot
iplt.show()
fig99.savefig(output_path + os.sep + 'globe_mask_SODA3.jpg',dpi = 500)

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
