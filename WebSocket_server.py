from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
import sys
from twisted.python import log
from twisted.internet import reactor
from server_lib import gpio
import json
import os
import threading

import parse_message, TCP_client, socket, errno, traceback

class ws_server(WebSocketServerProtocol):

    def send(self, message):
        print "WS - Sending %s" % message
        self.sendMessage(message)

    def onConnect(self, request):
        print("WS - Client connecting: {0}".format(request.peer))

    def onOpen(self):
        pass

    def onMessage(self, payload, isBinary):
        try:
            
            print "WS - Received %s" % (payload.decode('utf8'))

            obj = json.loads(payload.decode('utf8'))
            

            if obj['DestinationAddress'] == 'self':
                parse_message.onMessage(obj, config_file, self.send)
            else:
                # self.relayMessage(obj)
                (threading.Thread(target=self.relayMessage, args=(obj,))).start()

                
        
        except Exception as e:
            print '\n'
            traceback.print_exc()
            print '\n'
            

    def onClose(self, wasClean, code, reason):
        print("WS - connection closed: {0}".format(reason))

    def relayMessage(self, obj):

        print "WS - Destination is not self - passing on to destination - %s" % obj['DestinationAddress']

        dest_addr = obj['DestinationAddress'].split(':')[0]
        dest_port = obj['DestinationAddress'].split(':')[1]

        try:
            
            q_reply = TCP_client.relaymessage(dest_addr, dest_port, json.dumps(obj))

            if q_reply != "":
                q_reply_obj = json.loads(q_reply)

                q_reply_obj['Sender'] = "%s:%s" % (dest_addr, dest_port)
                self.send(json.dumps(q_reply_obj))
        
        except socket.error, v:
            errorcode=v[0]
            
            errmsg = {
                "Sender": "self",
                "MessageType": "ErrorMessage",
                "Error": "TCP connection to %s failed (%s)" % (obj['DestinationAddress'], v)
            }

            # print "ERROR - WS - " + errmsg['Error']
            self.send(json.dumps(errmsg))

            print '\n'
            traceback.print_exc()
            print '\n'




        
        
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
