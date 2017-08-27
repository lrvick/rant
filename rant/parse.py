from markdown import markdown
import yaml
import re
from io import open


class Parser(object):

    def __init__(self, filename):
        self._filename = filename

    def _get_file_parts(self):
        fh = open(self._filename, 'r')
        content = fh.read().split('---')
        fh.close()
        headers = yaml.load(content[1])
        body = content[2]
        return [headers, body]

    def _get_permalink(self, headers):
        prefix = 'blog/' if headers['layout'] == 'post' else ''
        title = headers['title'].lower()
        permalink = '%s%s' % (prefix, re.sub("[^a-zA-Z0-9]+", "_", title))
        return permalink

    def parse(self):
        values, body = self._get_file_parts()
        if 'draft' in values and values['draft'] is True:
            return None
        values['content'] = markdown(
            body,
            extensions=[
                'markdown.extensions.codehilite',
                'markdown.extensions.tables'
            ],
            extension_configs={
                "codehilite":{
                    "linenums": True
                }
            }
        )
        values['permalink'] = self._get_permalink(values)
        return values
