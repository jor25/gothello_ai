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


import re
import numpy as np

# Get the data for winning log
with open("gothello-runs-depth3/2-20205/white-log") as f:
    data_text = f.readlines()   # Read in the text file
    data_text.pop(0)            # Remove the "logging"
    print(data_text)
    merged_data = ''.join(data_text)        # Put into one big string
    temp = merged_data.replace('\n','')     # Remove newlines
    x = re.split("\d+",temp)                # Split based on set of numbers
    x.pop(-1)                               # Remove the last element ''
    print(x)

    # Verify correct lengths
    print(len(x))
    for tf in x:
        print(len(tf))





# Get the data from winning output
with open("gothello-runs-depth3/2-20205/white-output") as f2:
    out_data = f2.readlines()   # Read in the text file
    print(out_data)

    merge_out_data = ''.join(out_data)        # Put into one big string
    print(merge_out_data)
    temp2 = merge_out_data.replace('\n','')     # Remove newlines
    print(temp2)
