import RPi.GPIO as GPIO
import time

# blink function
def Blink(pin,delay):
	print "LED On"
	GPIO.output(pin,GPIO.HIGH)
	time.sleep(delay)

	print "LED Off"
	GPIO.output(pin,GPIO.LOW)
	time.sleep(delay)
	return

pinNum=18
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pinNum,GPIO.OUT)

# get input from user
blinks = raw_input("Enter number of time to blink LED: ")
delay = raw_input("Enter number of seconds between blinks: ")

# blink the LED
for i in range(0,int(blinks)):
	Blink(pinNum,float(delay))
GPIO.cleanup()
