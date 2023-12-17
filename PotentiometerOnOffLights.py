import RPi.GPIO as GPIO
import threading

# make global variable to check
global manDecThresh
manDecThresh = 1

# Thread to turn on and off lights based on manDecThresh
class LEDThread(threading.Thread):
    def __init__(self):
        super(LEDThread, self).__init__()
        self.daemon = True
        self.paused = True
        self.state = threading.Condition()
    
    def run(self):
        global manDecThresh
        
        while True:
            # light LED's
            # curremntly a constant .5 decibal input
            if manDecThresh > .5:
                GPIO.output(light, GPIO.HIGH)
            elif manDecThresh <= .5:
                GPIO.output(light, GPIO.LOW)
        GPIO.output(light, GPIO.LOW)
            
    def stop(self):
        self.stopped = True

# thread to check potentiomerter status 
class Potenti(threading.Thread):
    def __init__(self):
        super(Potenti, self).__init__()
        self.daemon = True
        self.paused = True
        self.state = threading.Condition()
    
    def run(self):
        global manDecThresh
        
        while True:
            # light LED's
            manDecThresh = GPIO.input(potentiometer)
            
    def stop(self):
        self.stopped = True
        
# set up GPIO interface
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# label each part's pins
power = 2
potentiometer = 12
light = 18

# set sig as input for gpio
GPIO.setup(potentiometer, GPIO.IN)

# set light to on and output
GPIO.setup(light, GPIO.OUT)
GPIO.output(light, GPIO.HIGH)

# start 1 of each thread
potenti = Potenti()
potenti.start()

ledthread = LEDThread()
ledthread.start()


            
