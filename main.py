from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import *
import sys
import time
import shelve
import mainWindow
from kalmanDistance import *
import os, signal
from waveFiles import *
from mfccDistance import getInitialData, analyzeNewMFCCInput

INITIAL_DATA_COUNT = 2
                
     
class Main(QMainWindow, mainWindow.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.username = ""
        self.password = ""
        self.lineEditPassword.setMain(self)
        self.initialMeasurements = {}
        self.initialPasswords = {}
        self.initialMFCC = {}
        
        userPassDB = shelve.open('DB/UserPassDB')
        for username in userPassDB:
            self.initialPasswords[username] = userPassDB[username][0]
            self.initialMeasurements[username] = [userPassDB[username][1]] * INITIAL_DATA_COUNT
            
            
        userPassDB.close()
        
        self.lineEditUserName.setFocus()
        
    @pyqtSignature("")
    def on_pushButtonStart_clicked(self):
        self.username = str(self.lineEditUserName.text())
        self.password = str(self.lineEditPassword.text())
        self.lineEditPassword.setText("")

        self.lineEditUserName.setFocus()

        measurements = []
        log = open('log.txt')

        log.seek(0)
        l1 = log.readline()
        while l1:
            l2 = log.readline()
            if l1.split()[0] != '9':
                if l2:
                    entry = (float(l1.split()[2]) - float(l1.split()[1]), float(l2.split()[1]) - float(l1.split()[1]),
                             float(l2.split()[1]) - float(l1.split()[2]))
                else:
                    entry = (float(l1.split()[2]) - float(l1.split()[1]), 0 - float(l1.split()[1]), 0 - float(l1.split()[2]))
                measurements.append(entry)
            l1 = l2
            
        deNoise()
        mfccRet = getMFCC()
        cepsList = mfccRet[0]
        mspecList = mfccRet[1]
#        waves = shelve.open("DB/deNoisedDB")

        if self.username not in self.initialPasswords:
            self.initialPasswords[self.username] = self.password
        elif self.initialPasswords[self.username] != self.password:
            self.labelStatus.setText("Mismatch.")
            return None
        
        typingSequenceFlag = True

        try:
            if len(measurements) == len(self.initialMeasurements[self.username][0]):
                self.initialMeasurements[self.username].append(measurements)
                self.initialMFCC[self.username].append(cepsList)
            else:
                self.labelStatus.setText("Incorrect typing sequence.")
                typingSequenceFlag = False
        except KeyError:
            self.initialMeasurements[self.username] = [measurements]
            self.initialMFCC[self.username] = [cepsList]

        
        l = len(self.initialMeasurements[self.username])
        if l < INITIAL_DATA_COUNT and typingSequenceFlag:
            self.labelStatus.setText("Enter again. %d entries left" % (INITIAL_DATA_COUNT - l))
        elif l == INITIAL_DATA_COUNT and typingSequenceFlag:
            getDataToBeSaved(self.initialMeasurements[self.username], self.username)
            getInitialData(self.username, self.initialMFCC[self.username])
            self.labelStatus.setText("Username password combination saved.")
        elif typingSequenceFlag:
            mfccPassed, mfccPercentile = analyzeNewMFCCInput(cepsList, self.username)
            passed, percentile = analyzeNewInput(measurements, self.username)
            
#            if sum(percentile) + sum(mfccPercentile) > 0:
#                self.labelStatus.setText("Welcome!")
#            else:
#                self.labelStatus.setText("Impostor!")
            if passed:
                self.labelStatus.setText("Welcome!")
            else:
                self.labelStatus.setText("Impostor!")
                
            self.initialMeasurements[self.username] = self.initialMeasurements[self.username][1:]
#            self.initialMFCC[self.username] = self.initialMFCC[self.username][1:]
            
        
        self.lineEditPassword.setFocus()
        
        
    def closeEvent(self, event):
        userPassDB = shelve.open('DB/UserPassDB')
        for username in self.initialMeasurements:
            if len(self.initialMeasurements[username]) >= INITIAL_DATA_COUNT:
                userPassDB[username] = (self.initialPasswords[username], self.initialMeasurements[username][0])
        
        userPassDB.close()
        
        return QMainWindow.closeEvent(self, event)

        
def main():
    # Again, this is boilerplate, it'sampleRate going to be the same on
    # almost every app you write
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    # It'sampleRate exec_ because exec is a reserved word in Python
    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()
