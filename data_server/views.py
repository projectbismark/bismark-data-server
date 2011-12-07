import errno
from os import makedirs
from os.path import join, basename
import re

from django.conf import settings
from django.http import HttpResponse

node_id_matcher = re.compile(r'OW[0-9A-F]{12}$')

def upload(request):
    module = request.REQUEST['directory']
    if module not in settings.UPLOADER_MODULES:
        raise ValueError('Invalid module')
    if len(request.raw_post_data) > settings.UPLOADER_MODULES[module]:
        raise ValueError('Upload is too big')
    if node_id_matcher.match(request.REQUEST['node_id']) is None:
        raise ValueError('Invalid node id')

    path = join(settings.UPLOADS_ROOT, module, request.REQUEST['node_id'])
    try:
        makedirs(path)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise
    handle = open(join(path, basename(request.REQUEST['filename'])), 'w')
    handle.write(request.raw_post_data)
    handle.close()

    return HttpResponse('done')
