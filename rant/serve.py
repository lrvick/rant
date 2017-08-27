import logging
from rant.build import Builder
from livereload import Server as LRServer


class Server(object):
    """Generate web-ready static files from templates/data/config"""

    def __init__(self, source_dir='.', dest_dir='./deploy'):
        self._source_dir = source_dir
        self._dest_dir = dest_dir
        self._server = LRServer()
        self._port = 8080

    def serve(self):
        builder = Builder(self._source_dir, self._dest_dir)
        self._server.watch('*/*.md', builder.build, delay=2)
        self._server.serve(
            root=self._dest_dir,
            port=self._port
        )
        logging.info('Starting server on port: %s' % self._port)
