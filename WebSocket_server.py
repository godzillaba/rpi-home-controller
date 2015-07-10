from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
import sys
from twisted.python import log
from twisted.internet import reactor
from server_lib import gpio
import json
import os
import threading

import parse_message, TCP_client, socket, errno

class ws_server(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        try:
            
            obj = json.loads(payload.decode('utf8'))
            print obj

            if obj['DestinationAddress'] == 'self':
                parse_message.onMessage(obj, config_file, self.sendMessage)
            else:
                # self.relayMessage(obj)
                print '\n\nstarting thread\n\n'
                (threading.Thread(target=self.relayMessage, args=(obj,))).start()

                
        
        except Exception as e:
            print "\n\nEXCEPTION OCCURRED DURING PARSING (%s)\n\n" % e

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

    def relayMessage(self, obj):

        print "Destination is not self - passing on to destination - %s" % obj['DestinationAddress']

        dest_addr = obj['DestinationAddress'].split(':')[0]
        dest_port = obj['DestinationAddress'].split(':')[1]

        try:
            
            q_reply = TCP_client.relaymessage(dest_addr, dest_port, json.dumps(obj))

            if q_reply != "":
                q_reply_obj = json.loads(q_reply)

                q_reply_obj['Sender'] = "%s:%s" % (dest_addr, dest_port)
                self.sendMessage(json.dumps(q_reply_obj))
        
        except socket.error, v:
            errorcode=v[0]
            
            errmsg = {
                "Sender": "self",
                "MessageType": "ErrorMessage",
                "Error": "TCP connection to %s failed (%s)" % (obj['DestinationAddress'], v)
            }

            print errmsg['Error']

            self.sendMessage(json.dumps(errmsg))


        
        
pathname = os.path.dirname(sys.argv[0])        
fullpath = os.path.abspath(pathname)

config_file = fullpath + "/config/config.json"

with open(config_file) as data_file:
    data = json.load(data_file)

port = int(data['WebSocket']['port'])
address = "ws://localhost:%s" % port

threads = {}

def main():
    log.startLogging(sys.stdout)
    factory = WebSocketServerFactory(address, debug=False)
    factory.protocol = ws_server
    reactor.listenTCP(port, factory)
    reactor.run()
