from server_lib import gpio
from server_lib import config as conf
import socket

f = "server_lib/config.conf"


# relay init
relaypins = (conf.arg(f, "RELAYPINS")).split()
for pin in relaypins:
    rp = gpio.pin(int(pin), "OUT", 1)
    rp.toggle()

TCP_IP = conf.arg(f, "LISTENADDR")
TCP_PORT = int(conf.arg(f, "PORT"))
BUFFER_SIZE = int(conf.arg(f, "BUFFERSIZE"))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((TCP_IP, TCP_PORT))
s.listen(1)


while 1:
    conn, addr = s.accept()
    print 'Connection address:', addr
    
    data = (conn.recv(BUFFER_SIZE)).strip()
    print data
    
    if data:
        cmd = data.split('=')[0]
       
        if cmd == "PIN":
            p = gpio.parse(data)
            p.toggle()

    else:
        break
    
    conn.close()
