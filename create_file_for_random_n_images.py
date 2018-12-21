import pandas as pd

def start(n):
    colnames= ['IMG_ABS_PATH', 'class_name', 'x1', 'y1', 'x2', 'y2']
    odf = pd.read_csv('train_data.txt',names=colnames)
    samples = odf.sample(n)
    samples.to_csv('train_data_samples.txt', index=False,header=False)




if __name__ == '__main__':
    start(2000)