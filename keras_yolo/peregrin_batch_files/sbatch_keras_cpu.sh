#!/bin/bash
#SBATCH --time=40:00:00
#SBATCH --partition=regular
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --mem=32G
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=l.n.faber@student.rug.nl
#SBATCH --job-name=yolo_small_cpu
#SBATCH --output=keras_tiny_cpu.out

module load Python/3.6.4-intel-2018a
python train2.py
