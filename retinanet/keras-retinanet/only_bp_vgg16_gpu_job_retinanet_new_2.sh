#!/bin/bash
#SBATCH --time=72:00:00
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --mem=8GB
#SBATCH --job-name="2nd Time,20-> Train retinanet 1 gpu vgg16 backbone"
#SBATCH --mail-type=ALL
#SBATCH --mail-user=r.malhotra.1@student.rug.nl

module load Python/2.7.12-foss-2016a
module load PIL
module load cuDNN/6.0-CUDA-8.0.61
module load CUDA/8.0.61
module load tensorflow/1.3.1-foss-2016a-Python-2.7.12-CUDA-8.0.61


cd /data/s3801128/retinanet/keras-retinanet

pip install numpy==1.14 --user
pip install tensorflow-gpu --user
pip install Cython==0.28 --user
pip install configparser --user


python setup.py build_ext --inplace



python keras_retinanet/bin/train.py --weights snapshots/vgg16_csv_01.h5 --freeze-backbone --backbone vgg16  --tensorboard-dir ./logs_vgg16 csv train_data_bp.csv class.csv 
