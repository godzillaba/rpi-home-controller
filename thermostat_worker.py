import os, sys, json
import RPi.GPIO as GPIO


####### adafruit code #######

import glob
import time

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f


####### end adafruit code #######

####### heat / cool switch functions #######

def hvac_off():
    GPIO.output(heat_pin, 1)
    GPIO.output(cool_pin, 1)
    GPIO.output(fan_pin, 1)

def heat():
    if hvac_type != 'conventional':
        print "Only conventional hvac systems supported. For more info visit https://wiki.xtronics.com/index.php/Thermostat_signals_and_wiring"
    else:
        GPIO.output(cool_pin, 1)
        GPIO.output(fan_pin, 1)
        GPIO.output(heat_pin, 0)

def cool():
    GPIO.output(heat_pin, 1)
    GPIO.output(fan_pin, 0)
    GPIO.output(cool_pin, 0)

def fan_only():
    GPIO.output(heat_pin, 1)
    GPIO.output(cool_pin, 1)
    GPIO.output(fan_pin, 0)

####### end heat / cool switch functions #######


pathname = os.path.dirname(sys.argv[0])        
fullpath = os.path.abspath(pathname)

thermostat_file = fullpath + "/thermostat.json"
thermostat_config = fullpath + "/thermostat_config.json"

with open(thermostat_config) as config_file:
    config = json.load(config_file)


GPIO.setmode(GPIO.BOARD)



heat_pin = int(config['heat'])
cool_pin = int(config['compressor'])
fan_pin = int(config['fan'])

hvac_type = config['hvactype']

GPIO.setup(heat_pin, GPIO.OUT)
GPIO.setup(cool_pin, GPIO.OUT)
GPIO.setup(fan_pin, GPIO.OUT)


while 1:

    with open(thermostat_file) as data_file:
        thermostat_data = json.load(data_file)

    target = int(thermostat_data['target_temp'])
    system = thermostat_data['system']
    fan = thermostat_data['fan']

    actual = read_temp()[0]

    difference = actual - target

    print "target:%s actual:%s difference:%s fan:%s compressor:%s" % (target, actual, difference, fan, system)


    thermostat_data['actual_temp'] = actual

    with open(thermostat_file, 'w') as data_file:
        print 'writing to file'
        data_file.write(json.dumps(thermostat_data, indent=4))



    if fan == 'auto':

        if 1 > difference > -1:
            print "Turning off fan and compressor"
            # turn off fan and compressor
            hvac_off()

        #below target
        elif difference < -1:
            
            if system == 'heat' or system == 'auto':
                # turn on heater
                print "turning on heat"
                heat()

            elif system == 'cool':
                print "turning off fan and compressor"
                hvac_off()


        #above target
        elif difference > 1:
            if system == 'heat':
                print "turning off fan and compressor"
                hvac_off()

            if system == 'cool' or system == 'auto':
                # turn on ac
                print "turning on ac"
                cool()

    elif fan == 'on':
        
        if system == 'auto':

            if 1 > difference > -1:
                print 'turning on fan only'
                fan_only()

            #below target
            elif difference < -1:
                print "turning on heat"
                heat()

            #above target
            elif difference > 1:    
                print "turning on ac"
                cool()

        elif system == 'heat':
            print "turning on heat"
            heat()

        elif system == 'cool':
            print 'turning on ac'
            cool()

    elif fan == 'off':
        print 'turning hvac system off'
        hvac_off()



    time.sleep(120)