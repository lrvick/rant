import sys
import os
import shutil

def install(path):
    rant_path = "%s/rant" % os.path.dirname(sys.path[0])
    sample_config_file = '%s/defaults/config.yml' % rant_path
    if not os.path.isfile(sample_config_file):
        shutil.copy(sample_config_file,path)
    if not os.path.isdir('%s/posts' % path):
        os.makedirs('%s/posts' % path)
    if not os.path.isdir('%s/pages' % path):
        os.makedirs('%s/pages' % path)
    if not os.path.isdir('%s/layouts' % path):
        shutil.copytree("%s/defaults/layouts" % rant_path,"%s/layouts" % path)
    if not os.path.isdir('%s/deploy' % path):
        os.makedirs('%s/deploy' % path)
    print('\nInitialized rant in "%s"') % path
    print('\nYou may now edit "%s/config.yml" to your liking.') % path
