#!/bin/bash
#SBATCH --time=01:00:00
#SBATCH --partition=regular
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=32G
#SBATCH --job-name=testYolo
#SBATCH --output=testyolo.out

module load Python/3.6.4-intel-2018a
python3 test_keras_yolo.py -file ../mlproject_rug/non-motorized/test.csv 
