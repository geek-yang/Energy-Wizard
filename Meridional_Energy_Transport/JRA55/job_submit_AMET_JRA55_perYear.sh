#!/bin/bash
#SBATCH -n 1        # request 1 node
#SBATCH -p normal    # normal partition
#SBATCH -t 02:00:00 # wall time limit of job
python AMET_JRA55_Cartesius_memoryWise_perMonth_custom.py
