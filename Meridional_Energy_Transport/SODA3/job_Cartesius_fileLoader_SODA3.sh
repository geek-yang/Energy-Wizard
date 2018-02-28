#!/bin/bash
# In case, run dos2unix first since the code is made in Windows
#----------------------------------------------------------------------------------
#Copyright Netherlands eScience Center
#Function        : Schedule and execute job for the computation of OMET from SODA3 on Cartesius
#Author          : Yang Liu
#Date            : 2018.02.26
#Last Update     : 2018.02.28
#Description     : The code aims to submit series of jobs to Cartesius for the computation of
#                  OMET from SODA3. The file will be executed in job submission.
#Return Value    : NetCFD4 data file
#Dependencies    : python
#----------------------------------------------------------------------------------
# specify date and month list for file names
year_start=2015
year_end=2015
month=('01' '02' '03' '04' '05' '06' '07' '08' '09' '10' '11' '12')
# create a time log file for monitoring the progress
cd /home/lwc16308/reanalysis/SODA3/
touch time_progress.log
touch input_year.txt
# loop for computation
for (( year=${year_start}; year<=${year_end}; year++))
do
  # go to the project directory
  cd /projects/0/blueactn/reanalysis/SODA3/5day/soda$year
  touch namelist.txt
  for (( c_month=0; c_month<=11; c_month++))
  do
    ls soda3.4.1_5dy_ocean_or_${year}_${month[${c_month}]}_* > namelist.txt
    # pass the input time from bash to python
    echo ${year} > /home/lwc16308/reanalysis/SODA3/input_year.txt
    python /home/lwc16308/reanalysis/SODA3/OMET_SODA3_cGrid_Cartesius.py < /home/lwc16308/reanalysis/SODA3/input_year.txt
    # pass variable name from bash to python
    echo 'Computation complete for '${year}${month[${c_month}]} >> /home/lwc16308/reanalysis/SODA3/time_progress.log
    # specify the output name
    #mv /home/lwc16308/reanalysis/SODA3/output/OMET_SODA3_StreamFunction_Globe_${year}.png /home/lwc16308/reanalysis/SODA3/output/OMET_SODA3_StreamFunction_Globe_${year}${month[${c_month}]}.png
    #mv /home/lwc16308/reanalysis/SODA3/output/OMET_SODA3_StreamFunction_Atlantic_${year}.png /home/lwc16308/reanalysis/SODA3/output/OMET_SODA3_StreamFunction_Atlantic_${year}${month[${c_month}]}.png
    mv /home/lwc16308/reanalysis/SODA3/output/OMET_SODA3_monthly_${year}.png /home/lwc16308/reanalysis/SODA3/output/OMET_SODA3_monthly_${year}${month[${c_month}]}.png
    mv /home/lwc16308/reanalysis/SODA3/output/SODA3_model_5daily_mom5_E_point_${year}.nc /home/lwc16308/reanalysis/SODA3/output/SODA3_model_5daily_mom5_E_point_${year}${month[${c_month}]}.nc
    mv /home/lwc16308/reanalysis/SODA3/output/SODA3_model_5daily_mom5_E_zonal_int_${year}.nc /home/lwc16308/reanalysis/SODA3/output/SODA3_model_5daily_mom5_E_zonal_int_${year}${month[${c_month}]}.nc
  done
done
