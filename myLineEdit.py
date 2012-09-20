from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import *
import subprocess
from recorder import recordSoundThread
        
class MyLineEdit(QtGui.QLineEdit):

    def __init__(self, parent=None):
        super(MyLineEdit, self).__init__(parent)
        self.stopRecording = False
    def focusInEvent(self, e):
#        if self.main.recordFlag:
        subprocess.Popen('capture.exe')
        self.stopRecording = False
               
        self.rth = recordSoundThread(self)
        self.rth.start()
        return QtGui.QLineEdit.focusInEvent(self, e)

    def focusOutEvent(self, e):
        p = subprocess.Popen('taskkill /f /im capture.exe')
        self.stopRecording = True
        p.wait()
        
        
        # TODO: stop record thread
        
        return QtGui.QLineEdit.focusOutEvent(self, e)
            
    def setMain(self, main):
        self.main = main
