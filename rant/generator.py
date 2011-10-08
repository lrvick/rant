import os
import yaml
from jinja2 import Environment, FileSystemLoader

def generate():
    config_file = file('%s/config.yml' % os.getcwd())
    config = yaml.load(config_file)
    print config
    env = Environment(loader=FileSystemLoader('%s/layouts/' % os.getcwd()))
    template = env.get_template('base.html')
    print template.render(config=config)
    print "Site Generated"
    pass
