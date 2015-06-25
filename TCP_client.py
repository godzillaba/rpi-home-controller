import socket

def relaymessage(dest_addr, dest_port, msg):
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((dest_addr, int(dest_port)))
    
    s.send(str(msg))
    data = s.recv(1024)
    s.close()

    return data