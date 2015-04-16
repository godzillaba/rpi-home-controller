from jinja2 import Environment, PackageLoader
import json


def main(path):
	env = Environment(loader=PackageLoader('web', 'templates'))
	template = env.get_template('template1.html')

	with open('data.json') as data_file:    
	    data = json.load(data_file)


	groups = (data['Groups'])
	html = template.render(groups=groups)

	with open(path, 'w') as html_file:
		html_file.truncate()
		html_file.write(html)