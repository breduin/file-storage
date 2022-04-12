import os
from django.conf import settings


def get_upload_path(name=''):
    return os.path.join(settings.MEDIA_ROOT, name)
