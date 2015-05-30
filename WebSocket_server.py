from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
import sys
from twisted.python import log
from twisted.internet import reactor
from server_lib import gpio
import json
import os
import thread

class ws_server(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        
        try:
            obj = json.loads(payload.decode('utf8'))
            print obj
            
            # tested working
            if obj['MessageType'] == 'Command':
                cmd = obj['Command']
                
                if cmd == "pin_out":
                    print "Received pin_out Command - pin %s %s" % (obj['pin_number'], obj['value'])
                    gpio.cmd_pin_out(obj)
                    
                elif cmd == "SaveConfig":    
                    config_object = obj['ConfigData']
                    
                    json_to_file = json.dumps(config_object, indent=4)
                    print "Received SaveConfig Command \n %s" % json_to_file
                    
                    with open(config_file, 'w') as data_file:
                        data_file.truncate()
                        data_file.write(json_to_file)
                    
                    
                    
            
            # tested working
            elif obj['MessageType'] == 'Query':
                q = obj['Query']
                
                if q == "pin_out":
                    print "Received pin_out Query - pin %s" % obj['pin_number']
                    self.sendMessage(gpio.q_pin_out(obj))
                    
                
                elif q == "Config":
                    print "Received Config Query"
                    
                    with open(config_file) as data_file:
                        config_object = json.load(data_file)
                    
                    reply_object = {
                        
                        "MessageType": "QueryReply",
                        "Query": "Config",
                        "ConfigData": config_object
                        
                    }
                    
                    self.sendMessage(json.dumps(reply_object))
                    
                elif q == "People":
                    print "Received People Query - doing nothing"
                    
                else:
                    print "Query not recognized (%s)" % q
            
            
        except:
            print "EXCEPTION OCCURRED DURING PARSING"
        
        #######################

#        if cmd == "PIN":
#            
#            p = gpio.parse(payload)
#            toggle_output = str(p.toggle())
#            if p.iotype == "IN":
#                self.sendMessage("PIN %s %s" % (p.num, toggle_output))
#        
#        
#        elif cmd == "ALLRELAYS":
#            gpio.toggle_all_relays(int(payload.split('=')[1]))
#        elif cmd == "GETJSON":
#            with open(config_file) as data_file:
#                json_out = json.dumps(json.load(data_file))
#            self.sendMessage("JSON----------" + json_out)
#        elif cmd == "SAVEJSON":
#            jsontext = payload.split('=')[1]
#            json_in = json.loads(jsontext)
#            json_to_file = json.dumps(json_in, indent=4)
#            with open(config_file, 'w') as data_file:
#                data_file.truncate()
#                data_file.write(json_to_file)
#        elif cmd == "GETPEOPLE":
#            
#            with open(config_file) as data_file:
#                json_data = json.load(data_file)
#            
#            people = json_data['Web']['People']
#            
#            for person in people:
#                print "starting thread to ping " + person['hostname']
#                thread.start_new_thread( pinghost, (self, person, ) )
##                pinghost(self, person)
#                    
                    


    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


                                              
def pinghost(self, person):
    
    global pingthreads

    try:
        
    
        if pingthreads[str(person['hostname'])]:
            print "Already trying to ping %s" % person['hostname']
        
        else:
            pingthreads[str(person['hostname'])] = True
            
            ip = os.system("ping -c 1 " + person['hostname'] + " >> /dev/null")      
               
            print "pinging %s returned %s" % (person['hostname'], ip)
                       
            if ip == 0:
                msg = str("PERSON ," + person['name'] + ",IN")
                self.sendMessage(msg)
            else:
                msg = str("PERSON ," + person['name'] + ",OUT")
                self.sendMessage(msg)
                
            pingthreads[str(person['hostname'])] = False
    except:
        print "exeption occurred"


        

        
        
pathname = os.path.dirname(sys.argv[0])        
fullpath = os.path.abspath(pathname)

config_file = fullpath + "/config.json"

with open(config_file) as data_file:
    data = json.load(data_file)

port = int(data['WebSocket']['port'])
address = "ws://localhost:%s" % port

pingthreads = {}

people = data['Web']['People']

for person in people: 
    pingthreads[str(person['hostname'])] = False

def main():
    log.startLogging(sys.stdout)
    factory = WebSocketServerFactory(address, debug=False)
    factory.protocol = ws_server
    reactor.listenTCP(port, factory)
    reactor.run()
