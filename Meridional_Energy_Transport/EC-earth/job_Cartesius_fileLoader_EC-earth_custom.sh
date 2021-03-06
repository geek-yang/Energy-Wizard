#!/bin/bash
# In case, run dos2unix first since the code is made in Windows
#----------------------------------------------------------------------------------
#Copyright Netherlands eScience Center
#Function        : Schedule and execute job for the post-processing of EC-Earth output on Cartesius
#Author          : Yang Liu
#Date            : 2017.12.13
#Last Update     : 2017.12.13
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
counter=36
# specify date and month list for file names
year=1981
#month=('01' '02' '03' '04' '05' '06' '07' '08' '09' '10' '11' '12')
month=12
# loop for post-processing
# go to the project directory
cd /projects/0/blueactn/ECEARTH/ECE3/output/ifs
# adjust the month counter and the year
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
cp ICMGGECE3+${year}${month} /projects/0/blueactn/reanalysis/temp/ICMGGECE3+${year}${month}_gp
cdo sp2gpl ICMSHECE3+${year}${month} /projects/0/blueactn/reanalysis/temp/ICMSHECE3+${year}${month}_sp2gpl
date # print the curent time
# switch to the home directory
cd /home/lwc16308/ecearth_postproc/AMET
echo 'Finish the conversion from spectral field to Gaussian grid'${year}${month} >> log_time_custom.log
date >> log_time_custom.log
# pass variable name from bash to python
echo ${year}${month} > ./input_custom.txt
python AMET_ECearth_1st_AMIP_custom.py < ./input_custom.txt
# record
echo 'year and month'${year}${month} >> log_time_custom.log
date >> log_time_custom.log
# remove the temporary file
rm /projects/0/blueactn/reanalysis/temp/ICMGGECE3+${year}${month}_gp
rm /projects/0/blueactn/reanalysis/temp/ICMSHECE3+${year}${month}_sp2gpl

