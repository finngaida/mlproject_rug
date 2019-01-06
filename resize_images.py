import sys
import os
from PIL import Image


def resize_images(imgpath, sizes):
    # iterate over images and apply transform
    for filename in os.listdir(imgpath):
        # make sure we have an actual image
        filename_split = filename.split('.')
        if filename_split[1] != 'jpg':
            print('.{} is not a supported image format. Use \'.jpg\' instead.'.format(filename_split[1]))
            continue

        # do the resize
        with open(imgpath+filename, 'r+b') as f:
            with Image.open(f) as image:
                resized = image.resize((int(sizes[0]), int(sizes[1])))
                # thumb = resizeimage.resize_thumbnail(image, [int(sizes[0]), int(sizes[1])])
                resized.save(imgpath+'{}-resized.{}'.format(filename_split[0], filename_split[1]), image.format)


def main():
    imgpath = ""
    size = ""

    # parse inputs
    if len(sys.argv) < 5:
        print('Usage: python3.5 resize_images.py -p <path to folder containing .jpg files> -s <\'width\'x\'height\'>\nexample: python3.5 resize_images.py -p \"MIO-TCD-Localization/train\" -s 600x600')
        return

    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "-p":
            imgpath = sys.argv[i + 1]
            i += 1
        elif sys.argv[i] == "-s":
            size = sys.argv[i + 1]
            i += 1

    # parse the size string
    sizes = size.split('x')

    resize_images(imgpath, sizes)

if __name__ == '__main__':
    main()