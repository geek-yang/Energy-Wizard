#!/usr/bin/env python
"""
Copyright Netherlands eScience Center
Function        : SOM analysis of SLP and AMET
Author          : Yang Liu
Date            : 2018.07.04
Last Update     : 2018.07.08
Description     : The code aims to analyze spatial distribution of several fields
                  through Self Organizing Map.

                  The fields include Sea Level Pressure (SLP) and AMET, from ERA-Interim

Return Value    : NetCFD4 data file
Dependencies    : os, time, numpy, netCDF4, sys, matplotlib
variables       : Meridional Energy Transport               E         [Tera-Watt]
                  Meridional Overturning Circulation        Psi       [Sv]
Caveat!!        : Time range
                  ERA-Interim   1979 - 2016

                  We are only interested in the variables from 60N - 90N
"""

import numpy as np
import time as tttt
from netCDF4 import Dataset
import os
import seaborn as sns
import platform
import matplotlib.pyplot as plt
import matplotlib.path as mpath
from mpl_toolkits.basemap import Basemap, cm
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import sompy
# hitsmap
from sompy.visualization.bmuhits import BmuHitsView

# print the system structure and the path of the kernal
print platform.architecture()
print os.path

# calculate the time for the code execution
start_time = tttt.time()
# switch on the seaborn effect
sns.set()

################################   Input zone  ######################################
# specify data path
# AMET
datapath_ERAI = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ERAI/postprocessing'
# SLP
datapath_ERAI_fields = '/home/yang/workbench/Core_Database_AMET_OMET_reanalysis/ERAI/regression'
# output
output_path = '/home/yang/NLeSC/Computation_Modeling/BlueAction/AMET/ERA-Interim/SOM'
####################################################################################
print '*******************************************************************'
print '*********************** extract variables *************************'
print '*******************************************************************'
dataset_ERAI = Dataset(datapath_ERAI + os.sep + 'model_daily_075_1979_2016_E_point.nc')
dataset_ERAI_fields = Dataset(datapath_ERAI_fields + os.sep + 'surface_ERAI_monthly_regress_1979_2016.nc')

AMET_Lvq_ERAI = dataset_ERAI.variables['E_Lvq'][:,:,:41,:]/1000 # from Tera Watt to Peta Watt
AMET_E_ERAI = dataset_ERAI.variables['E'][:,:,:41,:]/1000 # from Tera Watt to Peta Watt
latitude_ERAI = dataset_ERAI.variables['latitude'][:41]
longitude_ERAI = dataset_ERAI.variables['longitude'][:]
year_ERAI = dataset_ERAI.variables['year'][:]             # from 1979 to 2016

SLP_ERAI_series = dataset_ERAI_fields.variables['msl'][:,:41,:]       # dimension (time, lat, lon)
latitude_ERAI_fields = dataset_ERAI_fields.variables['latitude'][:41]
longitude_ERAI_fields = dataset_ERAI_fields.variables['longitude'][:]

print '*******************************************************************'
print '*************************** whitening *****************************'
print '*******************************************************************'
month_ind = np.arange(12)
# climatology for Sea Level Pressure
seasonal_cycle_SLP_ERAI = np.zeros((12,len(latitude_ERAI_fields),len(longitude_ERAI_fields))) # from 20N - 90N
SLP_ERAI_white_series = np.zeros(SLP_ERAI_series.shape,dtype=float)
# anomalies of SLP
for i in month_ind:
    # calculate the monthly mean (seasonal cycling)
    seasonal_cycle_SLP_ERAI[i,:,:] = np.mean(SLP_ERAI_series[i::12,:,:],axis=0)
    # remove seasonal mean
    SLP_ERAI_white_series[i::12,:,:] = SLP_ERAI_series[i::12,:,:] - seasonal_cycle_SLP_ERAI[i,:,:]

# climatology of AMET
seansonal_cycle_AMET_E_ERAI = np.mean(AMET_E_ERAI,axis=0)
seansonal_cycle_AMET_Lvq_ERAI = np.mean(AMET_Lvq_ERAI,axis=0)
# anomalies of AMET
AMET_Lvq_ERAI_white = np.zeros(AMET_Lvq_ERAI.shape,dtype=float)
AMET_E_ERAI_white = np.zeros(AMET_E_ERAI.shape,dtype=float)

for i in np.arange(len(year_ERAI)):
    for j in month_ind:
        AMET_Lvq_ERAI_white[i,j,:] = AMET_Lvq_ERAI[i,j,:] - seansonal_cycle_AMET_Lvq_ERAI[j,:]
        AMET_E_ERAI_white[i,j,:] = AMET_E_ERAI[i,j,:] - seansonal_cycle_AMET_E_ERAI[j,:]
