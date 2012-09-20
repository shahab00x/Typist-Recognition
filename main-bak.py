from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import *
import sys
import time
import shelve
import mainWindow
from kalmanDistance import *
import os, signal
from multiprocessing.dummy import Process
from collections import deque
#from waveFiles import *

#import wmi
newUserPass = False
User = ""
Pass = ""

        
class loginButtonThread(QThread):
    def __init__(self, d, username, password, status, log): # d is the original class
        super(loginButtonThread, self).__init__(d)
        self.username = username
        self.password = password
        self.status = status
        self.log = log
        self.main = d
        
    def run(self):
        self.openDB()
        print "run"
    
    def stopRecording(self):
        print "stop recording"
        
    def openDB(self):
        print "openDB"
        global newUserPass
        global User
        global Pass
        
        if not os.path.exists("DB/"):
            os.mkdir("DB/")
        d = shelve.open("DB/UserPassDB")
        t = shelve.open("DB/TempDB")
        flag = False
        newInputFlag = False
        if(d.has_key(self.username)):
            if d[self.username] == self.password :
                self.status.setText("Username and password correct")
                newInputFlag = True
            else: self.status.setText("Wrong username or password")
        elif newUserPass == False: 
            User = self.username
            Pass = self.password
            self.status.setText("Enter again")
            newUserPass = True
        elif newUserPass == True:
            if User == self.username and Pass == self.password:
                d[User] = Pass
                User = ""
                Pass = ""
                newUserPass = False
                flag = True
                self.status.setText("New username and password combination saved!")
            else:
                self.status.setText("Mismatch")
                newUserPass = False
                User = ""
                Pass = ""
                
        d.close()
        
        input1 = []
        newInput = self.log
        #i = myInput.readline().split()[0][1]
        #print "i=",i
        
        print "newInput", newInput
        if newUserPass == True:
            t[self.username] = newInput
            
        if flag == True:
            flag = False
            input1 = t[self.username]
            print "input1,newInput", input1, newInput
            getDataToBeSaved(input1, newInput,self.username)
            os.remove("DB/tempDB")
        t.close()
           
        if newInputFlag == True:
            passed = analyzeNewInput(newInput,self.username)
            if passed == True: self.status.setText(self.status.text() + "Welcome!")
            else: self.status.setText("Imposter!")
            newInputFlag = False
        
                
class threadhandler(QThread):
    def __init__(self, d):
        super(threadhandler, self).__init__(d)
        self.d = d
    def run(self):
        self.h(self.d)
    def h(self, d):
        running = 0
        run = 0
        while d.ps != len(d.inlinks):
            if d.stop == True:
                return
            for i in d.inlinks:
                if d.threads[d.inlinks.index(i)].isRunning() == True:
                    running = running + 1
            if running != d.concurrency and run < len(d.inlinks):
                d.threads[run].start()
                run = run + 1
                
            running = 0
            time.sleep(0.1)
        if d.stop == False:
            self.emit(SIGNAL("fin()"))
     
     
class Main(QMainWindow, mainWindow.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.username = ""
        self.password = ""
        self.lineEditPassword.setMain(self)
#        self.stopRecording = False
#        self.recordFlag = True
        
        #self.th = loginButtonThread(self, self.username, self.password, self.labelStatus)
        newUserPass = False
        self.lineEditUserName.setFocus()
        
    @pyqtSignature("")
    def on_pushButtonStart_clicked(self):
        self.username = str(self.lineEditUserName.text())
        self.password = str(self.lineEditPassword.text())
        self.lineEditPassword.setText("")
#       c = wmi.WMI ()
#       for process in c.Win32_Process ():
#           if process.Name == "capture.exe":
#               print process.ProcessId, process.Name
#               while process in c.Win32_Process():
#                   pass
#        global newUserPass
        
#        self.stopRecording = True
#        self.recordFlag = True
        self.lineEditUserName.setFocus()
#        log = open("log.txt")
#        #print log.read()
#        temp1 = []
#        temp2 = []
#        newInput = []
#        i = -2
#        for line in log:
#            if int(line.split()[0]) == 9:
#                continue
#            if i < 0:
#                i = float(line.split()[1])
#            temp1.append(float(line.split()[1]) - i)
#            temp2.append(float(line.split()[2]) - i)
#        newInput.append(temp1)
#        newInput.append(temp2)
#        log.close()
#        
#        
#        deNoise()
#        getMFCC()
        
#        
#        state = []
#        input = open('log.txt')
#        line = input.readline()
#        while line:
#            line2 = input.readline()
#            if line.split()[0] != '9':
#                if line2:
#                    state.append(
#                                 (float(line.split()[2]) - float(line.split()[1]),
#                                  float(line2.split()[1]) - float(line.split()[1]),
#                                  float(line2.split()[1]) - float(line.split()[2]))
#                                 )                   
#                else:
#                    state.append((float(line.split()[2]) - float(line.split()[1]), 0,0))
#            line = line2
#        print "state",state
#        print len(state)
#        login = []
#        temp1 = []
#        temp2 = []
#        temp3 = []
#        for i in state:
#            temp1.append(i[0])
#            temp2.append(i[1])
#            temp3.append(i[2])
#        login.append(temp1)
#        login.append(temp2)
#        login.append(temp3)
#        login += newInput

        measurements = []
        log = open('log.txt')
        print 'log', log.read()
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
        
        self.th = loginButtonThread(self, self.username, self.password, self.labelStatus, measurements)
        self.th.start() 
        
        if newUserPass == False:
            self.lineEditPassword.setFocus()
#        if newUserPass == True: 
#            self.lineEditUserName.setText("")
#            os.remove("log.txt")
#        else:
#            subprocess.Popen("capture.exe")
            #self.lineEditUserName.setFocus() 
            #self.lineEditPassword.setFocus() 
        #else: self.lineEditUserName.setText("ssid")
        
    @pyqtSignature("QString")
    def on_lineEditUserName_textChanged(self):
        pass
        
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
