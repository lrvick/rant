import os
import shutil


class Initializer(object):
    """Initialize default rant source files in given directory"""

    def __init__(self, dest_dir):
        self._dest_dir = dest_dir
        self._rant_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        )

    def _create_tree(self):
        os.makedirs('%s/posts' % self._dest_dir)
        os.makedirs('%s/pages' % self._dest_dir)
        os.makedirs('%s/deploy' % self._dest_dir)
        os.makedirs('%s/deploy/blog' % self._dest_dir)

    def _copy_defaults(self):
        shutil.copy(
            '%s/defaults/config.yml' % self._rant_path,
            self._dest_dir
        )
        shutil.copytree(
            "%s/defaults/layouts" % self._rant_path,
            "%s/layouts" % self._dest_dir
        )

    def init(self):
        if os.listdir(self._dest_dir) != []:
            print('\nUnable to initialize rant: Directory not empty')
            return False
        self._create_tree()
        self._copy_defaults()
        print('\nInitialized rant in "%s"' % self._dest_dir)
        print('\nYou may now edit "%s/config.yml" as needed.' % self._dest_dir)
