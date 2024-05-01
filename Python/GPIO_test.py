import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

try:
    while True:
        GPIO.output(17, GPIO.HIGH)
        print("Pin 17 is ON")
        time.sleep(1)
        
        GPIO.output(17, GPIO.LOW)
        print("Pin 17 is OFF")
        time.sleep(1)
        
except KeyboardInterrupt:
    print("Kill program")
    GPIO.cleanup()
