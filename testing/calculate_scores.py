import argparse
from prettytable import PrettyTable

'''Extracts information from the truth file. This file is assumed to be formatted as follows:
   FILE_ID,CLASS_NAME,X1,Y1,X2,Y2
'''
def extract_truth(truth):
    print("Extracting truth file...")
    truth_dict = {}
    with open(truth,'r') as f:
        for line in f:
            entry = line.split(',')
            file_id,class_name,x1,y1,x2,y2 = entry[0],entry[1],entry[2], entry[3], entry[4], entry[5]
            if file_id not in truth_dict:
                truth_dict[file_id] = {class_name:[[x1,y1,x2,y2]]}
            else:
                if class_name not in truth_dict[file_id]:
                    truth_dict[file_id][class_name] = [[x1,y1,x2,y2]]
                else:
                    truth_dict[file_id][class_name].append([x1,y1,x2,y2])
    return truth_dict

def extract_predictions(predicitions, source):
    print("Extracting predictions file...")
    predictions_dict = {}
    with open(predicitions) as f:
        for line in f:
            # More source formats can be added here
            if(source=='kerasyolo'):
                filename,coordinates,class_name,certainty,time = line.split()
                file_id = filename.split('.')[0]
                x1,y1,x2,y2 = coordinates.split(',')
            if file_id not in predictions_dict:
                predictions_dict[file_id] = {class_name:[[x1,y1,x2,y2]]}
            else:
                if class_name not in predictions_dict[file_id]:
                    predictions_dict[file_id][class_name] = [[x1,y1,x2,y2]]
                else:
                    predictions_dict[file_id][class_name].append([x1,y1,x2,y2])

    return predictions_dict

def IoU(prediction_dict, truth_dict, class_name):
    # for each image predicted
        # if class in predictred classes
            # if image in truth
                # if class in image-truth
                    # for each location predicted
                        #for each location in truth
                            #calculate iou
                    #save max iou






FLAGS = None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        argument_default=argparse.SUPPRESS,
        description='''This program is made to calculate various test scores of object detection algorithms using a ground truth file and predicitions file. Requires PrettyTable for output.''',
        epilog='''Made by Lennart Faber.''')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    '''
    Command line options
    '''
    parser.add_argument(
        'truth', type=str,
        help='Annotation file containing ground truth. (e.g. test.csv)'
    )
    parser.add_argument(
        'predictions', type=str,
        help='File containing predicitions'
    )
    parser.add_argument(
        'source', type=str,
        help='Specify the format of the file containing the predictions. Current options: kerasyolo'
    )

    FLAGS = parser.parse_args()

    # Store truth in dict
    truth_dict = extract_truth(FLAGS.truth)
    # Store predictions in dict
    prediction_dict = extract_predictions(FLAGS.predictions,FLAGS.source)

    # First metric: IoU (Intersect over Union) for pedestrians
    pedestrian_iou = IoU(prediction_dict, truth_dict)











