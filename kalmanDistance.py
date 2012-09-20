# First predict the new mean and variance then calculate with new measurements, if there is not much 
# difference then update.
import random
import numpy as np
import shelve
from numpy import mean, divide, subtract
from collections import deque
from scipy.spatial import distance

DEQUE_MAXLEN = 75
PENALTY = 1

def dist(user, measurement):
    measurementsDB = shelve.open('DB/measurementsDB')
    savedMeasurement = measurementsDB[user]
    meanMeasurement = mean(savedMeasurement, axis=0)
    m = []
    for i in savedMeasurement:
        m.append(list(distance.cdist(meanMeasurement,i,'euclidean').diagonal()))
    
    for i in m:
        for j in i:
            j = j**2
    varMeasurement = mean(m,axis=0)
    distMatrix = distance.cdist(meanMeasurement, measurement,'euclidean')
    distArray = distMatrix.diagonal()
    measurementsDB.close()
    return distArray, varMeasurement

def analyzeNewInput(measurement,user):
    distArray, varArray = dist(user,measurement)
    
    sigmaArray = [np.sqrt(r)*PENALTY for r in varArray]
    subArray = subtract(sigmaArray, distArray)
    percentileArray = divide(subArray, sigmaArray)
    
    db = shelve.open("DB/measurementsDB")
    savedMeasurements = db[user]

    if(sum(subArray) > 0 ):
        savedMeasurements.append(measurement)
        db[user] = savedMeasurements
        db.close()
        return True, percentileArray
    
    db.close()
    return False, percentileArray

def getDataToBeSaved(measurements, username):
    q = deque([measurements[0]], DEQUE_MAXLEN)
    for i in measurements:
        q.append(i)
    db = shelve.open("DB/measurementsDB")
    db[username] = q
    db.close()
    return q
        