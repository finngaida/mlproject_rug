#!/bin/bash
#SBATCH --time=48:00:00
#SBATCH --partition=gpu
#SBATCH --gres=gpu:2
#SBATCH --mem=8GB
#SBATCH --job-name="Train retinanet multi gpu vgg backbone 500 batch size"
#SBATCH --mail-type=ALL
#SBATCH --mail-user=r.malhotra.1@student.rug.nl


module load Python/2.7.14-fosscuda-2018a
module load tensorflow/1.2.0-foss-2016a-Python-2.7.12-CUDA-8.0.61
module load cuDNN/7.0.5.15-fosscuda-2018a

cd /data/s3801128/retinanet/keras-retinanet

#pip install --upgrade pip setuptools --user
pip install numpy --user
pip install . --user
pip install tensorflow-gpu --user

retinanet-train --weights snapshots/vgg_model.h5 --freeze-backbone --backbone vgg --batch-size 500 --multi-gpu 1 --tensorboard-dir ./logs csv train_data_bp.csv class.csv 
