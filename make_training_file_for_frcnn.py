import pandas as pd


path_to_csv = '../MIO-TCD-Localization/gt_train.csv'
IMG_FOLDER_PATH = '/Users/rohitmalhotra/Desktop/RUG/Semester1b/MachineLearning/project/MIO-TCD-Localization/train/'
IMG_EXTN = '.jpg'

colnames_given= ['IMG_NAME','class_name','x1','y1','x2','y2']


def start():
    tcg = pd.read_csv(path_to_csv, names=colnames_given, header=None)  # training csv given
    rearranged_colmns = ['IMG_NAME', 'x1', 'y1', 'x2', 'y2', 'class_name']
    tcg = tcg[rearranged_colmns]
    tcg.rename(columns={'IMG_NAME': 'IMG_ABS_PATH'}, inplace=True)
    tcg['IMG_ABS_PATH'] = tcg['IMG_ABS_PATH'].apply(lambda x: IMG_FOLDER_PATH + ('{0:0>8}'.format(x)) + IMG_EXTN)
    tcg.to_csv('train_data.txt',index=False,header=False)



if __name__ == '__main__':
    start()
