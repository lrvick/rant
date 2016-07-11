from os import environ, system
from os.path import dirname, join, abspath
from shutil import copyfile
from tempfile import NamedTemporaryFile
from datetime import datetime
from time import gmtime, strftime
from rant.parse import Parser


class Creator(object):
    """Create new page or post"""

    def __init__(self, dest_dir, layout='post'):
        self._dest_dir = dest_dir
        self._layout = layout
        self._rant_path = abspath(join(dirname(__file__), ".."))
        self._time = gmtime()

    def _render_template(self):
        template_vars = [
            'layout: %s' % self._layout,
            'title: \'\'',
            'date: %s' % strftime('%Y-%m-%d %H:%M:%S', self._time),
        ]
        if self._layout == 'post':
            template_vars.append('tags: []')
            template_vars.append('comments: true')
            template_vars.append('draft: false')
        template = "---\n%s\n---\n" % "\n".join(template_vars)
        return template

    def _get_savepath(self, title):
        if self._layout == 'post':
            timestamp = datetime(*self._time[:6]).strftime("%Y-%m-%d-%H%M")
            filename = '%s-%s.md' % (timestamp, title.replace(' ', '_'))
        else:
            filename = '%s.md' % (title.replace(' ', '_'))
        filepath = '%s/%ss/%s' % (self._dest_dir, self._layout, filename)
        return filepath

    def _get_temppath(self, content):
        fh = NamedTemporaryFile(delete=False)
        fh.write(content.encode('UTF-8'))
        fh.close()
        return fh.name

    def _launch_editor(self, filepath):
        system('%s %s' % (environ.get('EDITOR', 'vim'), filepath))

    def create(self):
        rendered_template = self._render_template()
        tempfile_path = self._get_temppath(rendered_template)
        self._launch_editor(tempfile_path)
        parsed_tempfile = Parser(tempfile_path).parse()
        outfile_path = self._get_savepath(parsed_tempfile['title'])
        copyfile(tempfile_path, outfile_path)
        print("Saved to: %s" % outfile_path)
