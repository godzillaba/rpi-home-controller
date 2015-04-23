import json
import threading

print "importing TCP_server..."
import TCP_server
print "done"

print "importing HTTP_server..."
import HTTP_server
print "done"

print "importing WebSocket_server..."
import WebSocket_server
print "done"

tcp_thread = threading.Thread(target=TCP_server.main)
tcp_thread.setDaemon(True)

http_thread = threading.Thread(target=HTTP_server.main)
http_thread.setDaemon(True)

print "starting tcp thread..."
tcp_thread.start()

print "starting http thread..."
http_thread.start()

print "starting ws server on main thread..."
WebSocket_server.main()


