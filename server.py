from server_lib import gpio
import socket

TCP_IP = '0.0.0.0'
TCP_PORT = 5432
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((TCP_IP, TCP_PORT))
s.listen(1)


while 1:
    conn, addr = s.accept()
    print 'Connection address:', addr
    
    data = (conn.recv(BUFFER_SIZE)).strip()
    print(data)
    
    if data:
        cmd = data.split('=')[0]
       
        if cmd == "PIN":
            p = gpio.parse(data)
            gpio.toggle(p)

        

    else:
        break
    
    conn.close()