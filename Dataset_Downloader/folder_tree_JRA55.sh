#!/bin/sh
#"""
#Copyright Netherlands eScience Center
#
#Function        : Build folder tree for downloading JRA55 Atmospheric Reanalysis Data
#Author          : Yang Liu
#Date            : 2017.11.29
#Last Update     : 2017.11.29
#Description     : The code aims to build a folder tree in the project space for
#                  downloading data JRA55 from JDDS FTP. The data files have the format GRIB 1.
#==============================================================================
#--------------------   specify all the parameter   ---------------------------
#==============================================================================
year_start=1981
year_end=1981
#==============================================================================
month_list=('01' '02' '03' '04' '05' '06' '07' '08' '09' '10' '11' '12')
#cd /projects/0/blueactn/reanalysis/JRA55/subdaily
cd /project/Reanalysis/JRA55/subdaily
for ((year=${year_start};year<=${year_end};year++))
do
  mkdir jra${year}
  cd jra${year}
  for ((month=0;month<12;month++))
  do
    mkdir jra${year}${month_list[$month]}
    cd jra${year}${month_list[$month]}
    mkdir T gz q sp u v
    cd ../
  done
  cd /projects/0/blueactn/reanalysis/JRA55/subdaily
done
