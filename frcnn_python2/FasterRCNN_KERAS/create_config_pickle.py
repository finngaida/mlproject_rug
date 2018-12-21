import pickle
from keras_frcnn.config import Config


def start():
    c=Config()
    with open('config.pickle', 'wb') as f:
        pickle.dump(c,f, protocol=pickle.HIGHEST_PROTOCOL)



if __name__ == '__main__':
    start()