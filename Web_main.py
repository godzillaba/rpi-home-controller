import json
import threading

print "importing HTTP_server..."
import HTTP_server
print "done"

print "importing WebSocket_server..."
import WebSocket_server
print "done"

http_thread = threading.Thread(target=HTTP_server.main)
http_thread.setDaemon(True)

print "starting http thread..."
http_thread.start()

print "starting ws server on main thread..."
WebSocket_server.main()


