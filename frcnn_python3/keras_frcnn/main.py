from detector import FasterRCNNDetector
import cv2


def main():

    #detector = FasterRCNNDetector(model_path='./model/kitti_fcnn_last.hdf5')
    detector = FasterRCNNDetector(model_path='./model_given/resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5')#Added by rohit

    img = cv2.imread('images/000000.png')
    detector.detect_on_image(img)


if __name__ == '__main__':
    main()