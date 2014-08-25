import os
import tempfile
import shutil
import datetime
from time import gmtime, strftime

path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

def publish(layout='post'):
    template = '%s/defaults/layouts/publish.md' % path
    local_template = '%s/layouts/publish.md' % os.getcwd()
    if os.path.isfile(local_template):
        template = local_template
    template_fh = open(template, 'r')
    temp_fh = tempfile.NamedTemporaryFile(delete=False)
    line = template_fh.readline()
    date_format = '%Y-%m-%d %H:%M:%S'
    timestamp = strftime(date_format, gmtime())
    while line:
        temp_fh.write(bytes(line,'UTF-8'))
        line = template_fh.readline()
        if 'date' in line:
            line = "date: %s\n" % timestamp
    temp_fh.close()
    os.system('%s %s' % (os.environ.get('EDITOR','vim'),temp_fh.name))
    temp_fh = open(temp_fh.name, 'r')
    line = temp_fh.readline()
    while line:
        if 'date' in line:
            date = line.split(': ')[1].strip('\n ')
        if 'title' in line:
            title = line.split(':')[1].strip('\n ')
        if 'layout' in line:
            layout = line.split(':')[1].strip('\n ')
        line = temp_fh.readline()
    if layout == 'post':
        datetime_obj = datetime.datetime.strptime(date,date_format)
        timestamp = datetime_obj.strftime("%Y-%m-%d-%H%M")
        filename = '%s-%s.md' % (timestamp,title.replace(' ','_'))
    else:
        filename = '%s.md' % (title.replace(' ','_'))
    filepath = '%s/%ss/%s' % (os.getcwd(),layout,filename)
    shutil.copyfile(temp_fh.name,filepath)
    print("Saved to: %s" % filepath)
