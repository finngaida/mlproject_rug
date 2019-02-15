#!/bin/bash
#SBATCH --time=20:00:00
#SBATCH --partition=regular
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=6
#SBATCH --mem=32G
#SBATCH --job-name=kerasYolo
#SBATCH --output=runKeras.out

module load Python/3.6.4-intel-2018a
python kerasyolo_runtest.py -file ../mlproject_rug/kittidata/kitti_non_motorized_clean.txt -output output_kitti -create
