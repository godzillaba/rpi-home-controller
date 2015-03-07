from datetime import datetime
import time
import RPi.GPIO as GPIO


class alarm(object):
	def __init__(self, time, pnum, status):
		self.time = time
		self.pnum = pnum
		self.status = status


def parse(data):
	time = data.split(',')[0]
	pnum = int(data.split(',')[1])
	status = int(data.split(',')[2])
	a = alarm(time, pnum, status)
	return a


def ring():
	GPIO.output(a.pnum, 1)

def parsetime():
	t = ((str(datetime.now())).split(' ')[1])
	hours = t.split(':')[0]
	minutes = t.split(':')[1]
	parsedtime = "%s:%s" % (hours, minutes)
	return parsedtime

def wait(a):
	while 1:
		time.sleep(30)
		print parsetime()
		if parsetime() == a.time:
			ring()
			break
