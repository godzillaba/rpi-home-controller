import socket

local_ip = "0.0.0.0"
local_port = 5432
BUFFER_SIZE = 1024

dest_host = 'pi'
dest_ip = socket.gethostbyname(dest_host)
dest_port = 5432

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((local_ip, local_port))
s.listen(1)

def client(dest_ip, dest_port, msg):
	proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	proxy.connect((dest_ip, dest_port))
	proxy.send(msg)
	proxy.close()


while 1:
    conn, addr = s.accept()
    data = (conn.recv(BUFFER_SIZE)).strip()
    if data:
        print data
        client(dest_ip, dest_port, data)
    else:
        break
    
    conn.close()