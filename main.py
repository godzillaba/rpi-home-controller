#!/usr/bin/env python

import threading, argparse


##### argparse stuff #####

parser = argparse.ArgumentParser(description='Launcher for RPi Home Controller.')
parser.add_argument("--tcp", help="Enable TCP server", action="store_true")
parser.add_argument("--http", help="Enable HTTP server", action="store_true")
parser.add_argument("--ws", help="Enable WebSocket server", action="store_true")
parser.add_argument("--ping", help="Enable Ping worker", action="store_true")
parser.add_argument("--thermostat", help="Enable Thermostat worker", action="store_true")


args = parser.parse_args()

##########

if args.tcp:

    print "importing TCP_server..."
    import TCP_server
    print "done"

    tcp_thread = threading.Thread(target=TCP_server.main)
    tcp_thread.setDaemon(True)

    print "starting tcp thread..."
    tcp_thread.start()

if args.http:

    print "importing HTTP_server..."
    import HTTP_server
    print "done"

    http_thread = threading.Thread(target=HTTP_server.main)
    http_thread.setDaemon(True)

    print "starting http thread..."
    http_thread.start()

if args.ping:

    print "importing ping_worker..."
    import ping_worker
    print "done"

    ping_thread = threading.Thread(target=ping_worker.main)
    ping_thread.setDaemon(True)

    print "starting ping thread"
    ping_thread.start()

if args.thermostat:
    print "importing thermostat_worker..."
    import thermostat_worker
    print "done"

    thermostat_thread = threading.Thread(target=thermostat_worker.main)
    thermostat_thread.setDaemon(True)

    print "starting thermostat thread"
    thermostat_thread.start()


if args.ws:

    print "importing WebSocket_server..."
    import WebSocket_server
    print "done"

    print "starting ws server on main thread..."
    WebSocket_server.main()



