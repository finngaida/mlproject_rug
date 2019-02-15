import sys
import os
import argparse
import glob
import random
from yolo_runtest import YOLO
from PIL import Image
import pickle
'''
Uses the YOLO class to detect objects in images.

'''


def detect_img(yolo, images, output, create_img,resize):
    results = []
    for img in images:
        try:
            if resize:
                with open(img, 'r+b') as f:
                    with Image.open(f) as image:
                        sizes = [120,120]
                        resized = image.resize(sizes[0], sizes[1])
                        image = resized
                        #resized.save(outpath+filename, image.format)
            else:
                image = Image.open(img)
        except:
            print('Could not open image: ' + img)
        else:
            r_image, result = yolo.detect_image(image, create_img, img)
            if create_img:
                r_image.save(output + '/'+img.split('/')[-1])
            results.append(result)
    print(results)
    with open('keras_yolo_predictions.pkl','wb') as f:
        pickle.dump(results,f)
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
        '-folder', type=str,
        help='Folder in which the test images are located'
    )
    parser.add_argument(
        '-output', type=str, default='output/',
        help='Folder in which output images should be stored'
    )
    parser.add_argument(
        '-file', type=str,
        help='CSV file containing IDs of test images'
    )
    parser.add_argument(
        '-test', default=False, action='store_true',
        help='Enable testing mode, which only uses 5 randomly selected images from the input folder'
    )
    parser.add_argument(
        '-create', default=False, action='store_true',
        help='Create images showing boxes with detected classes'
    )
    parser.add_argument(
        '-resize', default=False, action='store_true',
        help='Resize images'
    )

    FLAGS = parser.parse_args()
    
    # Create output folder only if it does not exist yet to prevent accidental mixing of test results
    if FLAGS.create:
        if (os.path.exists(FLAGS.output)):
            print("Output directory already exists!")
            sys.exit(1)
        else:
            os.makedirs(FLAGS.output)

    # if FLAGS.folder:
    #     # Some people don't end paths with /
    #     if FLAGS.folder[:-1] != '/':
    #         FLAGS.folder = FLAGS.folder + '/'
    #     files = glob.glob(FLAGS.folder+'*.jpg')

    if FLAGS.file:
        files = []
        with open(FLAGS.file) as f:
            for line in f:
                image = '../kitti/training/image_2/'+line.split('\t')[0] + '.png'
                files.append(image)

    # Use only 5 files in testing mode
    if FLAGS.test:
        files = random.sample(files, 5)
        print('Randomly selected images:\n')
        for file in files:
            print(file.split('/')[-1])

    detect_img(YOLO(**vars(FLAGS)), files, FLAGS.output, FLAGS.create, FLAGS.resize)
