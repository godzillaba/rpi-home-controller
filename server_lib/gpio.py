import RPi.GPIO as GPIO
import logging
import config as conf

# get layout from conf
GPIO.setmode(GPIO.BOARD)

f = "server_lib/config.conf"


class pin(object):
	def __init__(self, num, iotype, state):
		self.num = num
		self.iotype = iotype
		self.state = state

	def toggle(self):
		if self.iotype == "OUT":
       			GPIO.setup(self.num, GPIO.OUT)
        		GPIO.output(self.num, self.state)
        		logging.info('Pin %s set %s', self.num, self.state)

		elif self.iotype == "IN":
			GPIO.setup(self.num, GPIO.OUT)
			return GPIO.input(self.num)


def parse(data):
	pnumber = int((data.split('=')[1]).split(',')[0])
	ptype = data.split(',')[1]
	pstate = int(data.split(',')[2])
	p = pin(pnumber, ptype, pstate)
	return p


def toggle_all_relays(hilo):
	relaypins = (conf.arg(f, "RELAYPINS")).split()
	for p in relaypins:
	    rp = pin(int(p), "OUT", hilo)
	    rp.toggle()
	    logging.info('Initializing relay pin %s', p)