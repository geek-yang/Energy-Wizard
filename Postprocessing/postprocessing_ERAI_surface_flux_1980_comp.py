#!/usr/bin/env python
"""
Copyright Netherlands eScience Center

Function        : Extract ERA-Interim vertical integral of meridional energy flux (surface)
Author          : Yang Liu
Date            : 2017.7.17
Description     : The code aims to extract the vertical integral of meridional
                  energy flux from ERA-Interim surface datasets. Plots with
                  aspect to meridional energy flux (incl. internal energy, latent
                  energy, geopotential energy) are generated for the verification
                  of the results given by the computation of meridional energy
                  transport using model level data with mass correction.
                  It is made for the dataset "ERA-Interim". But it could
                  be used to deal with other datasets from ECMWF as well
                  after small adjustment.
Input Value    : NetCFD4
Return Value   : -
Dependencies    : os, time, numpy, netCDF4, platform

"""

#from scipy.io import netcdf
import numpy as np
import matplotlib.pyplot as plt
import time
from netCDF4 import Dataset,num2date
import platform
import os

#from mpl_toolkits.basemap import Basemap

##########################################################################
###########################   Units vacabulory   #########################
# cpT:  [J / kg K] * [K]     = [J / kg]
# Lvq:  [J / kg] * [kg / kg] = [J / kg]
# gz in [m2 / s2] = [ kg m2 / kg s2 ] = [J / kg]

# multiply by v: [J / kg] * [m / s] => [J m / kg s]
# sum over longitudes [J m / kg s] * [ m ] = [J m2 / kg s]

# integrate over pressure: dp: [Pa] = [N m-2] = [kg m2 s-2 m-2] = [kg s-2]
# [J m2 / kg s] * [Pa] = [J m2 / kg s] * [kg / s2] = [J m2 / s3]
# and factor 1/g: [J m2 / s3] * [s2 /m2] = [J / s] = [Wat]
##########################################################################

print platform.architecture()
print os.path

start_time = time.time()

#sys.stdout = open('F:\DataBase\ERA_Interim\console.out','w')
################################   Input zone  ######################################
datapath = "F:\DataBase\ERA_Interim\Subdaily\\vertical_int_meridional_flux_197901-201704_surface_daily.nc"
datapath_comp = 'F:\DataBase\ERA_Interim\Subdaily\model_daily_075_1980\Monthly mean meridional E\\model_daily_075_1980_E_zonal_int.nc'
year = 1980
output_path = 'C:\Yang\PhD\Computation and Modeling\Reproduction of Trenberth and Caron\Figures\Meridional Energy Flux 1980'
####################################################################################

# define the constant:
constant ={'g' : 9.80616,      # gravititional acceleration [m / s2]
           'R' : 6371009,      # radius of the earth [m]
           'cp': 1004.64,      # heat capacity of air [J/(Kg*K)]
           'Lv': 2264670,      # Latent heat of vaporization [J/Kg]
           'R_dry' : 286.9,    # gas constant of dry air [J/(kg*K)]
           'R_vap' : 461.5,    # gas constant for water vapour [J/(kg*K)]
            }

#check the existance of the file
if not os.path.isfile(datapath):
    print 'file %s not found' % datapath

#check if the file is readable
if not os.access(datapath, os.R_OK):
    print 'file %s not readable' % datapath

# take the key of dataset and extarct
d = Dataset(datapath)
dd = Dataset(datapath_comp)

# ECMWF analysis
for k in d.variables:
    print d.variables['%s' % (k)]

date_start = 12 * (year-1979)
date_end = 24 * (year-1979)

