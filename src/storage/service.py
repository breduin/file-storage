from .utils import get_upload_path


def handle_uploaded_file(f=None):
    file_path = get_upload_path(f.name)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
