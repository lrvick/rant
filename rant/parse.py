import markdown
import yaml
import re


class Parser(object):

    def __init__(self, filename):
        self._filename = filename

    def parse(self):
        headers_text = ''
        content_text = ''
        headers_done = None
        content_fh = open(self._filename, 'r')
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
        if 'draft' in headers and headers['draft'] is True:
            return None
        permalink = '%s%s' % (
            'blog/' if headers['layout'] == 'post' else '',
            re.sub("[^a-zA-Z0-9]+", "_", headers['title']).lower()
        )
        content_vars = {
          'permalink': permalink,
          'content': content,
        }

        return dict(content_vars, **headers)
