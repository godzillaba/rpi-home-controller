import RPi.GPIO as GPIO
import socket

debug = True
GPIO.setmode(GPIO.BOARD)

# SOCKET INITIALIZATION STUFF
TCP_IP = '0.0.0.0'
TCP_PORT = 5432
BUFFER_SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
fin = False
while 1:
    conn, addr = s.accept()
    if debug: print 'Connection address:', addr
    
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if data:
            
            data = data.strip()
            
            if data.split('=')[0] == "PIN":
                
                # DATA PARSING STUFF
                # ADD IF STATEMENT(S) TO DETERMINE THAT THERE ARE 3 , AND 1 = (OTHERWISE THROW AN ERROR)
                # ADD IF STATEMENTS TO MAKE SURE THE FIRST VAR IS A VALID GPIO PIN (PRESENT IN RELAY), THE SECOND IS EITHER OUT OR IN, AND THE THIRD IS EITHER 1 OR 0
                pin = int((data.split('=')[1]).split(',')[0])
                pintype = data.split(',')[1]
                pinstate = int(data.split(',')[2])
    
                if debug: print "pin info (%s:%s:%s)" % (pin, pintype, pinstate)
                
                # GPIO STUFF
                if pintype == "OUT":
                    if debug: print "output type specified"
                    GPIO.setup(pin, GPIO.OUT)
                    GPIO.output(pin, pinstate)
                elif pintype == "IN":
                    if debug: print "input type specified"
                
            if data == "GPIO-CLEANUP/EXIT":
                fin = True
                break
        else:
            break
        if debug: print "data: ", data
    conn.close()
    if fin:
        break
if debug: print "cleanup!"
GPIO.cleanup()