from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
from server_lib import gpio


class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        print("Text message received: {0}".format(payload.decode('utf8')))
        cmd = payload.split('=')[0]

       
        if cmd == "PIN":
            p = gpio.parse(payload)
            toggle_output = str(p.toggle())
            if p.iotype == "IN":
                self.sendMessage("PIN %s %s" % (p.num, toggle_output))
        elif cmd == "ALLRELAYS":
            gpio.toggle_all_relays(int(payload.split('=')[1]))

        
        # self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory("ws://localhost:9000", debug=False)
    factory.protocol = MyServerProtocol
    # factory.setProtocolOptions(maxConnections=2)

    reactor.listenTCP(9000, factory)
    reactor.run()