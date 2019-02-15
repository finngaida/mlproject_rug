#!/bin/bash
#SBATCH --time=01:00:00
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --mem=8GB
#SBATCH --job-name="0.6resnet50 frcnn test gpu"
#SBATCH --mail-type=ALL
#SBATCH --mail-user=r.malhotra.1@student.rug.nl

module load Python/3.6.4-foss-2018a
module load tensorflow/1.5.0-foss-2016a-Python-3.5.2-CUDA-9.1.85
module load cuDNN/7.1.4.18-CUDA-9.0.176

cd /data/s3801128/frcnn
pip install -r requirements.txt --user
pip install tensorflow-gpu --user




python measure_map.py --path test_data_final.txt --config_filename config_only_bp_res50.pickle --parser simple | tee test_result_resnet50_gpu_iou06.txt
