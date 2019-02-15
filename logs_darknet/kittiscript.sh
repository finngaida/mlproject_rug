#!/bin/bash
#SBATCH --time=100:00:00
#SBATCH --nodes=1
#SBATCH --tasks=1
#SBATCH --mem=32GB
#SBATCH --job-name="kitti"
#SBATCH --mail-type=ALL
#SBATCH --mail-user=n.r.r.broekmans@student.rug.nl

cd /data/s2589036/ml/ml/darknet
python python/darknet.py

