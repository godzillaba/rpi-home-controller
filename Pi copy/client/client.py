#!/usr/bin/env python

import socket
import sys




pin = 37
hilo = 1


host = 'pi'
TCP_IP = socket.gethostbyname(host)
TCP_PORT = 5432
BUFFER_SIZE = 1024

MESSAGE = "PIN=%s,OUT,%s" % (pin, hilo)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
s.send(MESSAGE)
s.close()

