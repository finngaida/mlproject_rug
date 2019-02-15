#!/bin/bash
#SBATCH --time=00:30:00
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --mem=8GB
#SBATCH --job-name="Train retinanet multi gpu vgg backbone 500 batch size"
#SBATCH --mail-type=ALL
#SBATCH --mail-user=r.malhotra.1@student.rug.nl


#module load Python/2.7.12-foss-2016a
#module load Python/3.5.2-foss-2016a
#module load CUDA/8.0.61
#module load cuDNN/6.0-CUDA-8.0.61
#module load tensorflow/1.2.0-foss-2016a-Python-2.7.12-CUDA-8.0.61
#module load tensorflow/1.3.1-foss-2016a-Python-3.5.2-CUDA-8.0.61
#module load cuDNN/7.0.5.15-fosscuda-2018a
#module load CUDA/9.0.176
module load Python/2.7.12-foss-2016a
module load PIL
#module load tensorflow/1.2.0-foss-2016a-Python-2.7.12-CUDA-8.0.61

#module load tensorflow/1.5.0-foss-2016a-Python-3.5.2-CUDA-9.1.85
#module load cuDNN/7.1.4.18-CUDA-9.0.176
module load cuDNN/6.0-CUDA-8.0.61
module load CUDA/8.0.61
module load tensorflow/1.3.1-foss-2016a-Python-2.7.12-CUDA-8.0.61

cd /data/s3801128/retinanet/keras-retinanet

#pip install --upgrade pip setuptools --user
pip install numpy==1.14 --user
pip install tensorflow-gpu --user
#pip install . --user
pip install Cython==0.28 --user
#pip install progressbar2 --user
pip install configparser --user

python setup.py build_ext --inplace

python keras_retinanet/bin/train.py --weights snapshots/vgg_model.h5 --freeze-backbone --backbone vgg16 --batch-size 500  --tensorboard-dir ./logs_temp csv train_data_bp.csv class.csv
