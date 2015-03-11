from SimpleWebSocket import SimpleWebSocketServer, WebSocket
import os

tcpserver = 'localhost'
tcpport = 5432

class WebSocketProxy(WebSocket):
    def handleMessage(self):        
        cmd = ("python ../client/client.py %s %s '%s'") % (tcpserver, tcpport, self.data)
        os.system(cmd)

    def handleConnected(self):
        print self.address, 'connected'

    def handleClose(self):
        print self.address, 'closed'

server = SimpleWebSocketServer('', 5433, WebSocketProxy)
server.serveforever()