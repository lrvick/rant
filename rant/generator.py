import os
import yaml
import markdown
import re
import time
# import datetime
import codecs
from fnmatch import fnmatch
from jinja2 import Environment, FileSystemLoader


class Generator(object):
    """Generate web-ready static files from templates/data/config"""

    def __init__(self, source_dir='.', dest_dir='./deploy'):
        self._source_dir = source_dir
        self._dest_dir = dest_dir
        self.config = yaml.load(open('%s/config.yml' % source_dir))

        self._page_files = self._find_source_files('page')
        self._post_files = self._find_source_files('post')
        self._per_page = self.config['paginate']
        self._navigation = self._get_navigation()
        self._env = Environment(
            loader=FileSystemLoader('%s/layouts/' % self._source_dir)
        )
        self.all_content = {}

    def _find_source_files(self, layout):
        source_files = []
        file_names = os.listdir('%s/%ss' % (self._source_dir, layout))
        for file_name in file_names:
            if fnmatch(file_name, '*.md'):
                full_filename = '%s/%ss/%s' % (self._source_dir,
                                               layout,
                                               file_name)
                source_files.append(full_filename)
        return source_files

    def _get_navigation(self):
        navigation = ['blog']
        for filepath in self._page_files:
            filename = os.path.split(filepath)[1]
            nav_item = filename.split('.')[0].replace('_', ' ').lower()
            navigation.append(nav_item)
        return navigation

    def _parse_file(self, filename):
        headers_text = ''
        content_text = ''
        headers_done = None
        content_fh = codecs.open(filename, 'r', 'utf-8')
        line = content_fh.readline()
        while line:
            line = content_fh.readline()
            if not headers_done:
                if line != '---\n':
                    if line:
                        headers_text = "%s%s" % (headers_text, line)
                else:
                    headers_done = True
            elif line:
                content_text = "%s%s" % (content_text, line)
        headers = yaml.load(headers_text)
        content = markdown.markdown(
            content_text,
            ['codehilite(linenums=True)', 'tables']
        )
        if headers['draft']:
            return None
        permalink = re.sub("[^a-zA-Z0-9]+", "_", headers['title']).lower()
        content_vars = {
          'permalink': permalink,
          'content': content,
        }
        return dict(content_vars, **headers)

    def _render_html(self, context, layout):
        template = self._env.get_template('%s.html' % layout)
        if layout == 'post':
            current_page = 'blog'
        else:
            current_page = context['permalink']
        context['config'] = self.config
        context['navigation'] = self._navigation
        context['current_page'] = current_page
        return template.render(context)

    def _write_html(self, html, permalink, layout):
        if layout == 'page':
            save_folder = '%s/%s' % (self._dest_dir, permalink)
        elif layout == 'post':
            save_folder = '%s/blog/%s' % (self._dest_dir, permalink)
        if not os.path.isdir(save_folder):
            os.makedirs(save_folder)

        save_fh = codecs.open("%s/index.html" % save_folder, 'w', 'utf-8')
        save_fh.write(html)

    def _gen_blog_index_page(self, page_posts, page_num):
        post_count = len(self._post_files)
        total_index_pages = int(round(post_count / self._per_page, 0))
        index_template = self._env.get_template('blog_index.html')
        rendered_page = index_template.render(
            config=self._config,
            page_posts=page_posts,
            total_pages=total_index_pages,
            page_num=page_num,
            navigation=self._navigation,
            current_page='blog',
        )
        if page_num == 1:
            save_folder = '%s' % self._dest_dir
            save_fh = codecs.open("%s/index.html" % save_folder, 'w', 'utf-8')
            save_fh.write(rendered_page)
            save_folder = '%s/blog' % self._dest_dir
            if not os.path.isdir(self._dest_dir):
                os.makedirs(save_folder)
            save_fh = codecs.open("%s/index.html" % save_folder, 'w', 'utf-8')
            save_fh.write(rendered_page)
        save_folder = '%s/blog/pages/%s' % (self._dest_dir, page_num)
        if not os.path.isdir(save_folder):
            os.makedirs(save_folder)
        save_fh = codecs.open("%s/index.html" % save_folder, 'w', 'utf-8')
        save_fh.write(rendered_page)

    def _gen_posts(self):
        post_files = self._find_source_files('post')
        index_page_posts = []
        page_num = 0
        for filename in post_files:
            context = self._parse_file(filename)
            self.all_content['posts'][filename] = context
            index_page_posts.append(filename)
            if len(self._page_posts) == self._per_page:
                self._gen_blog_index_page(index_page_posts, page_num)
                page_num += 1
                index_page_posts = []
                rendered_page = self._render_html(context, 'post')
                self._write_html(rendered_page, context['permalink'], 'post')

    def _gen_pages(self):
        for filename in self._page_files:
            context = self._parse_file(filename)
            self.all_content['pages'][filename] = context
            rendered_page = self._render_html(context, 'page')
            self._write_html(rendered_page, context['permalink'], 'page')

    def generate(self):
        start_time = time.time()

        self._gen_pages()
        self._gen_posts()

        # print("\nGenerating XML Feeds...")
        # print(("="*50))
        # current_date = datetime.datetime.fromtimestamp(start_time)
        # template = env.get_template('atom.xml')
        # rendered_page = template.render(
        #                     config=config,
        #                     posts=all_content['post'],
        #                     current_date=current_date,
        #                 )
        # save_folder = '%s/deploy/blog/' % (cwd)
        # save_fh = codecs.open("%s/atom.xml" % save_folder,'w','utf-8')
        # save_fh.write(rendered_page)
        # print("-> '/blog/atom.xml'")
        # template = env.get_template('rss.xml')
        # rendered_page = template.render(
        #                     config=config,
        #                     posts=all_content['post'],
        #                     current_date=current_date,
        #                 )
        # save_folder = '%s/deploy/blog/' % (cwd)
        # save_fh = codecs.open("%s/rss.xml" % save_folder,'w','utf-8')
        # save_fh.write(rendered_page)
        # print("-> '/blog/rss.xml'")
        # template = env.get_template('sitemap.xml')
        # rendered_page = template.render(
        #                     config=config,
        #                     pages=all_content['post'],
        #                     posts=all_content['page'],
        #                     current_date=current_date,
        #                 )
        # save_folder = '%s/deploy/' % (cwd)
        # save_fh = codecs.open("%s/sitemap.xml" % save_folder,'w','utf-8')
        # save_fh.write(rendered_page)
        # print("-> '/sitemap.xml'")

        total_time = round(time.time() - start_time, 2)
        print("\nGeneration Completed in %s seconds" % total_time)
