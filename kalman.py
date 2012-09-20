# First predict the new mean and variance then calculate with new measurements, if there is not much 
# difference then update.
import random
import numpy as np
import shelve
from numpy import mean

class stru:
    def __init__(self,mu=0,sigma=0):
        self.mu = np.float64(mu)
        self.sigma = np.float64(sigma)
        
def update(mean1, var1, mean2, var2):
    new_mean = (var2 * mean1 + var1 * mean2) / (var1 + var2)
    new_var = 1/(1/var1 + 1/var2)
    return [new_mean, new_var]

def predict(mean1, var1, mean2, var2):
    new_mean = mean1 + mean2
    new_var = var1 + var2
    return [new_mean, new_var]

def meanAndVariance(l):
    m = 0.0
    m = sum(l)/len(l)
    v = 0.0
    for i in l:
        v += (i-m)**2
    v = v/len(l)
    if m == 0: m=0.00000001
    if v == 0: v=0.00000001
    return [m,v]

def distance(user, measurement):
    measurementsDB = shelve.open('measurmentsDB')
    savedMeasurement = measurementsDB[user]
    meanMeasurement = mean(savedMeasurement, axis=0)
    distMatrix = distance(meanMeasurement, measurement, 'cityblock')
    distArray = distMatrix.diagonal()    
    measurementsDB.close()
    return distArray

measurement_sig = .02
predict_sig = .007

def getDataToBeSaved(input1, input2,username):
    global measurement_sig
    global predict_sig
#    global md
    md = shelve.open("DB/predictSigmaDB",writeback = True)
    saved = []
    mu = 0
    sigma = 0
    for i in range(len(input1)):
        temp = []
        temp2 = []
        for j in range(len(input1[i])):
            temp.append(np.float64(input1[i][j]))
            temp.append(np.float64(input2[i][j]))
            mu,sigma = meanAndVariance(temp)
            s = stru(mu,sigma)
            temp2.append(s)
            temp = []
        saved.append(temp2)
        temp2 = []
    saved = np.copy(saved)
    md[username] = predict_sig
    md.close()
    return saved

#newInput = [[random.uniform(0,5) for r in range(5)] for x in range(4)]
def analyzeNewInput(saved, newInput, username):
    global predict_sig
    global measurement_sig
    portion = 1./2
    md = shelve.open("DB/predictSigmaDB", writeback=True)
    predict_sig = md[username]
    
    p = np.copy(saved) # predict the next round of data
    for i in range(len(p)):
        for j in range(len(p[i])):
            p[i][j].mu,p[i][j].sigma = predict(p[i][j].mu, p[i][j].sigma, 0, predict_sig)
    b = []
    mu = 0
    sigma = 0
    for i in p:
#        l = []
#        for j in range(len(i)):
#            l.append(i[j].mu)
#        mu,sigma = meanAndVariance(l)
        mu = sum([r.mu for r in i])/len(i)
        sigma = sum([np.sqrt(r.sigma) for r in i])/len(i)
        sigma = sigma**2
        b.append(stru(mu,sigma))
        mu = 0
        sigma = 0
    mu = sum([r.mu for r in b])/len(b)
    sigma = sum([np.sqrt(r.sigma) for r in b])/len(b)
    sigma = sigma**2
    c = stru(mu,sigma)
            
    db = [sum(r)/len(r) for r in newInput]
    dc = sum(db)/len(db)
    print "c.mu,c.sigma,dc",c.mu,c.sigma,dc,np.sqrt(c.sigma)
    if dc <= c.mu + np.sqrt(c.sigma)*portion and dc >= c.mu-np.sqrt(c.sigma)*portion:
        predict_sig = meanAndVariance([c.mu,dc])[1]
        print "predict_sig",predict_sig
        passed = True
        print "pass"
        for i in range(len(saved)):
            for j in range(len(saved[i])):
                saved[i][j].mu,saved[i][j].sigma = predict(saved[i][j].mu, saved[i][j].sigma,0, predict_sig)
                saved[i][j].mu,saved[i][j].sigma = update(saved[i][j].mu, saved[i][j].sigma, newInput[i][j], measurement_sig)
        md[username] = predict_sig
    else:
        passed = False
        print "fail"
    md.close()
    return passed, saved