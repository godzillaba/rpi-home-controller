from server_lib import gpio
from server_lib import config as conf
import socket
import logging
import RPi.GPIO as GPIO

# LOGGING / CONFIG VARIABLES
f = "server_lib/config.conf"
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)




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
TCP_IP = conf.arg(f, "LISTENADDR")
TCP_PORT = int(conf.arg(f, "PORT"))
BUFFER_SIZE = int(conf.arg(f, "BUFFERSIZE"))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
logging.info('TCP server listening on %s:%s', TCP_IP, TCP_PORT)

# SET UP RELAYS
gpio.toggle_all_relays(1)


# SERVE
try:
    serve_forever()
        
except KeyboardInterrupt:
    print '\n'
    logging.info('^C received! Running GPIO.cleanup()')
    GPIO.cleanup()