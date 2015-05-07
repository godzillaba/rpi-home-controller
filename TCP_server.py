from server_lib import gpio
import json
import socket
import logging

# LOGGING / CONFIG VARIABLES
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

with open('data.json') as data_file:
    data = json.load(data_file)


def serve_forever():
    while 1:
        conn, addr = s.accept()
        logging.info('Connection address %s', addr)
        data = (conn.recv(BUFFER_SIZE)).strip()
        logging.debug('Received "%s" from %s', data, addr)

        if data:
            cmd = data.split('=')[0]

            if cmd == "PIN":
                p = gpio.parse(data)
                toggle_output = str(p.toggle())
                conn.send(toggle_output)
            elif cmd == "ALLRELAYS":
                gpio.toggle_all_relays(int(data.split('=')[1]))
        else:
            break

        conn.close()


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
    logging.info('TCP server listening on %s:%s', TCP_IP, TCP_PORT)

    # SET UP RELAYS
    gpio.toggle_all_relays(1)

    serve_forever()
