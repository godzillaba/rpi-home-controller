import RPi.GPIO as GPIO


# get layout from conf
GPIO.setmode(GPIO.BOARD)

class pin(object):
	def __init__(self, num, iotype, state):
		self.num = num
		self.iotype = iotype
		self.state = state

	def toggle(self):
		if self.iotype == "OUT":
       		GPIO.setup(self.num, GPIO.OUT)
        	GPIO.output(self.num, self.state)

		elif self.iotype == "IN":
			return GPIO.input(self.num)


def parse(data):
	pnumber = int((data.split('=')[1]).split(',')[0])
	ptype = data.split(',')[1]
	pstate = int(data.split(',')[2])
	p = pin(pnumber, ptype, pstate)
	return p
