import sys
import os
import argparse
from PIL import Image

'''
Loops over the images in inpath and resizes all .jpg 's to the given size, then writes them to the outpath 
'''
def resize_images(inpath, outpath, sizes):
    # iterate over images and apply transform
    for filename in os.listdir(inpath):
        # make sure we have an actual image
        filename_split = filename.split('.')
        if not len(filename_split) > 1 or filename_split[1] != 'jpg' and filename_split[1] != 'jpeg':
            print('{} is not a supported image format, ignoring...'.format(filename))
            continue

        # do the resize
        with open(inpath+filename, 'r+b') as f:
            with Image.open(f) as image:
                resized = image.resize((int(sizes[0]), int(sizes[1])))
                resized.save(outpath+filename, image.format)

# store the arguments
FLAGS = None

if __name__ == '__main__':
    intro_text = '''
    Batch resize all the images in a given folder to the desired size
    '''
    parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS, description=intro_text)
    '''
    Command line options
    '''
    parser.add_argument(
        'folder', type=str,
        help='Folder in which the images are located'
    )
    parser.add_argument(
        '-output', type=str, default='output/',
        help='Folder in which output images should be stored'
    )
    parser.add_argument(
        '-size', type=str,
        help='Desired output size in the format like \'600x600\''
    )

    FLAGS = parser.parse_args()

    # Create output folder only if it does not exist yet to prevent accidentally mixing test results
    if not os.path.exists(FLAGS.output):
        os.makedirs(FLAGS.output)

    # Some people don't end paths with /
    if FLAGS.folder[:-1] != '/':
        FLAGS.folder = FLAGS.folder + '/'
    if FLAGS.output[:-1] != '/':
        FLAGS.output = FLAGS.output + '/'

    # split the size into an array already
    resize_images(FLAGS.folder, FLAGS.output, FLAGS.size.split('x'))