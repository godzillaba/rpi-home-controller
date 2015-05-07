from jinja2 import Environment, PackageLoader
import json


def main(path):
    env = Environment(loader=PackageLoader('web', 'templates'))
    template = env.get_template(path)

    with open('data.json') as data_file:
        data = json.load(data_file)

    html = template.render(data=data)

    return html
