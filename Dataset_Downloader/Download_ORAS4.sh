#!/bin/bash
# In case, run dos2unix first since the code is made in Windows
#----------------------------------------------------------------------------------
#Copyright Netherlands eScience Center
#Function        : Download ORAS4 from ICDC Uni-Hamburg
#Author          : Yang Liu
#Date            : 2017.9.25
#Description     : The code aims to download the ocean reanalysis data ORAS4 from.
#                  ICDC Uni-Hamburg. The data is on model level. It contains a full
#                  list of files which are in need for the quantification of
#                  meridional energy transport in the ocean
#variables       : Potential Temperature                     Theta
#                  Salinity                                  s
#                  Zonal Current Velocity                    u
#                  Meridional Current Velocity               v
#                  Sea Surface Height                        ssh
#----------------------------------------------------------------------------------
# No argument in need! Changes shall be made inside the bash script
# Changes are to be made inside the input zone below
#-----------------------   Input zone   -------------------------------------------
# specify the starting year
start_year=1958
# specify the ending year
end_year=2014
#----------------------------------------------------------------------------------
echo 'Start downloading ORAS4 from ICDC University of Hamburg!'
# go to the directory
# potential Temperature
echo 'Potential Temperature on model level (ORCA)!'
cd ~
cd /project/Reanalysis/ORAS4/Monthly/Model/theta/
for (( year=${start_year}; year<=${end_year}; year++))
do
  wget ftp://ftp-icdc.cen.uni-hamburg.de/EASYInit/ORA-S4/monthly_orca1/thetao_oras4_1m_${year}_grid_T.nc.gz
  echo $year
done
echo 'Complete downloading Potential Temperature on model level (ORCA)!'
sleep 5
#-----------#-----------#------------#
# Meridional Current Velocity
echo 'Meridional Current Velocity on model level (ORCA)!'
cd ~
cd /project/Reanalysis/ORAS4/Monthly/Model/v/
for (( year=${start_year}; year<=${end_year}; year++))
do
  wget ftp://ftp-icdc.cen.uni-hamburg.de/EASYInit/ORA-S4/monthly_orca1/vo_oras4_1m_${year}_grid_V.nc.gz
  echo $year
done
echo 'Complete downloading Meridional Current Velocity on model level (ORCA)!'
sleep 5
#-----------#-----------#------------#
# Zonal Current Velocity
echo 'Zonal Current Velocity on model level (ORCA)!'
cd ~
cd /project/Reanalysis/ORAS4/Monthly/Model/u/
for (( year=${start_year}; year<=${end_year}; year++))
do
  wget ftp://ftp-icdc.cen.uni-hamburg.de/EASYInit/ORA-S4/monthly_orca1/uo_oras4_1m_${year}_grid_U.nc.gz
  echo $year
done
echo 'Complete downloading Zonal Current Velocity on model level (ORCA)!'
sleep 5
#-----------#-----------#------------#
# Sea Surface Height
echo 'Sea Surface Height on model level (ORCA)!'
cd ~
cd /project/Reanalysis/ORAS4/Monthly/Model/zos/
for (( year=${start_year}; year<=${end_year}; year++))
do
  wget ftp://ftp-icdc.cen.uni-hamburg.de/EASYInit/ORA-S4/monthly_orca1/zos_oras4_1m_${year}_grid_T.nc.gz
  echo $year
done
echo 'Complete downloading Sea Surface Height on model level (ORCA)!'
sleep 5
#-----------#-----------#------------#
# Salinity
echo 'Salinity on model level (ORCA)!'
cd ~
cd /project/Reanalysis/ORAS4/Monthly/Model/s/
for (( year=${start_year}; year<=${end_year}; year++))
do
  wget ftp://ftp-icdc.cen.uni-hamburg.de/EASYInit/ORA-S4/monthly_orca1/so_oras4_1m_${year}_grid_T.nc.gz
  echo $year
done
echo 'Complete downloading Salinity on model level (ORCA)!'
#-----------#-----------#------------#
# Finish downloading the entire dataset
#-----------#-----------#------------#
# download mesh_mask.nc
wget ftp://ftp-icdc.cen.uni-hamburg.de/EASYInit/ORA-S4/orca1_coordinates/coordinates_grid_T.nc
wget ftp://ftp-icdc.cen.uni-hamburg.de/EASYInit/ORA-S4/orca1_coordinates/coordinates_grid_U.nc
wget ftp://ftp-icdc.cen.uni-hamburg.de/EASYInit/ORA-S4/orca1_coordinates/coordinates_grid_V.nc
wget ftp://ftp-icdc.cen.uni-hamburg.de/EASYInit/ORA-S4/orca1_coordinates/mesh_mask.nc
# Mission complete!
echo 'Finish downloading the entire dataset ORAS4 on model level (ORCA)!'
