import numpy as np

with open('state_data/data_0.csv','r') as f:
    lines = f.readlines()

lines = [line.strip().split(',') for line in lines]

data = []
for line in lines[0:10]:
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
 
print (lines[0:10],'\n-----\n',np.array(data))
