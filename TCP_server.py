from server_lib import gpio
import json
import socket
import logging
import os, sys

import parse_message

# LOGGING / CONFIG VARIABLES
# logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

pathname = os.path.dirname(sys.argv[0])        
fullpath = os.path.abspath(pathname)

config_file = fullpath + "/config/config.json"

with open(config_file) as data_file:
    data = json.load(data_file)


def serve_forever():
    while 1:
        try:
            conn, addr = s.accept()
            print 'TCP - Connection address %s' % addr[0]


            data = conn.recv(BUFFER_SIZE)
            print 'TCP - Received "%s" from %s' % (data, addr[0])

            if data:
                parse_message.onMessage(json.loads(data), config_file, conn.send)

            else:
                break

            conn.close()
        except Exception as e:
            print "Exception occurred during serve_forever() loop -- %s" % e


### START ###

# SET UP TCP SOCKET
TCP_IP = data['TCP']['listen_address']
TCP_PORT = int(data['TCP']['port'])
BUFFER_SIZE = int(data['TCP']['buffer_size'])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def main():
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    print 'TCP server listening on %s:%s' % (TCP_IP, TCP_PORT)

    # SET UP RELAYS
    gpio.toggle_all_relays(1)

    serve_forever()
