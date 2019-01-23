import numpy as np
import pandas as pand

# Fetching Iris Data
data = pand.read_csv('iris.txt')

# Extracting Class label from the data
col = data.columns[data.columns.str.startswith('I')]

# Seperating classlabel and data
classlabel = data[col]
features = data.drop(data.columns[4], axis=1)

X_train = features.as_matrix()

# Fuction for Calculating Initial Centriods
def initialCentriod(k=3):
    np.random.seed(0)
    cen = np.random.random((k,4))
    return cen

initialcen =initialCentriod()*5

# function to calculate the distance between centriod and data points
from math import sqrt
def pairwisedistance(datapoint,cent):
    return sqrt(np.sum((datapoint-cent)*(datapoint-cent)))

# Function for calculating Kmeans along with training data and iterations
def kmeansClustering(X_train,iterations):
    size = X_train.shape[0]
    centriod = initialCentriod(3)*5
    kvalue = centriod.shape[0]
    distance = np.zeros([size, kvalue])
    classAssign = np.zeros([size, ])
    cenn = centriod
    temp = np.zeros([1, 4])
    count = 0
    for t in range(iterations):
        # print(centriod)
        for r in range(0, size):
            for c in range(0, kvalue):
                distance[r][c] = pairwisedistance(X_train[r], centriod[c])
        classAssign = (np.argmin(distance, axis=1)).reshape((-1,))
        cenn = np.concatenate((cenn, centriod))
        print("\nThe Centriod values for each iteration:\n")
        print(centriod)
        for c in range(0, kvalue):
            temp = np.zeros([1, 4])
            count = 0
            for r in range(0, size):
                temp = temp + (0.98) * (classAssign[r] == c) * X_train[r] + (0.02) * (classAssign[r] != c) * X_train[r]
                count = count + (0.98) * (classAssign[r] == c) + (0.02) * (classAssign[r] != c)
            centriod[c] = (temp.reshape((-1,))) / (count)
    return centriod, classAssign, cenn

centroid ,classAssign,cenn = kmeansClustering(X_train,iterations=10)
print("\nKmeans Result Assignments:\n")
print(classAssign)