lon = d.variables['longitude'][:]
lat = d.variables['latitude'][:]
mass_flux = d.variables['p66.162'][date_start:date_end,:,:]             # Vertical integral of northward mass flux (kg m**-1 s**-1)
kinetic_flux = d.variables['p68.162'][date_start:date_end,:,:]           # Vertical integral of northward kinetic energy flux (units: W m**-1)
heat_flux = d.variables['p70.162'][date_start:date_end,:,:]              # Vertical integral of northward heat flux (units: W m**-1)
latent_flux = d.variables['p72.162'][date_start:date_end,:,:]            # Vertical integral of northward water vapour flux (units: kg m**-1 s**-1)
geopotential_flux = d.variables['p74.162'][date_start:date_end,:,:]      # Vertical integral of northward geopotential flux (units: W m**-1)
total_flux = d.variables['p76.162'][date_start:date_end,:,:]             # Vertical integral of northward total energy flux (units: W m**-1)

tt = d.variables['time'][12:24]
TT = num2date(tt,d.variables['time'].units)

# Calculation based on daily data on model level
E = dd.variables['E'][:]
E_internal = dd.variables['E_cpT'][:]
E_latent = dd.variables['E_Lvq'][:]
E_geopotential = dd.variables['E_gz'][:]

print ('The extracted data is from %s to %s' % (TT[0],TT[-1]))

# data postprocessing - zonal integral

kinetic_flux_int = np.sum(np.mean(kinetic_flux,0),1)
heat_flux_int = np.sum(np.mean(heat_flux,0),1)
latent_flux_int = np.sum(np.mean(latent_flux,0),1) * constant['Lv']
geopotential_flux_int = np.sum(np.mean(geopotential_flux,0),1)
total_flux_int = np.sum(np.mean(total_flux,0),1)

# make plots
# calculate zonal & meridional grid size on earth
# the earth is taken as a perfect sphere, instead of a ellopsoid
dx = 2 * np.pi * constant['R'] * np.cos(2 * np.pi * lat / 360) / len(lon)
dx[0] = 0
dx[-1] = 0

# Plot the total meridional energy transport against the latitude
# ECMWF analysis only
fig1 = plt.figure()
plt.axhline(y=0, color='r',ls='--')
plt.plot(lat,total_flux_int * dx / 1e+15,'b-',label='ECMWF')
plt.title('Total Atmospheric Meridional Energy Transport %d' % (year))
#plt.legend()
plt.xlabel("Laitude")
plt.xticks(np.linspace(-90,90,13))
plt.ylabel("Meridional Energy Transport (PW)")
#plt.show()
fig1.savefig(output_path + os.sep + 'Meridional_Energy_total_%d_ERAI_surface.jpg' % (year), dpi = 400)

# Plot the meridional internal energy transport against the latitude
fig2 = plt.figure()
plt.axhline(y=0, color='r',ls='--')
plt.plot(lat,heat_flux_int * dx / 1e+15,'b-',label='ECMWF')
plt.title('Atmospheric Meridional Internal Energy Transport %d' % (year))
#plt.legend()
plt.xlabel("Laitude")
plt.xticks(np.linspace(-90,90,13))
plt.ylabel("Meridional Energy Transport (PW)")
#plt.show()
fig2.savefig(output_path + os.sep + 'Meridional_Energy_internal_%d_ERAI_surface.jpg' % (year), dpi = 400)

# Plot the meridional latent energy transport against the latitude
fig3 = plt.figure()
plt.axhline(y=0, color='r',ls='--')
plt.plot(lat,latent_flux_int * dx / 1e+15,'b-',label='ECMWF')
plt.title('Atmospheric Meridional Latent Energy Transport %d' % (year))
#plt.legend()
plt.xlabel("Laitude")
plt.xticks(np.linspace(-90,90,13))
plt.ylabel("Meridional Energy Transport (PW)")
#plt.show()
fig3.savefig(output_path + os.sep + 'Meridional_Energy_latent_%d_ERAI_surface.jpg' % (year), dpi = 400)

