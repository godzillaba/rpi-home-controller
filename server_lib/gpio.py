import RPi.GPIO as GPIO
import logging
import json

# get layout from conf
GPIO.setmode(GPIO.BOARD)

with open('data.json') as data_file:
    data = json.load(data_file)


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
    relaypins = data['Web']['Groups']
    for p in relaypins:
        rp = pin(int(p['gpiopin']), "OUT", hilo)
        rp.toggle()
        logging.info('Initializing relay pin %s (%s)', p['gpiopin'], p['description'])
