'''
Test of mailings API
'''
import django_rq
import os

from django.conf import settings
from django_rq import get_worker
from django.test import TestCase

from .service import handle_uploaded_file
from .utils import get_upload_path

from django.core.files.uploadedfile import SimpleUploadedFile


class TestFileUploading(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        pass

    def test_get_upload_path(self):
        path = get_upload_path()
        self.assertEqual(path.split('/')[-2], 'media')

    def test_file_upload(self):
        file_name = 'test.txt'
        file_base_path = os.path.join(settings.BASE_DIR, file_name)
        file_to_upload = SimpleUploadedFile(
            file_base_path,
            content=b'Hello world!'*1024,
            )
        django_rq.enqueue(handle_uploaded_file, file_to_upload)
        get_worker().work(burst=True)
        file_upload_path = get_upload_path(file_name)
        self.assertTrue(os.path.exists(file_upload_path))
        os.remove(file_upload_path)
