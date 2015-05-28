import SimpleHTTPServer
import SocketServer
import os, sys
from server_lib import render_html
import json
import base64

class render(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def render(self, template_path):
        self.do_HEAD()
        self.wfile.write(render_html.main(template_path))
        return

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        print "send header"
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

        print addr, subnet, exempt_subnets

        if subnet in exempt_subnets:
            self.do_GET_authed()

        else:
            self.auth()


    def do_GET_authed(self):
        
        template_path = self.path
        self.path = fullpath + "/web/templates" + self.path
        
        is_file = os.path.isfile(self.path)
        is_dir = os.path.isdir(self.path)

        if is_file:
            extension = self.path.split('.')[2]
            if extension == "html":
                print "Compiling %s (%s)" % (template_path, self.path)
                self.render(template_path)
            else:
                SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

        elif is_dir:
            ls = os.listdir(self.path)
            if "index.html" in ls:
                print "Compiling %s (%s)" % (template_path, self.path)
                self.render(template_path + "index.html")
            else:
                SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
        else:
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


pathname = os.path.dirname(sys.argv[0])        
fullpath = os.path.abspath(pathname)

config_file = fullpath + "/data.json"
users_file = fullpath + "/users.json"

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

httpd = SocketServer.TCPServer(("", PORT), Handler)

def main():
    httpd.serve_forever()
