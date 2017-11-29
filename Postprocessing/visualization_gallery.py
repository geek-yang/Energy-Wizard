#!/usr/bin/env python
"""
Copyright Netherlands eScience Center

Function        : Visualization of AMET and OMET from reanalysis datasets
Author          : Yang Liu
Date            : 2017.11.28
Last Update     : 2017.11.28
Description     : The code aims to project the atmospheric/oceanic meridional energy
                  transport on the map.
Return Value    : PNGs
Dependencies    : os, time, numpy, netCDF4, sys, matplotlib, logging, iris, cartopy
variables       : AMET               Tera Watt
                  OMET               Tera Watt
                  Land-Sea Mask      mask
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
# specify data path
datapath_ERAI = 'F:\DataBase\HPC_out\ERAI\postprocessing'
datapath_MERRA2 = 'F:\DataBase\HPC_out\MERRA2\postprocessing'
datapath_ORAS4 = 'F:\DataBase\HPC_out\ORAS4\postprocessing'
datapath_GLORYS2V3 = 'F:\DataBase\HPC_out\GLORYS2V3\postprocessing'

maskpath_ORAS4 = 'F:\DataBase\ORAS\ORAS4\Monthly\model'
maskpath_GLORYS2V3 = 'F:\DataBase\GLORYS\S2V3\Monthly'
# specify output path
output_path = 'C:\Yang\PhD\Computation and Modeling\Blue Action\Visualization'
####################################################################################
print '*******************************************************************'
print '*********************** extract variables *************************'
print '*******************************************************************'
# data
dataset_ERAI = Dataset(datapath_ERAI + os.sep + 'model_daily_075_1979_2016_E_point.nc')
dataset_MERRA2 = Dataset(datapath_MERRA2 + os.sep + 'AMET_MERRA2_model_daily_1980_2016_E_point.nc')
dataset_GLORYS2V3 = Dataset(datapath_GLORYS2V3 + os.sep + 'GLORYS2V3_model_monthly_orca025_E_point.nc')
dataset_ORAS4 = Dataset(datapath_ORAS4 + os.sep + 'oras4_model_monthly_orca1_E_point.nc')
# mesh and mask
mesh_mask_ORAS4 = Dataset(maskpath_ORAS4 + os.sep + 'mesh_mask.nc')
mesh_mask_GLORYS2V3 = Dataset(maskpath_GLORYS2V3 + os.sep + 'G2V3_mesh_mask_myocean.nc')

# from 20N - 90N
AMET_ERAI = dataset_ERAI.variables['E'][:-2,:,:,:]/1000 # from Tera Watt to Peta Watt
#AMET_MERRA2 = dataset_MERRA2.variables['E'][:]/1000 # from Tera Watt to Peta Watt
OMET_ORAS4 = dataset_ORAS4.variables['E'][21:,:,180:,:]/1000 # start from 1979
OMET_GLORYS2V3 = dataset_GLORYS2V3.variables['E'][:,:,579:,:]/1000 # start from 1993

#mask (surface mask only)
vmask_ORAS4 = mesh_mask_ORAS4.variables['vmask'][0,0,180:,:] # from 20N
vmask_GLORYS2V3 = mesh_mask_GLORYS2V3.variables['vmask'][0,0,579:,:] # from 20N
# year
year_ERAI = dataset_ERAI.variables['year'][:-2]             # from 1979 to 2014
#year_MERRA2 = dataset_MERRA2.variables['year'][:]         # from 1980 to 2014
year_ORAS4 = dataset_ORAS4.variables['year'][21:]         # from 1958 to 2014
year_GLORYS2V3 = dataset_GLORYS2V3.variables['year'][:]   # from 1993 to 2014

#latitude
latitude_ERAI = dataset_ERAI.variables['latitude'][:]
#latitude_MERRA2 = dataset_MERRA2.variables['latitude'][:]
latitude_ORAS4 = dataset_ORAS4.variables['latitude'][180:]
latitude_GLORYS2V3 = dataset_GLORYS2V3.variables['latitude'][579:]
#longitude
longitude_ERAI = dataset_ERAI.variables['longitude'][:]
#longitude_MERRA2 = dataset_MERRA2.variables['longitude'][:]
longitude_ORAS4 = dataset_ORAS4.variables['longitude'][180:]
longitude_GLORYS2V3 = dataset_GLORYS2V3.variables['longitude'][579:]
print '*******************************************************************'
print '************************** maps factory ***************************'
print '*******************************************************************'
print 'The visualization of AMET and OMET are complete with Iris and Cartopy.'

# support NetCDF
iris.FUTURE.netcdf_promote = True

print '========================  ERA-Interim  ========================'

# ERA-Interim only
# create cube for plot in an elegant way
latitude_AMET = iris.coords.DimCoord(latitude_ERAI,standard_name='latitude',long_name='latitude',
                             var_name='lat',units='degrees')
longitude_AMET = iris.coords.DimCoord(longitude_ERAI,standard_name='longitude',long_name='longitude',
                             var_name='lon',units='degrees')
cube_ERAI = iris.cube.Cube(AMET_ERAI[0,0,:,:],long_name='Atmospheric Meridional Energy Transport',
                           var_name='AMET',units='PW',dim_coords_and_dims=[(latitude_AMET, 0), (longitude_AMET, 1)])
# sample plot
# figsize works for the size of the map, not the entire figure
fig1 = plt.figure(figsize=(6,6))

# suptitle is the title for the figure
fig1.suptitle('Atmospheric Meridional Energy Transport in 1979 (year) 1 (month)',fontsize = 12,y=0.93)

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
#gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,linewidth=1, color='gray', alpha=0.5,linestyle='--')
gl = ax.gridlines(linewidth=1, color='gray', alpha=0.5,linestyle='--')
# set gridline details, only work for PlateCarree() and Mercator()
# switch of label locations
#gl.xlabels_top = False
#ax.ylabels_left = False
# specify label styles
#gl.xlabel_style = {'size': 8, 'color': 'gray'}
#gl.ylabel_style = {'size': 8, 'color': 'gray'}
# switch of ticks
#gl.set_xticks()
#gl.set_yticks()
# switch of lines
#gl.xlines = False
# specify the location of labels
#gl.ylocator = mticker.FixedLocator([30, 60])
# use of formatter (fixed)
#gl.xformatter = LONGITUDE_FORMATTER
#gl.yformatter = LATITUDE_FORMATTER

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
cbar = fig1.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.05)
cbar.set_label('PW (1E+15W)')

# show and save plot
iplt.show()
fig1.savefig(output_path + os.sep + 'ERA-Interim' + os.sep + 'ERAI.jpg',dpi = 500)

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
fig2 = plt.figure(figsize=(6,6))
fig2.suptitle('Oceanic Meridional Energy Transport in 1979 (year) 1 (month)',fontsize = 12,y=0.93)

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
cbar = fig2.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.05)
cbar.set_label('PW (1E+15W)')

# show and save plot
iplt.show()
fig2.savefig(output_path + os.sep + 'ORAS4' + os.sep + 'OMET_ORAS4.jpg',dpi = 500)

print '========================  GLORYS2v3  ========================'
# use Iris for interpolation/regridding
# create cube for plot in an elegant way

# mask the array
OMET_GLORYS2V3_mask = np.ma.masked_where(vmask_GLORYS2V3 == 0, OMET_GLORYS2V3[0,0,:,:])

# define the cube for the use of iris package
latitude_OMET_GLORYS2V3 = iris.coords.AuxCoord(latitude_GLORYS2V3,standard_name='latitude',units='degrees')
longitude_OMET_GLORYS2V3 = iris.coords.AuxCoord(longitude_GLORYS2V3,standard_name='longitude',units='degrees')
cube_GLORYS2V3 = iris.cube.Cube(OMET_GLORYS2V3_mask,long_name='Oceanic Meridional Energy Transport',
                                var_name='OMET',units='PW',aux_coords_and_dims=[(latitude_OMET_GLORYS2V3,(0,1)),(longitude_OMET_GLORYS2V3,(0,1))])
#print cube_ORAS4
# Transform cube to target projection
cube_GLORYS2V3_regrid, extent = iris.analysis.cartography.project(cube_GLORYS2V3, ccrs.PlateCarree(), nx=1440, ny=900)
# interpolation complete!!
print cube_GLORYS2V3_regrid

# plot
fig3 = plt.figure(figsize=(6,6))
fig3.suptitle('Oceanic Meridional Energy Transport in 1993 (year) 1 (month)',fontsize = 12,y=0.93)

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
cbar = fig3.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.05)
cbar.set_label('PW (1E+15W)')

# show and save plot
iplt.show()
fig3.savefig(output_path + os.sep + 'GLORYS2V3' + os.sep + 'OMET_GLORYS2V3.jpg',dpi = 500)
print '*******************************************************************'
print '*********************** animation factory *************************'
print '*******************************************************************'
# animation for ERA-Interim
for i in year_ERAI:
    for j in np.arange(0,12,1):
        cube_ERAI = iris.cube.Cube(AMET_ERAI[i-1979,j,:,:],long_name='Atmospheric Meridional Energy Transport',
                           var_name='AMET',units='PW',dim_coords_and_dims=[(latitude_AMET, 0), (longitude_AMET, 1)])
        fig11 = plt.figure(figsize=(6,6))
        fig11.suptitle('Atmospheric Meridional Energy Transport in %d (year) %d (month)' % (i,j+1),fontsize = 12,y=0.93)
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
        cbar = fig11.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.05)
        cbar.set_label('PW (1E+15W)')
        iplt.show()
        fig11.savefig(output_path + os.sep + 'ERA-Interim' + os.sep + 'animation' + os.sep + 'AMET_ERAI_%dy_%dm.png' % (i,j+1),dpi = 500)

# animation for ORAS4
for i in year_ORAS4:
    for j in np.arange(0,12,1):
        OMET_ORAS4_mask = np.ma.masked_where(vmask_ORAS4 == 0, OMET_ORAS4[i-1979,j,:,:])
        cube_ORAS4 = iris.cube.Cube(OMET_ORAS4_mask,long_name='Oceanic Meridional Energy Transport',
                                    var_name='OMET',units='PW',aux_coords_and_dims=[(latitude_OMET_ORAS4,(0,1)),(longitude_OMET_ORAS4,(0,1))])
        cube_ORAS4_regrid, extent = iris.analysis.cartography.project(cube_ORAS4, ccrs.PlateCarree(), nx=720, ny=140)
        fig22 = plt.figure(figsize=(6,6))
        fig22.suptitle('Oceanic Meridional Energy Transport in %d (year) %d (month)' % (i,j+1),fontsize = 12,y=0.93)
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
        cbar = fig22.colorbar(cs,extend='both',orientation='horizontal',shrink =0.8,pad=0.05)
        cbar.set_label('PW (1E+15W)')
        iplt.show()
        fig22.savefig(output_path + os.sep + 'ORAS4' + os.sep + 'animation' + os.sep + 'OMET_ORAS4_%dy_%dm.png' % (i,j+1),dpi = 500)

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
