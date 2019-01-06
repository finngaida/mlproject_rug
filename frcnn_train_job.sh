#!/bin/bash
#SBATCH --time=12:00:00
#SBATCH --mem=8GB
#SBATCH --job-name="Train th FRCNN Keras model with some POC data"
#SBATCH --mail-type=ALL
#SBATCH --mail-user=f.m.gaida@student.rug.nl

module load Python/3.6.4-foss-2018a
module load tensorflow/1.5.0-foss-2016a-Python-3.5.2-CUDA-9.1.85

cd /data/s3838730/ml/keras-frcnn
pip install tensorflow --user
pip install -r requirements.txt --user
python train_frcnn.py -p VOCdevkit
