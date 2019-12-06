# Creating a model architecture file



import numpy as np
from operator import add
from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers.core import Dense, Dropout
import keras.losses as kl
import random
import sys

class Collection():
    def __init__(self):
        self.learning_rate = 0.001
        #self.model = self.network()
        self.model = self.network("weight_files/nn_3.hdf5")


    def network(self, weights=None):
        model = Sequential()
        model.add(Dense(output_dim=75, activation='relu', input_dim=50))        # max 144
        #model.add(Dropout(0.15))
        model.add(Dense(output_dim=75, activation='relu'))
        #model.add(Dropout(0.15))
        model.add(Dense(output_dim=75, activation='relu'))
        #model.add(Dropout(0.15))

        model.add(Dense(output_dim=25, activation='softmax'))
        opt = Adam(self.learning_rate)
        #model.compile(loss='mse', metrics=['accuracy'], optimizer=opt)
        #model.compile(loss=kl.BinaryCrossentropy(), metrics=['accuracy'], optimizer=opt)
        model.compile(loss=kl.categorical_crossentropy, metrics=['accuracy'], optimizer=opt)

        if weights:
            model.load_weights(weights)
            print("model loaded")
        return model


def read_data(data_file="../data_gothello/state_data/data_0.csv"):
    ''' Read the csv file data into a 2d numpy array.
        Give back 2d array and the number of instances.
        ndarray data
        int num_p
    '''
    # Numpy read in my data - separate by comma, all ints.  
    data = np.loadtxt(data_file, delimiter=",", dtype=int)
    
    return data
