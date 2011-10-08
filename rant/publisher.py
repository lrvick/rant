import os
import tempfile
import yaml
import shutil
from time import gmtime, strftime


def publish(layout='post'):
    template = '%s/rant/defaults/layouts/publish.md' % os.path.dirname(os.getcwd())
    local_template = '%s/layouts/publish.md' % os.getcwd()
    if os.path.isfile(local_template):
        template = local_template
    template_fh = file(template, 'r')
    temp_fh = tempfile.NamedTemporaryFile(delete=False)
    line = template_fh.readline()
    timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    while line:
        temp_fh.write(line)
        line = template_fh.readline()
        if 'date' in line:
            line = "date: %s\n" % timestamp
    temp_fh.close()
    os.system('vim %s' % temp_fh.name)
    temp_fh = file(temp_fh.name, 'r')
    content = yaml.load_all(temp_fh)
    for item in content:
        if 'layout' in item:
            headers = item
    if headers['layout'] == 'post':
        filename = '%s-%s.md' % (headers['date'].strftime("%Y%m%d%H%M%S"),headers['title'].replace(' ','_'))
    else:
        filename = '%s.md' % (headers['title'].replace(' ','_'))
    filepath = '%s/%ss/%s' % (os.getcwd(),headers['layout'],filename)
    shutil.copyfile(temp_fh.name,filepath)
    print "Saved to: %s" % filepath
