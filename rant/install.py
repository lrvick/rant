import logging
from os import makedirs, listdir
from os.path import abspath, dirname, join
from shutil import copy, copytree


class Installer(object):
    """Initialize default rant source files in given directory"""

    def __init__(self, dest_dir):
        self._dest_dir = dest_dir
        self._rant_path = abspath(join(dirname(__file__), ".."))

    def _create_tree(self):
        makedirs('%s/posts' % self._dest_dir)
        makedirs('%s/pages' % self._dest_dir)
        makedirs('%s/static' % self._dest_dir)
        makedirs('%s/deploy' % self._dest_dir)
        makedirs('%s/deploy/blog' % self._dest_dir)

    def _copy_defaults(self):
        copy('%s/defaults/config.yml' % self._rant_path, self._dest_dir)
        copytree(
            "%s/defaults/layouts" % self._rant_path,
            "%s/layouts" % self._dest_dir
        )
        copytree(
            "%s/defaults/css" % self._rant_path,
            "%s/static/css" % self._dest_dir
        )

    def install(self):
        if listdir(self._dest_dir) != []:
            logging.info('\nUnable to initialize rant: Directory not empty')
            return False
        self._create_tree()
        self._copy_defaults()
        logging.info('\nInitialized rant in "%s"' % self._dest_dir)
        logging.info('\nYou may now edit "%s/config.yml" as needed.' % self._dest_dir)
