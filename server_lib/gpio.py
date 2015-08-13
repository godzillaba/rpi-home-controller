import RPi.GPIO as GPIO
import logging
import json
import os, sys

# get layout from conf
GPIO.setmode(GPIO.BOARD)

pathname = os.path.dirname(sys.argv[0])        
fullpath = os.path.abspath(pathname)

config_file = fullpath + "/config/config.json"

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


        
        
        
# tested working
def cmd_pin_out(obj):

    pnumber = int(obj['pin_number'])
    GPIO.setup(pnumber, GPIO.OUT)    

    if obj['value'] == "!":
        pvalue = int(not GPIO.input(pnumber))
    else:
        pvalue = int(obj['value'])
    
    GPIO.output(pnumber, pvalue)

    
# tested working
def q_pin_out(obj):
    pnumber = int(obj['pin_number'])
    
    GPIO.setup(pnumber, GPIO.OUT)
    pvalue = int(GPIO.input(pnumber))
    
    reply_object = {
        "Sender": data1['servername'],
        "MessageType": "QueryReply",
        "Query": "pin_out",
        "pin_number": pnumber,
        "value": pvalue
    }
    
    reply_string = json.dumps(reply_object)
    
    return reply_string
