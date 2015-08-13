#!/usr/bin/env python

import threading, argparse, time, logging

logging.basicConfig(format='[%(asctime)s][%(module)s][%(levelname)s] %(message)s', level=logging.DEBUG)


##### argparse stuff #####

parser = argparse.ArgumentParser(description='Launcher for RPi Home Controller.')
parser.add_argument("--tcp", help="Enable TCP server", action="store_true")
parser.add_argument("--http", help="Enable HTTP server", action="store_true")
parser.add_argument("--ws", help="Enable WebSocket server", action="store_true")
parser.add_argument("--ping", help="Enable Ping worker", action="store_true")
parser.add_argument("--thermostat", help="Enable Thermostat worker", action="store_true")


args = parser.parse_args()

##########

threads = []


def setupthread(thread_obj, name):
    thread_obj.setDaemon(True)
    thread_obj.name = name

    print "starting %s thread..." % name
    thread_obj.start()

    threads.append(thread_obj)

def threadmonitor():
    while 1:
        time.sleep(600)
        for thread in threads:
            logging.info("%s Alive: %s" % (thread.name, thread.isAlive()))

if args.tcp:

    print "importing TCP_server..."
    import TCP_server
    print "done"

    tcp_thread = threading.Thread(target=TCP_server.main)
    setupthread(tcp_thread, 'tcp')

if args.http:

    print "importing HTTP_server..."
    import HTTP_server
    print "done"

    http_thread = threading.Thread(target=HTTP_server.main)
    setupthread(http_thread, 'http')

if args.ping:

    print "importing ping_worker..."
    import ping_worker
    print "done"

    ping_thread = threading.Thread(target=ping_worker.main)
    setupthread(ping_thread, 'ping')

if args.thermostat:
    print "importing thermostat_worker..."
    import thermostat_worker
    print "done"

    thermostat_thread = threading.Thread(target=thermostat_worker.main)
    setupthread(thermostat_thread, 'thermostat')


########## threadmonitor

threadmonitor_thread = threading.Thread(target=threadmonitor)

print "starting threadmonitor thread..."

threadmonitor_thread.setDaemon(True)

threadmonitor_thread.start()



if args.ws:

    print "importing WebSocket_server..."
    import WebSocket_server
    print "done"

    print "starting ws server on main thread..."
    WebSocket_server.main()


else:
    from twisted.python import log
    import sys
    log.startLogging(sys.stdout)

    while 1:
        pass
        time.sleep(3600)
        

