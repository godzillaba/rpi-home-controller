import os, sys, json


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





pathname = os.path.dirname(sys.argv[0])        
fullpath = os.path.abspath(pathname)

thermostat_file = fullpath + "/thermostat.json"



while 1:

    with open(thermostat_file) as data_file:
        thermostat_data = json.load(data_file)

    target = thermostat_data['target_temp']
    system = thermostat_data['system']
    fan = thermostat_data['fan']

    actual = read_temp()[0]

    difference = actual - target

    print "target:%s actual:%s difference:%s" % (target, actual, difference)


    thermostat_data['actual_temp'] = actual

    with open(thermostat_file, 'w') as data_file:
        print 'writing to file'
        data_file.write(json.dumps(thermostat_data, indent=4))



    if fan == 'auto':

        if 1 > difference > -1:
            print "Turning off fan and compressor"
            # turn off fan and compressor

        #below target
        elif difference < -1:
            
            if system == 'heat':
                # turn on heater
                print "turning on heat"
            elif system == 'cool':
                print "turning off fan and compressor"


        #above target
        elif difference > 1:
            if system == 'heat':
                print "turning off fan and compressor"

            if system == 'cool':
                # turn on ac
                print "turning on ac"

    time.sleep(120)