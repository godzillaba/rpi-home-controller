from datetime import datetime
import time
import os
import RPi.GPIO as GPIO

alarmtime = "17:57"

pins = [37, 40]

for pin in pins:
	GPIO.setup(pin, GPIO.OUT)

def ring():
	print "ringing!"
	for pin in pins:
		GPIO.output(pin, 1)
	print "done"



while 1:
	time.sleep(30)
	t = ((str(datetime.now())).split(' ')[1])
	hours = t.split(':')[0]
	minutes = t.split(':')[1]
	parsedtime = "%s:%s" % (hours, minutes)
	print parsedtime
	
	if parsedtime == alarmtime:
		ring()
		break


