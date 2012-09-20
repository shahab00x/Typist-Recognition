from scipy.spatial import distance
import shelve
import numpy

def distance(user, measurements):
    measurementsDB = shelve.open('measurementsDB')
    savedMeasurements = measurementsDB[user]
    distMatrix = distance.cdist(measurements, savedMeasurements, 'cityblock')
    distanceArray = numpy.diagonal(distMatrix)          #top left -> bottom right
    sumOfDistance = sum(distanceArray)
    
