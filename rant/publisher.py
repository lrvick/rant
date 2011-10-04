import os
import tempfile
import yaml

def publish(layout='post'):
    template = '%s/defaults/layouts/publish.md' % os.path.dirname(os.getcwd())
    local_template = '%s/layouts/publish.md' % os.getcwd()
    if os.path.isfile(local_template):
        template = local_template
    template_fh = file(template, 'r')
    header = template_fh.read()
    temp_fh = tempfile.NamedTemporaryFile(delete=False)
    temp_fh.write(header)
    temp_fh.close()
    #print header
    os.system('vim %s' % temp_fh.name)
    temp_fh = file(temp_fh.name, 'r')
    content = yaml.load_all(temp_fh)
    for item in content:
        if 'layout' in item:
            headers = item
        else:
            body = item
    print headers
    print body

