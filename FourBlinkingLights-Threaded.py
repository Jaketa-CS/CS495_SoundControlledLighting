import RPi.GPIO as GPIO
import time
import threading

stopper = False

class LEDThread(threading.Thread):
    def __init__(self):
        super(LEDThread, self).__init__()
        self.daemon = True
        self.paused = True
        self.state = threading.Condition()
    
    def run(self):
        
        while True:
            # light LED's

            GPIO.output(red, GPIO.HIGH)
            if stopper:
                break
            time.sleep(0.400)
            GPIO.output(red, GPIO.LOW)
            if stopper:
                break
            time.sleep(0.400)
            GPIO.output(yellow, GPIO.HIGH)
            if stopper:
                break
            time.sleep(0.400)
            GPIO.output(yellow, GPIO.LOW)
            if stopper:
                break
            time.sleep(0.400)
            GPIO.output(green, GPIO.HIGH)
            if stopper:
                break
            time.sleep(0.400)
            GPIO.output(green, GPIO.LOW)
            if stopper:
                break
            time.sleep(0.400)
            GPIO.output(blue, GPIO.HIGH)
            if stopper:
                break
            time.sleep(0.400)
            GPIO.output(blue, GPIO.LOW)
            if stopper:
                break
            time.sleep(0.400)
        GPIO.output(red, GPIO.LOW)
        GPIO.output(yellow, GPIO.LOW)
        GPIO.output(green, GPIO.LOW)
        GPIO.output(blue, GPIO.LOW)
            
    def stop(self):
        self.stopped = True
        
def checkButton():
    buttonstate = GPIO.input(button)
    if buttonstate == 0:
        return True
    else:
        return False

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

button = 32

GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

red = 18
yellow = 22
green = 24
blue = 26

GPIO.setup(red, GPIO.OUT)
GPIO.output(red, GPIO.LOW)

GPIO.setup(yellow, GPIO.OUT)
GPIO.output(yellow, GPIO.LOW)

GPIO.setup(green, GPIO.OUT)
GPIO.output(green, GPIO.LOW)

GPIO.setup(blue, GPIO.OUT)
GPIO.output(blue, GPIO.LOW)

ledThread = LEDThread()
ledThread.start()

buttonstate = GPIO.input(button)
while True:
    buttonstate = GPIO.input(button)
    if buttonstate == 0:
        if ledThread.is_alive():
            stopper = True
            time.sleep(.3)
        elif not ledThread.is_alive():
            stopper = False
            ledThread = LEDThread()
            ledThread.start()
            time.sleep(.3)
            while buttonstate == 0:
                buttonstate = GPIO.input(button)
                continue
            
