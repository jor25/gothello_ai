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
import os

STATUS = False

def write_data(data, file_name="state_data/data"):
    np.savetxt("{}.csv".format(file_name), data, delimiter=",", fmt='%i')
    
    if STATUS:
        print("DATA SAVED.")
    pass


def append_data(data, file_name="state_data/data"):
    with open("{}.csv".format(file_name),'ab') as f:
        np.savetxt(f, data, delimiter=",", fmt='%i')
    
    if STATUS:
        print("DATA APPENDED.")


def convert_labels(labels):
    # Given a value, give me back an index as my label.
    ''' # Delete in cleanup
    # THIS IS HOW THE THING IS FOR MY THING!!! (BART'S UPSIDEDOWN)
    moves = ['a1','b1','c1','d1','e1',
            'a2','b2','c2','d2','e2',
            'a3','b3','c3','d3','e3',
            'a4','b4','c4','d4','e4',
            'a5','b5','c5','d5','e5']
    '''
    # according to bart's data - this is how the field is layed out!!!
    #'''        
    moves = ['a5','b5','c5','d5','e5',
            'a4','b4','c4','d4','e4',
            'a3','b3','c3','d3','e3',
            'a2','b2','c2','d2','e2',
            'a1','b1','c1','d1','e1']
    #'''

    temp_labels = []
    for lab in labels:
        if lab in moves:
            lab = moves.index(lab)
            #print(lab)
            temp_labels.append(lab)
    #print(temp_labels)
    conv_labels = np.asarray(temp_labels)
    
    if STATUS:
        print(conv_labels)
    
    return conv_labels  # Give back numpy array
    

# Open gthd and look at who won the game example.
# Give back the char for winner and loser
def who_won(path="gothello-runs-depth3/2-20205"):
    file_path = "{}/gthd".format(path)
    
    if STATUS:
        print("IT WORKED {}".format(file_path))

    #with open("gothello-runs-depth3/2-20205/gthd") as f:
    with open(file_path) as f:
        gthd_data = f.readlines()   # Read in the text file
        win_line = gthd_data[-1]    # Get the last line
        
        if STATUS:
            print(win_line)
        
        if "White" in win_line:
            if STATUS:
                print("white")
            win = 'w'
            loss = 'b'

        elif "Black" in win_line:
            if STATUS:
                print("black")
            win = 'b'
            loss = 'w'

        else:
            if STATUS:
                print(win_line)

    return win, loss


# Take the best player
def assign_data(ndata, winner='w', loser='b'):
    ndata[ndata == winner] = 2  # Winner will be 2
    ndata[ndata == loser] = 1   # Loser will be 1
    ndata[ndata == '.'] = 0     # Blank will be 0
    ndata2 = ndata.astype(int)
    
    if STATUS:
        print(ndata2)
    return ndata2


# Choose black or white files
def choose_file(win):
    if win == 'w':
        name = "white"
    else:
        name = "black"
    
    return name


# Get the data for winning log
def get_log_data(win, loss, path="gothello-runs-depth3/2-20205"):
    #file_name = "gothello-runs-depth3/2-20205/{}-log".format(choose_file(win))
    file_name = "{}/{}-log".format(path, choose_file(win))

    #with open("gothello-runs-depth3/2-20205/white-log") as f:
    with open(file_name) as f:
        data_text = f.readlines()   # Read in the text file
        data_text.pop(0)            # Remove the "logging"
        #print(data_text)
        merged_data = ''.join(data_text)        # Put into one big string
        temp = merged_data.replace('\n','')     # Remove newlines
        x = re.split("\d+|-\d+", temp)          # Split based on set of numbers, also remove neg sign
        x.pop(-1)                               # Remove the last element ''
        #print(x)

        # Verify correct lengths
        '''
        print(len(x))
        for tf in x:
            print(len(tf))
        '''
        
        # Convert strings to lists
        x2 = [list(xs) for xs in x]
        
        ndata = np.asarray(x2)
        if STATUS:
            print(ndata)
     
        '''
        ndata[ndata == 'w'] = 2   # Winner will be 2
        ndata[ndata == 'b'] = 1   # Loser will be 1
        ndata[ndata == '.'] = 0   # Blank will be 0
        ndata2 = ndata.astype(int)
        print(ndata2)
        return ndata2
        '''
        # Dynamically call a winner and loser - train on winner
        return assign_data(ndata, win, loss)





# Get the data from winning output
def get_out_data(win, path="gothello-runs-depth3/2-20205"):
    #file_name = "gothello-runs-depth3/2-20205/{}-output".format(choose_file(win))
    file_name = "{}/{}-output".format(path, choose_file(win))

    #with open("gothello-runs-depth3/2-20205/white-output") as f2:
    with open(file_name) as f2:
        labels = []
        out_data = f2.readlines()   # Read in the text file
        winner = out_data[-1]
        #print(winner)

        out_data.pop(-1)
        #print(out_data)

        for output in out_data:
            if "me:" in output:
                lab = output.replace('\n','')
                #print(lab)
                labels.append(lab[-2:])
        
        labels.pop(-1)
        #print(labels)

        nlabels = np.asarray(labels)
        
        if STATUS:
            print(nlabels)

        conv_labels = convert_labels(nlabels)
        return conv_labels


# Call Main and do the good stuff
if __name__== "__main__" :
    # Testing this out
    #'''
    count = 0   # Collect data in incremental files
    increments = 0

    for (root,dirs,files) in os.walk("gothello-runs-depth3", topdown=True): 
        try:
            count += 1   # Keep track of how many files I've been through
            if count % 25000 == 0: # New file every 25,000 files 
                increments += 1     # Go to a new file

            #str_datafile = "state_data/data_{}".format(increments)
            #str_labelfile = "state_data/labels_{}".format(increments)

            win, loss = who_won(root)
            str_datafile = "state_data/{}_data_{}".format(win, increments)
            str_labelfile = "state_data/{}_labels_{}".format(win, increments)
            
            if STATUS:
                print (root) 
                #print (dirs) 
                #print (files) 
                print(win)
                print(loss)

            state_data = get_log_data(win, loss, root)
            state_labels = get_out_data(win, root)
            append_data(state_data, str_datafile)
            append_data(state_labels, str_labelfile)

            if count % 25000 == 0: # New file every 25,000 files 
                print("************************************************************************")
                print("FILES SAVED TO: {}\t{}".format(str_datafile, str_labelfile))
                print("************************************************************************")
        
        except (KeyboardInterrupt, SystemExit):
            raise

        except:
            if STATUS:
                print("Something went wrong here: {}".format(root))
            
    #'''
    
    '''
    win, loss = who_won("gothello-runs-depth3/2-20207")
    state_data = get_log_data(win, loss, "gothello-runs-depth3/2-20207")
    state_labels = get_out_data(win, "gothello-runs-depth3/2-20207")
    write_data(state_data)
    write_data(state_labels, "state_data/labels")
    print("wrote to files!")
    '''



