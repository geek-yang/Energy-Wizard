#!/usr/bin/env python
"""
Copyright Netherlands eScience Center

Function        : Visualization of AMET and OMET from reanalysis datasets
Author          : Yang Liu
Date            : 2017.11.28
Last Update     : 2018.03.12
Description     : The code aims to project the atmospheric/oceanic meridional energy
                  transport on the map.
Return Value    : PNGs
Dependencies    : os, time, numpy, netCDF4, sys, matplotlib, logging, iris, cartopy
variables       : AMET               Tera Watt
                  OMET               Tera Watt
                  Land-Sea Mask      mask
Caveat!!        : Spatial and temporal coverage
                  Atmosphere
                  ERA-Interim 1979 - 2016
                  MERRA2      1980 - 2016
                  JRA55       1979 - 2015
                  Ocean
                  GLORYS2V3   1993 - 2014
                  ORAS4       1958 - 2014
                  SODA3       1980 - 2015

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
import matplotlib.ticker as mticker
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
# specify data path
datapath_ERAI = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ERAI/postprocessing'
datapath_MERRA2 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/MERRA2/postprocessing'
datapath_JRA55 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/JRA55/postprocessing'

datapath_ORAS4 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ORAS4/postprocessing'
datapath_GLORYS2V3 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/GLORYS2V3/postprocessing'
datapath_SODA3 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/SODA3/postprocessing'

maskpath_ORAS4 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ORAS4'
maskpath_GLORYS2V3 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/GLORYS2V3'
maskpath_SODA3 = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/SODA3'
# specify output path
output_path = '/home/yang/NLeSC/Computation_Modeling/BlueAction/Visualization'
####################################################################################
print '*******************************************************************'
print '*********************** extract variables *************************'
print '*******************************************************************'
# data
dataset_ERAI = Dataset(datapath_ERAI + os.sep + 'model_daily_075_1979_2016_E_point.nc')
dataset_MERRA2 = Dataset(datapath_MERRA2 + os.sep + 'AMET_MERRA2_model_daily_1980_2016_E_point.nc')
dataset_JRA55 = Dataset(datapath_JRA55 + os.sep + 'AMET_JRA55_model_daily_1979_2015_E_point.nc')

dataset_ORAS4 = Dataset(datapath_ORAS4 + os.sep + 'oras4_model_monthly_orca1_E_point.nc')
dataset_GLORYS2V3 = Dataset(datapath_GLORYS2V3 + os.sep + 'GLORYS2V3_model_monthly_orca025_E_point.nc')
dataset_SODA3 = Dataset(datapath_SODA3 + os.sep + 'OMET_SODA3_model_5daily_1980_2015_E_point.nc')
# mesh and mask
mesh_mask_ORAS4 = Dataset(maskpath_ORAS4 + os.sep + 'mesh_mask.nc')
mesh_mask_GLORYS2V3 = Dataset(maskpath_GLORYS2V3 + os.sep + 'G2V3_mesh_mask_myocean.nc')
mesh_mask_SODA3 = Dataset(maskpath_SODA3 + os.sep + 'topog.nc')
# from 20N - 90N
AMET_ERAI = dataset_ERAI.variables['E'][:]/1000
AMET_MERRA2 = dataset_MERRA2.variables['E'][:]/1000
AMET_JRA55 = dataset_JRA55.variables['E'][:,:,0:125,:]/1000

OMET_ORAS4 = dataset_ORAS4.variables['E'][21:,:,180:,:]/1000 # start from 1979
OMET_GLORYS2V3 = dataset_GLORYS2V3.variables['E'][:,:,579:,:]/1000 # start from 1993
OMET_SODA3 = dataset_SODA3.variables['E'][:,:,569:,:]/1000 # start from 1993
#mask (surface mask only)
vmask_ORAS4 = mesh_mask_ORAS4.variables['vmask'][0,0,180:,:] # from 20N
vmask_GLORYS2V3 = mesh_mask_GLORYS2V3.variables['vmask'][0,0,579:,:] # from 20N
vmask_SODA3 = mesh_mask_SODA3.variables['wet_c'][569:,:] # from 20N
# year
year_ERAI = dataset_ERAI.variables['year'][:]             # from 1979 to 2016
year_MERRA2 = dataset_MERRA2.variables['year'][:]         # from 1980 to 2016
year_JRA55 = dataset_JRA55.variables['year'][:]           # from 1979 to 2015

year_ORAS4 = dataset_ORAS4.variables['year'][21:]         # from 1958 to 2014
year_GLORYS2V3 = dataset_GLORYS2V3.variables['year'][:]   # from 1993 to 2014
year_SODA3 = dataset_SODA3.variables['year'][:]           # from 1980 to 2015
#latitude
latitude_ERAI = dataset_ERAI.variables['latitude'][:]
latitude_MERRA2 = dataset_MERRA2.variables['latitude'][:]
latitude_JRA55 = dataset_JRA55.variables['latitude'][0:125]

latitude_ORAS4 = dataset_ORAS4.variables['latitude'][180:,:]
latitude_GLORYS2V3 = dataset_GLORYS2V3.variables['latitude'][579:,:]
latitude_SODA3 = dataset_SODA3.variables['latitude'][569:,:]
#longitude
longitude_ERAI = dataset_ERAI.variables['longitude'][:]
longitude_MERRA2 = dataset_MERRA2.variables['longitude'][:]
longitude_JRA55 = dataset_JRA55.variables['longitude'][:]

longitude_ORAS4 = dataset_ORAS4.variables['longitude'][180:,:]
longitude_GLORYS2V3 = dataset_GLORYS2V3.variables['longitude'][579:,:]
longitude_SODA3 = dataset_SODA3.variables['longitude'][569:,:]
print '*******************************************************************'
print '************************** maps factory ***************************'
print '*******************************************************************'
print 'The visualization of AMET and OMET are complete with Iris and Cartopy.'

# support NetCDF
iris.FUTURE.netcdf_promote = True

print '========================  ERA-Interim  ========================'

# ERA-Interim only
print 'NorthPolarStereo!'
# create cube for plot in an elegant way
latitude_AMET_ERAI = iris.coords.DimCoord(latitude_ERAI,standard_name='latitude',long_name='latitude',
                             var_name='lat',units='degrees')
longitude_AMET_ERAI = iris.coords.DimCoord(longitude_ERAI,standard_name='longitude',long_name='longitude',
                             var_name='lon',units='degrees')
cube_ERAI = iris.cube.Cube(AMET_ERAI[0,0,:,:],long_name='Atmospheric Meridional Energy Transport',
                           var_name='AMET',units='PW',dim_coords_and_dims=[(latitude_AMET_ERAI, 0), (longitude_AMET_ERAI, 1)])
# sample plot
# figsize works for the size of the map, not the entire figure
fig1 = plt.figure(figsize=(4,3.6))

# suptitle is the title for the figure
fig1.suptitle('Atmospheric Meridional Energy Transport in 1979 (year) 1 (month)',fontsize = 7,y=0.93)

# this works for the entire size of the figure
#fig1.set_size_inches(5, 5)

# Set up axes, which means different view of maps
#ax = plt.axes(projection=ccrs.PlateCarree())
#ax = plt.axes(projection=ccrs.Mercator(central_longitude=0, min_latitude=30, max_latitude=90))
ax = plt.axes(projection=ccrs.NorthPolarStereo())

# background image in cartopy(map style)
#ax.background_img(name='pop', resolution='high')
#ax.background_img(name='BM', resolution='low')

# Set limits of the map (choose area for plot)
#ax.set_global()
ax.set_extent([-180,180,20,90],ccrs.PlateCarree()) # East, West, South, Nouth

# adjust map by data coverage (function from matplotlib)
# could make the map an ellipse
#ax.set_aspect('auto')
ax.set_aspect('1')

# set ticks (overlap with gridlines)
#ax.set_xticks([-180, 120, 60, 0, 60, 120, 180], crs=ccrs.PlateCarree())
#ax.set_yticks([30, 60], crs=ccrs.PlateCarree())

# Draw coastlines
ax.coastlines()

# map features
#ax.add_feature(cartopy.feature.LAND)
#ax.add_feature(cartopy.feature.OCEAN)
#ax.add_feature(cartopy.feature.COASTLINE)
#ax.add_feature(cartopy.feature.BORDERS, linestyle=':')

# set gridlines and ticks
# options of crs and draw_labels only work for PlateCarree() and Mercator()
# for other axes, do not specify them
gl = ax.gridlines(linewidth=1, color='gray', alpha=0.5,linestyle='--')
# set gridline details, only work for PlateCarree() and Mercator()
# switch of label locations
#gl.xlabels_top = False
#gl.ylabels_left = False
# use of formatter (fixed)
#gl.xformatter = LONGITUDE_FORMATTER
#gl.yformatter = LATITUDE_FORMATTER
# specify label styles
#gl.xlabel_style = {'size': 8, 'color': 'gray'}
#gl.ylabel_style = {'size': 8, 'color': 'gray'}
# switch of lines
#gl.xlines = False
# specify the location of labels
#gl.ylocator = mticker.FixedLocator([30, 60])

# Compute a circle in axes coordinates, which we can use as a boundary
# for the map. We can pan/zoom as much as we like - the boundary will be
# permanently circular.
theta = np.linspace(0, 2*np.pi, 100)
center, radius = [0.5, 0.5], 0.5
verts = np.vstack([np.sin(theta), np.cos(theta)]).T
circle = mpath.Path(verts * radius + center)
ax.set_boundary(circle, transform=ax.transAxes)

# plot with Iris plot pcolormesh
# camp is the colormap, vmin and vmax determines the minimum and maximum of data plotting range
cs = iplt.pcolormesh(cube_ERAI,cmap='coolwarm',vmin=-1.2,vmax=1.2)
#cs = iplt.contour(cube_ERAI,cmap='coolwarm',vmin=-1.0,vmax=1.0)
#cs = iplt.contourf(cube_ERAI,cmap='coolwarm',vmin=-1.0,vmax=1.0)
# setup colorbar, shrink is the horizontal size, pad determines the space between the map
cbar = fig1.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.05,format="%.1f")
cbar.set_label('PW (1E+15W)',size = 6)
cbar.set_ticks([-1.2, -0.8, -0.4, 0, 0.4, 0.8, 1.2])
cbar.ax.tick_params(labelsize = 6)

# show and save plot
iplt.show()
fig1.savefig(output_path + os.sep + 'ERA-Interim' + os.sep + 'ERAI_NorthPolarStereo.jpg',dpi = 300)
plt.close(fig1)

print 'PlateCarree'

# figsize works for the size of the map, not the entire figure
fig2 = plt.figure(figsize=(4,2.7))

# suptitle is the title for the figure
fig2.suptitle('Atmospheric Meridional Energy Transport in 1979 (year) 1 (month)',fontsize = 7,y=0.93)

# this works for the entire size of the figure
#fig1.set_size_inches(5, 5)

# Set up axes, which means different view of maps
ax = plt.axes(projection=ccrs.PlateCarree())
#ax = plt.axes(projection=ccrs.Mercator(central_longitude=0, min_latitude=20, max_latitude=90))
#ax = plt.axes(projection=ccrs.NorthPolarStereo())

# background image in cartopy(map style)
#ax.background_img(name='pop', resolution='high')
#ax.background_img(name='BM', resolution='low')

# Set limits of the map (choose area for plot)
#ax.set_global()
ax.set_extent([-180,180,20,90],ccrs.PlateCarree()) # East, West, South, Nouth

# adjust map by data coverage (function from matplotlib)
# could make the map an ellipse
#ax.set_aspect('auto')
ax.set_aspect('2.5')

# set ticks (overlap with gridlines, better to switch off)
#ax.set_xticks([-180, -120, -60, 0, 60, 120, 180], crs=ccrs.PlateCarree())
#ax.set_yticks([30, 60, 90], crs=ccrs.PlateCarree())

# Draw coastlines
ax.coastlines()

# map features
#ax.add_feature(cartopy.feature.LAND)
#ax.add_feature(cartopy.feature.OCEAN)
#ax.add_feature(cartopy.feature.COASTLINE)
#ax.add_feature(cartopy.feature.BORDERS, linestyle=':')

# set gridlines and ticks
# options of crs and draw_labels only work for PlateCarree() and Mercator()
# for other axes, do not specify them
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,linewidth=1, color='gray', alpha=0.5,linestyle='--')
# set gridline details, only work for PlateCarree() and Mercator()
# !! Attention !! The configuration should follow the order below
# switch of label locations
gl.xlabels_top = False
#ax.ylabels_left = False
# switch of lines
#gl.xlines = False
#gl.ylines = False
# specify the location of labels
#gl.xlocator = mticker.FixedLocator([-180, -45, 0, 45, 180])
#gl.ylocator = mticker.FixedLocator([30, 60])
# use of formatter (fixed), only after this the style setup will work
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
# specify label styles
gl.xlabel_style = {'size': 6, 'color': 'gray'}
gl.ylabel_style = {'size': 6, 'color': 'gray'}

# plot with Iris plot pcolormesh
# camp is the colormap, vmin and vmax determines the minimum and maximum of data plotting range
cs = iplt.pcolormesh(cube_ERAI,cmap='coolwarm',vmin=-1.2,vmax=1.2)
#cs = iplt.contour(cube_ERAI,cmap='coolwarm',vmin=-1.0,vmax=1.0)
#cs = iplt.contourf(cube_ERAI,cmap='coolwarm',vmin=-1.0,vmax=1.0)
# setup colorbar, shrink is the horizontal size, pad determines the space between the map
cbar = fig2.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.1,format="%.1f")
cbar.set_ticks([-1.2, -0.8, -0.4, 0, 0.4, 0.8, 1.2])
cbar.ax.tick_params(labelsize = 6)
cbar.set_label('PW (1E+15W)',size = 6)

# show and save plot
iplt.show()
fig2.savefig(output_path + os.sep + 'ERA-Interim' + os.sep + 'ERAI_PlateCarree.jpg',dpi = 300)
plt.close(fig2)

print '========================  MERRA2  ========================'
# MERRA2 only
print 'NorthPolarStereo!'
# create cube for plot in an elegant way
latitude_AMET_MERRA2 = iris.coords.DimCoord(latitude_MERRA2,standard_name='latitude',long_name='latitude',
                             var_name='lat',units='degrees')
longitude_AMET_MERRA2 = iris.coords.DimCoord(longitude_MERRA2,standard_name='longitude',long_name='longitude',
                             var_name='lon',units='degrees')
cube_MERRA2 = iris.cube.Cube(AMET_MERRA2[0,0,:,:],long_name='Atmospheric Meridional Energy Transport',
                           var_name='AMET',units='PW',dim_coords_and_dims=[(latitude_AMET_MERRA2, 0), (longitude_AMET_MERRA2, 1)])
# sample plot
# figsize works for the size of the map, not the entire figure
fig3 = plt.figure(figsize=(4,3.6))
fig3.suptitle('Atmospheric Meridional Energy Transport in 1980 (year) 1 (month)',fontsize = 7,y=0.93)
ax = plt.axes(projection=ccrs.NorthPolarStereo())
ax.set_extent([-180,180,20,90],ccrs.PlateCarree()) # East, West, South, Nouth
ax.set_aspect('1')
ax.coastlines()
gl = ax.gridlines(linewidth=1, color='gray', alpha=0.5,linestyle='--')

theta = np.linspace(0, 2*np.pi, 100)
center, radius = [0.5, 0.5], 0.5
verts = np.vstack([np.sin(theta), np.cos(theta)]).T
circle = mpath.Path(verts * radius + center)
ax.set_boundary(circle, transform=ax.transAxes)

cs = iplt.pcolormesh(cube_MERRA2,cmap='coolwarm',vmin=-1.2,vmax=1.2)
cbar = fig3.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.05,format="%.1f")
cbar.set_label('PW (1E+15W)',size = 6)
cbar.set_ticks([-1.2, -0.8, -0.4, 0, 0.4, 0.8, 1.2])
cbar.ax.tick_params(labelsize = 6)
# show and save plot
iplt.show()
fig3.savefig(output_path + os.sep + 'MERRA2' + os.sep + 'MERRA2_NorthPolarStereo.jpg',dpi = 300)
plt.close(fig3)

print 'PlateCarree'

# figsize works for the size of the map, not the entire figure
fig4 = plt.figure(figsize=(4,2.7))
fig4.suptitle('Atmospheric Meridional Energy Transport in 1980 (year) 1 (month)',fontsize = 7,y=0.93)
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([-180,180,20,90],ccrs.PlateCarree()) # East, West, South, Nouthpse
ax.set_aspect('2.5')
ax.coastlines()
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,linewidth=1, color='gray', alpha=0.5,linestyle='--')
gl.xlabels_top = False
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
gl.xlabel_style = {'size': 6, 'color': 'gray'}
gl.ylabel_style = {'size': 6, 'color': 'gray'}

cs = iplt.pcolormesh(cube_MERRA2,cmap='coolwarm',vmin=-1.2,vmax=1.2)
cbar = fig4.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.1,format="%.1f")
cbar.set_ticks([-1.2, -0.8, -0.4, 0, 0.4, 0.8, 1.2])
cbar.ax.tick_params(labelsize = 6)
cbar.set_label('PW (1E+15W)',size = 6)
# show and save plot
iplt.show()
fig4.savefig(output_path + os.sep + 'MERRA2' + os.sep + 'MERRA2_PlateCarree.jpg',dpi = 300)
plt.close(fig4)
print '========================  JRA55  ========================'
# JRA55 only
print 'NorthPolarStereo!'
# create cube for plot in an elegant way
latitude_AMET_JRA55 = iris.coords.DimCoord(latitude_JRA55,standard_name='latitude',long_name='latitude',
                             var_name='lat',units='degrees')
longitude_AMET_JRA55 = iris.coords.DimCoord(longitude_JRA55,standard_name='longitude',long_name='longitude',
                             var_name='lon',units='degrees')
cube_JRA55 = iris.cube.Cube(AMET_JRA55[0,0,:,:],long_name='Atmospheric Meridional Energy Transport',
                           var_name='AMET',units='PW',dim_coords_and_dims=[(latitude_AMET_JRA55, 0), (longitude_AMET_JRA55, 1)])
# sample plot
# figsize works for the size of the map, not the entire figure
fig5 = plt.figure(figsize=(4,3.6))
fig5.suptitle('Atmospheric Meridional Energy Transport in 1979 (year) 1 (month)',fontsize = 7,y=0.93)
ax = plt.axes(projection=ccrs.NorthPolarStereo())
ax.set_extent([-180,180,20,90],ccrs.PlateCarree()) # East, West, South, Nouth
ax.set_aspect('1')
ax.coastlines()
gl = ax.gridlines(linewidth=1, color='gray', alpha=0.5,linestyle='--')

theta = np.linspace(0, 2*np.pi, 100)
center, radius = [0.5, 0.5], 0.5
verts = np.vstack([np.sin(theta), np.cos(theta)]).T
circle = mpath.Path(verts * radius + center)
ax.set_boundary(circle, transform=ax.transAxes)

cs = iplt.pcolormesh(cube_JRA55,cmap='coolwarm',vmin=-1.2,vmax=1.2)
cbar = fig5.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.05,format="%.1f")
cbar.set_label('PW (1E+15W)',size = 6)
cbar.set_ticks([-1.2, -0.8, -0.4, 0, 0.4, 0.8, 1.2])
cbar.ax.tick_params(labelsize = 6)
# show and save plot
iplt.show()
fig5.savefig(output_path + os.sep + 'JRA55' + os.sep + 'JRA55_NorthPolarStereo.jpg',dpi = 300)
plt.close(fig5)

print 'PlateCarree'

# figsize works for the size of the map, not the entire figure
fig6 = plt.figure(figsize=(4,2.7))
fig6.suptitle('Atmospheric Meridional Energy Transport in 1979 (year) 1 (month)',fontsize = 7,y=0.93)
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([-180,180,20,90],ccrs.PlateCarree()) # East, West, South, Nouthpse
ax.set_aspect('2.5')
ax.coastlines()
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,linewidth=1, color='gray', alpha=0.5,linestyle='--')
gl.xlabels_top = False
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
gl.xlabel_style = {'size': 6, 'color': 'gray'}
gl.ylabel_style = {'size': 6, 'color': 'gray'}

cs = iplt.pcolormesh(cube_JRA55,cmap='coolwarm',vmin=-1.2,vmax=1.2)
cbar = fig6.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.1,format="%.1f")
cbar.set_ticks([-1.2, -0.8, -0.4, 0, 0.4, 0.8, 1.2])
cbar.ax.tick_params(labelsize = 6)
cbar.set_label('PW (1E+15W)',size = 6)
# show and save plot
iplt.show()
fig6.savefig(output_path + os.sep + 'JRA55' + os.sep + 'JRA55_PlateCarree.jpg',dpi = 300)
plt.close(fig6)

print '========================  ORAS4  ========================'
# ORAS4 only
# use Iris for interpolation/regridding
# create cube for plot in an elegant way

# mask the array
OMET_ORAS4_mask = np.ma.masked_where(vmask_ORAS4 == 0, OMET_ORAS4[0,0,:,:])

# choose interpolation method
method_int = 2 # ! 1 = bilinear interpolation ! 2 = nearest neghbour interpolation
if method_int == 1:
    # prepare the cube
    latitude_OMET_ORAS4 = iris.coords.AuxCoord(latitude_ORAS4,standard_name='latitude',units='degrees')
    longitude_OMET_ORAS4 = iris.coords.AuxCoord(longitude_ORAS4,standard_name='longitude',units='degrees')
    cube_ORAS4 = iris.cube.Cube(OMET_ORAS4_mask,long_name='Oceanic Meridional Energy Transport', var_name='OMET',units='PW',
                              aux_coords_and_dims=[(latitude_OMET_ORAS4,(0,1)),(longitude_OMET_ORAS4,(0,1))])
    # choose the coordinate system for Cube (for regrid module)
    coord_sys = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)
    # Feed cube with coordinate system
    cube_ORAS4.coord('latitude').coord_system = coord_sys
    cube_ORAS4.coord('longitude').coord_system = coord_sys
    #print cube_ORAS4
    # create grid_cube for regridding, this is a dummy cube with desired grid
    lat_grid = np.linspace(20, 90, 71)
    lon_grid = np.linspace(-180, 180, 361)
    # interpolate_points = [('latitude', np.linspace(-90, 90, 181)),
    #                       ('longitude', np.linspace(-180, 181, 361))]
    lat_aux = iris.coords.DimCoord(lat_grid, standard_name='latitude',
                                   units='degrees_north', coord_system='GeogCS')
    lon_aux = iris.coords.DimCoord(lon_grid, standard_name='longitude',
                                   units='degrees_east', coord_system='GeogCS')
    dummy_data = np.zeros((len(lat_grid), len(lon_grid)))
    aux_cube = iris.cube.Cube(dummy_data,dim_coords_and_dims=[(lat_aux, 0), (lon_aux, 1)])
    # Feed cube with coordinate system
    aux_cube.coord('latitude').guess_bounds()
    aux_cube.coord('longitude').guess_bounds()
    aux_cube.coord('latitude').coord_system = coord_sys
    aux_cube.coord('longitude').coord_system = coord_sys
    # create a weight matrix for regridding
    weights = np.ones(cube_ORAS4.shape)
    # interpolate from ORCA grid to rectilinear grid through bilinear interpolation
    # The method uses point in cell interpolation and then perform the bilinear interpolation
    # based on distance and weight
    cube_ORAS4_regrid = iris.experimental.regrid.regrid_weighted_curvilinear_to_rectilinear(cube_ORAS4,weights,aux_cube)
else:
    # define the cube for the use of iris package
    latitude_OMET_ORAS4 = iris.coords.AuxCoord(latitude_ORAS4,standard_name='latitude',units='degrees')
    longitude_OMET_ORAS4 = iris.coords.AuxCoord(longitude_ORAS4,standard_name='longitude',units='degrees')
    cube_ORAS4 = iris.cube.Cube(OMET_ORAS4_mask,long_name='Oceanic Meridional Energy Transport',
                            var_name='OMET',units='PW',aux_coords_and_dims=[(latitude_OMET_ORAS4,(0,1)),(longitude_OMET_ORAS4,(0,1))])
    #print cube_ORAS4
    # Transform cube to target projection
    cube_ORAS4_regrid, extent = iris.analysis.cartography.project(cube_ORAS4, ccrs.PlateCarree(), nx=720, ny=140)
    # interpolation complete!!
    print cube_ORAS4_regrid

# plot
fig7 = plt.figure(figsize=(4,3.6))
fig7.suptitle('Oceanic Meridional Energy Transport in 1979 (year) 1 (month)',fontsize = 7,y=0.93)

# Set up axes
ax = plt.axes(projection=ccrs.NorthPolarStereo())

# Set limits
#ax.set_global()
ax.set_extent([-180,180,20,90],ccrs.PlateCarree()) # East, West, South, Nouth

# adjust map by data coverage (function from matplotlib)
# could make the map an ellipse
#ax.set_aspect('auto')
ax.set_aspect('1')

# Draw coastlines
ax.coastlines()

# set gridlines and ticks
# options of crs and draw_labels only work for PlateCarree() and Mercator()
gl = ax.gridlines(linewidth=1, color='gray', alpha=0.5,linestyle='--')

# Compute a circle in axes coordinates, which we can use as a boundary
# for the map. We can pan/zoom as much as we like - the boundary will be
# permanently circular.
theta = np.linspace(0, 2*np.pi, 100)
center, radius = [0.5, 0.5], 0.5
verts = np.vstack([np.sin(theta), np.cos(theta)]).T
circle = mpath.Path(verts * radius + center)
ax.set_boundary(circle, transform=ax.transAxes)

# plot with Iris quickplot pcolormesh
cs = iplt.pcolormesh(cube_ORAS4_regrid,cmap='coolwarm',vmin=-0.2,vmax=0.2)
cbar = fig7.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.05,format="%.2f")
cbar.set_ticks([-0.2, -0.1, 0, 0.1, 0.2])
cbar.set_label('PW (1E+15W)',size = 6)
cbar.ax.tick_params(labelsize = 6)

# show and save plot
iplt.show()
fig7.savefig(output_path + os.sep + 'ORAS4' + os.sep + 'ORAS4_NorthPolarStereo.jpg',dpi = 300)
plt.close(fig7)

print 'PlateCarree'

# figsize works for the size of the map, not the entire figure
fig8 = plt.figure(figsize=(4,2.7))
fig8.suptitle('Oceanic Meridional Energy Transport in 1979 (year) 1 (month)',fontsize = 7,y=0.93)
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([-180,180,20,90],ccrs.PlateCarree()) # East, West, South, Nouthpse
ax.set_aspect('2.5')
ax.coastlines()
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,linewidth=1, color='gray', alpha=0.5,linestyle='--')
gl.xlabels_top = False
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
gl.xlabel_style = {'size': 6, 'color': 'gray'}
gl.ylabel_style = {'size': 6, 'color': 'gray'}

cs = iplt.pcolormesh(cube_ORAS4_regrid,cmap='coolwarm',vmin=-0.15,vmax=0.15)
cbar = fig8.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.1,format="%.2f")
cbar.set_ticks([-0.15, -0.10, -0.05, 0, 0.05, 0.10, 0.15])
cbar.ax.tick_params(labelsize = 6)
cbar.set_label('PW (1E+15W)',size = 6)
# show and save plot
iplt.show()
fig8.savefig(output_path + os.sep + 'ORAS4' + os.sep + 'ORAS4_PlateCarree.jpg',dpi = 300)
plt.close(fig8)

print '========================  GLORYS2v3  ========================'
# use Iris for interpolation/regridding
# create cube for plot in an elegant way

# mask the array
OMET_GLORYS2V3_mask = np.ma.masked_where(vmask_GLORYS2V3 == 0, OMET_GLORYS2V3[0,0,:,:])
np.ma.set_fill_value(OMET_GLORYS2V3_mask,0) # change the filled value to 0
# define the cube for the use of iris package
latitude_OMET_GLORYS2V3 = iris.coords.AuxCoord(latitude_GLORYS2V3,standard_name='latitude',units='degrees')
longitude_OMET_GLORYS2V3 = iris.coords.AuxCoord(longitude_GLORYS2V3,standard_name='longitude',units='degrees')
cube_GLORYS2V3 = iris.cube.Cube(OMET_GLORYS2V3_mask,long_name='Oceanic Meridional Energy Transport',
                                var_name='OMET',units='PW',aux_coords_and_dims=[(latitude_OMET_GLORYS2V3,(0,1)),(longitude_OMET_GLORYS2V3,(0,1))])
coord_sys = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)
cube_GLORYS2V3.coord('latitude').coord_system = coord_sys
cube_GLORYS2V3.coord('longitude').coord_system = coord_sys
# Transform cube to target projection
cube_GLORYS2V3_regrid, extent = iris.analysis.cartography.project(cube_GLORYS2V3, ccrs.PlateCarree(), nx=1440, ny=350)
# interpolation complete!!
print cube_GLORYS2V3_regrid

# plot
fig9 = plt.figure(figsize=(4,3.6))
fig9.suptitle('Oceanic Meridional Energy Transport in 1993 (year) 1 (month)',fontsize = 7,y=0.93)

# Set up axes
ax = plt.axes(projection=ccrs.NorthPolarStereo())

# Set limits
#ax.set_global()
ax.set_extent([-180,180,20,90],ccrs.PlateCarree()) # East, West, South, Nouth

# adjust map by data coverage (function from matplotlib)
# could make the map an ellipse
#ax.set_aspect('auto')
ax.set_aspect('1')

# Draw coastlines
ax.coastlines()

# set gridlines and ticks
# options of crs and draw_labels only work for PlateCarree() and Mercator()
gl = ax.gridlines(linewidth=1, color='gray', alpha=0.5,linestyle='--')

# Compute a circle in axes coordinates, which we can use as a boundary
# for the map. We can pan/zoom as much as we like - the boundary will be
# permanently circular.
theta = np.linspace(0, 2*np.pi, 100)
center, radius = [0.5, 0.5], 0.5
verts = np.vstack([np.sin(theta), np.cos(theta)]).T
circle = mpath.Path(verts * radius + center)
ax.set_boundary(circle, transform=ax.transAxes)

# plot with Iris quickplot pcolormesh
cs = iplt.pcolormesh(cube_GLORYS2V3_regrid,cmap='coolwarm',vmin=-0.2,vmax=0.2)
cbar = fig9.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.05,format="%.1f")
cbar.set_ticks([-0.2, -0.1, 0, 0.1, 0.2])
cbar.set_label('PW (1E+15W)',size = 6)
cbar.ax.tick_params(labelsize = 6)

# show and save plot
iplt.show()
fig9.savefig(output_path + os.sep + 'GLORYS2V3' + os.sep + 'OMET_GLORYS2V3.jpg',dpi = 300)
plt.close(fig9)

print 'PlateCarree'

# figsize works for the size of the map, not the entire figure
fig10 = plt.figure(figsize=(4,2.7))
fig10.suptitle('Oceanic Meridional Energy Transport in 1979 (year) 1 (month)',fontsize = 7,y=0.93)
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([-180,180,20,90],ccrs.PlateCarree()) # East, West, South, Nouthpse
ax.set_aspect('2.5')
ax.coastlines()
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,linewidth=1, color='gray', alpha=0.5,linestyle='--')
gl.xlabels_top = False
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
gl.xlabel_style = {'size': 6, 'color': 'gray'}
gl.ylabel_style = {'size': 6, 'color': 'gray'}

cs = iplt.pcolormesh(cube_GLORYS2V3_regrid,cmap='coolwarm',vmin=-0.15,vmax=0.15)
cbar = fig10.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.1,format="%.2f")
cbar.set_ticks([-0.15, -0.10, -0.05, 0, 0.05, 0.10, 0.15])
cbar.ax.tick_params(labelsize = 6)
cbar.set_label('PW (1E+15W)',size = 6)
# show and save plot
iplt.show()
fig10.savefig(output_path + os.sep + 'GLORYS2V3' + os.sep + 'GLORYS2V3_PlateCarree.jpg',dpi = 300)
plt.close(fig10)

print '========================  SODA3  ========================'

# use Iris for interpolation/regridding
# create cube for plot in an elegant way

# mask the array
OMET_SODA3_mask = np.ma.masked_where(vmask_SODA3 == 0, OMET_SODA3[0,0,:,:])
np.ma.set_fill_value(OMET_SODA3_mask,0) # change the filled value to 0
# define the cube for the use of iris package
latitude_OMET_SODA3 = iris.coords.AuxCoord(latitude_SODA3,standard_name='latitude',units='degrees')
longitude_OMET_SODA3 = iris.coords.AuxCoord(longitude_SODA3,standard_name='longitude',units='degrees')
cube_SODA3 = iris.cube.Cube(OMET_SODA3_mask,long_name='Oceanic Meridional Energy Transport',
                                var_name='OMET',units='PW',aux_coords_and_dims=[(latitude_OMET_SODA3,(0,1)),(longitude_OMET_SODA3,(0,1))])
coord_sys = iris.coord_systems.GeogCS(iris.fileformats.pp.EARTH_RADIUS)
cube_SODA3.coord('latitude').coord_system = coord_sys
cube_SODA3.coord('longitude').coord_system = coord_sys
# Transform cube to target projection
cube_SODA3_regrid, extent = iris.analysis.cartography.project(cube_SODA3, ccrs.PlateCarree(), nx=1440, ny=350)
# interpolation complete!!
print cube_SODA3_regrid

# plot
fig11 = plt.figure(figsize=(4,3.6))
fig11.suptitle('Oceanic Meridional Energy Transport in 1980 (year) 1 (month)',fontsize = 7,y=0.93)

# Set up axes
ax = plt.axes(projection=ccrs.NorthPolarStereo())

# Set limits
#ax.set_global()
ax.set_extent([-180,180,20,90],ccrs.PlateCarree()) # East, West, South, Nouth

# adjust map by data coverage (function from matplotlib)
# could make the map an ellipse
#ax.set_aspect('auto')
ax.set_aspect('1')

# Draw coastlines
ax.coastlines()

# set gridlines and ticks
# options of crs and draw_labels only work for PlateCarree() and Mercator()
gl = ax.gridlines(linewidth=1, color='gray', alpha=0.5,linestyle='--')

# Compute a circle in axes coordinates, which we can use as a boundary
# for the map. We can pan/zoom as much as we like - the boundary will be
# permanently circular.
theta = np.linspace(0, 2*np.pi, 100)
center, radius = [0.5, 0.5], 0.5
verts = np.vstack([np.sin(theta), np.cos(theta)]).T
circle = mpath.Path(verts * radius + center)
ax.set_boundary(circle, transform=ax.transAxes)

# plot with Iris quickplot pcolormesh
cs = iplt.pcolormesh(cube_GLORYS2V3_regrid,cmap='coolwarm',vmin=-0.2,vmax=0.2)
cbar = fig11.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.05,format="%.1f")
cbar.set_ticks([-0.2, -0.1, 0, 0.1, 0.2])
cbar.set_label('PW (1E+15W)',size = 6)
cbar.ax.tick_params(labelsize = 6)

# show and save plot
iplt.show()
fig11.savefig(output_path + os.sep + 'SODA3' + os.sep + 'SODA3.jpg',dpi = 300)
plt.close(fig11)

print 'PlateCarree'

# figsize works for the size of the map, not the entire figure
fig12 = plt.figure(figsize=(4,2.7))
fig12.suptitle('Oceanic Meridional Energy Transport in 1980 (year) 1 (month)',fontsize = 7,y=0.93)
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([-180,180,20,90],ccrs.PlateCarree()) # East, West, South, Nouthpse
ax.set_aspect('2.5')
ax.coastlines()
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,linewidth=1, color='gray', alpha=0.5,linestyle='--')
gl.xlabels_top = False
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
gl.xlabel_style = {'size': 6, 'color': 'gray'}
gl.ylabel_style = {'size': 6, 'color': 'gray'}

cs = iplt.pcolormesh(cube_SODA3_regrid,cmap='coolwarm',vmin=-0.15,vmax=0.15)
cbar = fig12.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.1,format="%.2f")
cbar.set_ticks([-0.15, -0.10, -0.05, 0, 0.05, 0.10, 0.15])
cbar.ax.tick_params(labelsize = 6)
cbar.set_label('PW (1E+15W)',size = 6)
# show and save plot
iplt.show()
fig12.savefig(output_path + os.sep + 'SODA3' + os.sep + 'SODA3_PlateCarree.jpg',dpi = 300)
plt.close(fig12)

# print '*******************************************************************'
# print '*********************** animation factory *************************'
# print '*******************************************************************'
# animation for ERA-Interim - NorthPolarStereo
for i in year_ERAI:
    for j in np.arange(0,12,1):
        cube_ERAI = iris.cube.Cube(AMET_ERAI[i-1979,j,:,:],long_name='Atmospheric Meridional Energy Transport',
                           var_name='AMET',units='PW',dim_coords_and_dims=[(latitude_AMET_ERAI, 0), (longitude_AMET_ERAI, 1)])
        fig13 = plt.figure(figsize=(4,3.6))
        fig13.suptitle('Atmospheric Meridional Energy Transport in %d (year) %d (month)' % (i,j+1),fontsize = 7,y=0.93)
        ax = plt.axes(projection=ccrs.NorthPolarStereo())
        ax.set_extent([-180,180,20,90],ccrs.PlateCarree())
        ax.set_aspect('1')
        ax.coastlines()
        gl = ax.gridlines(linewidth=1, color='gray', alpha=0.5,linestyle='--')
        theta = np.linspace(0, 2*np.pi, 100)
        center, radius = [0.5, 0.5], 0.5
        verts = np.vstack([np.sin(theta), np.cos(theta)]).T
        circle = mpath.Path(verts * radius + center)
        ax.set_boundary(circle, transform=ax.transAxes)
        cs = iplt.pcolormesh(cube_ERAI,cmap='coolwarm',vmin=-1.2,vmax=1.2)
        cbar = fig13.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.05,format="%.1f")
        cbar.set_label('PW (1E+15W)',size = 6)
        cbar.set_ticks([-1.2, -0.8, -0.4, 0, 0.4, 0.8, 1.2])
        cbar.ax.tick_params(labelsize = 6)
        iplt.show()
        fig13.savefig(output_path + os.sep + 'ERA-Interim' + os.sep + 'animation' + os.sep + 'NorthPolarStereo' + os.sep + 'AMET_ERAI_%dy_%dm.png' % (i,j+1),dpi = 300)
        plt.close(fig13)

        # animation for ERA-Interim - PlateCarree
        fig14 = plt.figure(figsize=(4,2.7))
        fig14.suptitle('Atmospheric Meridional Energy Transport in %d (year) %d (month)' % (i,j+1),fontsize = 7,y=0.93)
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.set_extent([-180,180,20,90],ccrs.PlateCarree())
        ax.set_aspect('2.5')
        ax.coastlines()
        gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,linewidth=1, color='gray', alpha=0.5,linestyle='--')
        gl.xlabels_top = False
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER
        gl.xlabel_style = {'size': 6, 'color': 'gray'}
        gl.ylabel_style = {'size': 6, 'color': 'gray'}
        cs = iplt.pcolormesh(cube_ERAI,cmap='coolwarm',vmin=-1.2,vmax=1.2)
        cbar = fig14.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.1,format="%.1f")
        cbar.set_label('PW (1E+15W)',size = 6)
        cbar.set_ticks([-1.2, -0.8, -0.4, 0, 0.4, 0.8, 1.2])
        cbar.ax.tick_params(labelsize = 6)
        iplt.show()
        fig14.savefig(output_path + os.sep + 'ERA-Interim' + os.sep + 'animation' + os.sep + 'PlateCarree' + os.sep + 'AMET_ERAI_%dy_%dm.png' % (i,j+1),dpi = 300)
        plt.close(fig14)

# animation for MERRA2 - NorthPolarStereo
for i in year_MERRA2:
    for j in np.arange(0,12,1):
        cube_MERRA2 = iris.cube.Cube(AMET_MERRA2[i-1980,j,:,:],long_name='Atmospheric Meridional Energy Transport',
                           var_name='AMET',units='PW',dim_coords_and_dims=[(latitude_AMET_MERRA2, 0), (longitude_AMET_MERRA2, 1)])
        fig15 = plt.figure(figsize=(4,3.6))
        fig15.suptitle('Atmospheric Meridional Energy Transport in %d (year) %d (month)' % (i,j+1),fontsize = 7,y=0.93)
        ax = plt.axes(projection=ccrs.NorthPolarStereo())
        ax.set_extent([-180,180,20,90],ccrs.PlateCarree())
        ax.set_aspect('1')
        ax.coastlines()
        gl = ax.gridlines(linewidth=1, color='gray', alpha=0.5,linestyle='--')
        theta = np.linspace(0, 2*np.pi, 100)
        center, radius = [0.5, 0.5], 0.5
        verts = np.vstack([np.sin(theta), np.cos(theta)]).T
        circle = mpath.Path(verts * radius + center)
        ax.set_boundary(circle, transform=ax.transAxes)
        cs = iplt.pcolormesh(cube_MERRA2,cmap='coolwarm',vmin=-1.2,vmax=1.2)
        cbar = fig15.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.05,format="%.1f")
        cbar.set_label('PW (1E+15W)',size = 6)
        cbar.set_ticks([-1.2, -0.8, -0.4, 0, 0.4, 0.8, 1.2])
        cbar.ax.tick_params(labelsize = 6)
        iplt.show()
        fig15.savefig(output_path + os.sep + 'MERRA2' + os.sep + 'animation' + os.sep + 'NorthPolarStereo' + os.sep + 'AMET_MERRA2_%dy_%dm.png' % (i,j+1),dpi = 300)
        plt.close(fig15)

        # animation for MERRA2 - PlateCarree
        fig16 = plt.figure(figsize=(4,2.7))
        fig16.suptitle('Atmospheric Meridional Energy Transport in %d (year) %d (month)' % (i,j+1),fontsize = 7,y=0.93)
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.set_extent([-180,180,20,90],ccrs.PlateCarree())
        ax.set_aspect('2.5')
        ax.coastlines()
        gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,linewidth=1, color='gray', alpha=0.5,linestyle='--')
        gl.xlabels_top = False
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER
        gl.xlabel_style = {'size': 6, 'color': 'gray'}
        gl.ylabel_style = {'size': 6, 'color': 'gray'}
        cs = iplt.pcolormesh(cube_MERRA2,cmap='coolwarm',vmin=-1.2,vmax=1.2)
        cbar = fig16.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.05,format="%.1f")
        cbar.set_label('PW (1E+15W)',size = 6)
        cbar.set_ticks([-1.2, -0.8, -0.4, 0, 0.4, 0.8, 1.2])
        cbar.ax.tick_params(labelsize = 6)
        iplt.show()
        fig16.savefig(output_path + os.sep + 'MERRA2' + os.sep + 'animation' + os.sep + 'PlateCarree' + os.sep + 'AMET_MERRA2_%dy_%dm.png' % (i,j+1),dpi = 300)
        plt.close(fig16)

for i in year_JRA55:
    for j in np.arange(0,12,1):
        cube_JRA55 = iris.cube.Cube(AMET_JRA55[i-1979,j,:,:],long_name='Atmospheric Meridional Energy Transport',
                           var_name='AMET',units='PW',dim_coords_and_dims=[(latitude_AMET_JRA55, 0), (longitude_AMET_JRA55, 1)])
        # animation for JRA55 - NorthPolarStereo
        fig17 = plt.figure(figsize=(4,3.6))
        fig17.suptitle('Atmospheric Meridional Energy Transport in %d (year) %d (month)' % (i,j+1),fontsize = 7,y=0.93)
        ax = plt.axes(projection=ccrs.NorthPolarStereo())
        ax.set_extent([-180,180,20,90],ccrs.PlateCarree())
        ax.set_aspect('1')
        ax.coastlines()
        gl = ax.gridlines(linewidth=1, color='gray', alpha=0.5,linestyle='--')
        theta = np.linspace(0, 2*np.pi, 100)
        center, radius = [0.5, 0.5], 0.5
        verts = np.vstack([np.sin(theta), np.cos(theta)]).T
        circle = mpath.Path(verts * radius + center)
        ax.set_boundary(circle, transform=ax.transAxes)
        cs = iplt.pcolormesh(cube_JRA55,cmap='coolwarm',vmin=-1.2,vmax=1.2)
        cbar = fig17.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.05,format="%.1f")
        cbar.set_label('PW (1E+15W)',size = 6)
        cbar.set_ticks([-1.2, -0.8, -0.4, 0, 0.4, 0.8, 1.2])
        cbar.ax.tick_params(labelsize = 6)
        iplt.show()
        fig17.savefig(output_path + os.sep + 'JRA55' + os.sep + 'animation' + os.sep + 'NorthPolarStereo' + os.sep + 'AMET_JRA55_%dy_%dm.png' % (i,j+1),dpi = 300)
        plt.close(fig17)
        # animation for JRA55 - PlateCarree
        fig18 = plt.figure(figsize=(4,2.7))
        fig18.suptitle('Atmospheric Meridional Energy Transport in %d (year) %d (month)' % (i,j+1),fontsize = 7,y=0.93)
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.set_extent([-180,180,20,90],ccrs.PlateCarree())
        ax.set_aspect('2.5')
        ax.coastlines()
        gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,linewidth=1, color='gray', alpha=0.5,linestyle='--')
        gl.xlabels_top = False
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER
        gl.xlabel_style = {'size': 6, 'color': 'gray'}
        gl.ylabel_style = {'size': 6, 'color': 'gray'}
        cs = iplt.pcolormesh(cube_JRA55,cmap='coolwarm',vmin=-1.2,vmax=1.2)
        cbar = fig18.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.1,format="%.1f")
        cbar.set_label('PW (1E+15W)',size = 6)
        cbar.set_ticks([-1.2, -0.8, -0.4, 0, 0.4, 0.8, 1.2])
        cbar.ax.tick_params(labelsize = 6)
        iplt.show()
        fig18.savefig(output_path + os.sep + 'JRA55' + os.sep + 'animation' + os.sep + 'PlateCarree' + os.sep + 'AMET_JRA55_%dy_%dm.png' % (i,j+1),dpi = 300)
        plt.close(fig18)

# animation for ORAS4 - NorthPolarStereo
for i in year_ORAS4:
    for j in np.arange(0,12,1):
        OMET_ORAS4_mask = np.ma.masked_where(vmask_ORAS4 == 0, OMET_ORAS4[i-1979,j,:,:])
        cube_ORAS4 = iris.cube.Cube(OMET_ORAS4_mask,long_name='Oceanic Meridional Energy Transport',
                                    var_name='OMET',units='PW',aux_coords_and_dims=[(latitude_OMET_ORAS4,(0,1)),(longitude_OMET_ORAS4,(0,1))])
        cube_ORAS4_regrid, extent = iris.analysis.cartography.project(cube_ORAS4, ccrs.PlateCarree(), nx=720, ny=140)
        fig19 = plt.figure(figsize=(4,3.6))
        fig19.suptitle('Oceanic Meridional Energy Transport in %d (year) %d (month)' % (i,j+1),fontsize = 7,y=0.93)
        ax = plt.axes(projection=ccrs.NorthPolarStereo())
        ax.set_extent([-180,180,20,90],ccrs.PlateCarree())
        ax.set_aspect('1')
        ax.coastlines()
        gl = ax.gridlines(linewidth=1, color='gray', alpha=0.5,linestyle='--')
        theta = np.linspace(0, 2*np.pi, 100)
        center, radius = [0.5, 0.5], 0.5
        verts = np.vstack([np.sin(theta), np.cos(theta)]).T
        circle = mpath.Path(verts * radius + center)
        ax.set_boundary(circle, transform=ax.transAxes)
        cs = iplt.pcolormesh(cube_ORAS4_regrid,cmap='coolwarm',vmin=-0.2,vmax=0.2)
        cbar = fig19.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.05, format="%.1f")
        cbar.set_ticks([-0.2, -0.1, 0, 0.1, 0.2])
        cbar.set_label('PW (1E+15W)',size = 6)
        cbar.ax.tick_params(labelsize = 6)
        iplt.show()
        fig19.savefig(output_path + os.sep + 'ORAS4' + os.sep + 'animation' + os.sep + 'NorthPolarStereo' + os.sep + 'OMET_ORAS4_%dy_%dm.png' % (i,j+1),dpi = 300)
        plt.close(fig19)
        # animation for ORAS4 - PlateCarree
        fig20 = plt.figure(figsize=(4,2.7))
        fig20.suptitle('Oceanic Meridional Energy Transport in %d (year) %d (month)' % (i,j+1),fontsize = 7,y=0.93)
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.set_extent([-180,180,20,90],ccrs.PlateCarree()) # East, West, South, Nouthpse
        ax.set_aspect('2.5')
        ax.coastlines()
        gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,linewidth=1, color='gray', alpha=0.5,linestyle='--')
        gl.xlabels_top = False
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER
        gl.xlabel_style = {'size': 6, 'color': 'gray'}
        gl.ylabel_style = {'size': 6, 'color': 'gray'}
        cs = iplt.pcolormesh(cube_ORAS4_regrid,cmap='coolwarm',vmin=-0.15,vmax=0.15)
        cbar = fig20.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.1,format="%.2f")
        cbar.set_ticks([-0.15, -0.10, -0.05, 0, 0.05, 0.10, 0.15])
        cbar.ax.tick_params(labelsize = 6)
        cbar.set_label('PW (1E+15W)',size = 6)
        # show and save plot
        iplt.show()
        fig20.savefig(output_path + os.sep + 'ORAS4' + os.sep + 'PlateCarree' + os.sep + 'OMET_ORAS4_%dy_%dm.png' % (i,j+1),dpi = 300)
        plt.close(fig20)

# animation for GLORYS2V3 - NorthPolarStereo
for i in year_GLORYS2V3:
    for j in np.arange(0,12,1):
        OMET_GLORYS2V3_mask = np.ma.masked_where(vmask_GLORYS2V3 == 0, OMET_GLORYS2V3[i-1993,j,:,:])
        cube_GLORYS2V3 = iris.cube.Cube(OMET_GLORYS2V3_mask,long_name='Oceanic Meridional Energy Transport',
                                    var_name='OMET',units='PW',aux_coords_and_dims=[(latitude_OMET_GLORYS2V3,(0,1)),(longitude_OMET_GLORYS2V3,(0,1))])
        cube_GLORYS2V3_regrid, extent = iris.analysis.cartography.project(cube_GLORYS2V3, ccrs.PlateCarree(), nx=1440, ny=350)
        fig21 = plt.figure(figsize=(4,3.6))
        fig21.suptitle('Oceanic Meridional Energy Transport in %d (year) %d (month)' % (i,j+1),fontsize = 7,y=0.93)
        ax = plt.axes(projection=ccrs.NorthPolarStereo())
        ax.set_extent([-180,180,20,90],ccrs.PlateCarree())
        ax.set_aspect('1')
        ax.coastlines()
        gl = ax.gridlines(linewidth=1, color='gray', alpha=0.5,linestyle='--')
        theta = np.linspace(0, 2*np.pi, 100)
        center, radius = [0.5, 0.5], 0.5
        verts = np.vstack([np.sin(theta), np.cos(theta)]).T
        circle = mpath.Path(verts * radius + center)
        ax.set_boundary(circle, transform=ax.transAxes)
        cs = iplt.pcolormesh(cube_GLORYS2V3_regrid,cmap='coolwarm',vmin=-0.2,vmax=0.2)
        cbar = fig21.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.05, format="%.1f")
        cbar.set_ticks([-0.2, -0.1, 0, 0.1, 0.2])
        cbar.set_label('PW (1E+15W)',size = 6)
        cbar.ax.tick_params(labelsize = 6)
        iplt.show()
        fig21.savefig(output_path + os.sep + 'GLORYS2V3' + os.sep + 'animation' + os.sep + 'NorthPolarStereo' + os.sep + 'OMET_GLORYS2V3_%dy_%dm.png' % (i,j+1),dpi = 300)
        plt.close(fig21)
        # animation for GLORYS2V3 - PlateCarree
        fig22 = plt.figure(figsize=(4,2.7))
        fig22.suptitle('Oceanic Meridional Energy Transport in %d (year) %d (month)' % (i,j+1),fontsize = 7,y=0.93)
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.set_extent([-180,180,20,90],ccrs.PlateCarree()) # East, West, South, Nouthpse
        ax.set_aspect('2.5')
        ax.coastlines()
        gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,linewidth=1, color='gray', alpha=0.5,linestyle='--')
        gl.xlabels_top = False
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER
        gl.xlabel_style = {'size': 6, 'color': 'gray'}
        gl.ylabel_style = {'size': 6, 'color': 'gray'}
        cs = iplt.pcolormesh(cube_GLORYS2V3_regrid,cmap='coolwarm',vmin=-0.15,vmax=0.15)
        cbar = fig22.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.1,format="%.2f")
        cbar.set_ticks([-0.15, -0.10, -0.05, 0, 0.05, 0.10, 0.15])
        cbar.ax.tick_params(labelsize = 6)
        cbar.set_label('PW (1E+15W)',size = 6)
        # show and save plot
        iplt.show()
        fig22.savefig(output_path + os.sep + 'GLORYS2V3' + os.sep + 'PlateCarree' + os.sep + 'OMET_GLORYS2V3_%dy_%dm.png' % (i,j+1),dpi = 300)
        plt.close(fig22)

# animation for SODA3 - NorthPolarStereo
for i in year_SODA3:
    for j in np.arange(0,12,1):
        OMET_SODA3_mask = np.ma.masked_where(vmask_SODA3 == 0, OMET_SODA3[i-1980,j,:,:])
        cube_SODA3 = iris.cube.Cube(OMET_SODA3_mask,long_name='Oceanic Meridional Energy Transport',
                                    var_name='OMET',units='PW',aux_coords_and_dims=[(latitude_OMET_SODA3,(0,1)),(longitude_OMET_SODA3,(0,1))])
        cube_SODA3_regrid, extent = iris.analysis.cartography.project(cube_SODA3, ccrs.PlateCarree(), nx=1440, ny=350)
        fig23 = plt.figure(figsize=(4,3.6))
        fig23.suptitle('Oceanic Meridional Energy Transport in %d (year) %d (month)' % (i,j+1),fontsize = 7,y=0.93)
        ax = plt.axes(projection=ccrs.NorthPolarStereo())
        ax.set_extent([-180,180,20,90],ccrs.PlateCarree())
        ax.set_aspect('1')
        ax.coastlines()
        gl = ax.gridlines(linewidth=1, color='gray', alpha=0.5,linestyle='--')
        theta = np.linspace(0, 2*np.pi, 100)
        center, radius = [0.5, 0.5], 0.5
        verts = np.vstack([np.sin(theta), np.cos(theta)]).T
        circle = mpath.Path(verts * radius + center)
        ax.set_boundary(circle, transform=ax.transAxes)
        cs = iplt.pcolormesh(cube_SODA3_regrid,cmap='coolwarm',vmin=-0.2,vmax=0.2)
        cbar = fig23.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.05, format="%.1f")
        cbar.set_ticks([-0.2, -0.1, 0, 0.1, 0.2])
        cbar.set_label('PW (1E+15W)',size = 6)
        cbar.ax.tick_params(labelsize = 6)
        iplt.show()
        fig23.savefig(output_path + os.sep + 'SODA3' + os.sep + 'animation' + os.sep + 'NorthPolarStereo' + os.sep + 'OMET_SODA3_%dy_%dm.png' % (i,j+1),dpi = 300)
        plt.close(fig23)
        # animation for SODA3 - PlateCarree
        fig24 = plt.figure(figsize=(4,2.7))
        fig24.suptitle('Oceanic Meridional Energy Transport in %d (year) %d (month)' % (i,j+1),fontsize = 7,y=0.93)
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.set_extent([-180,180,20,90],ccrs.PlateCarree()) # East, West, South, Nouthpse
        ax.set_aspect('2.5')
        ax.coastlines()
        gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,linewidth=1, color='gray', alpha=0.5,linestyle='--')
        gl.xlabels_top = False
        gl.xformatter = LONGITUDE_FORMATTER
        gl.yformatter = LATITUDE_FORMATTER
        gl.xlabel_style = {'size': 6, 'color': 'gray'}
        gl.ylabel_style = {'size': 6, 'color': 'gray'}
        cs = iplt.pcolormesh(cube_SODA3_regrid,cmap='coolwarm',vmin=-0.15,vmax=0.15)
        cbar = fig24.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.1,format="%.2f")
        cbar.set_ticks([-0.15, -0.10, -0.05, 0, 0.05, 0.10, 0.15])
        cbar.ax.tick_params(labelsize = 6)
        cbar.set_label('PW (1E+15W)',size = 6)
        # show and save plot
        iplt.show()
        fig24.savefig(output_path + os.sep + 'SODA3' + os.sep + 'PlateCarree' + os.sep + 'OMET_SODA3_%dy_%dm.png' % (i,j+1),dpi = 300)
        plt.close(fig24)

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
