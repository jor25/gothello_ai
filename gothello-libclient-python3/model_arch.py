# Creating a model architecture file
# This will be what I use to train based off previous winning games.

# Note: change self.network file path for different weights or scratch training.

# References:
# myself - gen_dino game
# https://github.com/jor25/Dino_Game/blob/master/collect_states.py


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
        #self.model = self.network()                        # No initial weights
        self.model = self.network("weight_files/nn_3.hdf5") # Using my trained weights

    def network(self, weights=None):
        # Create my model
        model = Sequential()    
        model.add(Dense(output_dim=75, activation='relu', input_dim=50))
        model.add(Dense(output_dim=75, activation='relu'))
        model.add(Dense(output_dim=75, activation='relu'))
        model.add(Dense(output_dim=25, activation='softmax'))
        opt = Adam(self.learning_rate)
        
        # Compile model
        model.compile(loss=kl.categorical_crossentropy, metrics=['accuracy'], optimizer=opt)

        # Load weights if they're available
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
