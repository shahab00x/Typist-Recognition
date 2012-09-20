import pyaudio
import wave
from PyQt4.QtCore import QThread

class recordSoundThread(QThread):
    def __init__(self, d): # d is the original class in which this is called from
        super(recordSoundThread, self).__init__(d)
        self.d = d
        
    def run(self):
        print "recordSoundThread run"
        self.startRecording()
        
    def startRecording(self):
        print "start recording"
        chunk = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        WAVE_OUTPUT_FILENAME = "output.wav"
        
        p = pyaudio.PyAudio()
        
        stream = p.open(format = FORMAT,
                        channels = CHANNELS,
                        rate = RATE,
                        input = True,
                        frames_per_buffer = chunk)
        
        print "* recording"
        all = []
        while True:
            data = stream.read(chunk)
            all.append(data)
            if self.d.stopRecording :
                self.d.stopRecording = False
                break
#        
        print "* done recording"
        
        stream.close()
        p.terminate()
        
        # write data to WAVE file
        data = ''.join(all)
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(data)
        wf.close()