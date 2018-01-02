#!/bin/bash
#SBATCH -p staging       # use the partition staging
#SBATCH -t 5-00:00:00    # set the wall clock time
cd /projects/0/blueactn/reanalysis/SODA3/5day
for (( year=1980; year<=2014; year++))
do
  # zip the file
  tar -zcvf soda${year}.tar soda${year}
  cp soda${year}.tar /archive/lwc16308/SODA3/
  rm soda${year}.tar
  rm -r soda${year}
done
