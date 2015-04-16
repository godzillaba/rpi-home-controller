import SimpleHTTPServer
import SocketServer
import compile_html

PORT = 8001

class compile_handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_GET(self):
		print "Compiling page"
		compile_html.main()
		if self.path == "/":
			self.path = "/web/html"
		SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
		

Handler = compile_handler

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()
