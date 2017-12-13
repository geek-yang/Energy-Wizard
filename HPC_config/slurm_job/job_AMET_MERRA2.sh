#!/bin/bash
#SBATCH -N 1        # request 1 node
#SBATCH -p normal    # short partition
#SBATCH -t 1-12:00:00 # wall time limit of job

# run 16 jobs on one node
cd /projects/0/blueactn/reanalysis/MERRA2/input
for ((i=0; i<=10; i++)); do
(
  python AMET_MERRA2_Cartesius.py < ./input_stream_1/input.$i   # read time from a txt file
)&
done
# wait until all the processes are ended
wait
