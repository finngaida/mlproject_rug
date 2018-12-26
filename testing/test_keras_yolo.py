import sys
import os
import argparse
import glob
import random
from yolo import YOLO
from PIL import Image

'''
Uses the YOLO class to detect objects in images.

TODO: 

- Extract output coordinates for each object in every file and save it in a text file

- Implement some scoring function to be able to compare different models (e.g. accuracy vs. time needed)

- Maybe create a general version of this program in which every technique (keras, darknet, MASK-RCNN) can be compared directly

'''
def detect_img(yolo, images, output):
    for img in images:
        try:
            image = Image.open(img)
        except:
            print('Could not open image: ' + img)
        else:
            r_image = yolo.detect_image(image)
            r_image.save(output + img.split('/')[-1])
    yolo.close_session()


FLAGS = None

if __name__ == '__main__':
    intro_text = '''
    This program is made to be run in the keras-yolo3 folder of https://github.com/qqwweee/keras-yolo3
    '''
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS, description=intro_text)
    '''
    Command line options
    '''
    parser.add_argument(
        'folder', type=str,
        help='Folder in which the test images are located'
    )
    parser.add_argument(
        '-output', type=str, default='output/',
        help='Folder in which output images should be stored'
    )
    parser.add_argument(
        '-test', default=False, action='store_true',
        help='Enable testing mode, which only uses 5 randomly selected images from the input folder'
    )

    FLAGS = parser.parse_args()

    # Create output folder only if it does not exist yet to prevent accidentally mixing test results
    if not os.path.exists(FLAGS.output):
        os.makedirs(FLAGS.output)
    else:
        print("Output directory already exists!")
        sys.exit(1)

    # Some people don't end paths with /
    if FLAGS.folder[:-1] != '/':
        FLAGS.folder = FLAGS.folder + '/'

    # Use only 5 files in testing mode
    files = glob.glob(FLAGS.folder+'*.jpg')
    if FLAGS.test:
        files = random.sample(files, 5)
        print('Randomly selected images:\n')
        for file in files:
            print(file.split('/')[-1])

    detect_img(YOLO(**vars(FLAGS)), files, FLAGS.output)
