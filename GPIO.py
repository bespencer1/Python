import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)

pinNum = int(sys.argv[1])
print "GPIO: ", str(pinNum)

GPIO.setup(pinNum,GPIO.OUT)

print "LED on"
GPIO.output(pinNum,GPIO.HIGH)
time.sleep(3)

print "LED off"
GPIO.output(pinNum,GPIO.LOW)

GPIO.cleanup()
