#import RPi.GPIO as GPIO
import socket

debug = False


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
                try:
                    pin = int((data.split('=')[1]).split(',')[0])
                    pintype = data.split(',')[1]
                    if pintype == "OUT":
                        pinstate = int(data.split(',')[2])
                    elif pintype == "IN":
                        pinstate = 0
                except ValueError:
                    print "\nValueError during parsing\n"
                    conn.send("\nValueError during parsing\n\n")
                    break
                except IndexError:
                    print "\nIndexError during parsing\n"
                    conn.send("\nIndexError during parsing\n\n")
                    break
                    
                if debug: print "pin info (%s:%s:%s)" % (pin, pintype, pinstate)
                
                # SYNTAX CHECKING                
                if (pintype != "OUT") and (pintype != "IN"):
                    print "\nInvalid Syntax - Neither out or in specified\n"
                    conn.send("\nInvalid Syntax - Neither out or in specified\n\n")
                    break
                if pinstate != 1 and pinstate != 0:
                    print "\nInvalid Syntax - High/Low not specified as binary\n"
                    conn.send("\nInvalid Syntax - High/Low not specified as binary\n\n")
                    break
                
                """# GPIO STUFF
                try:
                    GPIO.setup(pin, GPIO.OUT)
                    if pintype == "OUT":
                        if debug: print "output type specified"
                        GPIO.output(pin, pinstate)
                    elif pintype == "IN":
                        if debug: print "input type specified"
                        conn.send(str(GPIO.input(pin)) + "\n")
                except ValueError:
                    print "\nERROR: Invalid RPi GPIO Pin\n"
                    conn.send("\nERROR: Invalid RPi GPIO Pin\n\n")
                    break
                """
            elif data == "GPIO-CLEANUP/EXIT":
                fin = True
                break
            else:
                if data != "":
                    print "\nInvalid Command\n"
                    conn.send("\nInvalid Command\n\n")
                    break
        else:
            break
        if debug: print "data: ", data
    conn.close()
    if fin:
        break
if debug: print "cleanup!"
#GPIO.cleanup()