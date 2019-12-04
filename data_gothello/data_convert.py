# Name: Jordan Le
# Date: 12/4/19
# File to convert data from games into csv data files
# Goal is to learn from the winner of the game.
# Doing this the ugly way first.

# Citations:
# Remove newlines from string
# https://stackoverflow.com/questions/16566268/remove-all-line-breaks-from-a-long-string-of-text

# split string into list
# https://www.w3schools.com/python/python_regex.asp

# Replace specific instances
# https://stackoverflow.com/questions/19666626/replace-all-elements-of-python-numpy-array-that-are-greater-than-some-value

import re
import numpy as np


def write_data(data, file_name="state_data/data"):
    np.savetxt("{}.csv".format(file_name), data, delimiter=",", fmt='%i')
    print("DATA SAVED.")
    pass

def append_data(data, file_name="state_data/data"):
    with open("{}.csv".format(file_name),'ab') as f:
        np.savetxt(f, data, delimiter=",", fmt='%i')
    print("DATA APPENDED.")


def convert_labels(labels):
    # Given a value, give me back an index as my label.
    moves = ['a5','b5','c5','d5','e5',
            'a4','b4','c4','d4','e4',
            'a3','b3','c3','d3','e3',
            'a2','b2','c2','d2','e2',
            'a1','b1','c1','d1','e1']

    temp_labels = []
    for lab in labels:
        if lab in moves:
            lab = moves.index(lab)
            #print(lab)
            temp_labels.append(lab)
    print(temp_labels)
    conv_labels = np.asarray(temp_labels)
    print(conv_labels)
    return conv_labels  # Give back numpy array
    

# Get the data for winning log
def get_log_data():
    with open("gothello-runs-depth3/2-20205/white-log") as f:
        data_text = f.readlines()   # Read in the text file
        data_text.pop(0)            # Remove the "logging"
        print(data_text)
        merged_data = ''.join(data_text)        # Put into one big string
        temp = merged_data.replace('\n','')     # Remove newlines
        x = re.split("\d+", temp)               # Split based on set of numbers
        x.pop(-1)                               # Remove the last element ''
        print(x)

        # Verify correct lengths
        print(len(x))
        for tf in x:
            print(len(tf))

        x2 = [list(xs) for xs in x]
        
        ndata = np.asarray(x2)
        print(ndata)
      
        ndata[ndata == 'w'] = 2   # Winner will be 2
        ndata[ndata == 'b'] = 1   # Loser will be 1
        ndata[ndata == '.'] = 0   # Blank will be 0
        ndata2 = ndata.astype(int)
        print(ndata2)
        return ndata2




# Get the data from winning output
def get_out_data():
    with open("gothello-runs-depth3/2-20205/white-output") as f2:
        labels = []
        out_data = f2.readlines()   # Read in the text file
        winner = out_data[-1]
        print(winner)

        out_data.pop(-1)
        print(out_data)

        for output in out_data:
            if "me:" in output:
                lab = output.replace('\n','')
                print(lab)
                labels.append(lab[-2:])
        
        labels.pop(-1)
        print(labels)

        nlabels = np.asarray(labels)
        print(nlabels)

        conv_labels = convert_labels(nlabels)
        return conv_labels


# Call Main and do the good stuff
if __name__== "__main__" :
    state_data = get_log_data()
    state_labels = get_out_data()
    append_data(state_data)
    append_data(state_labels, "state_data/labels")
    print("wrote to files!")
