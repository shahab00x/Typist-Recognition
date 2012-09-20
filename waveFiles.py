from scipy.io import wavfile
import numpy as np
from scikits.talkbox.features import mfcc
import subprocess
#import pysox

NOISERED_CONSTANT = 0.2
DEL_WAVE_TIME_MARGIN = 0.0019
MFCC_WINDOW = 256

def getClicks(timeStamps, sampleRate, wave):
    d = DEL_WAVE_TIME_MARGIN
    if d*sampleRate < MFCC_WINDOW:
        d = float(MFCC_WINDOW)/sampleRate/2
         
    clicksList = []
    
    
    clicksList.append(wave[:int(sampleRate*d*2)])
    for t in timeStamps[1:-1]:
            clicksList.append(wave[int(sampleRate*(t-d)):int(sampleRate*(t+d))])
    clicksList.append(wave[-int(sampleRate*d*2):])
    
    return clicksList


def deNoise():
    trimTime = 0
    log = open('log.txt')
    for line in log:
        trimTime = float(line.split()[1])
        if trimTime != 0:
            break
    log.close()
    
    p1 = subprocess.Popen('sox output.wav -n trim 0 %f noiseprof noise-profile' % trimTime)
    p1.wait()
    p2 = subprocess.Popen('sox output.wav deNoised.wav noisered noise-profile %f' % NOISERED_CONSTANT)
    p2.wait()
    
#inFile = pysox.CSoxStream('output.wav')
#noiseFile = pysox.CNullFile()
#chain = pysox.CEffectsChain(inFile, noiseFile)
#trim = pysox.CEffect('trim', [b'0', str(trimTime)])
#noiseProfile = pysox.CEffect('noiseprof', [b'noise-profile'])
#chain.add_effect(trim)
#chain.add_effect(noiseProfile)
#chain.flow_effects()
#inFile.close()
#
#inFile = pysox.CSoxStream('output.wav')
#print inFile.get_signal()
#outFile = pysox.CSoxStream('deNoised.wav', 'waveData', inFile.get_signal())
#chain = pysox.CEffectsChain(inFile, outFile)
#noiseRed = pysox.CEffect('noisered', [b'noise-profile', str(NOISERED_CONSTANT)])
#chain.add_effect(noiseRed)
#chain.flow_effects()
#inFile.close()
#outFile.close()

def getMFCC():
    sampleRate, waveData = wavfile.read("deNoised.wav")
    waveData = np.float64(waveData/32768.)
    
    state = []
    inputFile = open('log.txt')
    for line in inputFile:
        state.append(float(line.split()[1]))
        state.append(float(line.split()[2]))
    
    clicks = getClicks(state, sampleRate, waveData)
    cepsList = []
    mspecList = []
    for click in clicks:
        #if len(click) != 0:
        ceps = mfcc(click, fs=sampleRate)
        cepsList.append(ceps[0][0][0])
        mspecList.append(ceps[1])

    for i in cepsList:
        print i
    return cepsList, mspecList

if __name__ == "__main__":
    deNoise()
    getMFCC()
