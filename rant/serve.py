import logging
from rant.build import Builder
from livereload import Server as LRServer


class Server(object):
    """Generate web-ready static files from templates/data/config"""

    def __init__(
            self,
            source_dir='.',
            dest_dir='./deploy',
            host='::1',
            port=8080):
        self._source_dir = source_dir
        self._dest_dir = dest_dir
        self._server = LRServer()
        self._host = host
        self._port = port

    def serve(self):
        builder = Builder(self._source_dir, self._dest_dir)
        self._server.watch('*/*.md', builder.build, delay=2)
        print self._host, self._port
        self._server.serve(
            root=self._dest_dir,
            host=self._host,
            port=self._port
        )
        logging.info('Starting server on port: %s' % self._port)
