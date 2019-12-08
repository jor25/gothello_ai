# Jordan Le
# Model training file:

# References:
# Stratify example
# https://stackoverflow.com/questions/29438265/stratified-train-test-split-in-scikit-learn

# Sklearn train_test_split
# https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html

import numpy as np
import model_arch as ma
from sklearn.model_selection import train_test_split


if __name__ == "__main__":
    
    with open('../data_gothello/state_data/data_0.csv','r') as f:
        lines = f.readlines()

    # Got this section of code from ta to convert my 25 entries into 50 one hot
    lines = [line.strip().split(',') for line in lines]

    data = []
    for line in lines:
        row = []
        for val in line:
            feature = [0,0]
            if val == '1':
                feature[0] = 0 # winningPlayerPresent
                feature[1] = 1 # losingPlayerPresent
            elif val == '2':
                feature[0] = 1
                feature[1] = 0
            row.append(feature)
        row = np.array(row).flatten()
        data.append(row)

    data = np.array(data)
    nn = ma.Collection()
    
    labels = ma.read_data("../data_gothello/state_data/hot_labs_0.csv")     # Get the labels
    #labels = ma.read_data("../data_gothello/state_data/labels_1.csv")     # Get the labels

    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.3, stratify=labels)
    print("\n\nData was split\n\n")
    print(X_train.shape)
    print(y_train.shape)

    #'''
    # Train Model
    nn.model.fit(X_train, y_train, epochs=10, verbose=1)        # Change epochs for more training

    # Verify Model
    loss, acc = nn.model.evaluate(X_test, y_test, verbose=2)    

    print("Loss: {}\tAcc: {}".format(loss, acc))

    nn.model.save_weights('weight_files/nn_2.hdf5')         # Change this to save new weight file
    print ("Weights saved!")
    #'''
