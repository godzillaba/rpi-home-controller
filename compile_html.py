from jinja2 import Environment, PackageLoader
import json

env = Environment(loader=PackageLoader('web', 'templates'))
template = env.get_template('template1.html')

with open('data.json') as data_file:    
    data = json.load(data_file)

print (data['Groups'])[1]

groups = (data['Groups'])
html = template.render(groups=groups)
print html

with open('web/html/index.html', 'w') as html_file:
	html_file.truncate()
	html_file.write(html)