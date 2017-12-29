#!/bin/bash
# In case, run dos2unix first since the code is made in Windows
#----------------------------------------------------------------------------------
#Copyright Netherlands eScience Center
#Function        : Schedule and execute job for the post-processing of EC-Earth output on Cartesius
#Author          : Yang Liu
#Date            : 2017.12.13
#Last Update     : 2017.12.15
#Description     : The code aims to submit series of jobs to Cartesius for the post-processing
#                  of EC-Earth model output. The file will be executed in job submission. The
#                  post-processing mainly includes the computation of meridional energy transport
#                  in the atmosphere.
#Return Value    : NetCFD4 data file
#Dependencies    : CDO, python
#variables       : Output of fields on Gaussian Grid        ICMGGECE3
#                  Output of fields on Spectral Grid        ICMSHECE3

#Caveat!!        : Spatial and temporal coverage
#                  The model uses TL511 spectral resolution with N256 Gaussian Grid.
#                  For postprocessing, the spectral fields will be converted to grid.
#                  The spatial resolution of Gaussian grid is 512 (lat) x 1024 (lon)
#                  It uses hybrid vertical levels and has 91 vertical levels.
#                  The simulation starts from 00:00:00 01-01-1979.
#                  The time step in the dataset is 3 hours.
#                  00:00 03:00 06:00 09:00 12:00 15:00 18:00 21:00
#----------------------------------------------------------------------------------
# specify the global counter
counter=1
# specify date and month list for file names
year=1979
month=('01' '02' '03' '04' '05' '06' '07' '08' '09' '10' '11' '12')
# specify the counter for month
c_month=0
# loop for post-processing
for (( counter=1; counter<=1; counter++))
do
  # go to the project directory
  cd /projects/0/blueactn/ECEARTH/ECE3/output/ifs
  # adjust the month counter and the year
  if [ ${c_month} -gt 11 ]
  then
    c_month=0
    year=$((year+1))
  fi
  # start the post-processing
  if [ $counter -gt 99 ]
  then
    cd ./$counter
  elif [ $counter -gt 9 ]
  then
    cd ./0$counter
  else
    cd ./00$counter
  fi
  # convert the spectral field to grid field
  cp ICMGGECE3+${year}${month[${c_month}]} /projects/0/blueactn/reanalysis/temp/ICMGGECE3+${year}${month[${c_month}]}_gp
  cdo sp2gpl ICMSHECE3+${year}${month[${c_month}]} /projects/0/blueactn/reanalysis/temp/ICMSHECE3+${year}${month[${c_month}]}_sp2gpl
  # switch to the home directory
  cd /home/lwc16308/ecearth_postproc/AMET
  echo 'Finish the conversion from spectral field to Gaussian grid'${year}${month[${c_month}]} >> log_time.log
  date >> log_time.log
  # pass variable name from bash to python
  echo ${year}${month[${c_month}]} > input.txt
  python AMET_ECearth_1st_AMIP.py < ./input.txt
  # record
  echo 'year and month'${year}${month[${c_month}]} >> log_time.log
  date >> log_time.log
  # remove the temporary file
  rm /projects/0/blueactn/reanalysis/temp/ICMSHECE3+${year}${month[${c_month}]}_sp2gpl
  rm /projects/0/blueactn/reanalysis/temp/ICMGGECE3+${year}${month[${c_month}]}_gp
  # increase the month counter
  c_month=$((c_month+1))
done
