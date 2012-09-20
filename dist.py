'''
Created on Jun 30, 2012

@author: b
'''

from scipy.spatial import distance
import shelve

from numpy import mean



measurements = []
log = open('log.txt')
l1 = log.readline()
while l1:
    l2 = log.readline()
    if not l2:
        l2 = '0 0 0'
    entry = (float(l1.split()[2]) - float(l1.split()[1]), float(l2.split()[1]) - float(l1.split()[1]),
             float(l2.split()[1]) - float(l1.split()[2]))
    measurements.append(entry)
    l1 = l2
    
#def sumList(a, b):
#    r = []
#    for i in len(a):
#        r.append(a[i] + b[i])
#    return r
#    
#def getMeanMeasurement(measurements):
#    mean = []
#    listSum = reduce(sumList, measurements)
#    for i in listSum:
#        mean.append(i/len(measurements))
#    return mean
    
def distance(user, measurement):
    measurementsDB = shelve.open('measurmentsDB')
    savedMeasurement = measurementsDB[user]
    meanMeasurement = mean(savedMeasurement, axis=0)
    distMatrix = distance(meanMeasurement, measurement, 'cityblock')
    distArray = distMatrix.diagonal()
    
    
