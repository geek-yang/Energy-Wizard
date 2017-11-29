#!/usr/bin/env python
"""
Copyright Netherlands eScience Center

Function        : Animation of AMET and OMET from reanalysis datasets
Author          : Yang Liu
Date            : 2017.11.29
Last Update     : 2017.11.29
Description     : The code aims to project the atmospheric/oceanic meridional energy
                  transport on the map.
Return Value    : gif, mp4
Dependencies    : os, time, numpy, netCDF4, sys, matplotlib, logging
variables       : AMET pngs
                  OMET pngs
"""
import os
import time as tttt
import imageio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mgimg
from matplotlib import animation

# calculate the time for the code execution
start_time = tttt.time()
################################   Input zone  ######################################
# specify data path
datapath_ERAI = 'C:\Yang\PhD\Computation and Modeling\Blue Action\Visualization\ERA-Interim\\animation'
datapath_ORAS4 = 'C:\Yang\PhD\Computation and Modeling\Blue Action\Visualization\ORAS4\\animation'
# specify output path
output_path = 'C:\Yang\PhD\Computation and Modeling\Blue Action\Visualization'
####################################################################################
print '*******************************************************************'
print '********************* export animation gif ************************'
print '*******************************************************************'
# make a image pool
# images_ERAI = []
#images_ORAS4 = []
#
year_ERAI = np.arange(1979,2015,1) # from 1979 - 2014
year_ORAS4 = np.arange(1979,2015,1) # from 1979 - 2014
#For short movie

################################################################################
# for i in year_ERAI:
#     for j in np.arange(0,12,1):
#         images_ERAI.append(imageio.imread(datapath_ERAI + os.sep +'AMET_ERAI_%dy_%dm.png' % (i,j+1)))
# # quantizer determines the quality of gif, there are options like 'nq' 'wu'
# imageio.mimsave(output_path + os.sep + 'AMET_ERA-Interim.gif', images_ERAI,duration=0.3,quantizer='nq')
#
# for i in year_ORAS4:
#     for j in np.arange(0,12,1):
#         images_ORAS4.append(imageio.imread(datapath_ORAS4 + os.sep +'OMET_ORAS4_%dy_%dm.png' % (i,j+1)))
#
# imageio.mimsave(output_path + os.sep + 'OMET_ORAS4.gif', images_ORAS4,duration=0.3,quantizer='nq')
################################################################################
#For long movie (save memory)
# quantizer determines the quality of gif, there are options like 'nq' 'wu'
with imageio.get_writer(output_path + os.sep + 'AMET_ERA-Interim.gif', mode='I',duration=0.3,quantizer='nq') as writer:
    for i in year_ERAI:
        for j in np.arange(0,12,1):
            images_ERAI = imageio.imread(datapath_ERAI + os.sep +'AMET_ERAI_%dy_%dm.png' % (i,j+1))
            writer.append_data(image_ERAI)

with imageio.get_writer(output_path + os.sep + 'OMET_ORAS4.gif', mode='I',duration=0.3,quantizer='nq') as writer:
    for i in year_ORAS4:
        for j in np.arange(0,12,1):
            images_ORAS4 = imageio.imread(datapath_ORAS4 + os.sep +'OMET_ORAS4_%dy_%dm.png' % (i,j+1))
            writer.append_data(image_ORAS4)
# save mp4
# there are issues with contour plots when making animation with ArtistAnimation
# the contour module is not included in the 'Artist' section of animation
# there is method to deal with it
# https://stackoverflow.com/questions/23070305/how-can-i-make-an-animation-with-contourf

   #################################################################
    ## Bug fix for Quad Contour set not having attribute 'set_visible'
    # def setvisible(self,vis):
    #     for c in self.collections: c.set_visible(vis)
    # im.set_visible = types.MethodType(setvisible,im)
    # im.axes = pl.gca()
    # im.figure=fig
    ####################################################################

#blit=True means only re-draw the parts that have changed.
# fig1 = plt.figure()
# anim_ERAI = animation.ArtistAnimation(fig1, images_ERAI, interval=20, blit=True, repeat_delay=1000)
# anim_ERAI.save(output_path + os.sep + 'AMET_ERA-Interim_animation.mp4')
# plt.show()
#
# fig2 = plt.figure()
# anim_ORAS4 = animation.ArtistAnimation(fig2, images_ORAS4, interval=20, blit=True, repeat_delay=1000)
# anim_ORAS4.save(output_path + os.sep + 'AMET_ORAS4_animation.mp4')
# plt.show()

print ("--- %s minutes ---" % ((tttt.time() - start_time)/60))
