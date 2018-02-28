#!/bin/bash
#SBATCH -p staging       # use the partition staging
#SBATCH -t 5-00:00:00    # set the wall clock time
cd /projects/0/blueactn/reanalysis/SODA3/5day
for (( year=2000; year<=2014; year++))
do
  # unzip the file
  cp /archive/lwc16308/SODA3/soda${year}.tar ./
  tar -zxvf soda${year}.tar
  rm soda${year}.tar
done
