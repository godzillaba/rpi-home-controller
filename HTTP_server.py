import SimpleHTTPServer
import SocketServer
import os
from server_lib import render_html
import json

with open('data.json') as data_file:    
	    data = json.load(data_file)

PORT = int(data["HTTP"]['port'])

class render(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def render(self, template_path):
		self.send_response(200)
        	self.send_header('Content-type','text/html')
        	self.end_headers()
        	self.wfile.write(render_html.main(template_path))
        	return

	def do_GET(self):
		template_path = self.path
		self.path = "/web/templates" + self.path
		relative_path = "." + self.path
		is_file = os.path.isfile(relative_path)
		is_dir = os.path.isdir(relative_path)
		
		if is_file:
                        extension = relative_path.split('.')[2]
                        if extension == "html":
				print "Compiling %s" % template_path
				self.render(template_path)
			else:
				SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
                        
		elif is_dir:
			ls = os.listdir(relative_path)
			if "index.html" in ls:
				print "Compiling %sindex.html" % relative_path
				self.render(template_path + "index.html")
			else:
				SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
		else:
			SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

		
		

Handler = render
Handler.allow_reuse_address = True

httpd = SocketServer.TCPServer(("", PORT), Handler)

def main():
	httpd.serve_forever()
