import SimpleHTTPServer
import SocketServer
import os, sys
from server_lib import render_html
import json
import base64
import logging

class render(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def render(self, template_path):
#        self.do_HEAD()
        logging.debug("Serving dynamic file %s" % template_path)
    
        self.wfile.write(render_html.main(template_path))
        return
    
    def render_static(self, filepath):
#        self.do_HEAD()
        
        logging.debug("Serving static file %s" % filepath)
        
        with open(filepath) as static_file:
            file_contents = static_file.read()
        
        self.wfile.write(file_contents)

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Home Controller\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def auth(self):
        global key
        if self.headers.getheader('Authorization') == None:
            self.do_AUTHHEAD()
            self.wfile.write('no auth header received')
            pass
        elif (self.headers.getheader('Authorization')).split('Basic ')[1] in keys:
            self.do_GET_authed()
            pass
        else:
            self.do_AUTHHEAD()
            self.wfile.write(self.headers.getheader('Authorization'))
            self.wfile.write('not authenticated')
            pass

    def do_GET(self):
        global exempt_subnets

        addr = self.client_address[0]
        subnet = addr.rsplit('.',1)[0]

        if subnet in exempt_subnets:
            logging.debug("Client is exempt from authentication. Skipping basic auth")
            self.do_GET_authed()

        else:
            logging.debug("Client is not exempt from authentication. Proceeding with basic auth")
            self.auth()


    def do_GET_authed(self):
        
        template_path = self.path

        self.path = fullpath + "/web/templates" + self.path
        
        absolute_path = self.path
        
        is_file = os.path.isfile(absolute_path)
        is_dir = os.path.isdir(absolute_path)
        
        logging.info("URL requested: %s" % self.path)

        if is_file:
            logging.debug("Requested URL is a file")
            extension = absolute_path.split('.')[1]
            if extension == "html":
                logging.info("Compiling %s (%s)" % (template_path, absolute_path))
                self.render(template_path)
            else:
                self.render_static(absolute_path)

        elif is_dir:
            
            logging.debug("Requested URL is a directory")

            ls = os.listdir(absolute_path)
            if "index.html" in ls:
                logging.info("Compiling %s (%s)" % (template_path, absolute_path))
                self.render(template_path + "index.html")
            else:
                stringio_obj = self.list_directory(absolute_path)                
                self.wfile.write(stringio_obj.getvalue())
                
        else:
            stringio_obj = self.list_directory(absolute_path)                
            self.wfile.write(stringio_obj.getvalue())


pathname = os.path.dirname(sys.argv[0])        
fullpath = os.path.abspath(pathname)

config_file = fullpath + "/config/config.json"
users_file = fullpath + "/config/users.json"

with open(config_file) as data_file:
    data = json.load(data_file)

with open(users_file) as users_file:
    users = json.load(users_file)["Users"]

PORT = int(data["HTTP"]['port'])

keys = []

for user in users:
    key = base64.b64encode(user)
    keys.append(key)


exempt_subnets = data["Web"]["Exempt_Subnets"]

Handler = render
Handler.allow_reuse_address = True


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


# httpd = SocketServer.TCPServer(("", PORT), Handler)
httpd = ThreadedTCPServer(("", PORT), Handler)

def main():
    httpd.serve_forever()