print '*******************************************************************'
print '****************** prepare variables for plot *********************'
print '*******************************************************************'
# dataset without seasonal cycle - time series
AMET_Lvq_ERAI_white_series = AMET_Lvq_ERAI_white.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI),len(longitude_ERAI))
AMET_E_ERAI_white_series = AMET_E_ERAI_white.reshape(len(year_ERAI)*len(month_ind),len(latitude_ERAI),len(longitude_ERAI))
print '*******************************************************************'
print '*********************** reshape the input *************************'
print '*******************************************************************'
nt, ny, nx = AMET_E_ERAI_white_series.shape
AMET_E_ERAI_2D = np.reshape(AMET_E_ERAI_white_series,[nt,ny*nx], order='F') # F means Fortran like index ordering
print '*******************************************************************'
print '********************** train neural network ***********************'
print '*******************************************************************'
som = sompy.SOMFactory().build(AMET_E_ERAI_2D,mapsize=(5,7),mask=None, mapshape='planar', lattice='rect', normalization=None,initialization='pca',neighborhood='gaussian',training='batch')
#som.train(n_job=1,verbose='info', train_rough_len=20, train_finetune_len=10)
som.train(n_job=1,verbose='info')
###############################   cautious!   ##################################
########   we must monitor the topographic error and quantization error ########
# The quantization error:
#           average distance between each data vector and its BMU.
# The topographic error:
#           the proportion of all data vectors for which first and second BMUs are not adjacent units.
#
# A rule of thumb is to generate several models with different parameters and choose the one which,
# having a topographic error very near to zero, has the lowest quantization error. It is important
# to hold the topographic error very low in order to make the components smooth and easy to understand.
###############################   cautious!   ##################################
topographic_error = som.calculate_topographic_error()
#quantization_error = np.mean(som._bmu[1])
#print ("Topographic error = %s; Quantization error = %s" % (topographic_error, quantization_error))
print ("Topographic error = %s" % (topographic_error))
# grab the index of BMU for each input vector
BMU_index = som._bmu
# Translates a best matching unit index to the corresponding matrix x,y coordinates
BMU_index_array = som.bmu_ind_to_xy(np.array(BMU_index[0])) # rows and columns in the x,y coordinate
print '*******************************************************************'
print '********************     output master SOM    *********************'
print '*******************************************************************'
codebook = som.codebook.matrix
xx, yy = np.meshgrid(longitude_ERAI,latitude_ERAI)
#xx, yy = np.meshgrid(longitude_ERAI_fields,latitude_ERAI_fields)
proj = ccrs.NorthPolarStereo()
fig1, axes = plt.subplots(ncols=7,nrows=5, figsize=(16,12), subplot_kw=dict(projection=proj))
for i in range(som.codebook.nnodes):
    masterSOM = codebook[i,:].reshape(ny,nx,order='F')
    cs = axes.flat[i].contourf(xx,yy,masterSOM,transform=ccrs.PlateCarree(),cmap='coolwarm')
    #cs = axes.flat[i].contourf(xx,yy,masterSOM,levels=np.arange(950,1030,4),transform=ccrs.PlateCarree(),cmap='coolwarm')
    cbar = fig1.colorbar(cs,ax=axes.flat[i], shrink=0.8)
    #cbar.set_label('PW',labelpad=-3,size = 7)
    cbar.ax.tick_params(labelsize = 5)
    # draw
    axes.flat[i].coastlines()
    gl = axes.flat[i].gridlines(linewidth=1, color='gray', alpha=0.5,linestyle='--')
    theta = np.linspace(0, 2*np.pi, 100)
    center, radius = [0.5, 0.5], 0.5
    verts = np.vstack([np.sin(theta), np.cos(theta)]).T
    circle = mpath.Path(verts * radius + center)
    axes.flat[i].set_boundary(circle, transform=axes.flat[i].transAxes)
fig1.savefig(os.path.join(output_path,'SOM_AMET_E_ERAI.jpg'),dpi=400)
#fig1.savefig(os.path.join(output_path,'SOM_SLP_ERAI.jpg'),dpi=400)
#plt.close(fig1)
print '*******************************************************************'
print '***************           plot hitsmap            *****************'
print '***************   check the frequency of regimes  *****************'
print '*******************************************************************'
vhts = BmuHitsView(5,7,'Frequency',text_size=12,show_text=True)
#vhts = sompy.hitmap.HitMapView(5,7,'Frequency',text_size=12,show_text=True)
vhts.show(som, anotate=True, onlyzeros=False, labelsize=12, cmap='RdBu_r',logaritmic=False)
vhts.save(os.path.join(output_path,'vhts_AMET_E_ERAI.jpg'),dpi=400)
#vhts.save(os.path.join(output_path,'vhts_SLP_ERAI.jpg'),dpi=400)
print '*******************************************************************'
print '***************        K-means clustering         *****************'
print '*******************************************************************'
# determine how many groups we want to divide
# this is closely relate to physical aspect of view
# for instance, if there are 4 weather regimes in the Arctic
# then it is better to make 4 group
som.cluster(n_clusters=4)
setattr(som,'cluster_labels',[0,1,2,3])
hits = BmuHitsView(8,8,'Weather regimes clustering', text_size=12)
hits.show(som,what='cluster')
print '*******************************************************************'
print '***************      U matrix visualization       *****************'
print '*******************************************************************'
u = sompy.umatrix.UMatrixView(8,8,'U-Matrix of SLP', show_axis=True, text_size=12, show_text=True)
# U matrxi value
UMat = u.build_u_matrix(som,distance2=1,row_normalized=False)
# visualization
UMat = u.show(som,distance2=1,row_normalized=False,show_data=True,contooor=True,blob=False)
print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
