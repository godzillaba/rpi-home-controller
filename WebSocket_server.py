from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
import sys
from twisted.python import log
from twisted.internet import reactor
from server_lib import gpio
import json
import os
import thread

import parse_message

class ws_server(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        parse_message.onMessage(payload, config_file, self.sendMessage)

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
