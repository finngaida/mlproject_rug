# ML Project: Bike recognition
By Lennart, Niels, Rohit, Finn

---

## Overview
In the recent years, automatically analyzing traffic streams has become more and more popular. There seem to be many cases in which a system capable of recognizing traffic participants could be used. One of these cases was suggested by the [Gemeente Groningen](https://www.rtvnoord.nl/nieuws/201369/Stad-roept-hulp-bedrijven-in-bij-oplossen-drukte-fietsers-en-voetgangers). The city counsil would like to analyze the amount of cyclists and pedestrians using cameras. We believe this problem could be solved using machine learning. For our project we will try to come as close to an actual solution for this problem as possible, while prioritizing the machine learning aspect over the deployment of a live system.

## Relevant links

- [Dataset](http://podoce.dinf.usherbrooke.ca/challenge/dataset/)


## Train Faster R-CNN

- cd frcnn
- pip install -r requirements.txt --user
- pip install tensorflow-gpu --user
- python train_frcnn.py --path train_data_bp.txt --input_weight_path <\give input weights\> --output_weight_path <\output weight path> --config_filename <\pickle of config file>

## Test Faster R-CNN

- python measure_map.py --path test_data_final.txt --config_filename <\pickle of config file> --parser simple

## Train RetinaNet
- cd retinanet/keras-retinanet
- pip install Cython==0.28 --user
- pip install configparser --user
- python setup.py build_ext --inplace

- python keras_retinanet/bin/train.py --weights snapshots/vgg_model.h5 --freeze-backbone --backbone vgg16  --tensorboard-dir ./logs_vgg16 csv train_data_bp.csv class.csv

## Test RetinaNet

- python keras_retinanet/bin/evaluate.py --backbone resnet101 --iou-threshold 0.5 --convert-model csv test_data_final.txt class.csv <\path to weights>

## Darknet YOLO
- detect one picture:
 ./darknet detect cfg/yolov3.cfg yolov3.weights %data/kittidata/images/000145.png

- detect all pictures and store in file:
 python python/darknet.py
