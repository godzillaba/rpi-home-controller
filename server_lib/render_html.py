from jinja2 import Environment, PackageLoader
import json
import os, sys

import plotly.tools as tls

import traceback


pathname = os.path.dirname(sys.argv[0])        
fullpath = os.path.abspath(pathname)

config_file = fullpath + "/config/config.json"

def main(path):
    env = Environment(loader=PackageLoader('web', 'templates'))
    template = env.get_template(path)

    with open(config_file) as data_file:
        data = json.load(data_file)

    hvac_units = data['Web']['HVAC']
    
    embeds = {}
    
    for unit in hvac_units:
        if unit['plotly']['enabled']:
            try:
                embeds[unit['Address']] = tls.get_embed(unit['plotly']['url'])
            except Exception:
                print '\n'
                traceback.print_exc()
                print '\n'
                
    html = template.render(data=data, embeds=embeds)

    return html
