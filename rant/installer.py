import os
import shutil

def install(path):
    sample_config_file = '%s/rant/defaults/config.yml' % os.path.dirname(os.getcwd())
    if not os.path.isfile(sample_config_file):
        shutil.copy(sample_config_file,path)
    if not os.path.isdir('%s/posts' % path):
        os.makedirs('%s/posts' % path)
    if not os.path.isdir('%s/pages' % path):
        os.makedirs('%s/pages' % path)
    if not os.path.isdir('%s/templates' % path):
        os.makedirs('%s/templates' % path)
    if not os.path.isdir('%s/deploy' % path):
        os.makedirs('%s/deploy' % path)
    print('\nInitialized rant in "%s"') % os.getcwd()
    print('\nYou may now edit "%s/config.yml" to your liking.') % os.getcwd()
    pass
