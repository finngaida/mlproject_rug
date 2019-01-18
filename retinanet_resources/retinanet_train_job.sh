#!/bin/bash
#SBATCH --time=3-12:00:00
#SBATCH --nodes=1
#SBATCH --tasks=1
#SBATCH --mem=32GB
#SBATCH --job-name="Retinanet train"
#SBATCH --mail-type=ALL
#SBATCH --mail-user=f.m.gaida@student.rug.nl

module load OpenCV/3.1.0-foss-2016a
module load tensorflow/1.3.1-foss-2016a-Python-2.7.12
# module load cuDNN/6.0-CUDA-8.0.61
# module load tensorflow/1.2.0-foss-2016a-Python-2.7.12-CUDA-8.0.61

cd /data/s3838730/ml/keras-retinanet
# pip install tensorflow-gpu --user
# pip install . --user
retinanet-train --weights ../resnet50_weights.h5 --freeze-backbone --weighted-average csv ../mlproject_rug/non-motorized/train_retinanet.csv csv/class_map.txt
