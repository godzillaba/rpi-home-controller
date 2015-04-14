from jinja2 import Environment, PackageLoader
import json

class switchgroup(object):
	def __init__(self, description, gpiopin):
		self.description = description
		self.gpiopin = gpiopin

env = Environment(loader=PackageLoader('web', 'templates'))
template = env.get_template('template1.html')

with open('data.json') as data_file:    
    data = json.load(data_file)

print (data['Groups'])[1]

groups = (data['Groups'])



print template.render(groups=groups)

