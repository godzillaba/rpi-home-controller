from jinja2 import Environment, PackageLoader
import json
import os, sys

pathname = os.path.dirname(sys.argv[0])        
fullpath = os.path.abspath(pathname)

config_file = fullpath + "/config/config.json"

def main(path):
    env = Environment(loader=PackageLoader('web', 'templates'))
    template = env.get_template(path)

    with open(config_file) as data_file:
        data = json.load(data_file)

    html = template.render(data=data)

    return html
