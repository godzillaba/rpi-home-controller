import SimpleHTTPServer
import SocketServer
import os
import render_html

PORT = 8080

class render(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_GET(self):
		relative_path = "." + self.path
		is_file = os.path.isfile(relative_path)
		is_dir = os.path.isdir(relative_path)
		
		if is_file:
			if relative_path.split('.')[1] == "html":
				print "Compiling page"
				render_html.main(relative_path)
		elif is_dir:
			ls = os.listdir(relative_path)
			if "index.html" in ls:
				print "Compiling page"
				render_html.main(relative_path + "index.html")

		
		SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
		

Handler = render

httpd = SocketServer.TCPServer(("", PORT), Handler)

print "serving at port", PORT
httpd.serve_forever()
