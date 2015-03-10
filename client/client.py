#!/usr/bin/env python
import socket
import sys

def usage():
	print "Usage: python client.py <hostname or ip> <port> <message>"

try:
	host = sys.argv[1]
	TCP_IP = socket.gethostbyname(host)
	TCP_PORT = int(sys.argv[2])
	BUFFER_SIZE = 1024
	MESSAGE = sys.argv[3]

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))
	s.send(MESSAGE)
	s.close()

except NameError:
	usage()
except IndexError:
	usage()
except ValueError:
	usage()
