# Convert label numbers into one hots
import numpy as np

# One hot my data:
# https://stackoverflow.com/questions/29831489/convert-array-of-indices-to-1-hot-encoded-numpy-array

data_file = "state_data/b_labels_1.csv"
data = np.loadtxt(data_file, delimiter=",", dtype=int)
print(data)
print(len(data))
print(data.size)
print(data.max()+1)

# Do the one hot encoding
one_hot = np.zeros((data.size, data.max()+1), dtype=int)
one_hot[np.arange(data.size), data] = 1

'''
a = np.array([1, 0, 3])
b = np.zeros((a.size, a.max()+1))
b[np.arange(a.size),a] = 1
'''

file_name = "state_data/b_hot_labs_1"
np.savetxt("{}.csv".format(file_name), one_hot, delimiter=",", fmt='%i')
