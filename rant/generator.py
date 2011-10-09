import os
import yaml
import markdown
from jinja2 import Environment, FileSystemLoader

def generate():
    cwd = os.getcwd()
    config_file = file('%s/config.yml' % cwd)
    config = yaml.load(config_file)
    #print config
    env = Environment(loader=FileSystemLoader('%s/layouts/' % cwd))
    for layout in ['post','page']:
        content_files = os.listdir('%s/%ss' % (cwd,layout))
        for content_file in content_files:
            headers_text = ''
            content_text = ''
            headers_done = None
            content_fh = file('%s/%ss/%s' % (cwd,layout,content_file))
            line = content_fh.readline()
            while line:
                line = content_fh.readline()
                if not headers_done:
                    if line != '---\n':
                        if line:
                            headers_text = "%s%s" % (headers_text,line)
                    else:
                        headers_done = True
                elif line:
                    content_text = "%s%s" % (content_text,line)
            headers = yaml.load(headers_text)
            content = markdown.markdown(content_text)
            template = env.get_template('%s.html' % layout)
            rendered_page = template.render(
                                config=config,
                                content=content,
                                title=headers['title'],
                                tags=headers['tags'],
                            )
            print rendered_page
    print "Site Generated"
    pass
