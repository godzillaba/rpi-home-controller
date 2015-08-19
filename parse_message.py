from server_lib import gpio
import json, os, sys
import traceback
import tailer
import logging

pathname = os.path.dirname(sys.argv[0])        
fullpath = os.path.abspath(pathname)

config_file = fullpath + "/config/config.json"
people_file = fullpath + "/data.json"
thermostat_file = fullpath + "/thermostat.json"

with open(config_file) as data_file:
    conf_obj = json.load(data_file)

sender = conf_obj['servername']


def onMessage(obj, config_file, send_function):

    try:
        # obj = json.loads(payload.decode('utf8'))
        # print obj
        
        # tested working
        if obj['MessageType'] == 'Command':
            cmd = obj['Command']
            
            if cmd == "pin_out":
                logging.info("Received pin_out Command - pin %s %s" % (obj['pin_number'], obj['value']))
                gpio.cmd_pin_out(obj)
                
            elif cmd == "SaveConfig":    
                config_object = obj['ConfigData']
                
                json_to_file = json.dumps(config_object, indent=4)
                logging.info("Received SaveConfig Command \n %s" % json_to_file)
                
                with open(config_file, 'w') as data_file:
                    data_file.truncate()
                    data_file.write(json_to_file)

            elif cmd == "TempConfig":
                with open(thermostat_file) as d_file:
                    d_file_obj = json.load(d_file)
                
                d_file_obj['target_temp'] = obj['target_temp']
                d_file_obj['fan'] = obj['fan']
                d_file_obj['system'] = obj['system']

                with open(thermostat_file, 'w') as out_file:
                    out_file.write(json.dumps(d_file_obj, indent=4))


            else:
                logging.error("Command not recognized (%s)" % cmd)
                
                
                
        
        # tested working
        elif obj['MessageType'] == 'Query':
            q = obj['Query']
            
            if q == "pin_out":
                logging.info("Received pin_out Query - pin %s" % obj['pin_number'])
                # self.sendMessage(gpio.q_pin_out(obj))
                reply_objects = gpio.q_pin_out(obj)

                for r_obj in reply_objects:
                    send_function(json.dumps(r_obj))
                
            
            elif q == "Config":
                logging.info("Received Config Query")
                
                with open(config_file) as data_file:
                    config_object = json.load(data_file)
                
                reply_object = {
                    "Sender": sender,
                    "MessageType": "QueryReply",
                    "Query": "Config",
                    "ConfigData": config_object
                    
                }
                
                # self.sendMessage(json.dumps(reply_object))
                send_function(json.dumps(reply_object))
                
            elif q == "People":
                
                logging.info("Received People Query")

                with open(people_file) as d_file:
                    data_object = json.load(d_file)
                
                people_array = data_object['People']

                reply_object = {
                    "Sender": sender,
                    "MessageType": "QueryReply",
                    "Query": "People",
                    "People": people_array
                }

                # self.sendMessage(json.dumps(reply_object))
                send_function(json.dumps(reply_object))

            elif q == "ThermostatData":
                logging.info("Received Thermostat Query")

                with open(thermostat_file) as d_file:
                    data_object = json.load(d_file)

                reply_object = {
                    "Sender": sender,
                    "MessageType": "QueryReply",
                    "Query": "ThermostatData",
                    "Data": data_object
                }

                send_function(json.dumps(reply_object))

            elif q == "Log":
                logging.info("Received Log Query")

                logarray = tailer.tail(open('nohup.out'), 500)

                # logstr = '\n'.join(logarray)
                reply_object = {
                    "Sender": sender,
                    "MessageType": "QueryReply",
                    "Query": "Log",
                    "Data": logarray
                }
                send_function(json.dumps(reply_object))
                        
            else:
                logging.error("Query not recognized (%s)" % q)
                
                
    except Exception as e:
        logging.exception('')