import RPi.GPIO as GPIO


# get layout from conf
GPIO.setmode(GPIO.BOARD)

class pin(object):
	def __init__(self, num, iotype, state):
		self.num = num
		self.iotype = iotype
		self.state = state

def parse(data):
	pnumber = int((data.split('=')[1]).split(',')[0])
	ptype = data.split(',')[1]
	pstate = int(data.split(',')[2])
	p = pin(pnumber, ptype, pstate)
	return p

def toggle(p):
	if p.iotype == "OUT":
       		GPIO.setup(p.num, GPIO.OUT)
        	GPIO.output(p.num, p.state)

	elif p.iotype == "IN":
		return GPIO.input(p.num)
