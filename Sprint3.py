import sys
sys.path.append('/home/pi/.local/lib/python3.9/site-packages')
import pyaudio # used for microphone to python integration
import math # used to calculate decibel level
import struct # used to calculate decibel level
import RPi.GPIO as GPIO # used to integrate breadboard LED for testing
import threading # seperates constant tasks onto seperate threads
from gpiozero import MCP3008 # used to convert potentiometer from analog to serial input
import numpy as np # used for ML
import subprocess
import os
import time

# Initialize PyAudio object and microhone input stream
def open_stream(chunk=1024, sample_rate=44100, num_channels=128, device_index=2):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                     channels=num_channels,
                     rate=sample_rate,
                     input=True,
                     frames_per_buffer=chunk,
                     input_device_index=device_index)
    return p, stream

# Terminates PyAudio object and microphone input stream
def close_stream(p, stream):
    stream.stop_stream()
    stream.close()
    p.terminate()

# Converts raw audio input to decibel level
def calculate_decibel(data, chunk):
    data_int = struct.unpack(f"{chunk // 2}h", data)
    rms = math.sqrt(sum([(x ** 2) for x in data_int]) / chunk)
    decibel = 20 * math.log10(rms)
    return decibel

# Grabs raw audio input, calls decibel calculation fucntion, then returns true decibel value
def get_decibel(p, stream, chunk):
    data = stream.read(chunk, exception_on_overflow=False)
    data = data[:chunk]
    assert len(data) == chunk, f"Input data is {len(data)} bytes, expected {chunk} bytes"
    decibel = calculate_decibel(data[:chunk], chunk)
    return decibel

### Mic Indexes --- UNTESTED ###

# Grab device info from PyAudio
p = pyaudio.PyAudio()
num_devices = p.get_device_count()

output = subprocess.check_output(['arecord','-l'])
print(f"arecord output: {output}")

ids = []
# Determine PyAudio device indexes through ALSA's .asoundrc configuration
for i in range(num_devices):
    device_info = p.get_device_info_by_index(i)
    device_name = device_info["name"]
    if "USB" in device_name:
        ids.append(device_info["index"])

print(f"len ids: {len(ids)}")

mic1Index = ids[0]
mic2Index = ids[1]
mic3Index = ids[2]
mic4Index = ids[3]

# Opens each microphone input stream
p1, stream1 = open_stream(chunk=1024, sample_rate=44100, num_channels=1, device_index=mic1Index)
p2, stream2 = open_stream(chunk=1024, sample_rate=44100, num_channels=1, device_index=mic2Index)

### COMMENT OUT THESE LINES WHEN USING ONLY 2 MICS FOR TESTING ###
p3, stream3 = open_stream(chunk=1024, sample_rate=44100, num_channels=1, device_index=mic3Index)
p4, stream4 = open_stream(chunk=1024, sample_rate=44100, num_channels=1, device_index=mic4Index)

# Declare and initialize needed variables
global manDecThresh
global decibel1
global decibel2
global decibel3
global decibel4
global ml
global decVals
decibel1 = 1
decibel2 = 1
decibel3 = 1
decibel4 = 1
manDecThresh = 1