# Plot the meridional geopotential energy transport against the latitude
fig4 = plt.figure()
plt.axhline(y=0, color='r',ls='--')
plt.plot(lat,geopotential_flux_int * dx / 1e+15,'b-',label='ECMWF')
plt.title('Atmospheric Meridional Geopotential Energy Transport %d' % (year))
#plt.legend()
plt.xlabel("Laitude")
plt.xticks(np.linspace(-90,90,13))
plt.ylabel("Meridional Energy Transport (PW)")
#plt.show()
fig4.savefig(output_path + os.sep + 'Meridional_Energy_geopotential_%d_ERAI_surface.jpg' % (year), dpi = 400)

# Plot the meridional kinetic energy transport against the latitude
fig5 = plt.figure()
plt.axhline(y=0, color='r',ls='--')
plt.plot(lat,kinetic_flux_int * dx / 1e+15,'b-',label='ECMWF')
plt.title('Atmospheric Meridional Kinetic Energy Transport %d' % (year))
#plt.legend()
plt.xlabel("Laitude")
plt.xticks(np.linspace(-90,90,13))
plt.ylabel("Meridional Energy Transport (PW)")
#plt.show()
fig5.savefig(output_path + os.sep + 'Meridional_Energy_kinetic_%d_ERAI_surface.jpg' % (year), dpi = 400)

# comparison
fig11 = plt.figure()
plt.axhline(y=0, color='k',ls='--')
plt.plot(lat,total_flux_int * dx / 1e+15,'r-',label='Analysis')
plt.plot(lat,np.mean(E,0)/1000,'r--',label='Calculation')
plt.title('Total Atmospheric Meridional Energy Transport %d' % (year))
plt.legend()
plt.xlabel("Laitude")
plt.xticks(np.linspace(-90,90,13))
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig11.savefig(output_path + os.sep + 'Meridional_Energy_total_%d_ERAI_surface_comp.jpg' % (year), dpi = 400)

# Plot the meridional internal energy transport against the latitude
fig12 = plt.figure()
plt.axhline(y=0, color='k',ls='--')
plt.plot(lat,heat_flux_int * dx / 1e+15,'b-',label='Analysis')
plt.plot(lat,np.mean(E_internal,0)/1000,'r--',label='Calculation')
plt.title('Atmospheric Meridional Internal Energy Transport %d' % (year))
plt.legend()
plt.xlabel("Laitude")
plt.xticks(np.linspace(-90,90,13))
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig12.savefig(output_path + os.sep + 'Meridional_Energy_internal_%d_ERAI_surface_comp.jpg' % (year), dpi = 400)

# Plot the meridional latent energy transport against the latitude
fig13 = plt.figure()
plt.axhline(y=0, color='k',ls='--')
plt.plot(lat,latent_flux_int * dx / 1e+15,'b-',label='Analysis')
plt.plot(lat,np.mean(E_latent,0)/1000,'r--',label='Calculation')
plt.title('Atmospheric Meridional Latent Energy Transport %d' % (year))
plt.legend()
plt.xlabel("Laitude")
plt.xticks(np.linspace(-90,90,13))
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig13.savefig(output_path + os.sep + 'Meridional_Energy_latent_%d_ERAI_surface_comp.jpg' % (year), dpi = 400)

# Plot the meridional geopotential energy transport against the latitude
fig14 = plt.figure()
plt.axhline(y=0, color='k',ls='--')
plt.plot(lat,geopotential_flux_int * dx / 1e+15,'b-',label='Analysis')
plt.plot(lat,np.mean(E_geopotential,0)/1000,'r--',label='Calculation')
plt.title('Atmospheric Meridional Geopotential Energy Transport %d' % (year))
plt.legend()
plt.xlabel("Laitude")
plt.xticks(np.linspace(-90,90,13))
plt.ylabel("Meridional Energy Transport (PW)")
plt.show()
fig14.savefig(output_path + os.sep + 'Meridional_Energy_geopotential_%d_ERAI_surface_comp.jpg' % (year), dpi = 400)

print("--- %s seconds ---" % (time.time() - start_time))
