import SimpleHTTPServer
import SocketServer
import os
from server_lib import render_html
import json

with open('data.json') as data_file:    
	    data = json.load(data_file)

PORT = int(data["HTTP"]['port'])

class render(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_GET(self):
		self.path = "/web/html" + self.path
		relative_path = "." + self.path
		is_file = os.path.isfile(relative_path)
		is_dir = os.path.isdir(relative_path)
		
		if is_file:
                        extension = relative_path.split('.')[2]
                        if extension == "html" or extension == "css":
				print "Compiling %s" % relative_path
				render_html.main(relative_path)
                        
		elif is_dir:
			ls = os.listdir(relative_path)
			if "index.html" in ls:
				print "Compiling %sindex.html" % relative_path
				render_html.main(relative_path + "index.html")

		
		SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
		

Handler = render
Handler.allow_reuse_address = True

httpd = SocketServer.TCPServer(("", PORT), Handler)

def main():
	httpd.serve_forever()
