import sys
import os
import shutil

def install(path):
    rant_path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
    sample_config_file = '%s/defaults/config.yml' % rant_path
    if not os.path.isfile('%s/config.yml' % path):
        shutil.copy(sample_config_file,path)
    if not os.path.isdir('%s/posts' % path):
        os.makedirs('%s/posts' % path)
    if not os.path.isdir('%s/pages' % path):
        os.makedirs('%s/pages' % path)
    if not os.path.isdir('%s/layouts' % path):
        shutil.copytree("%s/defaults/layouts" % rant_path,"%s/layouts" % path)
    if not os.path.isdir('%s/deploy' % path):
        os.makedirs('%s/deploy' % path)
    if not os.path.isdir('%s/deploy/blog' % path):
        os.makedirs('%s/deploy/blog' % path)
    print(('\nInitialized rant in "%s"') % path)
    print(('\nYou may now edit "%s/config.yml" to your liking.') % path)
