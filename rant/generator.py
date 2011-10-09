import os
import yaml
import markdown
import re
from jinja2 import Environment, FileSystemLoader

def generate():
    cwd = os.getcwd()
    config_file = file('%s/config.yml' % cwd)
    config = yaml.load(config_file)
    env = Environment(loader=FileSystemLoader('%s/layouts/' % cwd))
    all_content = {
        'post' : [],
        'page' : []
    }
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
            all_content[layout].append({
                'headers' : headers,
                'content_text' : content_text,
            })
    for layout in ['post','page']:
        for item in all_content[layout]:
            headers = item['headers']
            content_text = item['content_text']
            content = markdown.markdown(
                                content_text,
                                ['codehilite(force_linenos=True)','tables']
                            )
            template = env.get_template('%s.html' % layout)
            rendered_page = template.render(
                                config=config,
                                content=content,
                                title=headers['title'],
                                tags=headers['tags'],
                            )
            url_title = re.sub(r'\W+','', headers['title'])
            if layout == 'page':
                save_folder = '%s/deploy/%s' % (cwd,url_title)
            elif layout == 'post':
                save_folder = '%s/deploy/blog/%s' % (cwd,url_title)
            if not os.path.isdir(save_folder):
                os.makedirs(save_folder)
            save_fh = open("%s/index.html" % save_folder,'w')
            save_fh.write(rendered_page)
            print "Rendered: '%s/index.html'" % save_folder
    print "Site Generated"
    pass
