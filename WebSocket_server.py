from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory
import sys
from twisted.python import log
from twisted.internet import reactor
from server_lib import gpio
import json

class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        global json_out
        print("Text message received: {0}".format(payload.decode('utf8')))
        cmd = payload.split('=')[0]

       
        if cmd == "PIN":
            p = gpio.parse(payload)
            toggle_output = str(p.toggle())
            if p.iotype == "IN":
                self.sendMessage("PIN %s %s" % (p.num, toggle_output))
        elif cmd == "ALLRELAYS":
            gpio.toggle_all_relays(int(payload.split('=')[1]))
        elif cmd == "GETJSON":
                self.sendMessage("JSON----------" + json_out)
        elif cmd == "SAVEJSON":
                jsontext = payload.split('=')[1]
                json_in = json.loads(jsontext)
                json_out = json.dumps(json_in, indent=4)
                with open('data.json', 'w') as data_file:
                        data_file.truncate()
                        data_file.write(json_out)


    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

with open('data.json') as data_file:
    data = json.load(data_file)
    json_out = json.dumps(data, indent=4)

port = int(data['WebSocket']['port'])
address = "ws://localhost:%s" % port

def main():
	log.startLogging(sys.stdout)
	factory = WebSocketServerFactory(address, debug=False)
	factory.protocol = MyServerProtocol
	reactor.listenTCP(port, factory)
	reactor.run()
