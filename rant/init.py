import os
import shutil


class Initializer(object):
    """Initialize default rant source files in given directory"""

    def __init__(self, dest_dir):
        self._dest_dir = dest_dir

    def init(self):
        rant_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        )
        sample_config_file = '%s/defaults/config.yml' % rant_path
        if not os.path.isfile('%s/config.yml' % self._dest_dir):
            shutil.copy(sample_config_file, self._dest_dir)
        if not os.path.isdir('%s/posts' % self._dest_dir):
            os.makedirs('%s/posts' % self._dest_dir)
        if not os.path.isdir('%s/pages' % self._dest_dir):
            os.makedirs('%s/pages' % self._dest_dir)
        if not os.path.isdir('%s/layouts' % self._dest_dir):
            shutil.copytree(
                "%s/defaults/layouts" % rant_path,
                "%s/layouts" % self._dest_dir
            )
        if not os.path.isdir('%s/deploy' % self._dest_dir):
            os.makedirs('%s/deploy' % self._dest_dir)
        if not os.path.isdir('%s/deploy/blog' % self._dest_dir):
            os.makedirs('%s/deploy/blog' % self._dest_dir)
        print('\nInitialized rant in "%s"' % self._dest_dir)
        print('\nYou may now edit "%s/config.yml" as needed.' % self._dest_dir)
