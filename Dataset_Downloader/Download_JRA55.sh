#!/bin/sh
#"""
#Copyright Netherlands eScience Center
#
#Function        : Download JRA55 Atmospheric Reanalysis Data
#Author          : Yang Liu
#Date            : 2017.11.28
#Last Update     : 2017.12.03
#Description     : The code aims to download atmospheric reanalysis data JRA55
#                  from JDDS FTP. The data files have the format GRIB 1.
#
#Attention       : Please refrain from making multiple connections and remaining
#                  connected for extended periods when downloading data. Users are
#                  asked to kindly limit connection time to 12 hours a day in total.
#
#Return Value    : GRIB 1 file
#variables       : Absolute Temperature              T
#                  Specific Humidity                 q
#                  Logarithmic Surface Pressure      lnsp
#                  Zonal Divergent Wind              u
#                  Meridional Divergent Wind         v
#                  Surface geopotential              z
#Caveat!!        : The data is from 90 deg south to 90 deg north (Globe).
#"""
#==============================================================================
#--------------------   specify all the parameter   ---------------------------
#==============================================================================
year_start=1979
year_end=1979
Host='ds.data.jma.go.jp'
User='jra04269'
Password='Bach1685'
#==============================================================================
touch download_JRA55.log
# specify constants
day_list=('01' '02' '03' '04' '05' '06' '07' '08' '09' '10'
           '11' '12' '13' '14' '15' '16' '17' '18' '19' '20'
					 '21' '22' '23' '24' '25' '26' '27' '28' '29' '30'
					 '31')
month_list=('01' '02' '03' '04' '05' '06' '07' '08' '09' '10' '11' '12')
#sleep 10
# log-on to the JMA Data Dissemination System (JDDS)
#!! A useful tip for spawning any process
# <<EOF
# so the ftp process is fed on stdin with everything up to EOF
#-i turns off interactive prompting.
#-n Restrains FTP from attempting the auto-login feature.
#-v enables verbose and progress.
# between heredoc no comment allowed
for ((year=${year_start};year<=${year_end};year++))
do
  for ((month=0;month<12;month++))
  do
      ftp -inv $Host << End-Of-Session
      user $User $Password
      binary
      cd JRA-55/Hist/Daily/anl_mdl/${year}${month_list[$month]}
      lcd /projects/0/blueactn/reanalysis/JRA55/subdaily/jra${year}/jra${year}${month_list[$month]}/gz
      mget anl_mdl_hgt*
      lcd /projects/0/blueactn/reanalysis/JRA55/subdaily/jra${year}/jra${year}${month_list[$month]}/T
      mget anl_mdl_tmp*
      lcd /projects/0/blueactn/reanalysis/JRA55/subdaily/jra${year}/jra${year}${month_list[$month]}/u
      mget anl_mdl_ugrd*
      lcd /projects/0/blueactn/reanalysis/JRA55/subdaily/jra${year}/jra${year}${month_list[$month]}/v
      mget anl_mdl_vgrd*
      lcd /projects/0/blueactn/reanalysis/JRA55/subdaily/jra${year}/jra${year}${month_list[$month]}/q
      mget anl_mdl_spfh*
      bye
End-Of-Session
      ftp -inv $Host << End-Of-Session
      user $User $Password
      binary
      cd JRA-55/Hist/Daily/anl_surf/${year}${month_list[$month]}
      lcd /projects/0/blueactn/reanalysis/JRA55/subdaily/jra${year}/jra${year}${month_list[$month]}/sp
      mget anl_surf*
      bye
End-Of-Session
    sleep 10
  done
  echo "Downloading complete!!" >> download_JRA55.log
  echo "year "$y >> download_JRA55.log
done
