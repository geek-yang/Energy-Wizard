#!/bin/bash
# In case, run dos2unix first since the code is made in Windows
#----------------------------------------------------------------------------------
#Copyright Netherlands eScience Center
#Function        : Schedule and execute job for the computation of OMET from SODA3 on Cartesius
#Author          : Yang Liu
#Date            : 2018.02.26
#Last Update     : 2018.02.26
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
touch time_progress_statistics.log
touch input_year_statistics.txt
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
    echo ${year} > /home/lwc16308/reanalysis/SODA3/input_year_statistics.txt
    python /home/lwc16308/reanalysis/SODA3/Statistics_SODA3_OHC.py < /home/lwc16308/reanalysis/SODA3/input_year_statistics.txt
    # pass variable name from bash to python
    echo 'Computation complete for '${year}${month[${c_month}]} >> /home/lwc16308/reanalysis/SODA3/time_progress_statistics.log
    # specify the output name
    mv /projects/0/blueactn/reanalysis/SODA3/statistics/SODA3_model_5daily_mom5_OHC_point_${year}.nc /projects/0/blueactn/reanalysis/SODA3/statistics/SODA3_model_5daily_mom5_OHC_point_${year}${month[${c_month}]}.nc
    mv /projects/0/blueactn/reanalysis/SODA3/statistics/SODA3_model_5daily_mom5_psi_point_${year}.nc /projects/0/blueactn/reanalysis/SODA3/statistics/SODA3_model_5daily_mom5_psi_point_${year}${month[${c_month}]}.nc
    mv /projects/0/blueactn/reanalysis/SODA3/statistics/SODA3_model_5daily_mom5_var_point_${year}.nc /projects/0/blueactn/reanalysis/SODA3/statistics/SODA3_model_5daily_mom5_var_point_${year}${month[${c_month}]}.nc
  done
done
