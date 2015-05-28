import RPi.GPIO as GPIO
import logging
import json
import os, sys

# get layout from conf
GPIO.setmode(GPIO.BOARD)

pathname = os.path.dirname(sys.argv[0])        
fullpath = os.path.abspath(pathname)

config_file = fullpath + "/data.json"

with open(config_file) as data_file:
    data1 = json.load(data_file)


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
    relaypins = data1['Web']['Groups'][0]
    for p in relaypins:
        if p != 'self':
            rp = pin(int(p['gpiopin']), "OUT", hilo)
            rp.toggle()
            logging.info('Initializing relay pin %s (%s)', p['gpiopin'], p['description'])
