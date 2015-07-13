from server_lib import gpio
import json
import os, sys

import parse_message

import SocketServer

pathname = os.path.dirname(sys.argv[0])        
fullpath = os.path.abspath(pathname)

config_file = fullpath + "/config/config.json"

with open(config_file) as data_file:
    data = json.load(data_file)


######## new code ########
SocketServer.TCPServer.allow_reuse_address = True


class MyTCPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        print "TCP - %s connected to socket" % self.client_address[0]

        self.data = self.request.recv(BUFFER_SIZE).strip()
        
        print 'TCP - Received "%s" from %s' % (self.data, self.client_address[0])

        # just send back the same data, but upper-cased
        # self.request.sendall(self.data.upper())
        
        obj = json.loads(self.data)
        parse_message.onMessage(obj, config_file, self.request.sendall)
        self.request.close()
        print 'TCP - Closed connection to %s' % self.client_address[0]


################


### START ###

# SET UP TCP SOCKET
TCP_IP = data['TCP']['listen_address']
TCP_PORT = int(data['TCP']['port'])
BUFFER_SIZE = int(data['TCP']['buffer_size'])


def main():

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((TCP_IP, TCP_PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()