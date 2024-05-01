import numpy as np
import spidev
import RPi.GPIO as GPIO
import time

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz= 1*(10**6)
buttonPin = 26
ssPin = 24
GPIO.setmode(GPIO.BCM)

GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ssPin, GPIO.OUT, initial=GPIO.LOW)

value = 67
def buttonPress():
    #print("Button pressed")
    spi.xfer([value])


GPIO.add_event_detect(buttonPin, GPIO.FALLING, callback = buttonPress, bouncetime=200)
#Loop 
try:
    while True:
        value = 145
        buttonPress()
        print("Pin 17 is ON")
        time.sleep(4*(10**-6))
        
        #value = 61
        #buttonPress()
       # print("Pin 17 is OFF")
        #time.sleep(4*(10**-6))
        
except KeyboardInterrupt:
    print("Kill program")
    GPIO.cleanup()

    
