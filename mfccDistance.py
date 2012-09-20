import shelve
from numpy import mean, sqrt, subtract, divide
from collections import deque
from scipy.spatial import distance

DEQUE_MAXLEN = 75
PENALTY = 1

def getInitialData(username, measurements):
    q = deque([measurements[0]], DEQUE_MAXLEN)
    for i in measurements:
        q.append(i)
    db = shelve.open("DB/mfccDB")
    db[username] = q
    db.close()
    return q

def distMFCC(user, measurement):
    measurementsDB = shelve.open('DB/mfccDB')
    savedMeasurement = measurementsDB[user]
    
    for i in savedMeasurement:
        print i

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

def analyzeNewMFCCInput(measurement,user):
    distArray, varArray = distMFCC(user,measurement)
    
    sigmaArray = [sqrt(r)*PENALTY for r in varArray]
    subArray = subtract(sigmaArray, distArray)
    
    percentileArray = divide(subArray, sigmaArray)
    db = shelve.open("DB/mfccDB")

    savedMeasurements = db[user]
    if(sum(subArray) > 0 ):
        savedMeasurements.append(measurement)
        db[user] = savedMeasurements
        db.close()
        return True, percentileArray
    
    db.close()
    return False, percentileArray