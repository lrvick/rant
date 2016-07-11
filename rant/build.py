from io import open
import os
import yaml
import time
from datetime import datetime
from fnmatch import fnmatch
from jinja2 import Environment, FileSystemLoader
from rant.parse import Parser
from shutil import copytree


class Builder(object):
    """Generate web-ready static files from templates/data/config"""

    def __init__(self, source_dir='.', dest_dir='./deploy'):
        self._source_dir = source_dir
        self._dest_dir = dest_dir

        with open('%s/config.yml' % source_dir, 'r') as fh:
            self.config = yaml.load(fh)
            fh.close()

        self._page_files = self._find_source_files('page')
        self._post_files = self._find_source_files('post')
        self._per_page = self.config['paginate']
        self._navigation = self._get_navigation()
        self._env = Environment(
            loader=FileSystemLoader('%s/layouts/' % self._source_dir)
        )

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

    def _render_html(self, context):
        template = self._env.get_template('%s.html' % context['layout'])
        current_page = context['permalink']
        if context['layout'] == 'post':
            current_page = 'blog'
        context['config'] = self.config
        context['navigation'] = self._navigation
        context['current_page'] = current_page
        return template.render(context)

    def _write_file(self, content, permalink, filename='index.html'):
        save_folder = '%s/%s' % (self._dest_dir, permalink)
        if not os.path.isdir(save_folder):
            os.makedirs(save_folder)
        filepath = "%s/%s" % (save_folder, filename)
        with open(filepath, 'w', 1) as save_fh:
            save_fh.write(content)
            save_fh.close()
        print("-> '%s'" % filepath)

    def _gen_contexts(self, filenames):
        contexts = []
        for filename in filenames:
            context = Parser(filename).parse()
            if context is None:
                break
            context['rendered_html'] = self._render_html(context)
            contexts.append(context)
        return contexts

    def _write_contexts(self, contexts):
        for context in contexts:
            self._write_file(context['rendered_html'], context['permalink'])

    def _render_blog_index_page(self, page_posts, page_num):
        post_count = len(self._post_files)
        total_index_pages = int(round(post_count / self._per_page, 0))
        index_template = self._env.get_template('blog_index.html')
        rendered_page = index_template.render(
            config=self.config,
            page_posts=page_posts,
            total_pages=total_index_pages,
            page_num=page_num,
            navigation=self._navigation,
            current_page='blog',
        )
        return rendered_page

    def _write_blog_index_page(self, page_posts, page_num):
        rendered_page = self._render_blog_index_page(page_posts, page_num)
        if page_num == 1:
            self._write_file(rendered_page, '')
            self._write_file(rendered_page, 'blog')
        self._write_file(
            rendered_page,
            'blog/pages/%s' % page_num
        )

    def _write_blog_index(self, posts):
        index_posts = []
        processed = 0
        page_num = 1
        for post in posts:
            index_posts.append(post)
            processed += 1
            if len(index_posts) == self._per_page or processed == len(posts):
                self._write_blog_index_page(index_posts, page_num)
                page_num += 1
                index_posts = []

    def _write_feed(self, schema, posts):
        template = self._env.get_template('%s.xml' % schema)
        rendered_feed = template.render(
            config=self.config,
            posts=posts,
            current_date=datetime.fromtimestamp(time.time()),
        )
        self._write_file(rendered_feed, 'blog', '%s.xml' % schema)

    def _write_sitemap(self, posts, pages):
        template = self._env.get_template('sitemap.xml')
        rendered_feed = template.render(
            config=self.config,
            posts=posts,
            pages=pages,
            current_date=datetime.fromtimestamp(time.time()),
        )
        self._write_file(rendered_feed, '', 'sitemap.xml')

    def _copy_static(self):
        copytree("%s/static" % self._source_dir, self._dest_dir)

    def build(self):
        start_time = time.time()

        print("\nGenerating Pages...")
        print(("="*50))
        page_contexts = self._gen_contexts(self._page_files)
        self._write_contexts(page_contexts)

        print("\nGenerating Posts...")
        print(("="*50))
        post_contexts = self._gen_contexts(self._post_files)
        self._write_contexts(post_contexts)

        print("\nGenerating Blog Index...")
        print(("="*50))
        self._write_blog_index(post_contexts)

        print("\nGenerating Feeds...")
        print(("="*50))
        self._write_feed('atom', post_contexts)
        self._write_feed('rss', post_contexts)

        print("\nGenerating Sitemap...")
        print(("="*50))
        self._write_sitemap(post_contexts, page_contexts)

        print("\nCopying Static Files...")
        print(("="*50))

        total_time = round(time.time() - start_time, 2)
        print("\nGeneration Completed in %s seconds" % total_time)
        self._copy_static()