### CURRENTLY ONLY USES decibel1 AND 1 LIGHT ###
# Thread to turn on and off each section of lights
class LEDThread(threading.Thread):
    def __init__(self):
        super(LEDThread, self).__init__()
        self.daemon = True
        self.paused = True
        self.state = threading.Condition()
    
    def run(self):
        global manDecThresh
        global decibel1
        global decibel2
        global decibel3
        global decibel4

        sentCmd1 = False
        sentCmd2 = False
        sentCmd3 = False
        sentCmd4 = False
        
        while True:
            # light LED's
            if  decibel1 > manDecThresh:
                if not sentCmd1:
                    print("\n\n\n\n\nSent on!\n\n\n\n\n")
                    command = "/home/pi/Documents/CS495_SoundControlledLighting/scripts/31on.sh"
                    os.system("lxterminal -e 'bash -c \"" + command + "; exit\"'")
                    sentCmd1 = True
                    GPIO.output(light, GPIO.HIGH)
            elif decibel1 <= manDecThresh:
                if sentCmd1:
                  sentCmd1 = False
                  print("\n\n\n\n\nSent off!\n\n\n\n\n")
                  command = "/home/pi/Documents/CS495_SoundControlledLighting/scripts/31off.sh"
                  os.system("lxterminal -e 'bash -c \"" + command + "; exit\"'")
                  GPIO.output(light, GPIO.LOW)
                  
            if  decibel2 > manDecThresh:
                if not sentCmd2:
                    print("\n\n\n\n\nSent on!\n\n\n\n\n")
                    command = "/home/pi/Documents/CS495_SoundControlledLighting/scripts/34on.sh"
                    os.system("lxterminal -e 'bash -c \"" + command + "; exit\"'")
                    sentCmd2 = True
                    GPIO.output(light, GPIO.HIGH)
            elif decibel2 <= manDecThresh:
                if sentCmd2:
                  sentCmd2 = False
                  print("\n\n\n\n\nSent off!\n\n\n\n\n")
                  command = "/home/pi/Documents/CS495_SoundControlledLighting/scripts/34off.sh"
                  os.system("lxterminal -e 'bash -c \"" + command + "; exit\"'")
                  GPIO.output(light, GPIO.LOW)
                  
            if  decibel3 > manDecThresh:
                if not sentCmd3:
                    print("\n\n\n\n\nSent on!\n\n\n\n\n")
                    command = "/home/pi/Documents/CS495_SoundControlledLighting/scripts/37on.sh"
                    os.system("lxterminal -e 'bash -c \"" + command + "; exit\"'")
                    sentCmd3 = True
                    GPIO.output(light, GPIO.HIGH)
            elif decibel3 <= manDecThresh:
                if sentCmd3:
                  sentCmd3 = False
                  print("\n\n\n\n\nSent off!\n\n\n\n\n")
                  command = "/home/pi/Documents/CS495_SoundControlledLighting/scripts/37off.sh"
                  os.system("lxterminal -e 'bash -c \"" + command + "; exit\"'")
                  GPIO.output(light, GPIO.LOW)
                  
            if  decibel4 > manDecThresh:
                if not sentCmd4:
                    print("\n\n\n\n\nSent on!\n\n\n\n\n")
                    command = "/home/pi/Documents/CS495_SoundControlledLighting/scripts/38on.sh"
                    os.system("lxterminal -e 'bash -c \"" + command + "; exit\"'")
                    sentCmd4 = True
                    GPIO.output(light, GPIO.HIGH)
            elif decibel4 <= manDecThresh:
                if sentCmd4:
                  sentCmd4 = False
                  print("\n\n\n\n\nSent off!\n\n\n\n\n")
                  command = "/home/pi/Documents/CS495_SoundControlledLighting/scripts/38off.sh"
                  os.system("lxterminal -e 'bash -c \"" + command + "; exit\"'")
                  GPIO.output(light, GPIO.LOW)
 
    def stop(self):
        self.stopped = True

# Thread to check potentiomerter status. Enables and disables ML accordingly
class Potenti(threading.Thread):
    def __init__(self):
        super(Potenti, self).__init__()
        self.daemon = True
        self.paused = True
        self.state = threading.Condition()
    
    def run(self):
        global manDecThresh
        global ml
        global decVals
        ml = False
        while True:
            # light LED's
            #print(f"potval: {potentiometer.value}")
            if potentiometer.value * 100.0 > 10:
                ml = False
                manDecThresh = potentiometer.value * 100.0
            else:
                if len(decVals) < 3500: 
                    manDecThresh = 1

                if not ml:
                    decVals = []
                ml = True
            #print(manDecThresh)
            
    def stop(self):
        self.stopped = True

# Disble GPIO warnings
GPIO.setwarnings(False)

# label each part's pins
light = 24
potentiometer = MCP3008(0)

# set light to on and output
GPIO.setup(light, GPIO.OUT)
GPIO.output(light, GPIO.LOW)

# start 1 of each thread
potenti = Potenti()
potenti.start()
ledthread = LEDThread()
ledthread.start()

# prepare empty list for ML
decVals = []

# DRIVER CODE: constantly sets decibel levels and sets up machine learning if needed
while True:
    decibel1 = get_decibel(p1, stream1, chunk=1024)
    decibel2 = get_decibel(p2, stream2, chunk=1024)
    
    ### USE THESE LINES WHEN USING 2 MICS FOR TESTING ###
    #decibel3 = 45
    #decibel4 = 40
    
    ### USE THESE LINES WHEN USING 4 MICS FOR FINAL PRODUCT ###
    decibel3 = get_decibel(p3, stream3, chunk=1024)
    decibel4 = get_decibel(p4, stream4, chunk=1024)

    # ML code initialization
    if len(decVals) < 3500 and ml:
        decVals.append(decibel1)
        decVals.append(decibel2)
        decVals.append(decibel3)
        decVals.append(decibel4)
        GPIO.output(light,GPIO.LOW)

    elif ml:
        decVals = np.array(decVals)
        manDecThresh = np.median(decVals)
        print(f"\n\nmanDecThresh: {manDecThresh}\n\n")
        GPIO.output(light,GPIO.HIGH) 
    #if manual
    if not ml:
        GPIO.output(light,GPIO.HIGH) 
    # print variables to debug
    print(f"Microphone 1: {decibel1}, Microphone 2: {decibel2}, Microphone 3: {decibel3}, Microphone 4: {decibel4}, Decibel Threshold: {manDecThresh}")

# close microphone input streams
close_stream(p1, stream1)
close_stream(p2, stream2)

### COMMENT OUT THESE LINES WHEN USING ONLY 2 MICS FOR TESTING ###
close_stream(p3, stream3)
close_stream(p4, stream4)
