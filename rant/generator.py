import os
import yaml
import markdown
import re
import time
from fnmatch import fnmatch
from jinja2 import Environment, FileSystemLoader

def generate():
    start_time = time.time()
    cwd = os.getcwd()
    config_file = file('%s/config.yml' % cwd)
    config = yaml.load(config_file)
    env = Environment(loader=FileSystemLoader('%s/layouts/' % cwd))

    print "\nParsing all posts and pages..."
    print("="*50)
    all_content = {
        'post' : [],
        'page' : []
    }
    for layout in ['post','page']:
        for content_file in os.listdir('%s/%ss' % (cwd,layout)):
            if fnmatch(content_file,'*.md'):
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
                content = markdown.markdown(
                                content_text,
                                ['codehilite(force_linenos=True)','tables']
                            )
                if not headers['draft']:
                    permalink = re.sub("[^a-zA-Z0-9]+","_",headers['title']).lower()
                    all_content[layout].append({
                        'title' : headers['title'],
                        'permalink' : permalink,
                        'tags' : headers['tags'],
                        'date' : headers['date'],
                        'comments' : headers['comments'],
                        'content' : content,
                    })
                print "<- '%s'" % content_file

    print "\nGenerating Main Navigation..."
    print("="*50)
    navigation = ['blog']
    for item in all_content['page']:
        navigation.append(item['title'].lower())
    print '-> %s' % navigation

    print "\nGenerating HTML blog index from templates..."
    print("="*50)
    per_page = config['paginate']
    post_count = len(all_content['post'])
    total_pages = int(round(post_count / per_page,0))
    page_posts = []
    page_num = 0
    posts_processed = 0
    index_template = env.get_template('blog_index.html')
    for item in all_content['post']:
        page_posts.append(item)
        posts_processed += 1
        if len(page_posts) == per_page or posts_processed == post_count:
            page_num += 1
            print page_num,total_pages
            rendered_page = index_template.render(
                                config=config,
                                page_posts=page_posts,
                                total_pages=total_pages,
                                page_num=page_num,
                                navigation=navigation,
                            )
            if page_num == 1:
                save_folder = '%s/deploy' % cwd
                save_fh = open("%s/index.html" % save_folder,'w')
                save_fh.write(rendered_page)
                print "-> '/'"
                save_folder = '%s/deploy/blog' % cwd
                save_fh = open("%s/index.html" % save_folder,'w')
                save_fh.write(rendered_page)
                print "-> '/blog'"
            save_folder = '%s/deploy/blog/pages/%s' % (cwd,page_num)
            if not os.path.isdir(save_folder):
                os.makedirs(save_folder)
            save_fh = open("%s/index.html" % save_folder,'w')
            save_fh.write(rendered_page)
            print "-> '%s/'" % save_folder.replace('%s/deploy' % cwd,'')
            page_posts = []

    print "\nRendering HTML posts and pages from templates..."
    print("="*50)
    for layout in ['post','page']:
        for item in all_content[layout]:
            template = env.get_template('%s.html' % layout)
            rendered_page = template.render(
                                config=config,
                                content=item['content'],
                                title=item['title'],
                                navigation=navigation,
                                tags=item['tags'],
                            )
            if layout == 'page':
                save_folder = '%s/deploy/%s' % (cwd,item['permalink'])
            elif layout == 'post':
                save_folder = '%s/deploy/blog/%s' % (cwd,permalink)
            if not os.path.isdir(save_folder):
                os.makedirs(save_folder)
            save_fh = open("%s/index.html" % save_folder,'w')
            save_fh.write(rendered_page)
            print "-> '%s/'" % save_folder.replace('%s/deploy' % cwd,'')
    total_time = round(time.time() - start_time,2)
    print "\nGeneration Completed in %s seconds" % total_time
